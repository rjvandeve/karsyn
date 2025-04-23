#!/bin/bash

# Load environment variables
if [ -f .env ]; then
  export $(cat .env | grep -v '#' | sed 's/\r$//' | xargs)
fi

# Start MySQL in Docker
docker run -d --name travel-mysql \
  -p $MYSQL_PORT:3306 \
  -e MYSQL_ROOT_PASSWORD=root_pw \
  -e MYSQL_DATABASE=$MYSQL_DATABASE \
  -e MYSQL_USER=$MYSQL_USER \
  -e MYSQL_PASSWORD=$MYSQL_PASSWORD \
  mysql:8.0

echo "MySQL container started. It may take a few seconds to initialize..."
sleep 5

# Check if container is running
if docker ps | grep -q travel-mysql; then
  echo "✅ MySQL is running successfully at $MYSQL_HOST:$MYSQL_PORT"
else
  echo "❌ Failed to start MySQL container"
fi 