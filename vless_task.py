import paramiko
import os

# Function to execute the remote command
def execute_remote_command():
    hostname = "s8.serv00.com"
    port = 22  # Updated SSH port
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
        print("STDOUT:")
        print(stdout.read().decode())
        print("STDERR:")
        print(stderr.read().decode())
    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials.")
    except paramiko.SSHException as sshException:
        print(f"Unable to establish SSH connection: {sshException}")
    except paramiko.BadHostKeyException as badHostKeyException:
        print(f"Unable to verify server's host key: {badHostKeyException}")
    except Exception as e:
        print(f"Operation error: {e}")
    finally:
        ssh.close()

# Execute the command
execute_remote_command()
