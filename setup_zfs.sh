#!/bin/bash

set -e

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required commands
for cmd in sgdisk zpool zfs; do
    if ! command_exists "$cmd"; then
        echo "Error: $cmd is not installed. Please install it and try again."
        exit 1
    fi
done

# Disk partitioning and ZFS setup script
DISK="/dev/disk/by-id/REPLACE_WITH_YOUR_DISK_ID"
POOLNAME="zroot"
# Ensure the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root" >&2
    exit 1
fi

# Partition the disk
echo "Partitioning $DISK..."
sgdisk -Z $DISK
sgdisk -n 1:0:+500M -t 1:EF00 -c 1:"ESP" $DISK
sgdisk -n 2:0:+8M -t 2:EF02 -c 2:"BIOS boot" $DISK
sgdisk -n 3:0:0 -t 3:BF00 -c 3:"ZFS" $DISK

# Create and mount the ESP
echo "Creating and mounting ESP..."
mkfs.vfat -F 32 -n ESP ${DISK}-part1
#mkdir -p /mnt/boot
#mount ${DISK}-part1 /mnt/boot

# Create ZFS pool
echo "Creating ZFS pool..."
zpool create -f -o ashift=12 -O acltype=posixacl -O canmount=off -O compression=zstd \
    -O dnodesize=auto -O normalization=formD -O relatime=on -O xattr=sa \
    -O mountpoint=none ${POOLNAME} ${DISK}-part3

# Set autoexpand
zpool set autoexpand=on rpool

# Create ZFS datasets
echo "Creating ZFS datasets..."
zfs create -o canmount=off ${POOLNAME}/local
zfs create -o mountpoint=/ ${POOLNAME}/local/root
zfs create -o mountpoint=/nix ${POOLNAME}/local/nix
zfs create -o mountpoint=/var/log ${POOLNAME}/local/log
zfs create -o canmount=off ${POOLNAME}/safe
zfs create -o mountpoint=/home ${POOLNAME}/safe/home
zfs create -o mountpoint=/persistent ${POOLNAME}/safe/persistent
zfs create -o canmount=off -o reservation=500M ${POOLNAME}/reserved

echo "ZFS pool and datasets created successfully."
