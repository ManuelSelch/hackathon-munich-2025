import pathlib
from example_policies.data_ops.config.pipeline_config import PipelineConfig, ActionLevel

RAW_DATA_DIR = "/data/20250913_111243"
OUTPUT_DIR = "/home/jovyan/out/test"
TASK_LABEL = "pick up the red block"

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