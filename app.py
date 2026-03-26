# app.py
from flask import Flask, render_template, request, jsonify
import threading
import time
import random

app = Flask(__name__)

machines = []
tasks = []
results = []

# -------------------------
# Machine simulée
# -------------------------
class Machine:
    def __init__(self, ip):
        self.ip = ip
        self.busy = False

    def run_task(self, task):
        self.busy = True
        time.sleep(random.uniform(1, 3))
        result = f"{self.ip} a traité {task}"
        results.append(result)
        self.busy = False

# -------------------------
# Distribution dynamique
# -------------------------
def scheduler():
    while True:
        for m in machines:
            if not m.busy and tasks:
                task = tasks.pop(0)
                threading.Thread(target=m.run_task, args=(task,)).start()
        time.sleep(0.5)

threading.Thread(target=scheduler, daemon=True).start()

# -------------------------
# Routes
# -------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_machine", methods=["POST"])
def add_machine():
    ip = request.json["ip"]
    machines.append(Machine(ip))
    return jsonify({"status": "ok"})

@app.route("/add_task", methods=["POST"])
def add_task():
    task = request.json["task"]
    tasks.append(task)
    return jsonify({"status": "ok"})

@app.route("/status")
def status():
    return jsonify({
        "machines": [{"ip": m.ip, "busy": m.busy} for m in machines],
        "tasks": tasks,
        "results": results[-10:]
    })

if __name__ == "__main__":
    app.run(debug=True)
