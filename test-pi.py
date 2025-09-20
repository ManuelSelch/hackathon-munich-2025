import numpy as np
import grpc
import torch
from pathlib import Path
from example_policies.robot_deploy.robot_io.robot_service import robot_service_pb2_grpc
from example_policies.robot_deploy.robot_io.robot_interface import RobotInterface
from example_policies.robot_deploy.action_translator import ActionTranslator, ActionMode
from example_policies.robot_deploy.debug_helpers.replay_data import FakeConfig
from example_policies.robot_deploy.policy_loader import load_metadata
from lerobot.datasets.lerobot_dataset import LeRobotDataset
from openpi.training import config as _config
from openpi.policies import policy_config
from openpi.shared import download

SERVER_ENDPOINT = "192.168.0.206:50051"

# load policy
config = _config.get_config("pi05_droid")
checkpoint_dir = download.maybe_download("gs://openpi-assets/checkpoints/pi05_droid")
policy = policy_config.create_trained_policy(config, checkpoint_dir)

# connect to robot
channel = grpc.insecure_channel(SERVER_ENDPOINT)
stub = robot_service_pb2_grpc.RobotServiceStub(channel)
# data_cfg = DatasetConfig(repo_id=fake_repo_id, root=data_dir, episodes=[ep_index])

# use dummy episode to parse metadata
data_dir = Path("/home/jovyan/pickEcu")
ep_index = 0
meta_data = load_metadata(data_dir)
cfg = FakeConfig()

dataset = LeRobotDataset(
    repo_id="test",
    root=data_dir,
    episodes=[ep_index],
)

robot_interface = RobotInterface(stub, cfg)
model_to_action_trans = ActionTranslator(cfg)

# get current state
observation = robot_interface.get_observation("cpu")
current_state = observation["state"].cpu().numpy()

# run inference
example = {
    "observation": current_state,
    "prompt": "pick up the fork"
}
action_chunk = policy.infer(example)["actions"]

print(action_chunk)

# send action to robot
robot_interface.send_action(
    torch.from_numpy(action_chunk[None, :]),
    ActionMode.ABS_TCP
)