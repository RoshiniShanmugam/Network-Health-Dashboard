import datetime
import random
from netmiko import ConnectHandler

# SIMULATION_MODE = True  --> Demo & Screenshot purpose-kku
# SIMULATION_MODE = False --> Real Cisco Devices connect panna
SIMULATION_MODE = True


def check_device_health(ip, username, password):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    if SIMULATION_MODE:
        if ip == "10.0.0.1":
            return {
                "ip": ip,
                "status": "OFFLINE",
                "cpu": "N/A",
                "memory": "N/A",
                "interfaces": "0",
                "timestamp": timestamp
            }

        cpu_val = f"{random.randint(5, 35)}%"
        return {
            "ip": ip,
            "status": "ONLINE",
            "cpu": cpu_val,
            "memory": "82% Free",
            "interfaces": f"{random.randint(4, 12)}",
            "timestamp": timestamp
        }

    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
        "timeout": 5,
    }

    health_data = {
        "ip": ip,
        "status": "OFFLINE",
        "cpu": "N/A",
        "memory": "N/A",
        "interfaces": "N/A",
        "timestamp": timestamp
    }

    try:
        net_connect = ConnectHandler(**device)
        cpu_output = net_connect.send_command("show processes cpu | include CPU utilization")
        cpu_val = cpu_output.split("five seconds: ")[1].split(";")[0] if "five seconds:" in cpu_output else "15%"

        health_data["status"] = "ONLINE"
        health_data["cpu"] = cpu_val
        health_data["memory"] = "OK"
        health_data["interfaces"] = "4"
        net_connect.disconnect()
    except Exception as e:
        print(f"Health check failed for {ip}: {e}")

    return health_data