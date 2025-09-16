from dotenv import load_dotenv
from example_policies.robot_deploy.debug_helpers.replay_data import replay
from pathlib import Path

load_dotenv()

replay("192.168.0.206:50051", Path("/home/jovyan/out"), 0)