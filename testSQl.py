import sqlCRUD
from datetime import date

if 1: # vélo pour le test
    bike0 = ["AB123", "2023-03-15", "BikeCo", "VTC", "26pouces", "M", b"image_blob_1", b"image_blob_2", b"image_blob_3", False, "don", "en stock", "très bon", "à vendre", "John Doe", 300.00, "", "Vélo tout terrain en excellent état.", "", None, ""]
    bike1 = ["CD456", "2023-04-20", "SpeedyBike", "VTT", "29pouces", "L", b"image_blob_4", b"image_blob_5", b"image_blob_6", True, "trouvé", "en stock", "moyen", "à reparer", "Alice Smith", 500.00, "", "Vélo de montagne électrique, besoin de réparations.", "", None, ""]
    bike2 = ["AB123", "2023-03-15", "BikeCo", "VTC", "26pouces", "M", b"image_blob_1", b"image_blob_2", b"image_blob_3", False, "don", "en stock", "très bon", "à vendre", "John Doe", 300.00, "", "Vélo tout terrain en excellent état.", "", None, ""]
    bike3 = ["CD456", "2023-04-20", "SpeedyBike", "VTT", "29pouces", "L", b"image_blob_4", b"image_blob_5", b"image_blob_6", True, "trouvé", "en stock", "moyen", "à réparer", "Alice Smith", 500.00, "", "Vélo de montagne électrique, besoin de réparations.", "", None, ""]
    bike4 = ["EF789", "2023-05-10", "CityCruiser", "Ville", "28pouces", "S", b"image_blob_7", b"image_blob_8", b"image_blob_9", False, "récupéré", "réservé", "bon", "à vendre", "Bob Johnson", 250.00, "", "Vélo de ville en bon état, idéal pour la circulation urbaine.", "", None, ""]
    bike5 = ["GH012", "2023-06-02", "MountainMaster", "VTT", "27.5pouces", "XL", b"image_blob_10", b"image_blob_11", b"image_blob_12", False, "don", "en stock", "très bon", "à vendre", "Eva White", 400.00, "", "Vélo de montagne haut de gamme, excellente performance.", "", None, ""]
    bike6 = ["IJ345", "2023-07-15", "CommuterPro", "Ville", "26pouces", "M", b"image_blob_13", b"image_blob_14", b"image_blob_15", True, "don", "donné", "moyen", "à recycler", "Charlie Brown", 150.00, "", "Vélo de ville électrique, nécessite des réparations.", "", "2023-08-01", "recyclé"]
    bike7 = ["KL678", "2023-08-28", "RoadRacer", "Route", "700c", "L", b"image_blob_16", b"image_blob_17", b"image_blob_18", False, "trouvé", "en stock", "bon", "à vendre", "Grace Miller", 600.00, "", "Vélo de route rapide, idéal pour les courses.", "", None, ""]
    bike8 = ["MN901", "2023-09-10", "UrbanExplorer", "Ville", "24pouces", "S", b"image_blob_19", b"image_blob_20", b"image_blob_21", False, "récupéré", "en stock", "moyen", "à réparer", "Daniel Davis", 200.00, "", "Vélo de ville compact, parfait pour les déplacements urbains.", "", None, ""]
    bike9 = ["OP234", "2023-10-05", "TrailBlazer", "VTT", "29pouces", "M", b"image_blob_22", b"image_blob_23", b"image_blob_24", True, "don", "réservé", "très bon", "à vendre", "Sophie Taylor", 450.00, "", "Vélo de montagne tout terrain, excellentes performances hors route.", "", None, ""]

potentialErrorReturn = None


potentialErrorReturn = sqlCRUD.addBike("Louis", 123)


#potentialErrorReturn = sqlCRUD.modifyBike("julien", 1,["marque", "status"], [123, "donné"])


if potentialErrorReturn:
    for i in potentialErrorReturn:
        print(i)    