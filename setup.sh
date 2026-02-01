#!/bin/bash

# BIMFlow Suite - Automated Setup Script
# This script clones the repository, sets up PostgreSQL, installs dependencies,
# and starts both the backend and frontend servers.

set -e  # Exit on any error

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/Nnamdi-Oniya/bimflowsuite.git"
PROJECT_DIR="BIM-Project"
DB_NAME="bimflowsuite_db"
DB_USER="bimflow_user"
DB_HOST="localhost"
DB_PORT="5432"

# Ask user for database password
echo -e "${BLUE} Database Configuration${NC}"
read -s -p "Enter PostgreSQL password for database user (or press Enter for default): " DB_PASSWORD
echo

if [ -z "$DB_PASSWORD" ]; then
    DB_PASSWORD="bimflow_password_secure"
    echo -e "${YELLOW} Using default password: $DB_PASSWORD${NC}"
    echo -e "${YELLOW}   (Change this in production!)${NC}\n"
else
    echo -e "${GREEN} Password set${NC}\n"
fi

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}   BIMFlow Suite - Automated Setup Script${NC}"
echo -e "${BLUE}================================================${NC}\n"

# ==================== STEP 1: Check Prerequisites ====================
echo -e "${YELLOW}[1/9] Checking prerequisites...${NC}"

check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED} $1 is not installed. Please install it first.${NC}"
        exit 1
    fi
}

check_command "git"
check_command "python3"
check_command "npm"
check_command "psql"

echo -e "${GREEN} All prerequisites installed\n${NC}"

# ==================== STEP 2: Clone Repository ====================
echo -e "${YELLOW}[2/9] Cloning repository...${NC}"

if [ -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW} Directory $PROJECT_DIR already exists. Using existing directory.${NC}"
else
    git clone $REPO_URL $PROJECT_DIR
    echo -e "${GREEN} Repository cloned to $PROJECT_DIR\n${NC}"
fi

cd "$PROJECT_DIR/bimflowsuite"

# ==================== STEP 3: Setup PostgreSQL Database ====================
echo -e "${YELLOW}[3/9] Setting up PostgreSQL database...${NC}"

# Check if PostgreSQL is running
if ! psql -h $DB_HOST -U postgres -c "SELECT 1" &> /dev/null; then
    echo -e "${RED} PostgreSQL is not running. Please start PostgreSQL and try again.${NC}"
    echo -e "${YELLOW}   macOS: brew services start postgresql${NC}"
    echo -e "${YELLOW}   Linux: sudo systemctl start postgresql${NC}"
    exit 1
fi

# Create database and user
psql -h $DB_HOST -U postgres <<EOF
-- Create user if not exists
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_user WHERE usename = '$DB_USER') THEN
    CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
  END IF;
END
\$\$;

-- Grant privileges
ALTER USER $DB_USER CREATEDB;

-- Create database if not exists
SELECT 'CREATE DATABASE $DB_NAME'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec

-- Grant all privileges on database
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOF

echo -e "${GREEN} PostgreSQL database and user created\n${NC}"

# ==================== STEP 4: Setup Python Virtual Environment ====================
echo -e "${YELLOW}[4/9] Setting up Python virtual environment...${NC}"

if [ ! -d ".venv" ]; then
    python3.11 -m venv .venv
    echo -e "${GREEN} Virtual environment created${NC}"
else
    echo -e "${YELLOW} Virtual environment already exists${NC}"
fi

source .venv/bin/activate
echo -e "${GREEN} Virtual environment activated\n${NC}"

# ==================== STEP 5: Install Backend Dependencies ====================
echo -e "${YELLOW}[5/9] Installing backend dependencies...${NC}"

pip install --upgrade pip setuptools wheel
pip install -r requirements/local.txt

echo -e "${GREEN} Backend dependencies installed\n${NC}"

# ==================== STEP 6: Setup Environment Variables ====================
echo -e "${YELLOW}[6/9] Setting up environment variables...${NC}"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cat > .env <<EOF
# Django Settings
DJANGO_SETTINGS_MODULE=config.settings.local
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True

# Database Configuration
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0

# File Storage
USE_S3=False

# Email Configuration (Optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8000

# Allowed Hosts (for local development)
ALLOWED_HOSTS=localhost,127.0.0.1
EOF
    echo -e "${GREEN} .env file created with default values${NC}"
else
    echo -e "${YELLOW}b.env file already exists${NC}"
fi

# Update DATABASE_URL in .env
sed -i.bak "s|DATABASE_URL=.*|DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME|g" .env
rm -f .env.bak

echo -e "${GREEN} Environment variables configured\n${NC}"

# ==================== STEP 7: Run Django Migrations ====================
echo -e "${YELLOW}[7/9] Running Django migrations...${NC}"

DJANGO_SETTINGS_MODULE=config.settings.local python manage.py migrate

echo -e "${GREEN} Migrations completed\n${NC}"

# ==================== STEP 8: Install Frontend Dependencies ====================
echo -e "${YELLOW}[8/9] Installing frontend dependencies...${NC}"

cd ../bimflowsuite-ui
npm install

echo -e "${GREEN} Frontend dependencies installed\n${NC}"

# ==================== STEP 9: Provide Startup Instructions ====================
echo -e "${YELLOW}[9/9] Setup complete! Starting services...${NC}\n"

cd ..

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}   Setup Complete!${NC}"
echo -e "${GREEN}================================================${NC}\n"

echo -e "${BLUE} If you encounter any issues:${NC}"
echo -e "   1. Check SETUP_GUIDE.md for troubleshooting"
echo -e "   2. Follow manual setup instructions in README.md"
echo -e "   3. Verify database: python check_database.py\n"

echo -e "${BLUE} Next Steps:${NC}\n"

echo -e "${YELLOW}1. Backend Server (Django + DRF):${NC}"
echo -e "   cd bimflowsuite"
echo -e "   source .venv/bin/activate"
echo -e "   python manage.py runserver\n"

echo -e "${YELLOW}2. Frontend Server (React + Vite):${NC}"
echo -e "   cd bimflowsuite-ui"
echo -e "   npm run dev\n"

echo -e "${YELLOW}3. Celery Worker (for async tasks):${NC}"
echo -e "   cd bimflowsuite"
echo -e "   source .venv/bin/activate"
echo -e "   celery -A bimflowsuite worker -l info\n"

echo -e "${YELLOW}4. Redis Server (for cache/queue):${NC}"
echo -e "   redis-server\n"

echo -e "${BLUE} API Documentation:${NC}"
echo -e "   Swagger: http://localhost:8000/swagger/"
echo -e "   GraphQL: http://localhost:8000/graphql/\n"

echo -e "${BLUE} Database:${NC}"
echo -e "   Database: $DB_NAME"
echo -e "   User: $DB_USER"
echo -e "   Host: $DB_HOST:$DB_PORT\n"

echo -e "${BLUE} Quick Commands:${NC}"
echo -e "   Create superuser: python manage.py createsuperuser"
echo -e "   Reset migrations: python manage.py migrate zero app_label"
echo -e "   Collect static files: python manage.py collectstatic\n"

echo -e "${GREEN}Happy coding! ${NC}\n"
