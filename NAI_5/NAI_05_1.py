import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.preprocessing import StandardScaler

# Wczytujemy dane
data = pd.read_csv("pima-indians-diabetes.csv")
data_names = ["Number of times pregnant", "Plasma glucose concentration", "Diastolic blood pressure",
              "Triceps skinfold thickness", "2-Hour serum insulin", "Body mass index", "Diabetes pedigree function.",
              "Age", "Class variable"]
data.columns = data_names
data.fillna(data.median(), inplace=True)
X = data.drop('Class variable', axis=1)
y = data['Class variable']

# standaryzacja danych
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# podział na zbiory treningowe i testowe
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=42)

# Tworzenie sieci neuronowej
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# kompilacja modelu
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# trenowanie modelu
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# Dane do predykcji
example_data = np.array([[10, 101, 76, 48, 180, 32.9, 0.171, 63],
                         [2, 122, 70, 27, 0, 36.8, 0.340, 27],
                         [5, 121, 72, 23, 112, 26.2, 0.245, 30],
                         [1, 126, 60, 0, 0, 30.1, 0.349, 47],
                         [1, 93, 70, 31, 0, 30.4, 0.315, 23]])
# standaryzacja danych do predykcji
example_data_scaled = scaler.transform(example_data)

# Predykcja na example_data
predictions = (model.predict(example_data_scaled) > 0.5).astype(int)
print("\nPredykcje sieci neuronowej:", predictions)