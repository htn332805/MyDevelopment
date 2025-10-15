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
    #with open(filepath, "r", encoding="utf-8") as file:
    with open(filepath, "r") as file:
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
            time.sleep(3)
        except RuntimeError as e:
            print(e)
            break
#------------------------Logic starts here------------------------
# List of (regex pattern, command to send, number of log lines to check)
steps = [
    ("MyDevelopment\\$ ", "telnet 172.25.27.3 2030", 5),    #CHANGE THE PORT HERE
    ("\\]\\'.", "", 5),
    ("login:", "admin", 5),
    ("Password:", "Nbv12345", 5),
]

steps2 = [
    (r"\# ", "cd /mnt/emmc/hsu_intersight", 5),
    (r"\# ", "blade-power on", 5),
    (r"\# ", "/etc/scripts/getip_novlan.sh 0", 5),
    (r"\# ", "solshell -X", 5),
]
# Execute steps
tmux_session = "my_session"                             #CHANGE THE TMUX SESSION NAME HERE
windows_name = "GE"                                     #CHANGE THE TMUX WINDOW NAME HERE
pane_index = 8                                          #CHANGE THE TMUX PANE INDEX HERE
input_file = "../logs/BMC5.log"                         #CHANGE THE LOG NAME FOR THE PANE HERE

intial_login(steps, input_file, tmux_session, windows_name, pane_index)
time.sleep(3)
key=run_shell_command(f"python3 get_challenge_key.py {input_file}")
print(key)  
run_shell_command(f'ssh hain2@sjc-ads-3697 "./trinity_key.sh {key}" > key.{pane_index}')
run_shell_command(f"tail -n 1 key.{pane_index} > response.{pane_index}")
send_response_key = f"tmux send-keys -t {tmux_session}:{windows_name}.{pane_index} '{read_file(f"response.{pane_index}")}' C-m"
run_shell_command(send_response_key)
print(f"➡️ Sent command to tmux pane: {send_response_key}")
time.sleep(3)

set_timeout = f"tmux send-keys -t {tmux_session}:{windows_name}.{pane_index} 'resize && sed -i \"s/^export TMOUT=600;/export TMOUT=00;/\" /etc/bashrc' C-m"
run_shell_command(set_timeout)
print(f"➡️ Sent command to tmux pane: {set_timeout}")
time.sleep(3)

date=f"{get_local_host_time()}"
set_date = f"tmux send-keys -t {tmux_session}:{windows_name}.{pane_index} 'export TZ=UTC && date {date}' C-m"
run_shell_command(set_date)
print(f"➡️ Sent command to tmux pane: {set_date}")
time.sleep(3)
logout = f"tmux send-keys -t {tmux_session}:{windows_name}.{pane_index} 'logout' C-m"
run_shell_command(logout)
print(f"➡️ Sent command to tmux pane: {logout}")
time.sleep(3)
loginagain = f"tmux send-keys -t {tmux_session}:{windows_name}.{pane_index} 'admin' C-m"
run_shell_command(loginagain)
print(f"➡️ Sent command to tmux pane: {loginagain}")
time.sleep(1)
passwordagain = f"tmux send-keys -t {tmux_session}:{windows_name}.{pane_index} 'Nbv12345' C-m"
run_shell_command(passwordagain)
print(f"➡️ Sent command to tmux pane: {passwordagain}")
time.sleep(3)
key=run_shell_command(f"python3 get_challenge_key.py {input_file}")
print(key)  
run_shell_command(f'ssh hain2@sjc-ads-3697 "./trinity_key.sh {key}" > key.{pane_index}')
run_shell_command(f"tail -n 1 key.{pane_index} > response.{pane_index}")
send_response_key = f"tmux send-keys -t {tmux_session}:{windows_name}.{pane_index} '{read_file(f"response.{pane_index}")}' C-m"
run_shell_command(send_response_key)
print(f"➡️ Sent command to tmux pane: {send_response_key}")
time.sleep(3)

intial_login(steps2, input_file, tmux_session, windows_name, pane_index)
time.sleep(1)
print("DONE")