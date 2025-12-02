# arduino-gesture-recognition
Motion recognition (up, down, left, right) of an IMU sensor via Arduino and TensorFlow Lite.

# Arduino IMU Gesture Recognition

This project uses an Arduino and an IMU sensor to recognize simple movements (up, down, left, right) using a deep learning model running directly on the board.

## Objectives

- Record accelerometer and gyroscope data from an IMU (LSM9DS1).
- Clean and structure this data to train a model.
- Learn a model (MLP/dense) to classify gestures.
- Convert the model to .tflite and then to .c/.h for Arduino.
- Run the model in real time on the microcontroller board.

## Material used

- Arduino Nano 33 BLE Sense (IMU intégré LSM9DS1)
- Python 3.9+
- NumPy, Pandas, Scikit-Learn
- TensorFlow / TFLite
- IMU sensor (accelerometer + gyroscope)
- Cables and computer for development

## Record the movements 

The user selects a movement class via the terminal:

1: Left
2: Right
3: Up
4: Down
5: Rest

The values ​​(accX, accY, accZ, gyroX, gyroY, gyroZ) are exported in CSV format.

- Sensor movement for each gesture.
- Data saved to CSV files (`data.csv`).

## Data preprocessing 

The Python scripts handle :
- Cleaning (nettoyage.py)
- Normalization (scaler.pkl)
- Slicing and creating X/Y curves in .npy format

Python scripts (`python2.py`, `nettoyage.py`, `octets.py`, `convtf.py`) to clean and transform the data and then convert the file.

## Model's training

The final model is in : model/my_model.h5

It's a simple dense network that classifies the 5 movements.

Training a gesture recognition model (`mon_model.h5`).

## Conversion in TFLite + Arduino export

- Conversion : my_model.h5 → my_model.tflite
- Binary to C array conversion : my_model.tflite → my_model_data.c / .h
- This step is performed using : octets.py

Model conversion for microcontrollers using TensorFlow Lite (`mon_modele.tflite`, `mon_modele_data.h`).
These files are used directly by the Arduino sketch.

## Execution on Arduino

The file :

arduino/projetarduino/projetarduino.ino

Loads the embedded TFLite model, reads real-time IMU values, and predicts the movement performed.
Display via the serial port.

- Arduino sketch (`projetardui.ino`) incorporating the model.
- `.h` files for running the model directly on the board.
- The IMU sensor detects movements in real time and displays them.

## Project structure

```
projet-imu/
│
├── data/               # raw CSV (data.csv)
├── scripts/            # Python scripts for cleaning and converting
├── model/              # Trained and converted models (h5, TFLite, Arduino data)
├── arduino/            # Arduino files (.ino)
└── README.md
```

[Yasmine Aissa / Yasmine56]
