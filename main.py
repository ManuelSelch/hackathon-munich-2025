import os
from dotenv import load_dotenv
from robot.robot import Robot
load_dotenv()

RAW_DATA_DIR = os.getenv("RAW_DATA_DIR")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
TASK_LABEL = "task-label"
CHECKPOINT_DIR = os.getenv("CHECKPOINT_DIR")

robot = Robot()

robot.replay(OUTPUT_DIR, episode=0)