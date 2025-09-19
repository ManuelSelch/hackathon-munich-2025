import os
from dotenv import load_dotenv
from robot.robot import Robot
from robot.workflow import Workflow
load_dotenv()

RAW_DATA_DIR = os.getenv("RAW_DATA_DIR")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
CHECKPOINT_DIR = os.getenv("CHECKPOINT_DIR")

robot = Robot()
    
robot.convert(RAW_DATA_DIR, OUTPUT_DIR, "grap object")
# robot.replay(OUTPUT_DIR, episode=0)
# robot.train(OUTPUT_DIR)
# robot.deploy("/home/jovyan/hackathon/outputs/train/2025-09-18/11-14-37_integrated_so3_act")

flow = Workflow()
tasks = [
    ("01 pick ecu holder",      "deploy", ("data/01_pickEcuHolder"),  30),
    ("02 place ecu holder",     "replay", ("data/02_placeEcuHolder"), 30),
    ("03 pick ecu",             "replay", ("data/03_pickEcu"),        30),
    ("04 place ecu",            "replay", ("data/04_placeEcu"),       30),
    ("05 pick nut",             "deploy", ("data/05_pickNut"),        30),
    ("06 place nut A",          "replay", ("data/06_placeNutA"),      30),
    ("07 pick nut",             "deploy", ("data/05_pickNut"),        30),
    ("08 place nut B",          "replay", ("data/06_placeNutB"),      30),

]
# flow.run_sequence(tasks)