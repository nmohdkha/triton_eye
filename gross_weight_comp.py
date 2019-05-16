import numpy as np

from openmdao.api import ExplicitComponent

class GrossWeightComp(ExplicitComponent):

    def setup(self):
        self.add_input('W_lg')
        self.add_input('W_tail')
        self.add_input('W_wing')
        self.add_input('W_wing_control')
        self.add_output('W_0')
        #self.declare_partials('W_LG','W_0'),method='cs')
        
    def compute(self, inputs, outputs):
        W_lg = inputs['W_lg']
        W_tail = inputs['W_tail']
        W_wing = inputs['W_wing']
        W_wing_control = inputs['W_wing_control']
        
        outputs['W_0'] = W_lg + W_tail + W_wing + W_wing_control
#    def compute_partials(self, inputs, partials):
#        partials['W_tail', 'S_t'] = 3
