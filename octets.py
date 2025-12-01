# Importation de la bibliothèque numpy
import numpy as np

# Charger le modèle TensorFlow Lite en mode binaire
# Ouvrir le fichier 'mon_modele.tflite' en mode binaire ('rb') pour le lire
with open("mon_modele.tflite", "rb") as f:
    model_data = f.read()  # Lire le contenu du fichier et le stocker dans la variable 'model_data'

# Transformer les données du modèle en tableau d'octets C++
# Convertir chaque octet du modèle en sa représentation hexadécimale formatée
hex_array = ', '.join(f'0x{b:02X}' for b in model_data)

# Générer un fichier .c
# Ouvrir le fichier 'mon_modele_data.c' en mode écriture ('w')
with open("mon_modele_data.c", "w") as f:
    # Écrire le code C++ dans le fichier avec le modèle binaire en tableau d'octets
    f.write(f"""
#include "mon_modele_data.h"  // Inclure un fichier d'en-tête (hypothétique) pour déclarer le tableau
alignas(8) const unsigned char mon_modele_tflite[] = {{  // Déclarer le tableau de type 'unsigned char' pour stocker les données du modèle
    {hex_array}  // Insérer le tableau d'octets hexadécimaux généré précédemment
}};
const unsigned int mon_modele_tflite_len = {len(model_data)};  // Déclarer la taille du modèle en octets
""")

# Afficher un message indiquant que la conversion est terminée
print("Conversion terminée : Fichier mon_modele_data.c généré !")
