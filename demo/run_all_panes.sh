#!/bin/bash
# Run all pane scripts in parallel

python demo/pane0_ssh.py &
python demo/pane1_telnet.py &
python demo/pane2_local_script.py &
python demo/pane3_remote_script.py &

wait
echo "All pane scripts completed."