#!/bin/bash

LOG_FILE="system_monitor_log.txt"
ARCHIVE_DIR="ArchiveLogs"

# Create required files/directories
touch "$LOG_FILE"
mkdir -p "$ARCHIVE_DIR"

# Logging function
log_action() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Main menu
while true
do
    echo ""
    echo "======================================"
    echo " Smart Campus IoT Device Management"
    echo "======================================"
    echo "1. Display CPU and Memory Usage"
    echo "2. List Top 10 Memory Consuming Processes"
    echo "3. Terminate a Process"
    echo "4. Inspect Sensor Log Directory"
    echo "5. Archive Large Log Files"
    echo "6. Check ArchiveLogs Storage"
    echo "Bye. Exit System"
    echo "======================================"
    read -p "Enter your choice: " choice

    case "$choice" in
        1)
    echo ""
    echo "========== CPU and Memory Usage =========="

    echo ""
    echo "CPU Usage:"
    top -bn1 | grep "Cpu(s)" | awk '{print "CPU Used: " $2 + $4 "%"}'

    echo ""
    echo "Memory Usage:"
    free -h

    log_action "Viewed CPU and memory usage"
    ;;
        
	2)
    echo ""
    echo "========== Top 10 Memory Consuming Processes =========="
    echo ""
    printf "%-8s %-15s %-8s %-8s %-25s\n" "PID" "USER" "CPU%" "MEM%" "COMMAND"

    ps -eo pid,user,%cpu,%mem,comm --sort=-%mem | head -n 11 | tail -n 10

    log_action "Viewed top 10 memory consuming processes"
    ;;


        3)
            echo "Terminate a Process"
            ;;
        4)
            echo "Inspect Sensor Log Directory"
            ;;
        5)
            echo "Archive Large Log Files"
            ;;
        6)
            echo "Check ArchiveLogs Storage"
            ;;
        Bye|bye)
            read -p "Are you sure you want to exit? (Y/N): " confirm
            if [[ "$confirm" == "Y" || "$confirm" == "y" ]]
            then
                log_action "System exited by user"
                echo "Goodbye!"
                exit 0
            else
                echo "Exit cancelled."
            fi
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac
done
