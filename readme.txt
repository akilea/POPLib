#Description
POPlib est la librairie qui va supporter le développement de POP (Peck Order Pandemonium).
Les étudiants doivent implémenter des boids ainsi que l'interface d'unité de combat du jeu.
Ultimement, on aura un simulateur de combat de boid.

#Démarrage
cd poplib
pip install -r requirements.txt

Les fichiers dans la dossier _project_start_files devrait être copiés à la racine de votre projet et adaptés.

#Mise en place des tests unitaires
Configurez PyTest, puis inspirez-vous de .\_project_start_files\test_generic.py pour faire vos propres tests.

# Structure des dossiers
## _project_start_files
Contient les fichiers que vou devriez copier-coller dans votre projet pour démarrer

## _resssources
Contient des images/aides visuels.

## boid_system
Module contenant les interfaces/classes strictement liées aux boids

## game-engine
Contient les interfaces/classes strictement liées au simualteur de combat

## unit_test
Contient les interface/classe strictement liées au tests unitaire