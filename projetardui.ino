// Inclure la librairie
#include <Arduino_LSM9DS1.h> 

// Constantes pour l'enregistrement des mouvements
const int DURATION = 10000;  // Durée totale d'enregistrement (10 secondes)
const int MOVEMENT_TIME = 2000;  // Temps de mouvement (2 secondes)
const int CENTER_TIME = 2000;    // Temps de retour au centre (2 secondes)
const int INTERVAL = 100;  // Intervalle entre échantillons (100 ms)

// Variables de gestion de l'enregistrement
bool isRecording = false;    // Indicateur pour savoir si l'enregistrement est en cours
int currentLabel = -1;       // Label du mouvement en cours (Gauche, Droite, Haut, Bas, Repos)
unsigned long startTime = 0; // Temps de début de l'enregistrement
int sampleCount = 0;         // Compteur des échantillons enregistrés
bool isMoving = true;        // Indicateur pour savoir si on est dans la phase "mouvement" ou "retour au centre"

void setup() {
  Serial.begin(9600);  // Initialise la communication série à 9600 bauds
  while (!Serial);  // Attendre que la communication série soit prête

  // Initialiser le capteur IMU (si échec, arrêter le programme)
  if (!IMU.begin()) {
    Serial.println("Erreur : Impossible d'initialiser le capteur IMU !");
    while (1);  // Bloquer le programme si le capteur ne s'initialise pas correctement
  }

  Serial.println("Appuyez sur une touche pour enregistrer un mouvement.");
  Serial.println("'1' = Gauche, '2' = Droite, '3' = Haut, '4' = Bas, '5' = Repos");
}

void loop() {
  // Vérifier si une entrée a été reçue via le port série
  if (Serial.available()) {
    char input = Serial.read();  // Lire l'entrée de l'utilisateur
    
    // Si l'entrée est un chiffre entre 1 et 5, commencer l'enregistrement
    if (input >= '1' && input <= '5') {
      currentLabel = input - '0';  // Convertir le caractère en entier (1 à 5)
      Serial.print("Enregistrement de : ");
      Serial.println(getMovementName(currentLabel));  // Afficher le nom du mouvement
      Serial.println("Début dans 3 secondes...");
      delay(3000);  // Attendre 3 secondes avant de commencer

      // Initialiser les variables pour démarrer l'enregistrement
      isRecording = true;
      startTime = millis();  // Démarrer le chronomètre
      sampleCount = 0;       // Réinitialiser le compteur d'échantillons
      isMoving = true;       // Commencer par un mouvement
    }
  }

  // Si l'enregistrement est en cours et que la durée totale n'est pas atteinte
  if (isRecording && (millis() - startTime < DURATION)) {
    unsigned long elapsedTime = millis() - startTime;  // Temps écoulé depuis le début de l'enregistrement
    
    // Déterminer si on est dans la phase "mouvement" ou "retour au centre"
    if (elapsedTime % (MOVEMENT_TIME + CENTER_TIME) < MOVEMENT_TIME) {
      isMoving = true;  // On est dans la phase "mouvement"
    } else {
      isMoving = false; // On est dans la phase "retour au centre"
    }

    // Si les données du capteur IMU sont disponibles, les lire
    if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
      float accX, accY, accZ, gyroX, gyroY, gyroZ;
      IMU.readAcceleration(accX, accY, accZ);  // Lire les données d'accéléromètre
      IMU.readGyroscope(gyroX, gyroY, gyroZ);  // Lire les données de gyroscope

      // Inverser les axes Y pour correspondre à l'orientation du capteur
      accY = -accY;
      gyroY = -gyroY;
      
      // Afficher les résultats sous forme CSV (mouvement ou retour au centre)
      Serial.print(isMoving ? currentLabel : 5); Serial.print("; "); // "5" pour retour au centre
      Serial.print(accX); Serial.print("; ");
      Serial.print(accY); Serial.print("; ");
      Serial.print(accZ); Serial.print("; ");
      Serial.print(gyroX); Serial.print("; ");
      Serial.print(gyroY); Serial.print("; ");
      Serial.println(gyroZ);  // Affiche les données d'accéléromètre et gyroscope

      sampleCount++;  // Incrémenter le compteur d'échantillons
      delay(INTERVAL);  // Attendre 100 ms avant de prendre un nouvel échantillon
    }
  }

  // Si la durée d'enregistrement est atteinte, afficher le résultat
  if (isRecording && (millis() - startTime >= DURATION)) {
    Serial.print("Fin de l'enregistrement pour : ");
    Serial.println(getMovementName(currentLabel));  // Afficher le mouvement enregistré
    Serial.print("Total d’échantillons capturés : ");
    Serial.println(sampleCount);  // Afficher le nombre d'échantillons capturés
    Serial.println("Appuyez sur une touche pour recommencer.");

    isRecording = false;  // Arrêter l'enregistrement
  }
}

// Fonction pour obtenir le nom du mouvement en fonction du label
String getMovementName(int label) {
  switch (label) {
    case 1: return "Gauche";
    case 2: return "Droite";
    case 3: return "Haut";
    case 4: return "Bas";
    case 5: return "Repos (Retour au centre)";
    default: return "Inconnu";  // Si le label est invalide, retourner "Inconnu"
  }
}
