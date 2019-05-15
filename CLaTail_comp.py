import numpy as np

from openmdao.api import ExplicitComponent


class CLaTailComp(ExplicitComponent):

    def setup(self):
        self.add_input('AR_t')
        self.add_input('M')
        self.add_input('Cla_t')
        #self.add_input('Sweepmaxt') no sweep (can add later but makes eqn messy)
        #self.add_input('Sexposed') function of S
        self.add_input('S_t')
        self.add_input('d_fuse')
        self.add_input('b_t')
        self.add_output('CLa_t')
        self.declare_partials('AR_t','M','Cla_t','S_t','d_fuse','b_t','CLa_t',method='cs')
        self.declare_partials('CLa_t','*',method='cs')
        # do I need to declare partials if the values are constant? e.g. Cla
        # b_wing, AR, and S are not independent of each other...better to calc one below and
        # delete an input above?
        
    def compute(self, inputs, outputs):
        AR_t = inputs['AR_t']
        S_t = inputs['S_t']
        M = inputs['M']
        Beta = np.sqrt(1-M**2)
        neta_t = inputs['Cla_t']/(2*np.pi/Beta)
        #Sweepmaxt = inputs['Sweepmaxt']
        #Sexposed = inputs['Sexposed']
        d_fuse = inputs['d_fuse']
        b_t = inputs['b_t']
        F_t = 1.07*(1+d_fuse/b_t)**2

        outputs['CLa_t'] = 2*np.pi*AR_t*((S_t*.9)/S_t)*F_t/(2 + np.sqrt(4 + AR_t**2*Beta**2/(neta_t**2)))
