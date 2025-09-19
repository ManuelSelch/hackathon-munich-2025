from robot.workflow import Workflow

flow = Workflow()

def main():
    print("robot CLI control")
    print("available commands: replay <task>, deploy <task>, pause, stop, exit")

    while True:
        try:
            cmd = input("> ").strip().split()

            if not cmd:
                continue

            action = cmd[0].lower()

            if action == "replay":
                if len(cmd) < 2:
                    print("usage: replay <task>")
                else:
                    flow.run_replay("/home/jovyan/"+cmd[1], 0)

            if action == "deploy":
                if len(cmd) < 2:
                    print("usage: deploy <task>")
                else:
                    flow.run_deploy("/home/jovyan/"+cmd[1])

            elif action == "pause":
                # flow.pause_task()
                pass

            elif action == "stop":
                # flow.stop_task()
                pass

            elif action == "exit":
                print("bye")
                break

            else:
                print(f"unknown command: {action}")

        except KeyboardInterrupt:
            print("\nexiting...")
            break

if __name__ == "__main__":
    main()
