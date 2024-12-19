import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# Wczytanie danych
data = pd.read_csv("data.csv")
data_names = ["id", "diagnosis", "radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean",
              "compactness_mean", "concavity_mean", "concave points_mean", "symmetry_mean", "fractal_dimension_mean",
              "radius_se", "texture_se", "perimeter_se", "area_se", "smoothness_se", "compactness_se", "concavity_se",
              "concave points_se", "symmetry_se", "fractal_dimension_se", "radius_worst", "texture_worst",
              "perimeter_worst", "area_worst", "smoothness_worst", "compactness_worst", "concavity_worst",
              "concave points_worst", "symmetry_worst", "fractal_dimension_worst"
              ]

# Ustawienie kolumn dla danych
data.columns = data_names

# Zamiana danych w kolumnie diagnozy na wartości liczbowe
data['diagnosis'] = data['diagnosis'].apply(lambda x: 0 if x == 'M' else x)
data['diagnosis'] = data['diagnosis'].apply(lambda x: 1 if x == 'B' else x)

"""
Usunięcie kolumn diagnozy oraz id z wartości X
ustawienie wartości kolumn diagnozy na wartość y
"""
X = data.drop(['diagnosis', 'id'], axis=1)
y = data['diagnosis']

# Wypełnienie brakujących wartości w dataframie
data.fillna(data.median(), inplace=True)

# Podział na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Trenowanie klasyfikatora drzewa decyzyjnego
dt_classifier = DecisionTreeClassifier(random_state=42)
dt_classifier.fit(X_train, y_train)
dt_predictions = dt_classifier.predict(X_test)

# Trenowanie klasyfikatora SVM
svm_classifier = SVC(random_state=42)
svm_classifier.fit(X_train, y_train)
svm_predictions = svm_classifier.predict(X_test)

"""
Wypisanie najważniejszych metryk
Wypisanie macierzy błędów
Wypisanie dokładności modelu
"""
print("Drzewo decyzyjne:")
print(classification_report(y_test, dt_predictions))
print(confusion_matrix(y_test, dt_predictions))
print("Dokładność:", accuracy_score(y_test, dt_predictions))

print("\nSVM:")
print(classification_report(y_test, svm_predictions))
print(confusion_matrix(y_test, svm_predictions))
print("Dokładność:", accuracy_score(y_test, svm_predictions))

# Przykład wizualicacji danych na podstawie średniej promienia
plt.figure(figsize=(8, 6))
sns.histplot(data=data, x="radius_mean", hue="diagnosis", kde=True)
plt.title('Rozkład średniej promienia zależnie od wyniku')
plt.xlabel('Średni promień')
plt.ylabel('')
plt.show()

"""
Utworzenie listy danych dla procesu przewidywania przez algorytm klasyfikacji
Klasyfikacja danych na podstawie drzewa decyzyjnego i SVM
"""
example_data = np.array([[20.13, 28.25, 131.2, 1261, 0.0978, 0.1034, 0.144, 0.09791, 0.1752, 0.05533, 0.7655, 2.463,
                          5.203, 99.04, 0.005769, 0.02423, 0.0395, 0.01678, 0.01898, 0.002498, 23.69, 38.25, 155, 1731,
                          0.1166, 0.1922, 0.3215, 0.1628, 0.2572, 0.06637],
                         [16.6, 28.08, 108.3, 858.1, 0.08455, 0.1023, 0.09251, 0.05302, 0.159, 0.05648, 0.4564, 1.075,
                          3.425, 48.55, 0.005903, 0.03731, 0.0473, 0.01557, 0.01318, 0.003892, 18.98, 34.12, 126.7,
                          1124, 0.1139, 0.3094, 0.3403, 0.1418, 0.2218, 0.0782],
                         [20.6, 29.33, 140.1, 1265, 0.1178, 0.277, 0.3514, 0.152, 0.2397, 0.07016, 0.726, 1.595, 5.772,
                          86.22, 0.006522, 0.06158, 0.07117, 0.01664, 0.02324, 0.006185, 25.74, 39.42, 184.6, 1821,
                          0.165, 0.8681, 0.9387, 0.265, 0.4087, 0.124],
                         [7.76, 24.54, 47.92, 181, 0.05263, 0.04362, 0, 0, 0.1587, 0.05884, 0.3857, 1.428, 2.548, 19.15,
                          0.007189, 0.00466, 0, 0, 0.02676, 0.002783, 9.456, 30.37, 59.16, 268.6, 0.08996, 0.06444, 0,
                          0, 0.2871, 0.07039]
                         ])
dt_predictions = dt_classifier.predict(example_data)
svm_predictions = svm_classifier.predict(example_data)

# Wypisanie predykcji dla przykładowych danych wejściowych
print("\nPredykcje dla przykładowych danych - Drzewo decyzyjne:", dt_predictions)
print("\nPredykcje dla przykładowych danych - SVM:", svm_predictions)
