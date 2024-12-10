#!/bin/bash

wait_for_mysql() {
    local host=$1
    local port=$2
    local counter=0
    
    echo "Waiting for MySQL at $host:$port..."
    while ! nc -z "$host" "$port"; do
        counter=$((counter + 1))
        if [ $((counter % 5)) -eq 0 ]; then
            echo "Waiting for MySQL..."
        fi
        sleep 1
    done
    echo "MySQL is up!"
}