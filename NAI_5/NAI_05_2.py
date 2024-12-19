from tensorflow.keras import datasets
import numpy as np
from tensorflow.keras.layers import Conv2D, Dense, Flatten, Dropout
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import BatchNormalization
import matplotlib.pyplot as plt
import tensorflow as tf
import os
from deep_translator import GoogleTranslator

# Wczytanie danych
(X_train, y_train), (X_test, y_test) = datasets.cifar10.load_data()
classes = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]

# Podział danych na testowe i treningowe
X_train = X_train / 255.0
X_test = X_test / 255.0
y_train, y_test = y_train.flatten(), y_test.flatten()


def cifar10_nn_model():
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


# Trenowanie lub wczytanie modelu sieci neuronowej
cifar10_model = cifar10_nn_model()
if not os.path.exists("nai_05_2_model.keras"):
    cifar10_model.compile(optimizer='adam',
                          loss='sparse_categorical_crossentropy',
                          metrics=['accuracy'])

    r = cifar10_model.fit(
        X_train, y_train, validation_data=(X_test, y_test), epochs=10)

    cifar10_model.save('nai_05_2_model.keras')
else:
    cifar10_model.load_weights('nai_05_2_model.keras')


# Przewidywanie danych za pomocą modelu sieci neuronowej
labels = 'airplane automobile bird cat deer dog frog horse ship truck'.split()
p = np.array(X_test[5]).reshape(1, 32, 32, 3)
predicted_label = labels[cifar10_model.predict(p).argmax()]

translator = GoogleTranslator(source='en', target='pl')
# translated = translator.translate("Hello World.")
# print(translated)

# Tłumaczenie, wypisanie danych oraz pokazanie przewidywanego obrazu
translated_predicted_label = translator.translate(predicted_label)
print(f"na obrazie znajduje się {translated_predicted_label}")
plt.imshow(X_test[5])
plt.show()
