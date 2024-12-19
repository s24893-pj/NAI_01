from tensorflow.keras import datasets
from tensorflow.keras.layers import Conv2D, Dense, Flatten, Dropout
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import BatchNormalization
import tensorflow as tf

# Wczytanie danych
(X_train, y_train), (X_test, y_test) = datasets.cifar10.load_data()
classes = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]

# Podział danych na testowe i treningowe
X_train = X_train / 255.0
X_test = X_test / 255.0
y_train, y_test = y_train.flatten(), y_test.flatten()


def cifar10_nn_model_1():
    """Tworzy konwolucyjną sieć neuronową przeznaczoną do klasyfikacji obrazów z zestawu danych CIFAR-10.

        Model zaprojektowany jest do pracy z obrazami o rozmiarze 32x32 pikseli

        Returns:
            tf.keras.Sequential
    """
    input_shape = (32, 32, 3)
    K = 10
    model = tf.keras.Sequential([
        Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape),
        BatchNormalization(),
        Conv2D(32, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),

        Conv2D(64, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),

        Conv2D(128, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),

        Flatten(),
        Dropout(0.2),
        Dense(1024, activation='relu'),
        Dropout(0.2),
        Dense(K, activation='softmax')
    ])
    return model

def cifar10_nn_model_2():
    """Tworzy konwolucyjną sieć neuronową przeznaczoną do klasyfikacji obrazów z zestawu danych CIFAR-10.

        Model zaprojektowany jest do pracy z obrazami o rozmiarze 32x32 pikseli

        Returns:
            tf.keras.Sequential
    """
    input_shape = (32, 32, 3)
    K = 10
    model = tf.keras.Sequential([
        Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape),
        BatchNormalization(),
        Conv2D(32, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),

        Flatten(),
        Dropout(0.2),
        Dense(1024, activation='relu'),
        Dropout(0.2),
        Dense(K, activation='softmax')
    ])
    return model

model_1 = cifar10_nn_model_1()
model_2 = cifar10_nn_model_2()

model_1.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model_2.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Sprawdzamy dokładność ostatniej epoki obu modeli
history_1 = model_1.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=5)
history_2 = model_2.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=5)

train_accuracy_1 = history_1.history['accuracy'][-1]
train_accuracy_2 = history_2.history['accuracy'][-1]

val_accuracy_1 = history_1.history['val_accuracy'][-1]
val_accuracy_2 = history_2.history['val_accuracy'][-1]

print(f"Model 1 - Training Accuracy: {train_accuracy_1:.4f}")
print(f"Model 1 - Validation Accuracy: {val_accuracy_1:.4f}")

print(f"Model 2 - Training Accuracy: {train_accuracy_2:.4f}")
print(f"Model 2 - Validation Accuracy: {val_accuracy_2:.4f}")
