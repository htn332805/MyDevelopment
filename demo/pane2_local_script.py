from pexpect_handler import PexpectHandler
from logger import setup_logger

def main():
    logger = setup_logger()
    handler = PexpectHandler(command="bash ./local_script.sh")
    handler.spawn_process()
    handler.expect_output([r"(Script completed|Done)"])  # regex pattern
    logger.info(f"Pane 2 local script output: {handler.read_output()}")
    handler.close()

if __name__ == "__main__":
    main()