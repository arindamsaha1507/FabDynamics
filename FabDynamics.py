# -*- coding: utf-8 -*-
#
# This source file is part of the FabSim software toolkit, which is distributed under the BSD 3-Clause license.
# Please refer to LICENSE for detailed information regarding the licensing.
#
# This file contains FabSim definitions specific to FabDummy.

try:
    from fabsim.base.fab import *
except ImportError:
    from base.fab import *

# Add local script, blackbox and template path.
add_local_paths("FabDynamics")


@task
@load_plugin_env_vars("FabDynamics")
def dynamics(config,
            dynamics_script='run.py',
            **args):
    """Submit a job to the remote queue.
    The job results will be stored with a name pattern as defined in the environment,
    e.g. cylinder-abcd1234-legion-256
    config : config directory to use to define input files, e.g. config=cylinder
    Keyword arguments:
            cores : number of compute cores to request
            images : number of images to take
            steering : steering session i.d.
            wall_time : wall-time job limit
            memory : memory per node
    """

    print(env)

    update_environment(args, {"dynamics_script": dynamics_script})
    
    set_dynamics_args_list(args)
    
    with_config(config)
    execute(put_configs, config)
    job(dict(script='dynamics', wall_time='0:15:0', memory='2G'), args)


@task
@load_plugin_env_vars("FabDynamics")
def dynamics_ensemble(config="testing", 
                    dynamics_script='run.py',
                    **args):
    """
    Submits an ensemble of dummy jobs.
    One job is run for each file in <config_file_directory>/dummy_test/SWEEP.
    """

    update_environment(args, {"dynamics_script": dynamics_script})

    with_config(config)

    set_dynamics_args_list(args)

    path_to_config = find_config_file_path(config)
    sweep_dir = path_to_config + "/SWEEP"
    env.script = "dynamics"

    run_ensemble(config, sweep_dir, **args)


@task
@load_plugin_env_vars("FabDynamics")
def dynamics_dummy(config, **args):
    """Submit a LAMMPS job to the remote queue.
    The job results will be stored with a name pattern as defined in the environment,
    e.g. cylinder-abcd1234-legion-256
    config : config directory to use to define geometry, e.g. config=lamps_lj_liquid
    Keyword arguments:
            cores : number of compute cores to request
            images : number of images to take
            steering : steering session i.d.
            wall_time : wall-time job limit
            memory : memory per node
    """
    with_config(config)
    execute(put_configs, config)
    job(dict(script='lammps', wall_time='0:15:0', lammps_input="in.CG.lammps"), args)

def set_dynamics_args_list(*dicts):

    for adict in dicts:
        for key in env.dynamics_args.keys():
            if key in adict:
                env.dynamics_args[key] = adict[key]

    env.dynamics_args_list = ""
    for key, value in env.dynamics_args.items():
        if isinstance(value, (list)):
            env.dynamics_args_list += '  '.join(value)
        else:
            env.dynamics_args_list += " --%s=%s " % (key, value)

    print("Dynamics prepared with args list:", env.dynamics_args_list)

from plugins.FabDynamics.SA.dyn_sa import dyn_init_SA
from plugins.FabDynamics.SA.dyn_sa import dyn_analyse_SA