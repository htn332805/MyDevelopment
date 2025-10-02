import subprocess

def run_shell_command(cmd):
    result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip()

try:
    # Step 1: Run the local command and capture its output
    challenge_key = run_shell_command("python3 get_challenge_key.py")
    
    # Step 2: Construct remote ssh command with the captured output as argument
    ssh_cmd = f'ssh hain2@sjc-ads-3697 "./trinity_key.sh {challenge_key}"'
    
    # Step 3: Run the ssh command and capture output
    key = run_shell_command(ssh_cmd)
    
    # Step 4: Save output to local file 'key'
    with open("key", "w") as f:
        f.write(key)
    
    print("Key saved successfully.")
    
except subprocess.CalledProcessError as e:
    print(f"Command failed with exit c