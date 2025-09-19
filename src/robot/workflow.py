import multiprocessing
import time
from typing import List, Tuple, Literal
from robot import Robot

TaskType = Literal["deploy", "replay"]

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

class Workflow:
    def __init__(self):
        self.robot = Robot()

    def _run_deploy(self, checkpoint_dir: str):
        self.robot.deploy(checkpoint_dir)

    def _run_replay(self, output_dir: str, episode: int):
        self.robot.replay(output_dir, episode)

    def run_task(self, task_type: TaskType, args: Tuple, duration: float):
        if task_type == "deploy":
            target = self._run_deploy
        elif task_type == "replay":
            target = self._run_replay
        else:
            raise ValueError(f"Unknown task type: {task_type}")

        process = multiprocessing.Process(target=target, args=args)
        process.start()

        print(f"Started {task_type} with args {args}, PID={process.pid}")
        time.sleep(duration)

        print(f"Stopping {task_type} (PID={process.pid}) after {duration} seconds...")
        process.terminate()
        process.join()
        print(f"{task_type.capitalize()} stopped successfully.")

    def run_sequence(self, tasks: List[Tuple[str, TaskType, Tuple, float]]):
        # tasks = (name, type, args, duration)
        for task_type, args, duration in tasks:
            self.run_task(task_type, args, duration)