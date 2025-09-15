import pathlib
from example_policies.robot_deploy.deploy import deploy_policy
from example_policies.robot_deploy import policy_loader

CHECKPOINT_DIR = pathlib.Path("outputs/<policy_checkpoint_dir>")
SERVER_ENDPOINT = "localhost:50051"
INFERENCE_FREQUENCY_HZ: float = 1.0

policy, cfg = policy_loader.load_policy(CHECKPOINT_DIR)
print("✅ Policy loaded successfully!")
print(f"Action level from config: '{cfg.action_level}'")


print(f"Attempting to load policy from: {CHECKPOINT_DIR}")
print(f"Robot server endpoint: {SERVER_ENDPOINT}")
print(f"Inference frequency: {INFERENCE_FREQUENCY_HZ} Hz")
deploy_policy(policy, cfg, hz=INFERENCE_FREQUENCY_HZ, server=SERVER_ENDPOINT)