#!/bin/bash

set -e

# Ensure the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root" >&2
    exit 1
fi

# Import the ZFS pool
zpool import -f -R /mnt rpool

# Mount ZFS datasets
mount -t zfs rpool/local/nix /mnt/nix
mount -t zfs rpool/local/log /mnt/var/log
mount -t zfs rpool/safe/home /mnt/home
mount -t zfs rpool/safe/persistent /mnt/persistent

# Mount the ESP
mount /dev/disk/by-id/REPLACE_WITH_YOUR_DISK_ID-part1 /mnt/boot

echo "ZFS datasets mounted successfully for NixOS installation."
