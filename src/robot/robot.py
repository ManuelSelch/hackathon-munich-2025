from example_policies.robot_deploy.deploy import deploy_policy
from example_policies.robot_deploy import policy_loader
from example_policies.robot_deploy.debug_helpers.replay_data import replay
from pathlib import Path
from example_policies.data_ops.config.pipeline_config import PipelineConfig, ActionLevel
from example_policies.data_ops.dataset_conversion import convert_episodes
from example_policies.config_factory import act_config
from example_policies import lerobot_patches
from example_policies.train import train
lerobot_patches.apply_patches()


INFERENCE_FREQUENCY_HZ: float = 1.0
SERVER_ENDPOINT = "192.168.0.206:50051"

class Robot:
    def __init__(self):
        pass

    def replay(self, output_dir: str, episode: int):
        replay(SERVER_ENDPOINT, Path(output_dir), episode)

    def deploy(self, checkpoint_dir: str):
        policy, cfg = policy_loader.load_policy(checkpoint_dir)
        print("Policy loaded successfully!")
        # print(f"Action level from config: '{cfg.action_level}'")

        print(f"Attempting to load policy from: {checkpoint_dir}")
        print(f"Robot server endpoint: {SERVER_ENDPOINT}")
        print(f"Inference frequency: {INFERENCE_FREQUENCY_HZ} Hz")

        deploy_policy(policy, cfg, hz=INFERENCE_FREQUENCY_HZ, server=SERVER_ENDPOINT)

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
        cfg = act_config(data_dir)
        train(cfg)
        pass

    def moveLeftArm(self, dx, dy, dz):
        pass