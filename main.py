import pathlib
from example_policies.data_ops.config.pipeline_config import PipelineConfig, ActionLevel

print("hello world")

# --- Paths ---
# TODO: Set the input directory containing your .mcap files.
RAW_DATA_DIR = pathlib.Path("/data/SOME_RAW_DATA")

# TODO: Set your desired output directory name.
OUTPUT_DIR = pathlib.Path("/data/OUTPUT_NAME")

# --- Configuration ---
# TODO: A descriptive label for the task, used for VLA-style text conditioning.
TASK_LABEL = "pick up the red block"

cfg = PipelineConfig(
    task_name=TASK_LABEL,
    # Observation features to include in the dataset.
    include_tcp_poses=True,
    include_rgb_images=True,
    include_depth_images=False,
    # Action representation. DELTA_TCP is a good default.
    action_level=ActionLevel.DELTA_TCP,
    # Subsampling and filtering. These are task-dependent.
    target_fps=10,
    max_pause_seconds=0.2,
    min_episode_seconds=1,
)

print(f"Input path:  {RAW_DATA_DIR}")
print(f"Output path: {OUTPUT_DIR}")