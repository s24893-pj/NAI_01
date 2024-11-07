class Classificator:
    @staticmethod
    def classify_worker_output(worker_output) -> str:
        """
        Klasyfikuje kandydata do poszczególnej grupy

        :param worker_output:
        :return: poziom kwalifikacji kandydata
        """
        if worker_output <= 30:
            return "not qualified"
        elif worker_output <= 70:
            return "qualified"
        else:
            return "priority qualified"
