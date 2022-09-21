import numpy as np
import skfuzzy.membership as mf
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class Variable:
    def __init__(self, type, name) -> None:
        self.type = type
        self.name = name
        self.membership_functions = {}
        self.mf_function_value = {}
        self.var_fit = {}
        self.function_type = None
        self.fig, self.graph = plt.subplots(nrows=1, figsize=(10, 6))
        self.variable = None
        self.variable_ctrl = None
        self.input = None
        self.start = None
        self.end = None

    def set_input(self, input):
        self.input = input

    def init_range(self, start, end):
        self.start = start
        self.end = end
        if self.type == "input":
            self.variable_ctrl = ctrl.Antecedent(np.arange(start, end, 1), self.name)

        elif self.type == "output":
            self.variable_ctrl = ctrl.Consequent(np.arange(start, end, 1), self.name)
        self.variable = np.arange(start, end, 1)

    def add_plot(self, key, membership_funct):
        self.graph.plot(
            self.variable,
            membership_funct,
            linewidth=2,
            label=key,
        )

    def add_trimf_membership_function(self, key, values):
        self.variable_ctrl[key] = fuzz.trimf(self.variable_ctrl.universe, values)
        self.membership_functions[key] = mf.trimf(self.variable, values)
        self.add_plot(key, self.membership_functions[key])

        # self.membership_functions[key] = mf.trimf(self.variable, values)
        # self.add_plot(key, self.membership_functions[key])
        # if self.type == "input":
        #     self.var_fit[key] = fuzz.interp_membership(self.variable, self.membership_functions[key], self.input)

    def add_gaussmf_membership_function(self, key, mean, sigma):
        self.variable_ctrl[key] = fuzz.gaussmf(self.variable_ctrl.universe, mean, sigma)
        self.membership_functions[key] = mf.gaussmf(self.variable, mean, sigma)
        self.add_plot(key, self.membership_functions[key])

    def add_trapmf_membership_function(self, key, values):
        self.variable_ctrl[key] = fuzz.trapmf(self.variable_ctrl.universe, values)
        self.membership_functions[key] = mf.trapmf(self.variable, values)
        self.add_plot(key, self.membership_functions[key])
