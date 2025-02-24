import numpy as np
import matplotlib.pyplot as plt
from Activation import Activation


class JacTest:

    @staticmethod
    def func_by_x(activation_name, weights, biases, resnet=False):
        activation = Activation(activation_name)
        if resnet:
            return lambda x: activation.apply(np.dot(weights, x) + biases) + x
        else:
            return lambda x: activation.apply(np.dot(weights, x) + biases)

    @staticmethod
    def func_by_w(activation_name, input_value, biases, resnet=False):
        activation = Activation(activation_name)
        if resnet:
            return lambda w: activation.apply(np.dot(w, input_value) + biases) + input_value
        else:
            return lambda w: activation.apply(np.dot(w, input_value) + biases)

    @staticmethod
    def func_by_b(activation_name, input_value, weights, resnet=False):
        activation = Activation(activation_name)
        if resnet:
            return lambda b: activation.apply(np.dot(weights, input_value) + b) + input_value
        else:
            return lambda b: activation.apply(np.dot(weights, input_value) + b)

    def __init__(self, func, input_val, val_name):
        self.val_name = val_name
        self.eps0 = 1
        self.eps_i = 0.5
        self.func = func
        self.col, self.row = input_val.shape[0], input_val.shape[1]
        random_vec = np.random.rand(self.col, self.row)
        norm = np.linalg.norm(random_vec)
        self.d_vec = random_vec / norm
        self.input = input_val

    def jac_m_v(self, jac_val, v):
        result = None
        if self.val_name == "X":
            # x -> (input_dim, 1)
            # v = d -> (input_dim, 1)
            # jac_val -> (output_dim, input_dim)
            result = np.dot(jac_val, v)
        elif self.val_name == "W":
            # w -> (output-dim, input_dim)
            # v = d -> (output-dim, input_dim)
            # jac_val -> (output_dim, input_dim)
            result = np.sum(v * jac_val, axis=1).reshape(self.col, 1)
        else:
            # b -> (output-dim, 1)
            # v = d -> (output-dim, 1)
            # jac_val -> (output_dim, 1)
            result = np.multiply(jac_val, v)
        return result

    def jacobian_test(self, iterations, jac_input):
        O_e = []
        O_e2 = []
        for i in range(iterations):
            f_x = self.func(self.input)
            x_eps_d = self.input + (self.eps0 * self.eps_i ** i) * self.d_vec
            f_x_eps_d = self.func(x_eps_d)
            eps_d = (self.eps0 * self.eps_i ** i) * self.d_vec
            O_e.append(np.log(np.linalg.norm(f_x - f_x_eps_d)))
            O_e2.append(np.log(np.linalg.norm(f_x_eps_d - f_x - self.jac_m_v(jac_input, eps_d))))
        self.plot_jac(O_e, O_e2)

    def plot_jac(self, O_e, O_e2):
        indexes = range(1, len(O_e) + 1)
        plt.figure(figsize=(10, 5))
        plt.plot(indexes, O_e, marker='o', linestyle='-', color='blue', label='O_e1')
        plt.plot(indexes, O_e2, marker='s', linestyle='-', color='red', label='O_e2')
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.title(f"Jacobian of {self.val_name} - O(eps) and O(eps^2) Values by Index")
        plt.legend()
        plt.grid(True)
        plt.show()


""" 
        # Print both values in 2 columns
        print("Index\tO_e1\t\t\t\t\tO_e2")
        for i, (val1, val2) in enumerate(zip(O_e, O_e2), 1):
            print(f"{i}\t{val1}\t{val2}")
"""


