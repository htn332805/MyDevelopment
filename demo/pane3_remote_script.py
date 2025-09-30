from ssh_connection import SSHConnection
from logger import setup_logger

def main():
    logger = setup_logger()
    ssh_conn = SSHConnection(
        hostname="remote_host",
        username="user",
        password="password"
    )
    ssh_conn.connect()
    output = ssh_conn.execute_command("bash /path/to/remote_script.sh")
    logger.info(f"Pane 3 remote script output: {output}")
    ssh_conn.close()

if __name__ == "__main__":
    main()