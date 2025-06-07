import os
import time
import psycopg2
import logging
import statistics
from optimizeBikeTable import get_connection
from optimizePicturesTable import optimize_picture_table

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def measure_query_time(query, params=None, iterations=5):
    """Measure the execution time of a query"""
    connection = get_connection()
    cursor = connection.cursor()

    times = []
    try:
        for _ in range(iterations):
            start_time = time.time()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            cursor.fetchall()  # Fetch all results to ensure query completes
            end_time = time.time()
            times.append(end_time - start_time)

        # Calculate statistics
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)

        logger.info(f"Query execution times (seconds):")
        logger.info(f"  Average: {avg_time:.6f}")
        logger.info(f"  Minimum: {min_time:.6f}")
        logger.info(f"  Maximum: {max_time:.6f}")

        return avg_time
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def test_bike_performance():
    """Test the performance of common bike table queries"""
    logger.info("Testing performance of common bike table queries...")

    # Test 1: Query with ORDER BY dateentre
    logger.info("Test 1: Query with ORDER BY dateentre")
    query1 = "SELECT id, title, marque, typeVelo FROM bike ORDER BY dateentre DESC LIMIT 100"
    avg_time1 = measure_query_time(query1)

    # Test 2: Query with filter on statutVelo
    logger.info("Test 2: Query with filter on statutVelo")
    query2 = "SELECT id, title, marque, typeVelo FROM bike WHERE statutVelo = %s"
    avg_time2 = measure_query_time(query2, ('en stock',))

    # Test 3: Query with date range filter
    logger.info("Test 3: Query with date range filter")
    query3 = "SELECT id, title, marque, typeVelo FROM bike WHERE dateentre >= %s AND dateentre <= %s"
    avg_time3 = measure_query_time(query3, ('2020-01-01', '2023-12-31'))

    # Test 4: Query with multiple filters
    logger.info("Test 4: Query with multiple filters")
    query4 = "SELECT id, title, marque, typeVelo FROM bike WHERE marque = %s AND typeVelo = %s"
    avg_time4 = measure_query_time(query4, ('Shimano', 'VTT'))

    # Test 5: Query for distinct values (similar to getFilterValues)
    logger.info("Test 5: Query for distinct values")
    query5 = "SELECT DISTINCT marque FROM bike WHERE marque IS NOT NULL AND marque != ''"
    avg_time5 = measure_query_time(query5)

    return {
        "order_by_dateentre": avg_time1,
        "filter_statutVelo": avg_time2,
        "date_range_filter": avg_time3,
        "multiple_filters": avg_time4,
        "distinct_values": avg_time5
    }

def test_picture_performance():
    """Test the performance of common picture table queries"""
    logger.info("Testing performance of common picture table queries...")

    # Get a sample bike_id for testing
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM bike LIMIT 1")
        result = cursor.fetchone()
        if result:
            sample_bike_id = result[0]
        else:
            # If no bikes exist, use a default value
            sample_bike_id = 1
    except Exception as e:
        logger.error(f"Error getting sample bike_id: {e}")
        sample_bike_id = 1
    finally:
        cursor.close()
        connection.close()

    # Test 1: Query all pictures for a specific bike
    logger.info("Test 1: Query all pictures for a specific bike")
    query1 = "SELECT id, name, is_principal, data FROM picture WHERE bike_id = %s"
    avg_time1 = measure_query_time(query1, (sample_bike_id,))

    # Test 2: Query the principal picture for a specific bike
    logger.info("Test 2: Query the principal picture for a specific bike")
    query2 = "SELECT id, name, is_principal, data FROM picture WHERE bike_id = %s AND is_principal IS TRUE"
    avg_time2 = measure_query_time(query2, (sample_bike_id,))

    # Test 3: Query all pictures
    logger.info("Test 3: Query all pictures")
    query3 = "SELECT id, name, is_principal, data FROM picture"
    avg_time3 = measure_query_time(query3)

    return {
        "pictures_by_bike": avg_time1,
        "principal_picture": avg_time2,
        "all_pictures": avg_time3
    }

if __name__ == "__main__":
    # Test bike table performance
    logger.info("Starting bike table performance tests before optimization...")
    before_bike_times = test_bike_performance()

    logger.info("Running bike table optimizations...")
    optimize_bike_table()

    logger.info("Starting bike table performance tests after optimization...")
    after_bike_times = test_bike_performance()

    # Calculate improvement percentages for bike table
    logger.info("Bike table performance improvement summary:")
    for test_name in before_bike_times:
        if before_bike_times[test_name] and after_bike_times[test_name]:
            improvement = (before_bike_times[test_name] - after_bike_times[test_name]) / before_bike_times[test_name] * 100
            logger.info(f"  {test_name}: {improvement:.2f}% improvement")

    # Test picture table performance
    logger.info("Starting picture table performance tests before optimization...")
    before_picture_times = test_picture_performance()

    logger.info("Running picture table optimizations...")
    optimize_picture_table()

    logger.info("Starting picture table performance tests after optimization...")
    after_picture_times = test_picture_performance()

    # Calculate improvement percentages for picture table
    logger.info("Picture table performance improvement summary:")
    for test_name in before_picture_times:
        if before_picture_times[test_name] and after_picture_times[test_name]:
            improvement = (before_picture_times[test_name] - after_picture_times[test_name]) / before_picture_times[test_name] * 100
            logger.info(f"  {test_name}: {improvement:.2f}% improvement")
