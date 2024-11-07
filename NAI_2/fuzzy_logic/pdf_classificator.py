from cv_data_extractor import CVExtractor
from fuzzy_logic import FuzzyClassificator
from candidate_classificator import Classificator
import os
import shutil


class PdfClassificator:
    def __init__(self):
        self.cv_folder_path = "../CV"
        self.classified_folder_path = "../CV_classified"

    @staticmethod
    def classify_candidate(cv_path: str) -> str:
        """
        Wykonuję klasyfikacje kandydata do poszczególnej grupy
        
        :param cv_path: ścieżka do CV
        :return: wartość string opisująca kwalifikacje kandydata
        """
        language, education, experience = CVExtractor.extract_cv_details(cv_path)
        candidate_level = FuzzyClassificator.evaluate_candidate(language, education, experience)
        candidate_qualification = Classificator.classify_worker_output(candidate_level)
        return candidate_qualification

    def classify_all_cvs(self) -> None:
        """
        Klasyfikuję CV każdego kandydata w folderze
        
        :return:
        """
        for file in os.listdir(self.cv_folder_path):
            if file.endswith(".pdf"):
                path = self.cv_folder_path + "/" + file
                self.move_to_classified_folder(
                    PdfClassificator.classify_candidate(path),
                    path,
                )

    def move_to_classified_folder(self, candidate_qualification: str, source_path: str) -> None:
        """
        Przenosi CV kandydata do poszczególnego folderu w zależności od kwalifikacji 
        
        :param candidate_qualification: poziom kwalifikacji kandydata
        :param source_path: ścieżka CV do uporządkowania
        :return:
        """
        if candidate_qualification == "not qualified":
            destination_folder = os.path.join(self.classified_folder_path, "not qualified")
        elif candidate_qualification == "qualified":
            destination_folder = os.path.join(self.classified_folder_path, "qualified")
        elif candidate_qualification == "priority qualified":
            destination_folder = os.path.join(self.classified_folder_path, "priority")
        else:
            return

        os.makedirs(destination_folder, exist_ok=True)

        shutil.copy2(
            source_path,
            os.path.join(
                destination_folder,
                os.path.basename(source_path),
            ),
        )
