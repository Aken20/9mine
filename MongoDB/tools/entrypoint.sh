#!/bin/bash
set -eo pipefail

# Generate keyfile if not exists
if [ ! -f /etc/mongodb-keyfile ]; then
    echo "Generating new keyfile..."
    openssl rand -base64 756 > /etc/mongodb-keyfile
    chmod 400 /etc/mongodb-keyfile
    chown mongodb:mongodb /etc/mongodb-keyfile
fi

# Check if we need to create an admin user
if [ ! -f "/data/db/.admin_user_created" ]; then
    echo "Starting MongoDB temporarily without authentication to create admin user..."
    
    # Create a temporary configuration file without authentication
    cp /etc/mongod.conf /tmp/mongod-temp.conf
    sed -i 's/authorization: enabled/authorization: disabled/' /tmp/mongod-temp.conf
    
    # Start MongoDB in background with a PID file
    gosu mongodb mongod --config /tmp/mongod-temp.conf &
    MONGO_PID=$!
    
    # Wait for MongoDB to start
    echo "Waiting for MongoDB to start..."
    until mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; do
        sleep 1
    done
    
    # Create admin user - using environment variables or default values
    echo "Creating admin user..."
    mongosh admin --eval "db.createUser({user: '${MONGO_INITDB_ROOT_USERNAME:-admin}', pwd: '${MONGO_INITDB_ROOT_PASSWORD:-password}', roles: ['root', 'userAdminAnyDatabase']})"
    
    # Mark that we've created the user
    touch "/data/db/.admin_user_created"
    
    # Shutdown MongoDB gracefully
    echo "Shutting down temporary MongoDB instance..."
    
    # Use a simpler way to stop MongoDB - kill the process
    kill $MONGO_PID
    echo "Admin user created successfully."
    rm -f /tmp/mongod-temp.conf
fi

# Start MongoDB with authentication
exec gosu mongodb mongod --config /etc/mongod.conf