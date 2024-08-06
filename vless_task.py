import paramiko
import schedule
import time
import random
import os
from datetime import datetime, timedelta

# Function to execute the remote command
def execute_remote_command():
    hostname = "s8.serv00.com"
    port = 60710
    username = os.getenv("VPS_USERNAME")
    password = os.getenv("VPS_PASSWORD")

    if not username or not password:
        print("Environment variables for username and/or password are not set.")
        return

    # Create SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, port, username, password)
        command = f"cd ~/domains/{username}.serv00.net/vless && ./check_vless.sh"
        stdin, stdout, stderr = ssh.exec_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ssh.close()

# Function to schedule the task at random times between 5 and 7 hours
def schedule_random_task():
    delay = random.randint(5 * 60 * 60, 7 * 60 * 60)  # Random delay in seconds
    execution_time = datetime.now() + timedelta(seconds=delay)
    print(f"Task scheduled to run at: {execution_time}")
    schedule.every(delay).seconds.do(execute_remote_command)

# Schedule the task
schedule_random_task()

# Run the scheduled task
while True:
    schedule.run_pending()
    time.sleep(1)
