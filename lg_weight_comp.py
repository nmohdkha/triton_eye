import numpy as np

from openmdao.api import ExplicitComponent


class LGWeightComp(ExplicitComponent):

    def setup(self):
        self.add_input('W_0')
        self.add_output('W_LG')
        #self.declare_partials('W_LG','W_0)',method='cs')
        
    def compute(self, inputs, outputs):
        W_0 = inputs['W_0']
        outputs['W_LG'] = 62.21*(W_0*10**(-3))**0.84
#    def compute_partials(self, inputs, partials):
#        partials['W_LG', 'W0'] = 