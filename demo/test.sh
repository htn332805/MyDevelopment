#!/bin/bash

LOG_FILE="../logs/XFM1.log"
found_first_asterisk=0

while IFS= read -r line; do
    # Check if line consists only of asterisks (at least 5 stars)
    if [[ "$line" =~ ^\*{5,}$ ]]; then
        if (( found_first_asterisk == 0 )); then
            found_first_asterisk=1
        else
            found_first_asterisk=0
        fi
        continue
    fi

    # If we've just seen the first asterisk line, print this line (the challenge string)
    if (( found_first_asterisk == 1 )); then
        echo "$line"
        found_first_asterisk=0  # reset for next block if any
    fi
done < "$LOG_FILE"

