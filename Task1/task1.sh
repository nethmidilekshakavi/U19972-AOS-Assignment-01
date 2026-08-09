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
    echo ""
    echo "========== Terminate a Process =========="

    read -p "Enter PID of the process to terminate: " pid

    if ! [[ "$pid" =~ ^[0-9]+$ ]]
    then
        echo "Invalid PID. Please enter a numeric PID."
        log_action "Invalid PID entered: $pid"

    elif [[ "$pid" == "1" ]]
    then
        echo "ERROR: PID $pid is a critical system process and cannot be terminated."
        log_action "Blocked termination of critical process PID $pid"

    elif ! ps -p "$pid" > /dev/null 2>&1
    then
        echo "Process with PID $pid does not exist."
        log_action "Termination failed - PID $pid does not exist"

    else
        process_name=$(ps -p "$pid" -o comm=)

        echo "Process: $process_name"
        echo "PID: $pid"

        read -p "Are you sure you want to terminate this process? (Y/N): " confirm

        if [[ "$confirm" == "Y" || "$confirm" == "y" ]]
        then
            if kill "$pid" 2>/dev/null
            then
                echo "Process $pid terminated successfully."
                log_action "Terminated process PID $pid ($process_name)"
            else
                echo "Failed to terminate process $pid."
                log_action "Failed to terminate process PID $pid ($process_name)"
            fi
        else
            echo "Termination cancelled."
            log_action "Cancelled termination of PID $pid"
        fi
    fi
    ;;
        

    4)
        echo ""
        echo "========== Inspect Sensor Log Directory =========="
        echo ""

        read -p "Enter sensor log directory path: " sensor_dir

        if [[ ! -d "$sensor_dir" ]]
        then
            echo "Directory does not exist."
            log_action "Failed to inspect directory: $sensor_dir"
        else
            echo ""
            echo "Directory: $sensor_dir"
            echo ""

            echo "Disk Usage:"
            du -sh "$sensor_dir"

            echo ""
            echo "Log Files:"
            find "$sensor_dir" -type f -name "*.log" -exec ls -lh {} \;

            log_action "Inspected sensor log directory: $sensor_dir"
        fi
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
