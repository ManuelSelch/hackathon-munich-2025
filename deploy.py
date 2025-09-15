import os
from dotenv import load_dotenv
from example_policies.robot_deploy.deploy import deploy_policy
from example_policies.robot_deploy import policy_loader

load_dotenv()

CHECKPOINT_DIR = os.getenv("CHECKPOINT_DIR")
SERVER_ENDPOINT = os.getenv("SERVER_ENDPOINT")
INFERENCE_FREQUENCY_HZ: float = 1.0

policy, cfg = policy_loader.load_policy(CHECKPOINT_DIR)
print("Policy loaded successfully!")
print(f"Action level from config: '{cfg.action_level}'")


print(f"Attempting to load policy from: {CHECKPOINT_DIR}")
print(f"Robot server endpoint: {SERVER_ENDPOINT}")
print(f"Inference frequency: {INFERENCE_FREQUENCY_HZ} Hz")
deploy_policy(policy, cfg, hz=INFERENCE_FREQUENCY_HZ, server=SERVER_ENDPOINT)