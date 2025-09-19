import argparse
from robot.workflow import Workflow

flow = Workflow()

def main():
    parser = argparse.ArgumentParser(
        description="CLI to control the robot workflows"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # start <task>
    start_parser = subparsers.add_parser("start", help="Start a workflow step")
    start_parser.add_argument("task", type=str, help="Task name (e.g., step1, step2)")

    # pause
    subparsers.add_parser("pause", help="Pause the current task")

    # stop
    subparsers.add_parser("stop", help="Stop the current task")

    args = parser.parse_args()

    if args.command == "start":
        flow.run_task(args.task)
    elif args.command == "pause":
        # flow.pause_task()
        pass
    elif args.command == "stop":
        # flow.stop_task()
        pass

if __name__ == "__main__":
    main()
