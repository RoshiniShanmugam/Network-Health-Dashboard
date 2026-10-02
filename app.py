from flask import Flask, render_template, request, redirect, url_for
from monitor import check_device_health

app = Flask(__name__)

SSH_USER = "admin"
SSH_PASS = "cisco"

@app.route("/")
def dashboard():
    try:
        with open("devices.txt", "r") as f:
            ips = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        ips = ["192.168.1.1"]

    device_results = []
    online_count = 0
    offline_count = 0

    for ip in ips:
        data = check_device_health(ip, SSH_USER, SSH_PASS)
        device_results.append(data)
        if data.get("status") == "ONLINE":
            online_count += 1
        else:
            offline_count += 1

    return render_template(
        "dashboard.html",
        devices=device_results,
        total_count=len(device_results),
        online_count=online_count,
        offline_count=offline_count
    )

@app.route("/add", methods=["POST"])
def add_device():
    new_ip = request.form.get("device_ip").strip()
    if new_ip:
        with open("devices.txt", "a") as f:
            f.write(f"\n{new_ip}")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)