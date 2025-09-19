from robot.workflow import Workflow

flow = Workflow()

def main():
    print("🤖 Robot CLI Control")
    print("Available commands: start <task>, pause, stop, exit")

    while True:
        try:
            cmd = input("> ").strip().split()

            if not cmd:
                continue

            action = cmd[0].lower()

            if action == "start":
                if len(cmd) < 2:
                    print("⚠️ Usage: start <task>")
                else:
                    flow.run_task(cmd[1])

            elif action == "pause":
                # flow.pause_task()
                pass

            elif action == "stop":
                # flow.stop_task()
                pass

            elif action == "exit":
                print("👋 Goodbye")
                break

            else:
                print(f"❌ Unknown command: {action}")

        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break

if __name__ == "__main__":
    main()
