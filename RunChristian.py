from openmdao.api import Problem, Group, IndepVarComp, NonlinearBlockGS, view_model

from CLaTail_comp import CLaTailComp
from CLaWing_comp import CLaWingComp
from lg_weight_comp import LGWeightComp
from tail_weight_comp import TailWeightComp


prob = Problem()

group = Group()

## Inependent Variables (feed in constants until we can link sections together)
comp = IndepVarComp()
comp.add_output('AR', val=25.)
comp.add_output('AR_t', val=20.)
comp.add_output('M', val=0.3)
comp.add_output('S', val = 950)
comp.add_output('S_t', val = 95)
comp.add_output('Cla', val=0.11)
comp.add_output('Cla_t', val=0.11)
comp.add_output('d_fuse', val=10.)
comp.add_output('d_fuse_t', val=2.)
comp.add_output('b', val=150)
comp.add_output('b_t', val=15)
comp.add_output('W_0', val=18000)
group.add_subsystem('ivc', comp)

comp = CLaWingComp()
group.add_subsystem('cla_wing', comp)

comp = CLaTailComp()
group.add_subsystem('cla_tail', comp)

comp = LGWeightComp()
group.add_subsystem('W_lg', comp)

comp = TailWeightComp()
group.add_subsystem('W_tail', comp)


## Wing
group.connect('ivc.AR', 'cla_wing.AR')
group.connect('ivc.M', 'cla_wing.M')
group.connect('ivc.Cla', 'cla_wing.Cla')
group.connect('ivc.S','cla_wing.S')
group.connect('ivc.d_fuse', 'cla_wing.d_fuse')
group.connect('ivc.b', 'cla_wing.b')

## Tail
group.connect('ivc.AR_t', 'cla_tail.AR_t')
group.connect('ivc.M', 'cla_tail.M')
group.connect('ivc.Cla_t', 'cla_tail.Cla_t')
group.connect('ivc.S_t','cla_tail.S_t')
group.connect('ivc.d_fuse_t', 'cla_tail.d_fuse_t')
group.connect('ivc.b_t', 'cla_tail.b_t')

## Weights
group.connect('ivc.W_0','W_lg.W_0')
group.connect('ivc.S_t','W_tail.S_t')

group.nonlinear_solver = NonlinearBlockGS(iprint=2, maxiter=30)

prob.model = group
prob.setup()
prob.run_model()
print(prob['cla_wing.CLa'])
prob.check_partials(compact_print=True)

# TO RUN: 'python run.py'
# TO VISUALIZE: 'openmdao view_model run.py'

view_model(prob)
