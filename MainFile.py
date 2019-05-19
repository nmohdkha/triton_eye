from openmdao.api import Problem, Group, IndepVarComp, view_model, ScipyOptimizeDriver
from const_comp import ConstComp, PrelimComp
from weight_comps import WingWeightComp, TailWeightComp, FuselageWeightComp, \
                        LandingGearWeightComp, FuelTankWeightComp, \
                        PropellerWeightComp, MotorWeightComp, FuelCellWeightComp

# Initialize Problem
prob = Problem()

# Initialize Independent Variable Component and Declare Variables
ivc = prob.model.add_subsystem('ivc',IndepVarComp())
ivc.add_output('W0')    # Gross Weight
ivc.add_output('AR')    # Main Wing Aspect Ratio
ivc.add_output('Tap')   # Main Wing Taper Ratio
ivc.add_output('Swp')   # Main Wing Sweep
ivc.add_output('l')     # Fuselage Length
ivc.add_output('d')     # Fuselage Diameter
ivc.add_output('TAR')   # Tail Aspect Ratio
#ivc.add_output('P')     # Power
#ivc.add_output('S')     # Main Wing Reference Area

const = prob.model.add_subsystem('Constants', ConstComp())

prelim  = prob.model.add_subsystem('Prelims', PrelimComp())

aero = prob.model.add_subsystem('Aerodynamics', Group())


stab = prob.model.add_subsystem('Stability', Group())


prop = prob.model.add_subsystem('Propulsion', Group())


struct = prob.model.add_subsystem('Structures', Group())


weights = prob.model.add_subsystem('Weights', Group())
weights.add_subsystem('Wing',WingWeightComp())
weights.add_subsystem('Tail',TailWeightComp())
weights.add_subsystem('Fuselage',FuselageWeightComp())
weights.add_subsystem('LandingGear',LandingGearWeightComp())
weights.add_subsystem('FuelTank',FuelTankWeightComp())
weights.add_subsystem('Propeller',PropellerWeightComp())
weights.add_subsystem('Motor',MotorWeightComp())
weights.add_subsystem('FuelCell',FuelCellWeightComp())

# Connections
prob.model.connect("ivc.W0", "Prelims.W0")
prob.model.connect("Constants.P_W", "Prelims.P_W")
prob.model.connect("Constants.W_S", "Prelims.W_S")
prob.model.connect("ivc.W0", "Weights.Wing.W0")
prob.model.connect("Prelims.S", "Weights.Wing.S")
prob.model.connect("ivc.AR", "Weights.Wing.AR")
prob.model.connect("ivc.Tap", "Weights.Wing.Tap")
prob.model.connect("ivc.Swp", "Weights.Wing.Swp")
prob.model.connect("Constants.M0", "Weights.Wing.M0")
prob.model.connect("Constants.nUlt", "Weights.Wing.nUlt")
prob.model.connect("Constants.tc", "Weights.Wing.tc")
prob.model.connect("ivc.W0", "Weights.Tail.W0")
prob.model.connect("Constants.nUlt", "Weights.Tail.nUlt")
prob.model.connect("ivc.W0", "Weights.Fuselage.W0")
prob.model.connect("ivc.l", "Weights.Fuselage.l")
prob.model.connect("ivc.d", "Weights.Fuselage.d")
prob.model.connect("Constants.qmax", "Weights.Fuselage.qmax")
prob.model.connect("ivc.W0", "Weights.LandingGear.W0")
prob.model.connect("ivc.d", "Weights.FuelTank.d")
prob.model.connect("Constants.g", "Weights.FuelTank.g")
prob.model.connect("Constants.Np", "Weights.Propeller.Np")
prob.model.connect("Constants.Nb", "Weights.Propeller.Nb")
prob.model.connect("Constants.Np", "Weights.Motor.Np")
prob.model.connect("Constants.MotorWeight", "Weights.Motor.MotorWeight")
prob.model.connect("Constants.Np", "Weights.FuelCell.Np")
prob.model.connect("Constants.MotorWeight", "Weights.FuelCell.CellWeight")
prob.model.connect("Constants.hp", "Weights.Propeller.hp")
prob.model.connect("Constants.Pmax", "Weights.FuelTank.Pmax")
prob.model.connect("Constants.rhoT", "Weights.FuelTank.rhoT")
prob.model.connect("Constants.stressT", "Weights.FuelTank.stressT")

prob.setup(force_alloc_complex = True)
view_model(prob)