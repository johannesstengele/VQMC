"""
@author: Magdalena and Johannes
"""

import numpy as np
from helium import *
from harmonic_oscillator import *
from hydrogen import *

import matplotlib.pyplot as plt

class VQMC:
    """
    Variational Quantum Markov Chain class.
    """

    def __init__(self, num_walkers=400, max_step_length=0.5, num_steps_equilibrate=4000, model ="Helium", init_alpha=None): #need to include also the derivative function for gradient calculation!!!
        if model=="Helium":
            self.psi_T = helium_trial
            self.energy_L = helium_local
            self.alpha = helium_init_alpha
            self.dimension = helium_dimension
            self.derivation_log_trial = helium_trial_ln_derivation
        elif model=="Hydrogen":
            self.psi_T = hydrogen_trial
            self.energy_L = hydrogen_local
            self.alpha = hydrogen_init_alpha
            self.dimension = hydrogen_dimension
            self.derivation_log_trial = hydrogen_trial_ln_derivation
        elif model=="LHO":
            self.psi_T = ho_trial
            self.energy_L = ho_local
            self.alpha = ho_init_alpha
            self.dimension = ho_dimension
            self.derivation_log_trial = ho_trial_ln_derivation

            
        else:
            print("Check your model inputs!")
            exit(1)
        if init_alpha!=None:
            self.alpha=init_alpha

        self.num_walkers = num_walkers
        self.chains = [[] for i in range(self.num_walkers)]
        self.initialize_walkers()

        self.max_step_length = max_step_length
        self.energy = []
        
        self.num_tried = 0
        self.num_accepted = 0

        self.equilibrate(num_steps_equilibrate) #this probably needs to be moved elsewhere so the code makes more sence!!!




    def initialize_walkers(self):
        np.random.seed(42)
        init = np.random.normal(loc=0, scale=10, size=(self.num_walkers,self.dimension))
        self.old_psi_squared = []
        for walker in range(self.num_walkers):
            self.chains[walker].append(init[walker, :])
            self.old_psi_squared.append(self.psi_T(init[walker, :], self.alpha)**2)

        return 0

    def single_walker_step(self, old_state, old_psi_squared):
        
        self.num_tried += 1
        displacement = (2*np.random.rand(self.dimension) - 1)*self.max_step_length
        new_state = old_state + displacement
        new_psi_squared = self.psi_T(new_state, self.alpha)**2

        p = new_psi_squared/old_psi_squared
        if p >= 1.0:
            self.num_accepted +=1
            return new_state, new_psi_squared
        else:
            q = np.random.random()
            if q < p:
                self.num_accepted +=1
                return new_state, new_psi_squared
                
            else:
                return old_state, old_psi_squared

    def MC_step(self):
        for walker in range(self.num_walkers):
            #if walker == 0:
            #    print(self.old_psi_squared[walker])
            #    print(self.chains[walker])

            new_state, self.old_psi_squared[walker] = \
                self.single_walker_step(self.chains[walker][-1], self.old_psi_squared[walker])
            self.chains[walker].append(new_state)

    def equilibrate(self, num_steps): #NEEDS TO BE REDONE!!!
    
        for i in range(num_steps):
            self.MC_step()
            
        #print(self.chains)
        #print(self.old_psi_squared)
        print("accepted/tried ratio: ", self.num_accepted/self.num_tried)

        #print("Total energy: ", tot_energy/((num_steps-4000)*self.num_walkers))
        
    def get_energy_mean_value(self, num_steps):
        """
        Initializes the system and calculates the mean value of energy for a current alpha of the system.

        """
        tot_energy=0
        self.walker_energy = [[] for i in range(self.num_walkers)]
        for i in range(num_steps):
            self.MC_step()
            energy = 0
            for walker in range(self.num_walkers):
                E = self.energy_L(self.chains[walker][-1], self.alpha)
                self.walker_energy[walker].append(E)
                energy += E
            self.energy.append(energy/self.num_walkers)
            tot_energy += energy

        self.chains = [[self.chains[walker][-1]] for walker in range(self.num_walkers)]
        
        return tot_energy/((num_steps)*self.num_walkers)
    
    def save_energy_mean_value(self, name_of_file):
        """
        Saves mean value of energy and corresponding aplha to a file.

        """
        pass
    
    def optimize(self, max_parameters, step):
        """
        Optimization procedure to find the best alpha and corresponding approximate ground energy.

        """
        pass

    def plot_average_local_energies(self):
        """
        Plots the evolution of average local energy of all walkers.

        """
        #for walker in range(self.num_walkers):
        #    plt.plot(range(len(self.energy)), self.walker_energy[walker])

        plt.plot(range(len(self.energy)), self.energy)
        plt.show()
    
    def plot_energy_mean_values(self):
        """
        Plots dependence of mean value of energy on parameters

        """
        pass








