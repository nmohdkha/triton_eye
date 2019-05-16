import numpy as np

from openmdao.api import ExplicitComponent

class WingControlWeightComp(ExplicitComponent):

    def setup(self):
        self.add_input('W_0')
        self.add_output('W_WingControl')
        #self.declare_partials('W_LG','W_0)',method='cs')
        
    def compute(self, inputs, outputs):
        W_0 = inputs['W_0']
        outputs['W_WingControl'] = 56.01*(W_0*10**(-3))**(0.576)
#    def compute_partials(self, inputs, partials):
#        partials['W_tail', 'S_t'] = 3