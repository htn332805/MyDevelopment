BEGIN {
    FS=":"
    OFS=","
    DEBUG = 0  # <<< Set to 1 to enable debug logs
    print "Timestamp,GPUID,Board temp,HBM temp,Power,Board Serial #,TOTAL_HSC_POUT,TOTAL_HSC_PIN"
}

/^Timestamp:/ {
    timestamp_var = gensub(/^Timestamp:[ \t]*/, "", "g", $0)
    if (DEBUG) print "[DEBUG] Detected timestamp: " timestamp_var " on line " NR
}

/^HSC Totals/ {
    ge_block = 1
    if (DEBUG) print "[DEBUG] Entered GE block at line " NR
}

$0 ~ /TOTAL_HSC_POUT:/ && ge_block {
    total_pout = gensub(/[^0-9.]+/, "", "g", $0)
    if (DEBUG) print "[DEBUG] Found TOTAL_HSC_POUT: " total_pout " on line " NR
}

$0 ~ /TOTAL_HSC_PIN:/ && ge_block {
    total_pin = gensub(/[^0-9.]+/, "", "g", $0)
    if (DEBUG) print "[DEBUG] Found TOTAL_HSC_PIN: " total_pin " on line " NR
}

# End GE block
/^---$/ && ge_block {
    ge_block = 0
    if (DEBUG) print "[DEBUG] Exited GE block at line " NR
}

# GPU Info block start
/^GPU[1-9] Info/ {
    gpu_block = 1
    gpu_id = gensub(/^GPU([1-9]) Info.*/, "\\1", "g")
    board_temp = ""
    hbm_temp = ""
    power = ""
    serial_num = ""
    if (DEBUG) print "[DEBUG] Entered GPU block for GPU" gpu_id " at line " NR
}

/Board temp:/ && gpu_block {
    board_temp = gensub(/[^0-9]+([0-9]+).*/, "\\1", "g", $0)
    if (DEBUG) print "[DEBUG] GPU" gpu_id " Board temp: " board_temp " on line " NR
}

# HBM temp
/HBM temp:/ && gpu_block {
    if ($0 ~ /Unsupported/) {
        hbm_temp = "Unsupported"
    } else {
        hbm_temp = gensub(/[^0-9]+([0-9]+).*/, "\\1", "g", $0)
    }
    if (DEBUG) print "[DEBUG] GPU" gpu_id " HBM temp: " hbm_temp " on line " NR
}

# Power
/Power:/ && gpu_block {
    if ($0 ~ /Unsupported/) {
        power = "Unsupported"
    } else {
        power = gensub(/[^0-9.]+([0-9.]+).*/, "\\1", "g", $0)
    }
    if (DEBUG) print "[DEBUG] GPU" gpu_id " Power: " power " on line " NR
}

# Serial Number
/Board Serial Number/ && gpu_block {
    serial_num = gensub(/^.*Board Serial Number[ \t]*:[ \t]*/, "", "g", $0)
    if (DEBUG) print "[DEBUG] GPU" gpu_id " Serial Number: " serial_num " on line " NR
}

# GPU block end, print data
/^====================================$/ && gpu_block {
    if (gpu_id != "") {
        print timestamp_var, gpu_id, board_temp, hbm_temp, power, serial_num, total_pout, total_pin
        if (DEBUG) print "[DEBUG] Printed data for GPU" gpu_id " at line " NR
    }
    gpu_block = 0
    gpu_id = board_temp = hbm_temp = power = serial_num = ""
}

# End of data block
/press CTRL-C to exit loop/ {
    if (DEBUG) {
        print "[DEBUG] End of data block at line " NR
        print "[DEBUG] Resetting all variables"
    }
    timestamp_var = total_pout = total_pin = ""
    gpu_block = ge_block = 0
}
