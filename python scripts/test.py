import tensorflow as tf
import numpy as np

# Charger le modèle TensorFlow Lite depuis un fichier .tflite
interpreter = tf.lite.Interpreter(model_path='mon_modele.tflite')

# Allouer de la mémoire pour les tensors (c'est nécessaire avant de pouvoir effectuer des inférences)
interpreter.allocate_tensors()

# Obtenir les détails des entrées et sorties du modèle
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Afficher les détails des entrées et sorties pour comprendre le format des données
print("Détails des entrées:", input_details)
print("Détails des sorties:", output_details)

# Générer des données simulées pour tester le modèle (exemple de données pour un capteur ou un problème spécifique)
shape_entree = input_details[0]['shape']  # Récupérer la forme de l'entrée attendue par le modèle
data_simulee = np.array([[0.5, 0.1, -0.3, 0.7, 0.0, -0.5]], dtype=np.float32)  # Exemple de données simulées adaptées au modèle

# Charger ces données simulées dans l'entrée du modèle (préparer l'entrée pour l'inférence)
interpreter.set_tensor(input_details[0]['index'], data_simulee)

# Exécuter l'inférence : faire une prédiction en utilisant les données d'entrée
interpreter.invoke()

# Récupérer la sortie du modèle après l'inférence et afficher le résultat
output_data = interpreter.get_tensor(output_details[0]['index'])
print("Résultat de l'inférence:", output_data)

# Ré-exécuter l'inférence avec les mêmes données simulées
interpreter.set_tensor(input_details[0]['index'], data_simulee)
interpreter.invoke()

# Récupérer à nouveau la sortie du modèle et afficher le résultat pour la deuxième exécution
output_data = interpreter.get_tensor(output_details[0]['index'])
print("Résultat de l'inférence:", output_data)
