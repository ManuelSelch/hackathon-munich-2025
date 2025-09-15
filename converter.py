import os
from dotenv import load_dotenv
from example_policies.data_ops.config.pipeline_config import PipelineConfig, ActionLevel
import pathlib

load_dotenv()

OUTPUT_DIR = os.getenv("OUTPUT_DIR")
RAW_DATA_DIR = os.getenv("OUTRAW_DATA_DIRPUT_DIR")
RAW_DATA_DIR = pathlib.Path(RAW_DATA_DIR)
TASK_LABEL = "task-label"

config = PipelineConfig(
    task_name=TASK_LABEL,
    include_tcp_poses=True,
    include_rgb_images=True,
    include_depth_images=False,
    action_level=ActionLevel.DELTA_TCP,
    target_fps=10,
    max_pause_seconds=0.2,
    min_episode_seconds=1,
)

print(f"Input path:  {RAW_DATA_DIR}")
print(f"Output path: {OUTPUT_DIR}")

from example_policies.data_ops.dataset_conversion import convert_episodes
convert_episodes(RAW_DATA_DIR, OUTPUT_DIR, config)