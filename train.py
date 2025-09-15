import pathlib
from example_policies.config_factory import act_config, diffusion_config, smolvla_config
from example_policies import lerobot_patches
from example_policies.train import train

lerobot_patches.apply_patches()

DATA_DIR = pathlib.Path("../data/my_awesome_dataset")

cfg = act_config(DATA_DIR)

train(cfg)