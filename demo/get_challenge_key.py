#!/usr/bin/env python3

import argparse


def extract_challenge(filename):
    found_asterisk = False
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
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
        if key:
            print(key[-1])


def main():
    parser = argparse.ArgumentParser(description="Extract the challenge from the log file.")
    parser.add_argument("logfile", help="Path to the log file (e.g., ../logs/XFM1.log)")
    args = parser.parse_args()

    extract_challenge(args.logfile)


if __name__ == "__main__":
    main()
