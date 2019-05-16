import numpy as np

from openmdao.api import ExplicitComponent

class WingWeightComp(ExplicitComponent):

    def setup(self):
        self.add_input('S')
        self.add_input('AR')
        self.add_input('q')
        self.add_input('taper')
        self.add_input('thickness_ratio')
        self.add_input('n')
        self.add_input('W_0')
        self.add_output('W_wing')
        #self.declare_partials('W_LG','W_0'),method='cs')
        
    def compute(self, inputs, outputs):
        S = inputs['S']
        AR = inputs['AR']
        q = inputs['q']
        taper = inputs['taper']
        thickness_ratio = inputs['thickness_ratio']
        n_ult = 1.5*inputs['n']
        W_0 = inputs['W_0']
        fudge_wing = 0.85
        outputs['W_wing'] = fudge_wing*0.036*S**0.758*(AR)**0.6*q**0.006*taper**0.04*(100*thickness_ratio)**-0.3*(n_ult*W_0)**0.49
#    def compute_partials(self, inputs, partials):
#        partials['W_tail', 'S_t'] = 3
