from pypdf import PdfReader
import re


class CVExtractor:

    @staticmethod
    def convert_language_to_value(language: str) -> int:
        """
        Konwertuje poziom języka na wartość liczbową

        :param language: poziom znajomości języka
        :return: wartość liczbowa odpowiadająca poziomowi języka.
        """
        language_mapping = {
            "a1": 15,
            "a2": 45,
            "b1": 70,
            "b2": 85,
            "c1": 90,
            "c2": 100,
        }
        language_value: int = language_mapping[language]
        return language_value

    @staticmethod
    def convert_education_to_value(
        education_list: list[str],
    ) -> int:
        """
        Konwertuje najwyższy poziom edukacji na wartość liczbową

        :param education_list: lista zawierająca poziom wykształcenia
        :return: wartośc liczbowa odpowiadająca poziomowi edukacji
        """
        education_mapping = {
            "bachelor": 2,
            "master": 4,
            "phd": 6,
        }

        max_value = 0

        for edu in education_list:
            value = education_mapping.get(edu, 0)
            if value > max_value:
                max_value = value

        return max_value

    @staticmethod
    def extract_cv_details(pdf_path: str) -> tuple:
        """
        Wyciąga potrzebne informacje zawarte w CV

        :param pdf_path: ścieżka do pliku pdf zawierającego CV
        :return: informacje zawarte w CV w postaci liczbowej
        """
        reader = PdfReader(pdf_path)
        page = reader.pages[0]
        text = page.extract_text().lower()

        language_level = re.search(r"\b(A1|A2|B1|B2|C1|C2)\b", text, re.IGNORECASE).group(0)

        education_keywords = r"\b(bachelor|master|phd)\b"
        education = re.findall(education_keywords, text, re.IGNORECASE)

        experience = re.findall(r"(\d{4})\s*-\s*(\d{4})", text)
        total_years = sum(int(end) - int(start) for start, end in experience)

        return (
            CVExtractor.convert_language_to_value(language_level),
            CVExtractor.convert_education_to_value(education),
            total_years,
        )
