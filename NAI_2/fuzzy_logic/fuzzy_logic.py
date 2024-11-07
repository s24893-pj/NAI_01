import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import json


class FuzzyClassificator:

    @staticmethod
    def evaluate_candidate(lang_input: int, edu_input: int, exp_input: int):
        """
        Wykonuje ocenę kandydata na podstawie podanych parametrów w CV

        :param lang_input: wartość liczbowa poziomu języka
        :param edu_input: wartość liczbowa poziomu edukacji
        :param exp_input: wartość liczbowa poziomu doświadczenia zawodowego
        :return: ocena pracownika w postaci liczbowej
        """
        lang = ctrl.Antecedent(np.arange(0, 101, 1), "lang")
        edu = ctrl.Antecedent(np.arange(0, 9, 1), "edu")
        exp = ctrl.Antecedent(np.arange(0, 21, 1), "exp")
        candidate = ctrl.Consequent(np.arange(0, 100, 1), "candidate")

        lang["A1"] = fuzz.trimf(lang.universe, [0, 15, 30])
        lang["A2"] = fuzz.trimf(lang.universe, [20, 45, 60])
        lang["B1"] = fuzz.trimf(lang.universe, [45, 70, 80])
        lang["B2"] = fuzz.trimf(lang.universe, [75, 85, 90])
        lang["C1"] = fuzz.trimf(lang.universe, [85, 90, 95])
        lang["C2"] = fuzz.trimf(lang.universe, [90, 100, 100])

        edu["No Degree"] = fuzz.trimf(edu.universe, [0, 0, 1])
        edu["Bachelor"] = fuzz.trimf(edu.universe, [1, 2, 3])
        edu["Master"] = fuzz.trimf(edu.universe, [3, 4, 5])
        edu["PhD"] = fuzz.trimf(edu.universe, [5, 6, 7])

        exp["low"] = fuzz.trapmf(exp.universe, [0, 1, 2, 3])
        exp["medium"] = fuzz.trapmf(exp.universe, [2, 3, 4, 5])
        exp["high"] = fuzz.trapmf(exp.universe, [4, 6, 20, 20])

        candidate["low"] = fuzz.trapmf(candidate.universe, [0, 0, 20, 30])
        candidate["medium"] = fuzz.trapmf(candidate.universe, [20, 30, 50, 60])
        candidate["high"] = fuzz.trapmf(candidate.universe, [50, 70, 100, 100])

        with open("rules.json", "r") as file:
            json_rules = json.load(file)
        rules = []
        for rule in json_rules:
            rule_condition = lang[rule["lang"]] & edu[rule["edu"]] & exp[rule["exp"]]
            rules.append(ctrl.Rule(rule_condition, candidate[rule["candidate"]]))

        candidate_ctrl = ctrl.ControlSystem(rules)
        candidate_simulation = ctrl.ControlSystemSimulation(candidate_ctrl)

        candidate_simulation.input["lang"] = lang_input
        candidate_simulation.input["edu"] = edu_input
        candidate_simulation.input["exp"] = exp_input

        candidate_simulation.compute()

        return candidate_simulation.output["candidate"]
