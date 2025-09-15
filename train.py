import os
from dotenv import load_dotenv
from example_policies.config_factory import act_config, diffusion_config, smolvla_config
from example_policies import lerobot_patches
from example_policies.train import train

lerobot_patches.apply_patches()
load_dotenv()

DATA_DIR = os.getenv("DATA_DIR")

cfg = act_config(DATA_DIR)

train(cfg)