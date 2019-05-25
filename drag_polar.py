'''
Compute viscous drag polar by running sweep of anlaysis over different angle of
attacks. Plot drag polar at end. Check output directory for Tecplot solution files.
'''

import numpy as np

from openmdao.api import IndepVarComp, Problem

from openaerostruct.geometry.utils import generate_mesh
from openaerostruct.geometry.geometry_group import Geometry
from openaerostruct.aerodynamics.aero_groups import AeroPoint


# Instantiate the problem and the model group
prob = Problem()

# Define flight variables as independent variables of the model
indep_var_comp = IndepVarComp()
indep_var_comp.add_output('beta', val=0., units='deg') # Sideslip angle
indep_var_comp.add_output('omega', val=np.zeros(3), units='deg/s') # Rotation rate
indep_var_comp.add_output('v', val=87.17, units='m/s')
indep_var_comp.add_output('alpha', val=2.0, units='deg')
indep_var_comp.add_output('Mach_number', val=0.3)
indep_var_comp.add_output('re', val=1.e6, units='1/m')
indep_var_comp.add_output('rho', val=0.146645, units='kg/m**3')
indep_var_comp.add_output('cg', val=np.zeros((3)), units='m')
# Add vars to model, promoting is a quick way of automatically connecting inputs
# and outputs of different OpenMDAO components
prob.model.add_subsystem('flight_vars', indep_var_comp, promotes=['*'])

# Create a dictionary to store options about the surface
mesh_dict = {'num_y' : 35,
             'num_x' : 11,
             'wing_type' : 'rect',
             'symmetry' : True,
            #  'span' : 47.16761712,
            #  'chord' : 2,
             'span_cos_spacing' : 1.,
             'chord_cos_spacing' : 1.}

# Generate half-wing mesh of rectangular wing
mesh = generate_mesh(mesh_dict)

# Define input surface dictionary for our wing
surface = {
            # Wing definition
            'name' : 'wing',        # name of the surface
            'type' : 'aero',
            'symmetry' : True,     # if true, model one half of wing
                                    # reflected across the plane y = 0
            'S_ref_type' : 'projected', # how we compute the wing area,
                                     # can be 'wetted' or 'projected'

            'twist_cp' : np.zeros(3), # Define twist using 3 B-spline cp's
                                    # distributed along span
            'mesh' : mesh,

            # Aerodynamic performance of the lifting surface at
            # an angle of attack of 0 (alpha=0).
            # These CL0 and CD0 values are added to the CL and CD
            # obtained from aerodynamic analysis of the surface to get
            # the total CL and CD.
            # These CL0 and CD0 values do not vary wrt alpha.
           'CL0' : 1.1095,            # CL of the surface at alpha=0
           'CD0' : 0.01946,           # CD of the surface at alpha=0

            # Airfoil properties for viscous drag calculation
            'k_lam' : 0.05,         # percentage of chord with laminar
                                    # flow, used for viscous drag
            't_over_c_cp' : np.array([0.125]),      # thickness over chord ratio (TH 25816 HALE AIRFOIL)
            'c_max_t' : .237,       # chordwise location of maximum (TH 25816 HALE AIRFOIL)
                                    # thicknesss
            'with_viscous' : False,  # if true, compute viscous drag,
            'with_wave' : False,
            'taper':.3,
            'dihedral':0,
            'sweep':0,
            'chord_cp':0.5 * np.ones(5),
            'span' :47.16761712,
            'xshear_cp':0 * np.ones(5),
            'yshear_cp':0 * np.ones(5),
            'zshear_cp':0 * np.ones(5),
            } # end of surface dictionary

name = surface['name']

# Add geometry to the problem as the name of the surface.
# These groups are responsible for manipulating the geometry of the mesh,
# in this case spanwise twist.
geom_group = Geometry(surface=surface)
prob.model.add_subsystem(name, geom_group)

# Create the aero point group for this flight condition and add it to the model
aero_group = AeroPoint(surfaces=[surface], rotational=True)
point_name = 'aero_point_0'
prob.model.add_subsystem(point_name, aero_group,
                         promotes_inputs=['v', 'alpha', 'beta', 'omega', 'Mach_number', 're', 'rho', 'cg'])

# Connect the mesh from the geometry component to the analysis point
prob.model.connect(name + '.mesh', point_name + '.' + name + '.def_mesh')

# Perform the connections with the modified names within the
# 'aero_states' group.
prob.model.connect(name + '.mesh', point_name + '.aero_states.' + name + '_def_mesh')

# Connect the parameters within the model for each aero point
name = surface['name']
prob.model.connect(name + '.t_over_c', point_name + '.' + name + '_perf.' + 't_over_c')

# Set up the problem
prob.setup()

# Create arrays to hold polar data
alpha = np.linspace(-10,10,20)
CL = np.zeros_like(alpha)
CD = np.zeros_like(alpha)

# Sweep through alphas to create polar
for i in range(len(alpha)):
    # Set alpha
    prob['alpha'] = alpha[i]

    # Run analysis
    prob.run_model()

    # Record CL, CD
    CL[i] = prob['aero_point_0.wing_perf.CL'][0]
    CD[i] = prob['aero_point_0.wing_perf.CD'][0]

# Plot polar
import matplotlib.pyplot as plt
plt.plot(CD*1E4, CL, '-o')
plt.grid(color='lightgray', linestyle='-', linewidth=1)
plt.xlabel('$C_D$ (counts)')
plt.ylabel('$C_L$')
plt.title('Drag polar')
plt.show()