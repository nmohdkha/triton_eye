from openmdao.api import ExplicitComponent

class WingParamComp(ExplicitComponent):
    
    def setup(self):
        self.add_input('taper')
        self.add_input('b')
        self.add_input('croot')
        self.add_output('mac') #mean aerodynamic chord of the wing
        self.add_output('Ybar') #spanwise location of the mac

    def compute(self, inputs, outputs):
        taper=inputs['taper']
        b=inputs['b']
        croot=inputs['croot']
        #outputs['ybar']=(b/6)*(1+2*taper)/(1+taper)
        outputs['mac']=(2/3)*croot*(1+taper+taper**2)/(1+taper)