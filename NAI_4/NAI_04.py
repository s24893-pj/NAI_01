import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# Wczytanie danych
data = pd.read_csv("pima-indians-diabetes.csv")
data_names = ["Number of times pregnant", "Plasma glucose concentration", "Diastolic blood pressure",
              "Triceps skinfold thickness", "2-Hour serum insulin", "Body mass index", "Diabetes pedigree function.",
              "Age", "Class variable"]

# Ustawienie kolumn dla danych
data.columns = data_names

# Wypełnienie brakujących wartości w dataframie
data.fillna(data.median(), inplace=True)

"""
Usunięcie kolumn zmiennej klasy z wartości X
ustawienie wartości kolumn zmiennej klasy na wartość y
"""
X = data.drop('Class variable', axis=1)
y = data['Class variable']

# Podział na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

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

# Przykład wizualicacji danych na podstawie indeksu masy ciała
plt.figure(figsize=(8, 6))
sns.histplot(data=data, x="Body mass index", hue="Class variable", kde=True)
plt.title('Rozkład indeksu masy ciała w zależności od wyniku')
plt.xlabel('Body mass index')
plt.ylabel('')
plt.show()

"""
Utworzenie listy danych dla procesu przewidywania przez algorytm klasyfikacji
Klasyfikacja danych na drzewa decyzyjnego i SVM
"""
example_data = np.array([[10, 101, 76, 48, 180, 32.9, 0.171, 63],
                         [2, 122, 70, 27, 0, 36.8, 0.340, 27],
                         [5, 121, 72, 23, 112, 26.2, 0.245, 30],
                         [1, 126, 60, 0, 0, 30.1, 0.349, 47],
                         [1, 93, 70, 31, 0, 30.4, 0.315, 23]])
dt_example_predictions = dt_classifier.predict(example_data)
svm_example_predictions = svm_classifier.predict(example_data)

# Wypisanie predykcji dla przykładowych danych wejściowych
print("\nPredykcje dla przykładowych danych - Drzewo decyzyjne:", dt_example_predictions)
print("\nPredykcje dla przykładowych danych - SVM:", svm_example_predictions)
