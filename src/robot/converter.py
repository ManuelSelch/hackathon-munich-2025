from pathlib import Path
from example_policies.data_ops.dataset_conversion import convert_episodes
from pathlib import Path
from example_policies.data_ops.config.pipeline_config import PipelineConfig, ActionLevel
import numpy as np

def _is_paused(self, joint_velocity: np.ndarray) -> bool:
    """Checks if the robot is in a paused state."""
    if np.sum(np.abs(joint_velocity)) < self.cfg.pause_velocity:
        self.pause_detection_counter += 1
    else:
        self.pause_detection_counter = 0
    return self.pause_detection_counter >= self.cfg.max_pause_frames


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