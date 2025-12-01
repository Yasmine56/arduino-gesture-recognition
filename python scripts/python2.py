import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Charger le CSV après le nettoyage et l'équilibrage
file_path = "C:/Users/acer/Documents/MyTinyML/Data collection/data.csv"
df = pd.read_csv(file_path, sep=";", skiprows=1, header=None, on_bad_lines='skip')
logging.info("Données chargées. Nombre de lignes : %d", len(df))

# Noms des colonnes
df.columns = ["Label", "AccX", "AccY", "AccZ", "GyroX", "GyroY", "GyroZ"]

# Vérification des labels uniques
print("Labels uniques avant nettoyage :", df["Label"].unique())

# Convertir les colonnes numériques
for col in ["Label", "AccX", "AccY", "AccZ", "GyroX", "GyroY", "GyroZ"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")  # Convertir en numérique

# Suppression des lignes contenant des NaN
df.dropna(inplace=True)

# Répartition des classes avant nettoyage
print("Répartition initiale des classes :\n", df["Label"].value_counts())

# Fonction pour supprimer les valeurs aberrantes en fonction de l'IQR
def remove_outliers(df, columns, threshold=2.5):
    Q1 = df[columns].quantile(0.25)
    Q3 = df[columns].quantile(0.75)
    IQR = Q3 - Q1
    df_clean = df[~((df[columns] < (Q1 - threshold * IQR)) | (df[columns] > (Q3 + threshold * IQR))).any(axis=1)]
    return df_clean

# Fonction pour appliquer la suppression des valeurs aberrantes sur chaque groupe (par label)
def remove_outliers_by_label(df, columns, threshold=2.5):
    df_clean = df.groupby('Label').apply(lambda group: remove_outliers(group, columns, threshold))
    return df_clean.reset_index(drop=True)

# Appliquer la suppression des valeurs aberrantes par label
df_clean = remove_outliers_by_label(df, ["AccX", "AccY", "AccZ", "GyroX", "GyroY", "GyroZ"])

# Répartition des classes après suppression des valeurs aberrantes
print("Répartition des classes après suppression des valeurs aberrantes :")
print(df_clean['Label'].value_counts())

# Équilibrage des classes
min_samples = df_clean["Label"].value_counts().min()
df_balanced = df_clean.groupby("Label", group_keys=False, as_index=False).apply(lambda x: x.sample(min_samples, random_state=42))
logging.info("Données équilibrées. Répartition des classes après équilibrage :\n%s", df_balanced["Label"].value_counts())

# Adjust labels to be zero-indexed
df_balanced["Label"] = df_balanced["Label"] - 1

# Vérification des labels uniques après ajustement
print("Labels uniques après ajustement :", df_balanced["Label"].unique())

# Vérification de la répartition des classes après équilibrage
print("Répartition des classes après équilibrage :")
print(df_balanced['Label'].value_counts())

# Séparation des features (X) et labels (y)
X = df_balanced[["AccX", "AccY", "AccZ", "GyroX", "GyroY", "GyroZ"]].values
y = df_balanced["Label"].values

# Normalisation des données
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Sauvegarde du scaler
scaler_path = "C:/Users/acer/Documents/MyTinyML/Data collection/scaler.pkl"
joblib.dump(scaler, scaler_path)  # Sauvegarde du scaler
logging.info("Normalisation des données effectuée.")

# Vérification de la normalisation
print("Moyenne des features après normalisation :", X_scaled.mean(axis=0))
print("Écart-type après normalisation :", X_scaled.std(axis=0))

# Séparation en train (80%) et test (20%)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)
logging.info("Séparation des données effectuée. Train : %s, Test : %s", X_train.shape, X_test.shape)

# Sauvegarde des datasets
np.save("C:/Users/acer/Documents/MyTinyML/Data collection/X_train.npy", X_train)
np.save("C:/Users/acer/Documents/MyTinyML/Data collection/X_test.npy", X_test)
np.save("C:/Users/acer/Documents/MyTinyML/Data collection/Y_train.npy", y_train)
np.save("C:/Users/acer/Documents/MyTinyML/Data collection/Y_test.npy", y_test)
logging.info("Jeux de données sauvegardés.")

# Définition du modèle de réseau de neurones
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),  # Couche d'entrée
    tf.keras.layers.Dense(32, activation='relu'),  # Couche cachée
    tf.keras.layers.Dense(5, activation='softmax')  # 5 classes de sortie (une par mouvement)
])

# Compilation du modèle
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',  # Car on a des classes (0, 1, 2, 3, 4)
              metrics=['accuracy'])

# Affichage du résumé du modèle
model.summary()

# Entraînement du modèle
history = model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test))

# Évaluation du modèle sur les données de test
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Précision sur les données de test : {test_acc * 100:.2f}%")

# Courbes de précision et de perte
plt.figure(figsize=(12,5))

# Précision
plt.subplot(1,2,1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Époques')
plt.ylabel('Précision')
plt.legend()
plt.title('Évolution de la précision')

# Perte
plt.subplot(1,2,2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Époques')
plt.ylabel('Perte')
plt.legend()
plt.title('Évolution de la perte')

plt.show()

model.save("mon_model.h5")
