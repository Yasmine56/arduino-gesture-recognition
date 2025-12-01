import tensorflow as tf

# Charge le modèle Keras (modèle entraîné) à partir d'un fichier .h5
model = tf.keras.models.load_model('C:/Users/acer/Documents/MyTinyML/Data Collection/mon_model.h5')

# Utiliser le convertisseur TensorFlow Lite pour convertir le modèle Keras en modèle TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# Activer des optimisations pour réduire la taille du modèle et le rendre plus léger
# Cela permet d'améliorer les performances et de réduire la consommation de mémoire
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Convertir le modèle en format TensorFlow Lite (tflite)
tflite_model = converter.convert()

# Sauvegarder le modèle converti en TensorFlow Lite dans un fichier .tflite
with open('modele.tflite', 'wb') as f:
    f.write(tflite_model)

# Afficher un message une fois que la conversion et l'optimisation sont terminées
print("Conversion et optimisation en TFLite terminées !")

