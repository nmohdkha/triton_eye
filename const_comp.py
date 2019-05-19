from openmdao.api import ExplicitComponent

# Mission Requirements
Vcruise = 270           # Cruise Speed [ft/s]
Vmax    = Vcruise*1.5
rho65k  = 0.000175976   # Air density at 65,000 ft [slugs/ft^3]
sos65k  = 968.076       # Speed of Sound at 65,000 ft [ft/s]
P65k    = 117.787       # Pressure at 65,000 ft [lbf/ft^2]
nPos    = 2             # Max positive load factor
nNeg    = -1            # Max negative load factor   
nUlt    = 1.2*nPos  

# Known Aircraft Parameters
tc      = 0.12          # Max Airfoil thickness to chord ratio
Np      = 4             # Number of propellers
Nb      = 2             # Number of blades per propeller
hp      = 270           # Rated Engine Shaft Horsepower [hp]
MotorWeight = 50        # Weight of motor [lbf]
CellWeight  = 200       # Weight of fuelcell components required for each motor
Pmax    = 100           # Max Pressure in fuel tank [lbf/ft^2]
rhoT    = 10            # Density of tank material [lbf/ft^3]
stressT = 10000         # Max working stress of tank material [lbf/ft^2]
P_W     = 0.06941       # Power-to-weight ratio from prelim. design [hp/lbf]
W_S     = 19            # Wing loading from preliminary design [lbf/ft^2]

# Constants
rhoSL = 0.00237717      # Air density at Sea Level [slugs/ft^3]
sosSL = 1116.45         # Speed of Sound at Sea Level [ft/s]
g     = 32.2            # Acceleration due to gravity [ft/s^2]

class ConstComp(ExplicitComponent):
    def setup(self):
        # Outputs
        self.add_output('M0',           val = (rho65k/rhoSL)**0.5*Vmax/sosSL)
        self.add_output('rhoSL',        val = rhoSL)
        self.add_output('rho65k',       val = rho65k)   
        self.add_output('nUlt',         val = nUlt)
        self.add_output('tc',           val = tc)
        self.add_output('qmax',         val = 0.5*rho65k*Vmax*Vmax)
        self.add_output('g',            val = g)
        self.add_output('Np',           val = Np)
        self.add_output('Nb',           val = Nb)
        self.add_output('hp',           val = hp)
        self.add_output('MotorWeight',  val = MotorWeight)
        self.add_output('CellWeight',   val = CellWeight)
        self.add_output('Pmax',         val = Pmax)
        self.add_output('rhoT',         val = rhoT)
        self.add_output('stressT',      val = stressT)
        self.add_output('P_W',          val = P_W)
        self.add_output('W_S',          val = W_S)
        
        
class PrelimComp(ExplicitComponent):
    def setup(self):
        # Inputs
        self.add_input('W0')
        # Constant Inputs
        self.add_input('P_W')
        self.add_input('W_S')
        # Outouts
        self.add_output('P')
        self.add_output('S')
        # Partial Declaration
        self.declare_partials('P','W0',method='cs')
        self.declare_partials('S','W0',method='cs')
        
    def compute(self,inputs,outputs):
        outputs['P'] = inputs['P_W']*inputs['W0']
        outputs['S'] = inputs['W0']/inputs['W_S']