import numpy as np

from openmdao.api import ExplicitComponent


class CLaComp(ExplicitComponent):

    def setup(self):
        self.add_input('AR')
        self.add_input('M')
        self.add_input('Cla')
        #self.add_input('Sweepmaxt') no sweep (can add later but makes eqn messy)
        #self.add_input('Sexposed') function of S
        self.add_input('S')
        self.add_input('d_fuse')
        self.add_input('b_wing')
        self.add_output('CLa')
        self.declare_partials('AR','M','Cla','S','d_fuse','b_wing','CLa',method='cs')
        # do I need to declare partials if the values are constant? e.g. Cla
        # b_wing, AR, and S are not independent of each other...better to calc one below and
        # delete an input above?
        
    def compute(self, inputs, outputs):
        AR = inputs['AR']
        S = inputs['S']
        M = inputs['M']
        Beta = np.sqrt(1-M**2)
        neta = inputs['Cla']/(2*np.pi/Beta)
        #Sweepmaxt = inputs['Sweepmaxt']
        #Sexposed = inputs['Sexposed']
        d_fuse = inputs['d_fuse']
        b_wing = inputs['b_wing']
        F = 1.07*(1+d_fuse/b_wing)**2

        outputs['CLa'] = 2*np.pi*AR*((S*.9)/S)*F/(2 + np.sqrt(4 + AR**2*Beta**2/(neta**2)))


