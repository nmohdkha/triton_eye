from openmdao.api import Problem, Group, IndepVarComp, NonlinearBlockGS, view_model

from CLaTail_comp import CLaTailComp
from CLaWing_comp import CLaWingComp
from lg_weight_comp import LGWeightComp
from tail_weight_comp import TailWeightComp
from wing_weight_comp import WingWeightComp
from wing_control_weight_comp import WingControlWeightComp
from gross_weight_comp import GrossWeightComp
from wing_param_comp import WingParamComp

prob = Problem()

## Inependent Variables (feed in constants until we can link sections together)
comp = IndepVarComp()
comp.add_output('AR',       val=25.)
comp.add_output('AR_t',     val=20.)
comp.add_output('M',        val=0.3)
comp.add_output('S',        val = 950)
comp.add_output('S_t',      val = 95)
comp.add_output('Cla',      val=0.11)
comp.add_output('Cla_t',    val=0.11)
comp.add_output('d_fuse',   val=10.)
comp.add_output('d_fuse_t', val=2.)
comp.add_output('b',        val=150)
comp.add_output('b_t',      val=15)
comp.add_output('W_0',      val=18000) ## Delete this? no longer ivc
comp.add_output('q',        val = 46)
comp.add_output('taper',    val = 0.4) ## wing taper ratio
comp.add_output('thickness_ratio',val = 0.12)
comp.add_output('n',        val = 2)
comp.add_output('croot',        val = 8.8)
prob.model.add_subsystem('ivc', comp)

## AERODYNAMICS GROUP
group = Group()
group.add_subsystem('cla_wing',     CLaWingComp())
group.add_subsystem('cla_tail',     CLaTailComp())
group.add_subsystem('wing_param',   WingParamComp())
prob.model.add_subsystem('Aerodynamics', group)

## WEIGHTS GROUP
group = Group()
group.add_subsystem('W_lg',           LGWeightComp())
group.add_subsystem('W_tail',         TailWeightComp())
group.add_subsystem('W_wing',         WingWeightComp())
group.add_subsystem('W_wing_control', WingControlWeightComp())
group.add_subsystem('W_0',            GrossWeightComp())
prob.model.add_subsystem('Weights', group)

prob.model.connect("ivc.AR",        "Aerodynamics.cla_wing.AR")
prob.model.connect("ivc.M",         "Aerodynamics.cla_wing.M")
prob.model.connect("ivc.Cla",       "Aerodynamics.cla_wing.Cla")
prob.model.connect("ivc.S",         "Aerodynamics.cla_wing.S")
prob.model.connect("ivc.d_fuse",    "Aerodynamics.cla_wing.d_fuse")
prob.model.connect("ivc.b",         "Aerodynamics.cla_wing.b")
prob.model.connect("ivc.AR_t",      "Aerodynamics.cla_tail.AR_t")
prob.model.connect("ivc.M",         "Aerodynamics.cla_tail.M")
prob.model.connect("ivc.Cla_t",     "Aerodynamics.cla_tail.Cla_t")
prob.model.connect("ivc.S_t",       "Aerodynamics.cla_tail.S_t")
prob.model.connect("ivc.d_fuse_t",  "Aerodynamics.cla_tail.d_fuse_t")
prob.model.connect("ivc.b_t",       "Aerodynamics.cla_tail.b_t")
prob.model.connect("ivc.b",         "Aerodynamics.wing_param.b")
prob.model.connect("ivc.taper",     "Aerodynamics.wing_param.taper")
prob.model.connect("ivc.croot",     "Aerodynamics.wing_param.croot")
prob.model.connect("ivc.W_0",       "Weights.W_lg.W_0")
prob.model.connect("ivc.S_t",       "Weights.W_tail.S_t")
prob.model.connect("ivc.S",         "Weights.W_wing.S")
prob.model.connect("ivc.AR",        "Weights.W_wing.AR")
prob.model.connect("ivc.q",         "Weights.W_wing.q")
prob.model.connect("ivc.taper",     "Weights.W_wing.taper")
prob.model.connect("ivc.thickness_ratio",       "Weights.W_wing.thickness_ratio")
prob.model.connect("ivc.n",         "Weights.W_wing.n")
prob.model.connect("ivc.W_0",       "Weights.W_wing.W_0")
prob.model.connect("ivc.W_0",       "Weights.W_wing_control.W_0")
# replace all "ivc.W_0" with "Weights.GrossWeightComp.W_0"


group.nonlinear_solver = NonlinearBlockGS(iprint=2, maxiter=30)


prob.setup()
prob.run_model()
#print(prob['cla_wing.CLa'])
#prob.check_partials(compact_print=True)

# TO RUN: 'python run.py'
# TO VISUALIZE: 'openmdao view_model run.py'

view_model(prob)

