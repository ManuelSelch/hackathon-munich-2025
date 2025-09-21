from example_policies.robot_deploy.deploy import deploy_policy
from example_policies.robot_deploy import policy_loader
from example_policies.robot_deploy.debug_helpers.replay_data import replay
from pathlib import Path
from example_policies.data_ops.config.pipeline_config import PipelineConfig, ActionLevel
from example_policies.robot_deploy.robot_io.robot_interface import RobotInterface
from example_policies.robot_deploy.debug_helpers.replay_data import FakeConfig
from example_policies.data_ops.dataset_conversion import convert_episodes
from example_policies.robot_deploy.policy_loader import load_metadata
from example_policies.config_factory import act_config
from example_policies.robot_deploy.action_translator import ActionTranslator, ActionMode
from example_policies import lerobot_patches
from example_policies.train import train
from example_policies.robot_deploy.robot_io.robot_service import robot_service_pb2_grpc
from lerobot.datasets.lerobot_dataset import LeRobotDataset
import grpc
import torch
import numpy as np
import cv2
lerobot_patches.apply_patches()

INFERENCE_FREQUENCY_HZ: float = 1.0
SERVER_ENDPOINT = "192.168.0.206:50051"

class Robot:
    def __init__(self):
        pass

    def connect(self):
        # connect
        channel = grpc.insecure_channel(SERVER_ENDPOINT)
        stub = robot_service_pb2_grpc.RobotServiceStub(channel)

        # setup
        _, self.config = policy_loader.load_policy("/home/jovyan/hackathon/outputs/train/2025-09-18/11-14-37_integrated_so3_act")
        self.robot_interface = RobotInterface(stub, self.config)

    def replay(self, output_dir: str, episode: int):
        replay(SERVER_ENDPOINT, Path(output_dir), episode)

    def deploy(self, checkpoint_dir: str):
        policy, config = policy_loader.load_policy(checkpoint_dir)
        print("Policy loaded successfully!")
        # print(f"Action level from config: '{config.action_level}'")

        print(f"Attempting to load policy from: {checkpoint_dir}")
        print(f"Robot server endpoint: {SERVER_ENDPOINT}")
        print(f"Inference frequency: {INFERENCE_FREQUENCY_HZ} Hz")

        deploy_policy(policy, config, hz=INFERENCE_FREQUENCY_HZ, server=SERVER_ENDPOINT)

    def convert(self, data_dir: str, out_dir: str, label: str):
        config = PipelineConfig(
            task_name=label,
            include_tcp_poses=True,
            include_rgb_images=True,
            include_depth_images=True,
            # action_level=ActionLevel.DELTA_TCP,
            action_level=ActionLevel.TCP,
            target_fps=10,
            max_pause_seconds=0.2,
            min_episode_seconds=1,
        )
        convert_episodes(Path(data_dir), Path(out_dir), config)

    def train(self, data_dir: str):
        config = act_config(data_dir)
        train(config)
        pass

    def _get_observation(self, key):
        observation = self.robot_interface.get_observation(self.config.device, show=False)
        print("Observation keys:", observation.keys())
        return observation[key]

    def move_delta_left_arm(self, dx, dy, dz):
        current_state = self._get_observation("observation.state").cpu().numpy() # returns array with 32 numbers
        action = current_state[0, :14] # action for left arm, right arm & grippers

        # create action
        print(action)
        action[0] += dx
        action[1] += dy
        action[2] += dz
        action = action[None, :]

        # execute
        self.robot_interface.send_action(torch.from_numpy(action), ActionMode.ABS_TCP)
        pass

    def move_abs_left_arm(self, x, y, z):
        current_state = self._get_observation("observation.state").cpu().numpy() # returns array with 32 numbers
        action = current_state[0, :14] # action for left arm, right arm & grippers

        # create action
        print(action)
        action[0] = x
        action[1] = y
        action[2] = z
        action = action[None, :]

        # execute
        self.robot_interface.send_action(torch.from_numpy(action), ActionMode.ABS_TCP)
        pass

    def get_left_rgb(self):
        img_tensor = self._get_observation("observation.images.rgb_left")
        img_tensor = img_tensor.squeeze(0)  # now shape: [3, 640, 640]
        img = img_tensor.cpu().numpy()       # shape: [3, 640, 640]
        img = np.transpose(img, (1, 2, 0))  # now shape: [640, 640, 3]
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img_bgr
    
    def get_left_depth(self):
        depth_tensor = self._get_observation("observation.images.depth_left")
        print("torch shape:", depth_tensor.shape)

        # remove batch dimension if present
        depth_tensor = depth_tensor.squeeze(0)  # now shape: [1, H, W] or [H, W]
        print("after squeeze:", depth_tensor.shape)

        # convert to numpy
        depth = depth_tensor.cpu().numpy()

        # If it still has a channel dim (e.g. [1, H, W]), squeeze it
        if depth.ndim == 3:
            depth = depth.squeeze(0)  # now shape: [H, W]

        # Depth is usually in meters (float32), so for visualization we may normalize
        depth_vis = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX)
        depth_vis = np.uint8(depth_vis)

        # Optional: apply colormap for visualization
        depth_colormap = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)

        return depth, depth_colormap