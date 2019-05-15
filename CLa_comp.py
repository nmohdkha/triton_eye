import numpy as np

from openmdao.api import ExplicitComponent


class CLaComp(ExplicitComponent):

    def setup(self):
        self.add_input('AR')
        self.add_input('M')
        self.add_input('netta')
        #self.add_input('Sweepmaxt') no sweep (can add later but makes eqn messy)
        #self.add_input('Sexposed') function of S
        self.add_input('S')
        self.add_input('d_fuse')
        self.add_input('b_wing')
        self.add_output('CLa')
        

        self.declare_partials('*', '*')

    def compute(self, inputs, outputs):
        AR = inputs['AR']
        M = inputs['M']
        netta = inputs['netta']
        Sweepmaxt = inputs['Sweepmaxt']
        Sexposed = inputs['Sexposed']
        Sref = inputs['Sref']
        d_fuse = inputs['d_fuse']
        b_wing = inputs['b_wing']

        outputs['CLa'] = 2*np.pi*AR*((S*.9)/S)*(1.07*(1 + d_fuse/b_wing)**2)/(2 + np.sqrt(4 + AR^2*(1-M**2)/(neta**2)))

    #def compute_partials(self, inputs, partials):
    #    V0 = inputs['V0']
    #    theta = inputs['theta']
    #    t = inputs['t']

    #    partials['dy', 'V0'] = np.sin(theta) * t
    #    partials['dy', 'theta'] = V0 * np.cos(theta) * t
    #    partials['dy', 't'] = V0 * np.sin(theta) - 9.81 * t
