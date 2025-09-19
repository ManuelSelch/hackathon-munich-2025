from flask import Flask, render_template, redirect, url_for
import threading
from robot.workflow import Workflow

app = Flask(__name__)

flow = Workflow()

# State variables
robot_status = {"running": False, "paused": False, "current_task": None}
lock = threading.Lock()

def run_task(task_name):
    # set mode to running
    with lock:
        robot_status["running"] = True
        robot_status["paused"] = False
        robot_status["current_task"] = task_name

    print(f"[ROBOT] Starting {task_name}...")

    # trigger step
    flow.run_replay("data/02_placeEcuHolder", 0)

    # set mode to idle
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
        thread = threading.Thread(target=run_task, args=(task))
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
