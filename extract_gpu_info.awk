#!/usr/bin/awk -f  # Shebang: Run this script using awk interpreter

# BEGIN block initializes variables and prints CSV header
BEGIN {
    FS = ":"  # Set field separator to colon for key-value parsing

    DEBUG = 0  # Enable debug logging (set 0 to disable)

    current_timestamp = ""  # Holds current timestamp string
    current_gpu = ""        # Holds current GPU ID being processed
    in_gpu_section = 0      # Flag indicating if inside GPU info block
    in_hsc_totals = 0       # Flag indicating if inside TOTAL_HSC section

    # Print CSV header line
    print "Timestamp,GPU_ID,Board_Temp,HBM_Temp,Power_mW,Board_Serial,TOTAL_HSC_POUT,TOTAL_HSC_PIN"
}

# Debug function to print messages to stderr if DEBUG is enabled
function debug(msg, level) {
    if (DEBUG) {  # Only output if debug mode enabled
        # Print level, line number (FNR), and message to standard error
        printf("[DEBUG] %s | Line %d: %s\n", level, FNR, msg) > "/dev/stderr"
    }
}

# Match lines starting with "Timestamp"
# Example line: "Timestamp : 2025-09-24 14:00:00\r\n"
# Extract timestamp and clean whitespace and trailing CR/LF characters
/^Timestamp/ {
    current_timestamp = $2  # Extract value after colon

    # Remove any carriage return (\r) or newline (\n) characters in the timestamp
    gsub(/[\r\n]+/, "", current_timestamp)

    # Trim leading and trailing spaces
    gsub(/^ +| +$/, "", current_timestamp)

    debug("Found new timestamp: " current_timestamp, "INFO")  # Log new timestamp

    # Reset GPU data and HSC totals for this timestamp block
    delete gpu_data  # Clear any previous GPU info stored in gpu_data associative array
    hsc_pout = ""    # Clear stored total HSC power out
    hsc_pin = ""     # Clear stored total HSC power in

    next  # Skip further processing for this line
}

# Match start of GPU section indicated by lines like "===== GPU0 Info ====="
/^[=]+[ ]*GPU[0-9]+ Info[ ]*[=]+/ {
    # Extract GPU number using regex and store in current_gpu
    match($0, /GPU([0-9]+)/, m)
    current_gpu = m[1]

    in_gpu_section = 1  # Mark that we're now inside a GPU section
    debug("Entering GPU section for GPU" current_gpu, "INFO")  # Log entry into GPU section

    next  # Skip further processing of this line
}

# Match lines consisting of at least 5 equal signs (end of section marker)
/^={5,}$/ {
    if (in_gpu_section) {  # If currently processing a GPU section
        debug("Exiting GPU section for GPU" current_gpu, "INFO")  # Log GPU section exit
        save_gpu_record()  # Save collected GPU data to CSV output
        in_gpu_section = 0  # Clear GPU section flag
        current_gpu = ""    # Clear current GPU ID
    }

    in_hsc_totals = 0  # End of TOTAL_HSC section as well (reset flag)
    next  # Skip further processing for this line
}

# Match lines starting with TOTAL_HSC_POUT (system total power output)
/^[ \t]*TOTAL_HSC_POUT/ {
    in_hsc_totals = 1  # Mark that we're inside TOTAL_HSC section
    hsc_pout = $2      # Capture power output value (field after colon)

    gsub(/^ +| +$/, "", hsc_pout)  # Trim whitespace from the value

    debug("Captured TOTAL_HSC_POUT: " hsc_pout, "INFO")  # Log captured value
    next  # Skip further processing for this line
}

# Match lines starting with TOTAL_HSC_PIN (system total power input)
/^[ \t]*TOTAL_HSC_PIN/ {
    if (in_hsc_totals) {  # Only capture if currently inside TOTAL_HSC section
        hsc_pin = $2  # Capture power input value
        gsub(/^ +| +$/, "", hsc_pin)  # Trim whitespace

        debug("Captured TOTAL_HSC_PIN: " hsc_pin, "INFO")  # Log captured value
    }
    next  # Skip further processing for this line
}

# Default rule to process all other lines (mainly key-value pairs inside GPU sections)
{
    # Only parse key-value pairs if inside a GPU section and GPU ID is set
    if (in_gpu_section && current_gpu != "") {
        key = $1  # First field before colon (key)
        val = $2  # Second field after colon (value)

        gsub(/^ +| +$/, "", key)  # Trim whitespace from key
        gsub(/^ +| +$/, "", val)  # Trim whitespace from value

        # Capture known GPU attributes into gpu_data associative array
        if (key == "Board temp") {
            gpu_data["Board_Temp"] = val
            debug("GPU" current_gpu ": Board Temp = " val, "DATA")
        } else if (key == "HBM temp") {
            gpu_data["HBM_Temp"] = val
            debug("GPU" current_gpu ": HBM Temp = " val, "DATA")
        } else if (key == "Power") {
            gpu_data["Power"] = val
            debug("GPU" current_gpu ": Power = " val, "DATA")
        } else if (key == "Board Serial #") {
            gpu_data["Board_Serial"] = val
            debug("GPU" current_gpu ": Board Serial = " val, "DATA")
        } else if (key == "Board Serial Number") {
            # Handle alternate label for board serial number
            gpu_data["Board_Serial"] = val
            debug("GPU" current_gpu ": Board Serial (alt) = " val, "DATA")
        }
    }
}

# Function to save and print GPU record as CSV line
function save_gpu_record() {
    # Use "NA" if any expected field is missing (ternary expression)
    bt = (gpu_data["Board_Temp"] ? gpu_data["Board_Temp"] : "NA")
    ht = (gpu_data["HBM_Temp"] ? gpu_data["HBM_Temp"] : "NA")
    pw = (gpu_data["Power"] ? gpu_data["Power"] : "NA")
    sn = (gpu_data["Board_Serial"] ? gpu_data["Board_Serial"] : "NA")
    pout = (hsc_pout ? hsc_pout : "NA")
    pin = (hsc_pin ? hsc_pin : "NA")

    # Print CSV formatted output line
    print current_timestamp "," current_gpu "," bt "," ht "," pw "," sn "," pout "," pin

    # Log saving event for debugging
    debug("Saved GPU" current_gpu " record: " bt "," ht "," pw "," sn "," pout "," pin, "SAVE")
}
