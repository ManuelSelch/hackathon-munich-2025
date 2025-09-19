from flask import Flask, render_template, redirect, url_for
import threading
import time
from robot.workflow import Workflow, tasks

app = Flask(__name__)



# State variables
robot_status = {"running": False, "paused": False, "current_task": None}
lock = threading.Lock()

def run_task(task_name):
    """Simulate a long-running robot task"""
    with lock:
        robot_status["running"] = True
        robot_status["paused"] = False
        robot_status["current_task"] = task_name

    print(f"[ROBOT] Starting {task_name}...")

    for i in range(10):  # Simulate 10 steps
        with lock:
            if not robot_status["running"]:
                print(f"[ROBOT] Task '{task_name}' stopped.")
                return
            while robot_status["paused"]:
                print(f"[ROBOT] Paused at step {i+1}")
                time.sleep(1)

        print(f"[ROBOT] {task_name} step {i+1}/10")
        time.sleep(1)

    with lock:
        robot_status["running"] = False
        robot_status["current_task"] = None
    print(f"[ROBOT] {task_name} completed!")

@app.route("/")
def index():
    return render_template("index.html", status=robot_status)

@app.route("/start/<task>")
def start_task(task):
    if not robot_status["running"]:
        thread = threading.Thread(target=run_task, args=(task,))
        thread.start()
    return redirect(url_for("index"))

@app.route("/pause")
def pause_task():
    with lock:
        if robot_status["running"]:
            robot_status["paused"] = not robot_status["paused"]
    return redirect(url_for("index"))

@app.route("/stop")
def stop_task():
    with lock:
        robot_status["running"] = False
        robot_status["paused"] = False
        robot_status["current_task"] = None
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
