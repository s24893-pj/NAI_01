import tensorflow as tf
from tensorflow.keras import datasets
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np
import os
from deep_translator import GoogleTranslator
from sklearn.metrics import confusion_matrix
import seaborn as sns

# Wczytanie danych
(X_train, y_train), (X_test, y_test) = datasets.fashion_mnist.load_data()
X_train = np.expand_dims(X_train, -1)
X_test = np.expand_dims(X_test, -1)


def fashion_nn_model():
    """Tworzy konwolucyjną sieć neuronową przeznaczoną do klasyfikacji obrazów ubrań

        Model Jest zaprojektowany do pracy z obrazami o rozmiarze 28x28 pikseli

        Returns:
            tf.keras.Sequential
    """
    model = tf.keras.Sequential()

    model.add(Conv2D(64, (5, 5),
                     padding="same",
                     activation="relu",
                     input_shape=(28, 28, 1)))

    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, (5, 5), padding="same",
                     activation="relu"))

    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(256, (5, 5), padding="same",
                     activation="relu"))

    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(256, activation="relu"))

    model.add(Dense(10, activation="softmax"))
    return model

# Trenowanie lub wczytanie modelu sieci neuronowej
fashion_model = fashion_nn_model()
if not os.path.exists("nai_05_3_model.keras"):
    fashion_model.compile(optimizer=Adam(learning_rate=1e-3),
                          loss='sparse_categorical_crossentropy',
                          metrics=['sparse_categorical_accuracy'])

    fashion_model.fit(
        X_train.astype(np.float32), y_train.astype(np.float32),
        epochs=10,
        steps_per_epoch=100,
        validation_split=0.33
    )

    fashion_model.save('nai_05_3_model.keras')
else:
    fashion_model.load_weights('nai_05_3_model.keras')

# Przewidywanie danych za pomocą modelu sieci neuronowej
labels = ['t_shirt', 'trouser', 'pullover', 'dress', 'coat',
          'sandal', 'shirt', 'sneaker', 'bag', 'ankle_boots']
predictions = fashion_model.predict(X_test[:14])
predicted_label = labels[np.argmax(predictions[13])]

# Tłumaczenie, wypisanie danych oraz pokazanie przewidywanego obrazu
translator = GoogleTranslator(source='en', target='pl')
translated_predicted_label = translator.translate(predicted_label)
print(f"\nNa obrazie znajduje się: {translated_predicted_label}")
plt.imshow(X_test[:14][13])
plt.show()


# Tworzymy i wizualizujemy "Confussion matrix"
predictions = fashion_model.predict(X_test)
predicted_labels = np.argmax(predictions, axis=1)
cm = confusion_matrix(y_test, predicted_labels)

plt.figure(figsize=(10, 10))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.show()

