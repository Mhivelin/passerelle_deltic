# Documentation des test unitaires
> Ce fichier as pour but d'expliquer le fonctionnement de test du projet

## Test unitaire
Les tests unitaires sont des tests qui permettent de vérifier le bon fonctionnement d'une partie du code. Ils sont utilisés pour vérifier que chaque unité de code fonctionne correctement. Les tests unitaires sont écrits par les développeurs eux-mêmes et sont exécutés à chaque fois que le code est modifié. Ils permettent de s'assurer que les modifications apportées au code n'ont pas introduit de bugs.

## rappel notion :
* tearDown : méthode qui est appelée après chaque test pour nettoyer les ressources utilisées par le test, permet de ne pas conserver des données inutiles en mémoire et de ne pas altérer les résultats des tests suivants.
* setUp : méthode qui est appelée avant chaque test pour initialiser les ressources nécessaires au test, permet de s'assurer que chaque test part d'un état connu et cohérent.
* assert..... : méthode qui permet de vérifier que le résultat d'un test est conforme à ce qui est attendu. Si le résultat du test est conforme à ce qui est attendu, le test est considéré comme réussi. Sinon, le test est considéré comme échoué.

