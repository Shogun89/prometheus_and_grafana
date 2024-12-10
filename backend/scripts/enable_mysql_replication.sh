#!/bin/bash

# Setup replication between master and replica
setup_replication() {
    local MASTER_HOST=$1
    local REPLICA_HOST=$2

    echo "Setting up replication from $MASTER_HOST to $REPLICA_HOST..."
    
    # Get master status
    MASTER_STATUS=$(mysql -h $MASTER_HOST -uroot -prootpassword -e "SHOW MASTER STATUS\G")
    CURRENT_LOG=$(echo "$MASTER_STATUS" | grep File | awk '{print $2}')
    CURRENT_POS=$(echo "$MASTER_STATUS" | grep Position | awk '{print $2}')

    # Configure replica
    mysql -h $REPLICA_HOST -uroot -prootpassword -e "
        STOP SLAVE;
        CHANGE MASTER TO 
            MASTER_HOST='$MASTER_HOST',
            MASTER_USER='root',
            MASTER_PASSWORD='rootpassword',
            MASTER_LOG_FILE='$CURRENT_LOG',
            MASTER_LOG_POS=$CURRENT_POS;
        START SLAVE;
    "

    echo "Replication configured for $REPLICA_HOST"
}