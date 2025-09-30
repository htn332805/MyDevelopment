import sys
import re

# Debug mode
DEBUG = False

# State variables
timestamp_var = ""
ge_data = False
gpu_data = False
current_gpu_id = None
gpu_info = {}
hsc_pout = ""
hsc_pin = ""


def debug(msg):
    if DEBUG:
        print(f"[DEBUG] {msg}", file=sys.stderr)


def reset_gpu_info():
    return {"Board temp": "", "HBM temp": "", "Power": "", "Board Serial #": ""}


try:
    # Open stdin safely with fallback encoding
    import io

    stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")

    for line in stdin:
        line = line.strip()

        # 1) Timestamp
        if line.startswith("Timestamp:"):
            timestamp_var = line.replace("Timestamp:", "").strip()
            debug(f"Timestamp detected: {timestamp_var}")
            continue

        # 2) GPU[1-9] Info Start
        m = re.match(r"^GPU([1-9]) Info", line)
        if m:
            gpu_data = True
            current_gpu_id = f"GPU{m.group(1)}"
            gpu_info[current_gpu_id] = gpu_info.get(current_gpu_id, reset_gpu_info())
            debug(f"Start GPU Info block: {current_gpu_id}")
            continue

        # 3) Board temp
        if "Board temp:" in line:
            temp_match = re.search(r"Board temp:\s*([0-9]+)", line)
            if temp_match and current_gpu_id:
                gpu_info[current_gpu_id]["Board temp"] = temp_match.group(1)
                debug(f"{current_gpu_id} Board temp: {temp_match.group(1)}")
            continue

        # 4) HBM temp
        if "HBM temp:" in line:
            hbm_match = re.search(r"HBM temp:\s*([A-Za-z0-9]+)", line)
            if hbm_match and current_gpu_id:
                gpu_info[current_gpu_id]["HBM temp"] = hbm_match.group(1)
                debug(f"{current_gpu_id} HBM temp: {hbm_match.group(1)}")
            continue

        # 5) Power
        if "Power:" in line:
            power_match = re.search(r"Power:\s*([0-9\.]+)", line)
            if power_match and current_gpu_id:
                gpu_info[current_gpu_id]["Power"] = power_match.group(1)
                debug(f"{current_gpu_id} Power: {power_match.group(1)}")
            elif "Unsupported" in line and current_gpu_id:
                gpu_info[current_gpu_id]["Power"] = "Unsupported"
                debug(f"{current_gpu_id} Power: Unsupported")
            continue

        # 6) Board Serial Number
        if "Board Serial Number" in line:
            serial_match = re.search(r"Board Serial Number\s*:\s*(\S+)", line)
            if serial_match and current_gpu_id:
                gpu_info[current_gpu_id]["Board Serial #"] = serial_match.group(1)
                debug(f"{current_gpu_id} Serial: {serial_match.group(1)}")
            continue

        # 7) End of GPU Info block
        if line.startswith("Board Marketing Name:") and gpu_data:
            debug("End of GPU Info block")
            gpu_data = False
            for gpu_id, data in gpu_info.items():
                print(
                    f"{timestamp_var},{gpu_id},{data['Board temp']},{data['HBM temp']},{data['Power']},{data['Board Serial #']},{hsc_pout},{hsc_pin}"
                )
            gpu_info = {}
            continue

        # 8) HSC Totals (GE data block)
        if line.startswith("HSC Totals"):
            ge_data = True
            debug("Starting GE data block")
            continue

        # 9) TOTAL_HSC_POUT
        if "TOTAL_HSC_POUT:" in line and ge_data:
            pout_match = re.search(r"TOTAL_HSC_POUT:\s*([0-9\.]+)", line)
            if pout_match:
                hsc_pout = pout_match.group(1)
                debug(f"TOTAL_HSC_POUT: {hsc_pout}")
            continue

        # 10) TOTAL_HSC_PIN
        if "TOTAL_HSC_PIN:" in line and ge_data:
            pin_match = re.search(r"TOTAL_HSC_PIN:\s*([0-9\.]+)", line)
            if pin_match:
                hsc_pin = pin_match.group(1)
                debug(f"TOTAL_HSC_PIN: {hsc_pin}")
            continue

        # 11) End of GE block
        if "12V E-fuse" in line and ge_data:
            ge_data = False
            debug("End of GE data block")
            print(f"{timestamp_var},GEPOWER,,,,,{hsc_pout},{hsc_pin}")
            continue

        # 12) End of data block
        if "press CTRL-C to exit loop" in line:
            debug("End of full data block — resetting state")
            timestamp_var = ""
            hsc_pout = ""
            hsc_pin = ""
            current_gpu_id = None
            gpu_info = {}
            ge_data = False
            gpu_data = False
            continue

except Exception as e:
    print(f"[ERROR] {e}", file=sys.stderr)
