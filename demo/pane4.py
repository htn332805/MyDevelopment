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


# List of (regex pattern, command to send, number of log lines to check)
steps = [
    ("MyDevelopment\\$ ", "telnet 172.25.27.3 2026", 5),
    ("\\]\\'.", "", 5),
    ("login:", "admin", 5),
    ("Password:", "Nbv12345", 5),
]

steps2 = [
    ("login:", "admin", 5),
    ("Password:", "Nbv12345", 5),
]
# Execute steps
tmux_session = "my_session"
windows_name = "GE"
pane_index = 6
input_file = "../logs/BMC1.log"

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


#--------------------------Logic begins here--------------------------#
step0 = [
    ("MyDevelopment\\$ ", "cp ~/.ssh/backup ~/.ssh/known_hosts", 5),
    ("MyDevelopment\\$ ", "ssh root@172.25.27.70", 5),
    (r"\? ", "yes", 5),
    (r"assword: ", "cmc", 5),
    (r"\# ", "telnet bmc4 8021", 5),
    (r"\# ", "sldp", 5),
]

step1 = [
    ("MyDevelopment\\$ ", "telnet 172.25.27.3 2026", 5),
    ("\\]\\'.", "", 5),
    ("login:", "admin", 5),
    ("Password:", "Nbv12345", 5),
]

step2 = [
    ("login:", "admin", 5),
    ("Password:", "Nbv12345", 5),
]

step3 = [
    (r"\# ", "cd /mnt/emmc/hsu_intersight", 5),
    (r"\# ", "ps -lw | grep 'record_' | awk '\\''{print $3}'\\'' | xargs -r kill -9", 5),
    (r"\# ", "nohup sh record_bmc.sh > ge34.log &", 5),
    (r"\# ", "tail -F ge34.log", 5),
]
# Execute steps
tmux_session = "my_session"
windows_name = "GE"
pane_index = 4
input_file = "../logs/GE34.log"

intial_login(step0, input_file, tmux_session, windows_name, pane_index)
time.sleep(3)   
intial_login(step2, input_file, tmux_session, windows_name, pane_index)
time.sleep(3)
key=run_shell_command(f"python3 get_challenge_key.py {input_file}")
print(key)  
get_key_cmd=f'ssh hain2@sjc-ads-3697 "./trinity_key.sh {key}" > key.{pane_index}'
send_response_key = f"tmux send-keys -t {tmux_session}:{windows_name}.12 '{get_key_cmd}' C-m"
run_shell_command(f'{send_response_key}')

time.sleep(2)
response_key=f"tail -n 1 key.{pane_index} > response.{pane_index}"
get_response_key = f"tmux send-keys -t {tmux_session}:{windows_name}.12 '{response_key}' C-m"
run_shell_command(f'{get_response_key}')

time.sleep(2)  
print(read_file(f"response.{pane_index}"))
send_response_key = f"tmux send-keys -t {tmux_session}:{windows_name}.{pane_index} '{read_file(f"response.{pane_index}")}' C-m"
run_shell_command(send_response_key)
print(f"➡️ Sent command to tmux pane: {send_response_key}")

set_timeout = f"tmux send-keys -t {tmux_session}:{windows_name}.{pane_index} 'resize && sed -i \"s/^export TMOUT=600;/export TMOUT=00;/\" /etc/bashrc' C-m"
run_shell_command(set_timeout)
print(f"➡️ Sent command to tmux pane: {set_timeout}")
time.sleep(3)
logout = f"tmux send-keys -t {tmux_session}:{windows_name}.{pane_index} 'logout' C-m"
run_shell_command(logout)
print(f"➡️ Sent command to tmux pane: {logout}")
time.sleep(3)
dummy_cmd = f"tmux send-keys -t {tmux_session}:{windows_name}.{pane_index} 'sldp' C-m"
run_shell_command(dummy_cmd)
print(f"➡️ Sent command to tmux pane: {dummy_cmd}")
time.sleep(3)

intial_login(step2, input_file, tmux_session, windows_name, pane_index)
time.sleep(3)
key=run_shell_command(f"python3 get_challenge_key.py {input_file}")
print(key)  
get_key_cmd=f'ssh hain2@sjc-ads-3697 "./trinity_key.sh {key}" > key.{pane_index}'
send_response_key = f"tmux send-keys -t {tmux_session}:{windows_name}.12 '{get_key_cmd}' C-m"
run_shell_command(f'{send_response_key}')

time.sleep(2)
response_key=f"tail -n 1 key.{pane_index} > response.{pane_index}"
get_response_key = f"tmux send-keys -t {tmux_session}:{windows_name}.12 '{response_key}' C-m"
run_shell_command(f'{get_response_key}')

time.sleep(2)  
print(read_file(f"response.{pane_index}"))
send_response_key = f"tmux send-keys -t {tmux_session}:{windows_name}.{pane_index} '{read_file(f"response.{pane_index}")}' C-m"
run_shell_command(send_response_key)
print(f"➡️ Sent command to tmux pane: {send_response_key}")

date=f"{get_local_host_time()}"
set_date = f"tmux send-keys -t {tmux_session}:{windows_name}.{pane_index} 'export TZ=UTC && date {date}' C-m"
run_shell_command(set_date)
print(f"➡️ Sent command to tmux pane: {set_date}")

intial_login(step3, input_file, tmux_session, windows_name, pane_index)