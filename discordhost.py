import os
import signal
import subprocess
import time

FLAG_FILE = "restart_flag.txt"
DISCORD_PROCESS = None

def start_discord_bot():
    global DISCORD_PROCESS
    try:
        DISCORD_PROCESS = subprocess.Popen(["python", "discordbot.py"])
    except subprocess.CalledProcessError as e:
        print("Error starting Discord bot:", e)

def monitor_flag():
    while True:
        if os.path.exists(FLAG_FILE):
            print("\nRestarting Discord bot...\n")
            os.remove(FLAG_FILE)
            restart_discord_bot()
        time.sleep(1)

def restart_discord_bot():
    global DISCORD_PROCESS
    try:
        if DISCORD_PROCESS:
            DISCORD_PROCESS.terminate()
            DISCORD_PROCESS.wait()

        DISCORD_PROCESS = subprocess.Popen(["python", "discordbot.py"])
    except subprocess.CalledProcessError as e:
        print("Error starting Discord bot:", e)

if __name__ == "__main__":
    start_discord_bot()
    monitor_flag()
