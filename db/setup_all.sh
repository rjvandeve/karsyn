#!/bin/bash

echo "📦 Setting up Travel Database System"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "❌ Docker is not running. Please start Docker Desktop and try again."
  exit 1
fi

# Load environment variables
if [ -f .env ]; then
  export $(cat .env | grep -v '#' | sed 's/\r$//' | xargs)
fi

# Check if container already exists
if docker ps -a | grep -q travel-mysql; then
  echo "🔄 Removing existing travel-mysql container..."
  docker rm -f travel-mysql > /dev/null
fi

# Start MySQL
echo "🚀 Starting MySQL..."
docker run -d --name travel-mysql \
  -p $MYSQL_PORT:3306 \
  -e MYSQL_ROOT_PASSWORD=root_pw \
  -e MYSQL_DATABASE=$MYSQL_DATABASE \
  -e MYSQL_USER=$MYSQL_USER \
  -e MYSQL_PASSWORD=$MYSQL_PASSWORD \
  mysql:8.0 > /dev/null

echo "⏳ Waiting for MySQL to initialize (15 seconds)..."
sleep 15

# Load schema
echo "📝 Creating database schema..."
docker exec -i travel-mysql \
  mysql -u$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE < schema.sql

# Check if Python dependencies are installed
echo "🐍 Checking Python dependencies..."
pip install faker mysql-connector-python > /dev/null

# Seed the database
echo "🌱 Seeding database with test data..."
python3 seed_db.py

# Run smoke test
echo "🔍 Running smoke tests..."
docker exec -i travel-mysql \
  mysql -u$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE < smoke_test.sql

echo "✅ Database setup complete!"
echo "   - MySQL is running at $MYSQL_HOST:$MYSQL_PORT"
echo "   - Database: $MYSQL_DATABASE"
echo "   - User: $MYSQL_USER"
echo "   - Password: $MYSQL_PASSWORD"
echo ""
echo "To connect manually:"
echo "docker exec -it travel-mysql mysql -u$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE" 