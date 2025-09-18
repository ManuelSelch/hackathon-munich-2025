import os
from dotenv import load_dotenv
from robot.robot import Robot
load_dotenv()

RAW_DATA_DIR = os.getenv("RAW_DATA_DIR")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
CHECKPOINT_DIR = os.getenv("CHECKPOINT_DIR")

robot = Robot()
    
robot.convert(RAW_DATA_DIR, OUTPUT_DIR, "grap object")
# robot.replay(OUTPUT_DIR, episode=0)
# robot.train(OUTPUT_DIR)
# robot.deploy("/home/jovyan/hackathon/outputs/train/2025-09-18/11-14-37_integrated_so3_act")