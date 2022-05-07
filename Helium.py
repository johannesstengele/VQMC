"""
@author: Magdalena and Johannes
"""
import numpy as np

class Helium:
    def __init__(self):
        self.init_alpha = 0.25
        self.dimension = 6

    def trial(self, parameters, alpha):
        position_1 = parameters[:3]
        position_2 = parameters[3:]
        r12 = np.linalg.norm(position_1-position_2)
        return np.exp(-2*np.linalg.norm(position_1) - 2*np.linalg.norm(position_2) + r12/(2*(1 + alpha*r12)))

    def local(self, parameters, alpha):
        position_1 = parameters[:3]
        position_2 = parameters[3:]
        r_hat_1 = position_1/np.linalg.norm(position_1)
        r_hat_2 = position_2/np.linalg.norm(position_2)
        r12 = np.linalg.norm(position_1 - position_2)
        return -4 + np.dot((r_hat_1 - r_hat_2),(position_1 - position_2)) * (1/(r12*(1 + alpha*r12)**2)) \
                - 1/(r12*(1 + alpha*r12)**3) - 1/(4*(1 + alpha*r12)**4) + 1/r12

    def trial_ln_derivation(self, parameters,alpha):
        """
        Calculates the value of the derivation of log(\psi_trial) acording to alpha
        """
        position_1 = parameters[:3]
        position_2 = parameters[3:]
        r12 = np.linalg.norm(position_1-position_2)
        return - r12**2 / (2*(1+alpha*r12)**2)
