__copyright__ = (
    "Copyright (c) Microsoft Corporation and Mila - Quebec AI Institute"
)
__license__ = "MIT"

import os
import pickle
import time
from typing import Callable
import warnings
from gym import register

_SIM = None

ASSET_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "resources"
)


def get_sim():
    """Gets the sim, if set.
    :return: the simulator.
    """
    if _SIM is None:
        raise RuntimeError("Simulator not set yet")

    return _SIM


def set_sim(sim):
    global _SIM
    if _SIM is not None:
        warnings.warn(
            "Overwriting sim. This can have unexpected "
            "consequences if using old sim objects somewhere."
        )
    _SIM = sim


def timeit(fn: Callable):
    def timed_fn(*args, **kwargs):
        t0 = time.time()
        out = fn(*args, **kwargs)
        t1 = time.time()

        if _SIM is not None:
            if len(args) > 0:
                key = f"{args[0].__class__.__name__}.{fn.__name__}_time"
            else:
                key = f"{fn.__name__}_time"
            _SIM.update_results(key, t1 - t0)
        return out

    return timed_fn


def load_sim_from_file(path):
    """Loads a simulator from file.
    This uses pickle, so the simulator loaded will have its associated code
    intact. This can make the loaded sim incompatible with newer code.
    :param path: Path to pickle file.
    :return: Simulator.
    """
    with open(path, "rb") as f:
        sim = pickle.load(f)
    set_sim(sim)
    return sim


# The following block of code pre-registers a set of default configurations
# that can be used via env = gym.make('empty-easy-rgb') for example.

task_names = ["empty", "objects", "tiles"]
difficulties = ["easy", "medium", "hard"]
observations = ["rgb"]

for task in task_names:
    for difficulty in difficulties:
        for observation in observations:
            for n_entities in [1, 2, 3]:
                if task == "empty" and n_entities == 1:
                    env_name = f"Segar-{task}-{difficulty}-{observation}-v0"
                    # print(env_name)
                    register(
                        id=env_name,
                        entry_point="segar.envs:SEGARSingleEnv",
                        kwargs={
                            "env_name": f"{task}-{difficulty}-{observation}"
                        },
                        max_episode_steps=100,
                    )
                elif task != "empty":
                    env_name = (
                        f"Segar-{task}x{n_entities}-{difficulty}-"
                        f"{observation}-v0"
                    )
                    # print(env_name)
                    register(
                        id=env_name,
                        entry_point="segar.envs:SEGARSingleEnv",
                        kwargs={
                            "env_name": f"{task}x{n_entities}-{difficulty}-"
                            f"{observation}"
                        },
                        max_episode_steps=100,
                    )

# Current Envs (update as needed)
# Segar-empty-easy-rgb-v0
# Segar-empty-medium-rgb-v0
# Segar-empty-hard-rgb-v0
# Segar-objectsx1-easy-rgb-v0
# Segar-objectsx2-easy-rgb-v0
# Segar-objectsx3-easy-rgb-v0
# Segar-objectsx1-medium-rgb-v0
# Segar-objectsx2-medium-rgb-v0
# Segar-objectsx3-medium-rgb-v0
# Segar-objectsx1-hard-rgb-v0
# Segar-objectsx2-hard-rgb-v0
# Segar-objectsx3-hard-rgb-v0
# Segar-tilesx1-easy-rgb-v0
# Segar-tilesx2-easy-rgb-v0
# Segar-tilesx3-easy-rgb-v0
# Segar-tilesx1-medium-rgb-v0
# Segar-tilesx2-medium-rgb-v0
# Segar-tilesx3-medium-rgb-v0
# Segar-tilesx1-hard-rgb-v0
# Segar-tilesx2-hard-rgb-v0
# Segar-tilesx3-hard-rgb-v0