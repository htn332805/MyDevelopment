#!/usr/bin/env python3

LOG_FILE = "../logs/XFM1.log"


def extract_challenge(filename):
    found_asterisk = False
    with open(filename, "r") as f:
        key = []
        for line in f:
            line = line.rstrip("\n")
            if line and all(ch == "*" for ch in line):
                if not found_asterisk:
                    found_asterisk = True
                else:
                    found_asterisk = False
                continue

            if found_asterisk:
                if len(line) > 10:
                    key.append(line.strip())
                found_asterisk = False  # reset for multiple blocks if needed
        print(key[-1])


if __name__ == "__main__":
    extract_challenge(LOG_FILE)
