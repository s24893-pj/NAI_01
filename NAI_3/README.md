# Silnik rekomendacji filmów

Aplikacja rekomenduje filmy dla użytkownika na podstawie bazy danych w formacie JSON osób oceniających dane 
filmy, aplikacja korzysta z API serwisu zawierającego baze danych istniejących filmów udostniępniając ich opisy.
Sposoby rekomendacji filmów:
- Klasteryzacja
- Odległość Euklidesowa
- Korelacja Pearsona

## Autorzy

- Andrzej Ebertowski s25222
- Mateusz Wiśniewski s24893

## Wymagania

- Python 3.x
- Biblioteka `pandas`
- Biblioteka `scikit-learn`
- Biblioteka `numpy`
- Biblioteka `rich`

### Instalacja wymaganych bibliotek

Aby zainstalować niezbędne biblioteki, uruchom poniższe polecenia w terminalu:

```bash
pip install numpy
pip install pandas
pip install scikit-learn
pip install rich
```