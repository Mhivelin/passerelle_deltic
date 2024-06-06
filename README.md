# Passerelle DELTIC

## Description
La passerelle DELTIC est un projet qui permettra de faire communiquer plusieurs applications entre elles. Elle est basée sur les différentes API des applications à connecter. ce projet as donc pour but de faciliter la communication ainsi que la mise en place des différentes communications entre les applications.

## Installation

### Etape 1 : Clonez le projet
```bash
git clone https://github.com/Mhivelin/passerelleV2.git
```

### Etape 2 : Créez les variables d'environnement
> Créez un fichier .env dans /app et ajoutez les variables d'environnement suivantes :
> remplacer les ********* par les valeurs correspondantes

```bash
ADMIN_USERNAME=*********
ADMIN_PASSWORD=*********
SECRET_KEY=*********
JWT_SECRET_KEY=*********
```


* pour les tests en local, vous pouvez ajouter la variable suivante
```bash
IP=localhost
```


### Etape 3 : Lancez le projet
> Pour lancer le projet, vous avez besoin de docker et docker-compose

si vous n'avez pas docker : [Installer Docker](https://docs.docker.com/get-docker/)

```bash
docker build -t passerelle_deltic .
docker run -p 5000:5000 -d --name passerelle_deltic passerelle_deltic
```

## Utilisation
Pour utiliser la passerelle DELTIC, il suffit d'avoir les différentes informations de connexion des applications à connecter. ensuite, il suffit de les renseigner dans le formulaire de configuration de la passerelle. Puis, le l'application se chargera de faire la communication entre les applications en suivant sa routine.

## Les différentes passerelles
### Passerelle 1 : Remontée de paiement (EBP --> Zeendoc)

#### Objectif :
Remonter les paiements effectués dans EBP vers Zeendoc afin de faciliter cette démarche pour les utilisateurs, automatiser le processus et éviter les erreurs de saisie.


#### Paramétrage  :
créer un index de paiement dans Zeendoc

informations requises pour la configuration :
Les informations de connexion à l'API EBP
L'id (EBP Client ID)
Le client secret (EBP Client Secret)
La clé d'abonnement (EBP Subscription Key)ici
Les informations de connexion à l'API Zeendoc
Le login (Zeendoc login)
L'url du client (Zeendoc URL Client)
Le mot de passe (Zeendoc CPassword)

#### Configuration :
Se rendre sur cette page pour ajouter un nouveau client
Remplir les informations requises
Valider le formulaire
Se rendre sur la page de configuration du client
Se connecter à l'API EBP grace au bouton
selectionner les champs requis
EBP_FOLDER_ID : l'identifiant du dossier EBP
ZEENDOC_CLASSEUR : l'identifiant du classeur Zeendoc
Enregistrer les modifications
Tester la configuration en lançant une routine

### base de données

```sql

CLIENT {
    idClient integer PK
    username string "NOT NULL"
}
LOGICIEL {
    IdLogiciel integer PK
    LibLogiciel string "NOT NULL"
}
PASSERELLE {
    IdPasserelle integer PK
    LibPasserelle string "NOT NULL"
}
LOGICIEL_CLIENT {
    idLogicielClient integer PK
    IdLogiciel integer
    idClient integer
}
LOGICIEL_CLIENT_EBP {
    idLogicielClient integer PK
    Folder_Id string "NOT NULL"
    Client_Id string "NOT NULL"
    Client_Secret string "NOT NULL"
    Subscription_Key string "NOT NULL"
    Token string
}
LOGICIEL_CLIENT_ZEENDOC {
    idLogicielClient integer PK
    Index_Statut_Paiement string
    Index_Ref_Doc string
    Classeur string
    Login string "NOT NULL"
    Password string "NOT NULL"
    UrlClient string "NOT NULL"
}
CONNECTE_LOGICIEL_SOURCE {
    IdPasserelle integer PK
    IdLogiciel integer
}
CONNECTE_LOGICIEL_DESTINATION {
    IdPasserelle integer PK
    IdLogiciel integer
}
CLIENT_PASSERELLE {
    idClient integer PK
    IdPasserelle integer PK
}

```




# EXPLICATION BDD

## CLIENT
Le client est la personne qui utilise la passerelle. Il peut avoir plusieurs logiciels et plusieurs passerelles.

## LOGICIEL
Le logiciel correspond a une catégorie de logiciel, il permet de regrouper les logiciel client

## LOGICIEL_CLIENT
La table LOGICIEL_CLIENT permet de stocker les informations des clients pour chaque logiciel (id de connexion, etc)
l'heritage de la table LOGICIEL_CLIENT (pour l'instant LOGICIEL_CLIENT_EBP et LOGICIEL_CLIENT_ZEENDOC) permet de stocker les informations spécifiques a chaque logiciel par exemple, on ne retrouve pas les mêmes informations pour EBP et Zeendoc

## PASSERELLE
La table PASSERELLE permet de stocker les type de passerelle existant ( pour rappel, une passerelle correspond a une communication entre deux logiciels faites par le code de l'app)

## PASSERELLE_CLIENT
La table PASSERELLE_CLIENT permet de dire quels clients utilisent quelles passerelles


# probleme

## probleme 1
> token de connexion a EBP


* token 1 :
{'id_token': '',
'access_token': '',
'expires_in': 3600,
'token_type': 'Bearer',
'refresh_token': '',
'scope': ['openid', 'profile', 'offline_access'],
'expires_at': 1717584392.457478}


* token 2 :
{'id_token': '',
'access_token': '',
'expires_in': 3600,
'token_type': 'Bearer',
'refresh_token': '',
'scope': 'openid profile offline_access'}


