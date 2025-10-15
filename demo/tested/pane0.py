import pexpect, subprocess
import time
from datetime import datetime
from pexpect_handler import PexpectHandler
from logger import setup_logger

# Setup logger and shell handler (used if needed)
logger = setup_logger()
handler = PexpectHandler(command="bash")
handler.spawn_process()


def read_file(filepath):
    """
    Reads the contents of a file and returns it as a string.

    Args:
        filepath (str): Path to the file.

    Returns:
        str: File contents.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        IOError: If there is an error reading the file.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def run_shell_command(cmd):
    """
    Runs a shell command and returns its output as a string.

    Args:
        cmd (str): The shell command to run.

    Returns:
        str: The standard output from the command.

    Raises:
        subprocess.CalledProcessError: If the command exits with a non-zero status.
    """
    result = subprocess.run(
        cmd,
        shell=True,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def send_promptbased_command(
    regex_pattern,
    input_file,
    command_to_send,
    tmux_session,
    windows_name,
    pane_index,
    last_n_lines=30,
):
    # Execute shell command tail -n <last_n_lines> <input_file>
    child = pexpect.spawn(f"tail -n {last_n_lines} {input_file}")
    index = child.expect([regex_pattern, pexpect.TIMEOUT, pexpect.EOF], timeout=10)

    if index == 0:
        print(
            f"✅ Pattern '{regex_pattern}' found in the last {last_n_lines} lines of {input_file}."
        )
        tmux_command = f"tmux send-keys -t {tmux_session}:{windows_name}.{pane_index} '{command_to_send}' C-m"
        pexpect.run(tmux_command)
        print(f"➡️ Sent command to tmux pane: {tmux_command}")
        child.close()
        return 1
    elif index == 1:
        print(f"⏱️ Timeout while waiting for pattern '{regex_pattern}'.")
    elif index == 2:
        print(f"📄 End of file reached without finding pattern '{regex_pattern}'.")

    child.close()
    return 0  # treat both timeout and EOF as failure


def get_local_host_time():
    return datetime.now().strftime("%m%d%H%M%Y.%S")


def run_with_retries(
    pattern,
    command,
    lines,
    input_file,
    tmux_session,
    window_name,
    pane_index,
    max_retries=3,
):
    attempt = 0
    while attempt < max_retries:
        result = send_promptbased_command(
            pattern,
            input_file,
            command,
            tmux_session,
            window_name,
            pane_index,
            last_n_lines=lines,
        )
        if result == 1:
            return True  # success
        attempt += 1
        if attempt == 1:
            print(f"🔁 [Retry {attempt}] Waiting 15 seconds before retrying...")
            time.sleep(15)
        else:
            print(f"🔁 [Retry {attempt}] Waiting 30 seconds before retrying...")
            time.sleep(30)

    # All retries failed
    raise RuntimeError(
        f"❌ Command failed after {max_retries} attempts: pattern='{pattern}', command='{command}'"
    )


def intial_login(steps, input_file, tmux_session, windows_name, pane_index):
    for pattern, command, lines in steps:
        try:
            run_with_retries(
                pattern,
                command,
                lines,
                input_file,
                tmux_session,
                windows_name,
                pane_index,
            )
            time.sleep(1)
        except RuntimeError as e:
            print(e)
            break

#------------------------Logic starts here------------------------
step1 = [
     ("MyDevelopment\\$ ", "cp ~/.ssh/backup ~/.ssh/known_hosts", 5),
    ("MyDevelopment\\$ ", "telnet 172.25.27.3 2008", 5),
    ("\\]\\'.", "", 5),
    ("login:", "root", 5),
    ("Password:", "cmc", 5),
]

step2 = [
    ("login:", "admin", 5),
    ("Password:", "Nbv12345", 5),
]

step3 = [
    (r"\# ", "cd /flash/hai && resize", 5),
    (r"\# ", "ps -elf | grep 'dump_ifm' | awk '\\''{print $4}'\\'' | xargs -r kill -9 ", 5),
    (r"\# ", "thermal -c set_override enable 100 100 100 100 100 100 100 100", 5),
    (r"\# ", "sh prep.sh", 5),
    (r"\# ", "getip.sh", 5),
    (r"\# ", "nohup sh dump_ifm.sh > master &", 5),
    (r"\# ", "tail -F master | grep -E \"Timestamp|duty|CHS_\"", 5),
]
# Execute steps
tmux_session = "my_session"
windows_name = "GE"
pane_index = 0
input_file = "../logs/IFM1.log"

intial_login(step1, input_file, tmux_session, windows_name, pane_index)
time.sleep(2)

date=f"{get_local_host_time()}"
set_date = f"tmux send-keys -t {tmux_session}:{windows_name}.{pane_index} 'export TZ=UTC && date {date}' C-m"
run_shell_command(set_date)
print(f"➡️ Sent command to tmux pane: {set_date}")
time.sleep(2)

intial_login(step3, input_file, tmux_session, windows_name, pane_index)