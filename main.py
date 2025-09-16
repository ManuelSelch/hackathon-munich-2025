import os
from dotenv import load_dotenv
from robot.robot import Robot
load_dotenv()

RAW_DATA_DIR = os.getenv("RAW_DATA_DIR")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
CHECKPOINT_DIR = os.getenv("CHECKPOINT_DIR")

robot = Robot()

def grapPlateA():
    robot.deploy(CHECKPOINT_DIR)
    pass

def placePlateA():
    robot.replay(OUTPUT_DIR, episode=0)

def grapPlateB():
    robot.deploy(CHECKPOINT_DIR)
    pass

def placePlateB():
    robot.replay(OUTPUT_DIR, episode=1)

def grapScrew():
    robot.deploy(CHECKPOINT_DIR)
    pass

def screw():
    robot.replay(OUTPUT_DIR, episode=2)

def main():
    grapPlateA()
    placePlateA()
    grapPlateB()
    placePlateB()
    grapScrew()
    screw()

# main()
placePlateA()