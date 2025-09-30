# monitoring.py

import psutil
import time
import os

def clear_screen():
    """
    Clears the terminal screen for better readability.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def get_cpu_usage():
    """
    Retrieves the current CPU usage percentage.

    Returns:
        float: CPU usage percentage.
    """
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    """
    Retrieves the current memory usage statistics.

    Returns:
        tuple: Total, used, and free memory in bytes.
    """
    memory = psutil.virtual_memory()
    return memory.total, memory.used, memory.free

def get_disk_usage():
    """
    Retrieves the current disk usage statistics.

    Returns:
        tuple: Total, used, and free disk space in bytes.
    """
    disk = psutil.disk_usage('/')
    return disk.total, disk.used, disk.free

def get_network_stats():
    """
    Retrieves the current network statistics.

    Returns:
        tuple: Bytes sent and received per second.
    """
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent, net_io.bytes_recv

def display_system_stats():
    """
    Displays the current system health metrics.
    """
    clear_screen()
    print("System Health Metrics")
    print("---------------------")

    # CPU Usage
    cpu_usage = get_cpu_usage()
    print(f"CPU Usage: {cpu_usage}%")

    # Memory Usage
    total_memory, used_memory, free_memory = get_memory_usage()
    print(f"Memory Usage: {used_memory / (1024 ** 3):.2f} GB used / {total_memory / (1024 ** 3):.2f} GB total")

    # Disk Usage
    total_disk, used_disk, free_disk = get_disk_usage()
    print(f"Disk Usage: {used_disk / (1024 ** 3):.2f} GB used / {total_disk / (1024 ** 3):.2f} GB total")

    # Network Stats
    bytes_sent, bytes_recv = get_network_stats()
    print(f"Network: {bytes_sent / (1024 ** 2):.2f} MB sent / {bytes_recv / (1024 ** 2):.2f} MB received")

def main():
    """
    Main function that runs the monitoring loop.
    """
    try:
        while True:
            display_system_stats()
            time.sleep(5)  # Update every 5 seconds
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

if __name__ == "__main__":
    main()