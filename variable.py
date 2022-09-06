import numpy as np
import skfuzzy.membership as mf
import matplotlib.pyplot as plt


class Variable:
    def __init__(self, type) -> None:
        self.type = type
        self.colors = ["r", "g", "b", "y"]
        self.color_index = 0
        self.membership_functions = {}
        self.fig, self.graph = plt.subplots(nrows=1, figsize=(10, 6))

    def init_range(self, start, end):
        self.variable = np.arange(start, end, 1)

    def add_plot(self, key, membership_funct):
        self.graph.plot(
            self.variable,
            membership_funct,
            self.colors[self.color_index],
            linewidth=2,
            label=key,
        )
        self.color_index += 1

    def add_trimf_membership_function(self, key, values):
        self.membership_functions[key] = mf.trimf(self.variable, values)
        self.add_plot(key, self.membership_functions[key])

    def add_gaussmf_membership_function(self, key, values):
        self.membership_functions[key] = mf.gaussmf(self.variable, values)
        self.add_plot(key, self.membership_functions[key])

    def add_trapmf_membership_function(self, key, values):
        self.membership_functions[key] = mf.trapmf(self.variable, values)
        self.add_plot(key, self.membership_functions[key])
