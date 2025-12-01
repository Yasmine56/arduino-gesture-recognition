# Importer les bibliothèques
import serial
import time
import numpy as np
import tensorflow as tf
import csv

# Ouvrir la communication série avec l'Arduino
ser = serial.Serial('COM4', 115200)  # Remplacer 'COMx' par le port série de ton Arduino
time.sleep(2)  # Attendre 2 secondes pour que la connexion série soit prête

# Charger le modèle TensorFlow Lite depuis le fichier
interpreter = tf.lite.Interpreter(model_path="mon_modele.tflite")
interpreter.allocate_tensors()  # Allouer les ressources mémoire nécessaires pour les tensors

# Obtenir les détails des tensors d'entrée et de sortie du modèle
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Fonction pour faire une prédiction avec les données d'entrée
def predict(input_data):
    # Convertir les données d'entrée en tableau numpy de type float32
    input_data = np.array(input_data, dtype=np.float32)

    # Ajouter une dimension pour simuler un lot d'exemples (si nécessaire)
    input_data = np.reshape(input_data, (1, 6))  # Ici, nous avons 6 valeurs d'entrée
    interpreter.set_tensor(input_details[0]['index'], input_data)  # Définir l'entrée pour l'inférence
    interpreter.invoke()  # Exécuter l'inférence sur les données d'entrée

    # Obtenir le résultat de l'inférence (prédiction du modèle)
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data  # Retourner le résultat de la prédiction

# Ouvrir un fichier CSV en mode écriture
with open('gestes.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['ax', 'ay', 'az', 'gx', 'gy', 'gz', 'predicted_gesture'])  # Écrire les en-têtes du fichier CSV

# Initialiser un compteur pour le nombre de prédictions effectuées
prediction_count = 0
max_predictions = 30  # Limiter le nombre de prédictions à 30

# Boucle principale pour recevoir les données d'Arduino et effectuer la prédiction
while prediction_count < max_predictions:
    if ser.in_waiting > 0:  # Vérifier s'il y a des données disponibles en attente dans le buffer série
        # Lire la ligne de données envoyée par Arduino, décoder et supprimer les espaces superflus
        data = ser.readline().decode('utf-8').strip()

        # Afficher les données brutes pour le débogage
        print(f"Donnée brute reçue d'Arduino : {data}")

        # Vérifier si la donnée reçue contient des valeurs numériques (pas de texte comme 'Geste détecté par Python')
        if 'Geste détecté par Python' not in data:  # Ignorer les lignes contenant du texte
            data_values = data.split(',')  # Séparer les valeurs par des virgules
            print(f"Donnée reçue d'Arduino (séparée) : {data_values}")

            # Vérifier que la donnée contient bien 6 valeurs (accéléromètre et gyroscope)
            if len(data_values) == 6:
                try:
                    # Convertir les valeurs séparées en flottants
                    ax, ay, az, gx, gy, gz = map(float, data_values)
                    input_data = np.array([ax, ay, az, gx, gy, gz], dtype=np.float32)  # Créer un tableau numpy avec les données

                    # Effectuer une prédiction avec le modèle TensorFlow Lite
                    output = predict(input_data)
                    print(f"Prédiction du modèle : {output}")

                    # Logique pour déterminer le geste à partir de la prédiction
                    prediction_index = np.argmax(output)  # Trouver l'index de la classe prédite avec la probabilité la plus élevée
                    gestes = ["haut", "bas", "gauche", "droite"]  # Liste des gestes possibles

                    # Obtenir le geste correspondant à la prédiction
                    predicted_gesture = gestes[prediction_index]
                    print(f"Geste détecté : {predicted_gesture}")

                    # Écrire les données reçues et le geste prédit dans le fichier CSV
                    writer.writerow([ax, ay, az, gx, gy, gz, predicted_gesture])  # Ajouter une nouvelle ligne au fichier CSV
                    prediction_count += 1  # Incrémenter le compteur de prédictions

                except ValueError as e:
                    # Gérer les erreurs de conversion de données en flottants (par exemple, données mal formatées)
                    print(f"Erreur de conversion des données en flottants : {e}. Ignorer cette ligne.")
                except Exception as e:
                    # Gérer toutes les autres erreurs inattendues
                    print(f"Une erreur inattendue s'est produite : {e}")
            else:
                # Si les données sont mal formatées (ne contiennent pas 6 valeurs)
                print("Données mal formatées reçues, ignorées.")
        else:
            # Ignorer les lignes contenant du texte comme 'Geste détecté par Python'
            print(f"Donnée texte ignorée : {data}")

        # Attendre 0,5 seconde avant de lire à nouveau les données série
        time.sleep(0.5)

# Une fois que 30 prédictions ont été effectuées, arrêter la boucle et afficher un message
print("30 prédictions effectuées. Arrêt du programme.")
