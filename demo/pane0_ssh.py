from pexpect_handler import PexpectHandler
from logger import setup_logger

def main():
    logger = setup_logger()
    handler = PexpectHandler(command="ssh user@remote_host")
    handler.spawn_process()
    handler.send_input("echo 'SSH pane automation'")
    handler.expect_output([r"SSH pane automation"])  # regex pattern
    logger.info(f"Pane 0 SSH output: {handler.read_output()}")
    handler.close()

if __name__ == "__main__":
    main()