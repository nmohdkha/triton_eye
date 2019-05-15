import numpy as np

from openmdao.api import ExplicitComponent

class TailWeightComp(ExplicitComponent):

    def setup(self):
        self.add_input('S_t')
        self.add_output('W_Tail')
        #self.declare_partials('W_LG','W_0)',method='cs')
        
    def compute(self, inputs, outputs):
        S_t = inputs['S_t']
        outputs['W_Tail'] = 3*S_t
#    def compute_partials(self, inputs, partials):
#        partials['W_tail', 'S_t'] = 3