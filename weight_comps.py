from openmdao.api import ExplicitComponent
from numpy import cos
from math import pi



#********* WING WEIGHT **********
class WingWeightComp(ExplicitComponent): 
    def setup(self):
        # Variable Inputs
        self.add_input('W0')
        self.add_input('S')
        self.add_input('AR')
        self.add_input('Tap')
        self.add_input('Swp')
        # Constant Inputs
        self.add_input('M0')
        self.add_input('nUlt')
        self.add_input('tc')
        # Outputs
        self.add_output('WingW')
        # Partial Declaration
        self.declare_partials('WingW','*',method='cs')
        
    def compute(self, inputs, outputs):
        S    = inputs['S']
        W0   = inputs['W0']
        AR   = inputs['AR']
        Tap  = inputs['Tap']
        Swp  = inputs['Swp']
        M0   = inputs['M0']
        nUlt = inputs['nUlt']
        tc   = inputs['tc']
        
        outputs['WingW'] = 0.000428*S**0.48*AR*M0**0.43*(W0*nUlt)**0.84 \
        *Tap**0.14/(100*tc)**0.76/cos(Swp)**1.54



#********* TAIL WEIGHT **********
class TailWeightComp(ExplicitComponent):
    def setup(self):
        # Variable Inputs
        self.add_input('W0')
        self.add_input('Sh')
        self.add_input('bh')    # Horizontal Stabilizer Span [ft]
        self.add_input('trh')   # Thickness of horizontal tail at root [ft]
        self.add_input('mac')  
        self.add_input('tma')
        # Constant Inputs
        self.add_input('nUlt')
        # Outputs
        self.add_output('TailW')
        # Partial Declaration
        self.declare_partials('TailW','*',method='cs')
        
    def compute(self,inputs,outputs):
        W0 = inputs['W0']
        nUlt = inputs['nUlt']
        Sh = inputs['Sh']
        bh = inputs['bh']
        trh = inputs['trh']
        mac = inputs['mac']
        tma = inputs['tma']
        
        gamma = (W0*nUlt)**0.813*Sh**0.584*(bh/trh)**0.033*(mac/tma)**0.28
        HTailW = 0.0034*gamma**0.915
        
        outputs['TailW'] = HTailW



#********* FUSELAGE WEIGHT ********** 
class FuselageWeightComp(ExplicitComponent):  
    def setup(self):
        # Variable Inputs
        self.add_input('W0')
        self.add_input('l')
        self.add_input('d')
        # Constant Inputs
        self.add_input('qmax')
        # Outputs
        self.add_output('FuseW')
        # Partial Declaration
        self.declare_partials('FuseW','*',method='cs')
        
    def compute(self,inputs,outputs):
        W0   = inputs['W0']
        l    = inputs['l']
        d    = inputs['d']
        qmax = inputs['qmax']
        
        outputs['FuseW'] = 10.43*(qmax/100)**0.283*(W0/1000)**0.95*(l/d)**0.71



#********* LANDING GEAR WEIGHT **********
class LandingGearWeightComp(ExplicitComponent):
    def setup(self):
        # Variable Inputs
        self.add_input('W0')
        # Outputs
        self.add_output('LandGearW')
        # Partial Declaration
        self.declare_partials('LandGearW','*',method='cs')
        
    def compute(self,inputs,outputs):
        W0 = inputs['W0']
        outputs['LandGearW'] = 62.21*(W0/1000)**0.84
        


#********* FUEL TANK WEIGHT **********
class FuelTankWeightComp(ExplicitComponent):       
    def setup(self):
        # Variable Inputs
        self.add_input('d')
        self.add_input('lt')
        # Constant Inputs
        self.add_input('Pmax')
        self.add_input('rhoT')
        self.add_input('stressT')
        self.add_input('g')
        # Outputs
        self.add_output('TankW')
        # Partial Declaration
        self.declare_partials('TankW','*',method='cs')
        
    def compute(self,inputs,outputs):
        d       = inputs['d']
        lt      = inputs['lt']       # Cylinder length
        Pmax    = inputs['Pmax']     # Pressure Difference
        rhoT    = inputs['rhoT']     # Density of tank material
        stressT = inputs['stressT']  # Max tolerable stress of material
        g       = inputs['g']
        
        outputs['TankW'] = 2*pi*d*d/4*(d/2+lt)*Pmax*rhoT/stressT



#********* PROPELLER WEIGHT **********
class PropellerWeightComp(ExplicitComponent):
    def setup(self):
        # Variable Inputs
        self.add_input('dp')
        # Constant Inputs
        self.add_input('Np')
        self.add_input('Nb')
        self.add_input('hp')
        # Outputs
        self.add_output('PropW')
        # Partial Declaration
        self.declare_partials('PropW','*',method='cs')
        
    def compute(self,inputs,outputs):
        Np = inputs['Np']
        Nb = inputs['Nb']
        dp = inputs['dp']
        hp = inputs['hp']
        
        outputs['PropW'] = 28*Np*Nb**0.391*(dp*hp/1000)**0.782



#********* Motor Weight **********
class MotorWeightComp(ExplicitComponent):
    def setup(self):
        # Constant Inputs
        self.add_input('Np')
        self.add_input('MotorWeight')
        # Outputs
        self.add_output('MotorW')
        
    def compute(self,inputs,outputs):
        Np = inputs['Np']
        MotorWeight = inputs['MotorWeight']
        
        outputs['MotorW'] = Np*MotorWeight
        


#********* FUEL CELL WEIGHT **********
class FuelCellWeightComp(ExplicitComponent):
    def setup(self):
        # Constant Inputs
        self.add_input('Np')
        self.add_input('CellWeight')
        # Outputs
        self.add_output('CellW')
        
    def compute(self,inputs,outputs):
        Np = inputs('Np')
        CellWeight = inputs('CellWeight')
        
        outputs['CellW'] = Np*CellWeight