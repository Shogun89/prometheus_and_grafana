#!/bin/bash

# Source the helper scripts
source scripts/wait_for_mysql.sh
source scripts/enable_mysql_replication.sh

echo "Starting database initialization..."
echo "Environment variables:"
echo "SHARD: $SHARD"
echo "DB_HOST: $DB_HOST"
echo "DB_NAME: $DB_NAME"
echo "DB_USER: $DB_USER"

# Wait for MySQL master with increased timeout
wait_for_mysql "mysql-master-$SHARD" 3306 60

# Wait a bit more to ensure MySQL is fully ready
sleep 5

# Initialize the database first
python init_db.py

# Verify tables were created
mysql -h mysql-master-$SHARD -u root -prootpassword fastapi_db -e "SHOW TABLES;"

# Then setup replication for this shard
setup_replication "mysql-master-$SHARD" "mysql-replica-$SHARD"

# Start the application
uvicorn main:app --host 0.0.0.0 --port 8000