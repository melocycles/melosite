"""ajoute et/ou modifie la base de donné. Si une erreur de type est détecté (checkEntry dans addBike et modifyBike) elle est renvoyé dans potentialErrorReturn puis affiché par print."""
import sqlCRUD
from datetime import date

if 1: # vélo pour le test
    bike0 = {'bycode': 'AB123', 'dateEntre': '2023-03-15', 'marque': 'BikeCo', 'typeVelo': 'VTC', 'tailleRoue': '26pouces', 'tailleCadre': 'M', 'photo1': b'image_blob_1', 'photo2': b'image_blob_2', 'photo3': b'image_blob_3', 'electrique': False, 'origine': 'don', 'status': 'en stock', 'etatVelo': 'très bon', 'prochaineAction': 'à vendre', 'referent': 'John Doe', 'valeur': 300.0, 'destinataireVelo': '', 'descriptionPublic': 'Vélo tout terrain en excellent état.', 'descriptionPrive': '', 'dateSortie': None, 'typeSortie': ''}
    bike1 = {'bycode': 'CD456', 'dateEntre': '2023-04-20', 'marque': 'SpeedyBike', 'typeVelo': 'VTT', 'tailleRoue': '29pouces', 'tailleCadre': 'L', 'photo1': b'image_blob_4', 'photo2': b'image_blob_5', 'photo3': b'image_blob_6', 'electrique': True, 'origine': 'trouvé', 'status': 'en stock', 'etatVelo': 'moyen', 'prochaineAction': 'à reparer', 'referent': 'Alice Smith', 'valeur': 500.0, 'destinataireVelo': '', 'descriptionPublic': 'Vélo de montagne électrique, besoin de réparations.', 'descriptionPrive': '', 'dateSortie': None, 'typeSortie': ''}
    bike2 = {'bycode': 'AB123', 'dateEntre': '2023-03-15', 'marque': 'BikeCo', 'typeVelo': 'VTC', 'tailleRoue': '26pouces', 'tailleCadre': 'M', 'photo1': b'image_blob_1', 'photo2': b'image_blob_2', 'photo3': b'image_blob_3', 'electrique': False, 'origine': 'don', 'status': 'en stock', 'etatVelo': 'très bon', 'prochaineAction': 'à vendre', 'referent': 'John Doe', 'valeur': 300.0, 'destinataireVelo': '', 'descriptionPublic': 'Vélo tout terrain en excellent état.', 'descriptionPrive': '', 'dateSortie': None, 'typeSortie': ''}
    bike3 = {'bycode': 'CD456', 'dateEntre': '2023-04-20', 'marque': 'SpeedyBike', 'typeVelo': 'VTT', 'tailleRoue': '29pouces', 'tailleCadre': 'L', 'photo1': b'image_blob_4', 'photo2': b'image_blob_5', 'photo3': b'image_blob_6', 'electrique': True, 'origine': 'trouvé', 'status': 'en stock', 'etatVelo': 'moyen', 'prochaineAction': 'à réparer', 'referent': 'Alice Smith', 'valeur': 500.0, 'destinataireVelo': '', 'descriptionPublic': 'Vélo de montagne électrique, besoin de réparations.', 'descriptionPrive': '', 'dateSortie': None, 'typeSortie': ''}
    bike3 = {'bycode': 'CD456', 'dateEntre': '2023-04-20', 'marque': 'SpeedyBike', 'typeVelo': 'VTT', 'tailleRoue': '29pouces', 'tailleCadre': 'L', 'photo1': b'image_blob_4', 'photo2': b'image_blob_5', 'photo3': b'image_blob_6', 'electrique': True, 'origine': 'trouvé', 'status': 'en stock', 'etatVelo': 'moyen', 'prochaineAction': 'à réparer', 'referent': 'Alice Smith', 'valeur': 500.0, 'destinataireVelo': '', 'descriptionPublic': 'Vélo de montagne électrique, besoin de réparations.', 'descriptionPrive': '', 'dateSortie': None, 'typeSortie': ''}
    bike4 = {'bycode': 'EF789', 'dateEntre': '2023-05-10', 'marque': 'CityCruiser', 'typeVelo': 'Ville', 'tailleRoue': '28pouces', 'tailleCadre': 'S', 'photo1': b'image_blob_7', 'photo2': b'image_blob_8', 'photo3': b'image_blob_9', 'electrique': False, 'origine': 'récupéré', 'status': 'réservé', 'etatVelo': 'bon', 'prochaineAction': 'à vendre', 'referent': 'Bob Johnson', 'valeur': 250.0, 'destinataireVelo': '', 'descriptionPublic': 'Vélo de ville en bon état, idéal pour la circulation urbaine.', 'descriptionPrive': '', 'dateSortie': None, 'typeSortie': ''}
    bike5 = {'bycode': 'GH012', 'dateEntre': '2023-06-02', 'marque': 'MountainMaster', 'typeVelo': 'VTT', 'tailleRoue': '27.5pouces', 'tailleCadre': 'XL', 'photo1': b'image_blob_10', 'photo2': b'image_blob_11', 'photo3': b'image_blob_12', 'electrique': False, 'origine': 'don', 'status': 'en stock', 'etatVelo': 'très bon', 'prochaineAction': 'à vendre', 'referent': 'Eva White', 'valeur': 400.0, 'destinataireVelo': '', 'descriptionPublic': 'Vélo de montagne haut de gamme, excellente performance.', 'descriptionPrive': '', 'dateSortie': None, 'typeSortie': ''}
    bike6 = {'bycode': 'IJ345', 'dateEntre': '2023-07-15', 'marque': 'CommuterPro', 'typeVelo': 'Ville', 'tailleRoue': '26pouces', 'tailleCadre': 'M', 'photo1': b'image_blob_13', 'photo2': b'image_blob_14', 'photo3': b'image_blob_15', 'electrique': True, 'origine': 'don', 'status': 'donné', 'etatVelo': 'moyen', 'prochaineAction': 'à recycler', 'referent': 'Charlie Brown', 'valeur': 150.0, 'destinataireVelo': '', 'descriptionPublic': 'Vélo de ville électrique, nécessite des réparations.', 'descriptionPrive': '', 'dateSortie': '2023-08-01', 'typeSortie': 'recyclé'}
    bike7 = {'bycode': 'KL678', 'dateEntre': '2023-08-28', 'marque': 'RoadRacer', 'typeVelo': 'Route', 'tailleRoue': '700c', 'tailleCadre': 'L', 'photo1': b'image_blob_16', 'photo2': b'image_blob_17', 'photo3': b'image_blob_18', 'electrique': False, 'origine': 'trouvé', 'status': 'en stock', 'etatVelo': 'bon', 'prochaineAction': 'à vendre', 'referent': 'Grace Miller', 'valeur': 600.0, 'destinataireVelo': '', 'descriptionPublic': 'Vélo de route rapide, idéal pour les courses.', 'descriptionPrive': '', 'dateSortie': None, 'typeSortie': ''}
    bike8 = {'bycode': 'MN901', 'dateEntre': '2023-09-10', 'marque': 'UrbanExplorer', 'typeVelo': 'Ville', 'tailleRoue': '24pouces', 'tailleCadre': 'S', 'photo1': b'image_blob_19', 'photo2': b'image_blob_20', 'photo3': b'image_blob_21', 'electrique': False, 'origine': 'récupéré', 'status': 'en stock', 'etatVelo': 'moyen', 'prochaineAction': 'à réparer', 'referent': 'Daniel Davis', 'valeur': 200.0, 'destinataireVelo': '', 'descriptionPublic': 'Vélo de ville compact, parfait pour les déplacements urbains.', 'descriptionPrive': '', 'dateSortie': None, 'typeSortie': ''}
    bike9 = {'bycode': 'OP234', 'dateEntre': '2023-10-05', 'marque': 'TrailBlazer', 'typeVelo': 'VTT', 'tailleRoue': '29pouces', 'tailleCadre': 'M', 'photo1': b'image_blob_22', 'photo2': b'image_blob_23', 'photo3': b'image_blob_24', 'electrique': True, 'origine': 'don', 'status': 'réservé', 'etatVelo': 'très bon', 'prochaineAction': 'à vendre', 'referent': 'Sophie Taylor', 'valeur': 450.0, 'destinataireVelo': '', 'descriptionPublic': 'Vélo de montagne tout terrain, excellentes performances hors route.', 'descriptionPrive': '', 'dateSortie': None, 'typeSortie': ''}

potentialErrorReturn = None

# enlever le dièse dessous pour tester addBike
#potentialErrorReturn = sqlCRUD.addBike("Louis", bike0 )

# enlever le dièse dessous pour tester modifyBike
#potentialErrorReturn = sqlCRUD.modifyBike("julien", 1,{"marque" : 123, "status" : "donné"})

# enlever le dièse dessous pour tester readBike
#sqlCRUD.readBike({"typeVelo" : "VTT", "tailleCadre" : "L"})

# enlever le dièse dessous pour tester deleteBike
#sqlCRUD.deleteBike("Louis", 2)


if potentialErrorReturn:
    for i in potentialErrorReturn:
        print(i)    
