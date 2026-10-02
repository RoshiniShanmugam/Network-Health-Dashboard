import datetime
from netmiko import ConnectHandler

# Simple input for username & password
username = input("Enter SSH Username: ")
password = input("Enter SSH Password: ")

devices = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.1.1",
        "username": username,
        "password": password,
    },
]

today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

for device in devices:
    try:
        print(f"Connecting to {device['host']}...")
        net_connect = ConnectHandler(**device)
        output = net_connect.send_command("show running-config")

        filename = f"backup_{device['host']}_{today}.txt"
        with open(filename, "w") as f:
            f.write(output)

        print(f"Backup saved as {filename}")
        net_connect.disconnect()

    except Exception as e:
        print(f"Failed to backup {device['host']}: {e}")