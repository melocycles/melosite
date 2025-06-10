# Database Optimizations

This document describes the optimizations made to improve the performance of the database tables and related queries.

## Bike Table Optimizations

### Optimizations Implemented

### 1. Database Indexes

Added the following indexes to speed up common queries:

- `idx_bike_dateentre` on `dateentre` column
  - Improves performance of queries that sort by date entered (ORDER BY dateentre)
  - Particularly benefits the search page which displays bikes in reverse chronological order

- `idx_bike_datesortie` on `datesortie` column
  - Improves performance of date range queries on the exit date
  - Benefits export functionality and reporting

- `idx_bike_statutvelo` on `statutVelo` column
  - Speeds up filtering by bike status
  - Common operation in the UI for filtering bikes by their current status

- Filter column indexes:
  - `idx_bike_marque` on `marque` column
  - `idx_bike_typevelo` on `typeVelo` column
  - `idx_bike_tailleRoue` on `tailleRoue` column
  - `idx_bike_tailleCadre` on `tailleCadre` column
  - `idx_bike_etatVelo` on `etatVelo` column
  - These improve performance when filtering bikes by these attributes

- `idx_modification_bikeid` on `bikeid` column in the Modification table
  - Improves performance when looking up modification history for a specific bike

### 2. Query Optimization

Optimized the `getFilterValues` function to use a single query instead of multiple queries:

- Previously: One query per filter attribute (5+ separate database round-trips)
- Now: Single UNION ALL query that retrieves all filter values in one database round-trip
- Benefits: Reduces database load, network overhead, and response time

### 3. Database Statistics

Added ANALYZE commands to update the PostgreSQL query planner statistics:

- Ensures the query planner has accurate information about the data distribution
- Helps the planner choose the most efficient query execution plans
- Automatically runs after adding indexes

## Expected Performance Improvements

- Faster page loads, especially for:
  - The main bike listing page (uses ORDER BY dateentre)
  - Search results with filters
  - Bike detail pages (lookup by ID)
  - Export functionality (date range queries)

- Reduced database load:
  - Fewer queries needed for filter values
  - More efficient query execution plans
  - Better utilization of available resources

- Better scalability:
  - The application should handle more concurrent users
  - Performance should remain good as the bike table grows

## Implementation

The optimizations are implemented in two main files:

1. `optimizeBikeTable.py` - Contains functions to add indexes and update statistics
2. `init-db.py` - Updated to run the optimizations during database initialization

Additionally, the `sqlCRUD.py` file was modified to optimize the `getFilterValues` function.

## Testing

A performance testing script (`test_performance.py`) is provided to measure the impact of these optimizations. It tests common query patterns before and after applying the optimizations.

To run the performance tests:

```bash
python test_performance.py
```

This will output performance metrics showing the improvement for each query type.

## Picture Table Optimizations

### Optimizations Implemented

#### 1. Database Indexes

Added the following indexes to speed up common queries:

- `idx_picture_bike_id` on `bike_id` column
  - Improves performance of queries that filter pictures by bike ID
  - Benefits the bike detail page which displays pictures for a specific bike

- `idx_picture_is_principal` on `is_principal` column
  - Speeds up filtering for principal pictures
  - Common operation when displaying the main picture for a bike in listings

- `idx_picture_bike_principal` composite index on `bike_id` and `is_principal` columns
  - Optimizes the specific query pattern of finding the principal picture for a given bike
  - Particularly benefits the bike listing pages which show the main picture for each bike

#### 2. Database Statistics

Added ANALYZE commands to update the PostgreSQL query planner statistics:

- Ensures the query planner has accurate information about the data distribution
- Helps the planner choose the most efficient query execution plans
- Automatically runs after adding indexes

### Expected Performance Improvements

- Faster page loads, especially for:
  - Bike detail pages (loading all pictures for a bike)
  - Bike listing pages (loading principal pictures)
  - Any page that displays bike images

- Better scalability:
  - The application should handle more concurrent users
  - Performance should remain good as the picture table grows, which is important since images are typically the largest data in the system

### Implementation

The optimizations are implemented in:

- `optimizePicturesTable.py` - Contains functions to add indexes and update statistics for the Picture table
