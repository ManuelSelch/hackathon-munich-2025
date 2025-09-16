from dotenv import load_dotenv
from example_policies.robot_deploy.debug_helpers.replay_data import replay

load_dotenv()

replay("localhost:50051", "/home/jovyan/out", 0)