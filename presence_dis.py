import time
import psutil
import win32gui
import win32process
from pypresence import Presence
from datetime import datetime
import platform

CLIENT_ID = "1381835733458882675"
rpc = Presence(CLIENT_ID)
rpc.connect()

start_time = int(time.time())

def get_active_app_name():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        proc = psutil.Process(pid)
        name = proc.name().replace(".exe", "")
        return name.capitalize()
    except Exception:
        return "Unknown"

def get_asset_name(app_name: str) -> str:
    return app_name.lower().replace(" ", "") or "default"

def log_status(cpu, ram, app_name, asset_name):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] CPU: {cpu}%, RAM: {ram}% | App: {app_name} | Asset: {asset_name}")


os_version = platform.system() + " " + platform.release()

while True:
    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        app_name = get_active_app_name()
        asset_name = get_asset_name(app_name)

        rpc.update(
            details=f"CPU: {cpu}% | RAM: {ram}%",
            state=f"Active Window: {app_name}",
            start=start_time,
            large_image="cpu-z",
            buttons=[
                {"label": "My GitHub Profile", "url": "https://github.com/hoangtiennghiofficial"},
                {"label": "My Discord Server", "url": "https://discord.gg/PYSvBHG4yD"},
            ]
        )

        log_status(cpu, ram, app_name, asset_name)
        time.sleep(1)

    except Exception as e:
        print(f"[ERROR] {e}")
        time.sleep(1)
