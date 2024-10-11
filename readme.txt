#Description
POPlib est la librairie qui va supporter le développement de POP (Peck Order Pandemonium).

#Dépendances externes
cd poplib
pip install -r requirements.txt

#Architecture
Voir les images dans le dossier _ressources

#Concept
Les étudiants doivent implémenter des boids ainsi que l'interface d'unité de combat du jeu.
Ultimement, on aura un simulateur de combat de boid.

#Utilisation de base
Répliquer le code du main.py dans votre projet.

#Tests unitaires
Configurez PyTest, puis
from poplib.unit_test.manual_app_runner import run_ursina_for, assert_true, assert_false
Vous devriez pouvoir faire comme dans test_exemple.py