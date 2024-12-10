# Help Documentation
This documentation provides a comprehensive guide to the tools and technologies used in this project, including Nginx, Docker, and MySQL. It covers basic commands, configurations, and useful variables for each tool, as well as troubleshooting commands and performance monitoring.

## Table of Contents
- [Tools](#tools)
- [Nginx](#nginx)
  - [Basic Commands](#basic-commands)
  - [Common Configuration Locations](#common-configuration-locations)
  - [Example Load Balancer Configuration](#example-load-balancer-configuration)
  - [Common Configuration Parameters](#common-configuration-parameters)
  - [Useful Nginx Variables](#useful-nginx-variables)
  - [Monitoring and Logs](#monitoring-and-logs)
- [Docker](#docker)
  - [Container Management](#container-management)
  - [Image Management](#image-management)
  - [Docker Compose](#docker-compose)
  - [Scale Specific Service](#scale-specific-service)
  - [System Management](#system-management)
  - [Troubleshooting Commands](#troubleshooting-commands)
  - [Performance Monitoring](#performance-monitoring)
- [MySQL](#mysql)
  - [Basic Commands](#basic-commands)
  - [Common Configuration Locations](#common-configuration-locations)
  - [Common Configuration Parameters](#common-configuration-parameters)
  - [Useful MySQL Variables](#useful-mysql-variables)
  - [Monitoring and Logs](#monitoring-and-logs)
- [FastAPI](#fastapi)
  - [Basic Commands](#basic-commands)
  - [Common Configuration Locations](#common-configuration-locations)
  - [Common Configuration Parameters](#common-configuration-parameters)
  - [Useful FastAPI Variables](#useful-fastapi-variables)
  - [Monitoring and Logs](#monitoring-and-logs)
- [Python](#python)
  - [Basic Commands](#basic-commands)
  - [Common Configuration Locations](#common-configuration-locations)
  - [Common Configuration Parameters](#common-configuration-parameters)
  - [Useful Python Tools](#useful-python-tools)
  - [Monitoring and Logs](#monitoring-and-logs)
- [Uvicorn](#uvicorn)
  - [Basic Commands](#basic-commands)
  - [Common Configuration Locations](#common-configuration-locations)
  - [Common Configuration Parameters](#common-configuration-parameters)
  - [Useful Uvicorn Variables](#useful-uvicorn-variables)
  - [Monitoring and Logs](#monitoring-and-logs)
- [Pydantic](#pydantic)
  - [Basic Usage](#basic-usage)
  - [Common Validation Features](#common-validation-features)
  - [Configuration Options](#configuration-options)
  - [Useful Features](#useful-features)
  - [Common Patterns](#common-patterns)
  - [Validation and Error Handling](#validation-and-error-handling)
  - [Integration with FastAPI](#integration-with-fastapi)
- [SQLAlchemy](#sqlalchemy)
  - [Basic Usage](#basic-usage-1)
  - [Common Query Operations](#common-query-operations)
  - [Relationship Patterns](#relationship-patterns)
  - [Common Configuration Parameters](#common-configuration-parameters)
  - [Query Optimization](#query-optimization)
  - [FastAPI Integration](#fastapi-integration)
  - [Migration Management (Alembic)](#migration-management-alembic)
  - [Performance Monitoring](#performance-monitoring)
- [Bash](#bash)
  - [Basic Commands](#basic-commands-1)
  - [File Operations](#file-operations)
  - [System Information](#system-information)
  - [Process Management](#process-management)
  - [Network Commands](#network-commands)
  - [Text Processing](#text-processing)
  - [Permissions](#permissions)
- [Glossary](#glossary)

## Tools
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Curl](https://curl.se/)
- [Nginx](https://nginx.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [MySQL](https://www.mysql.com/)
- [Python](https://www.python.org/)
- [Uvicorn](https://www.uvicorn.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Bash](https://www.gnu.org/software/bash/)

## Nginx

Nginx is configured as a reverse proxy and load balancer in this project. Below are common configurations and commands:

### Basic Commands
```bash
# Test nginx configuration
nginx -t

# Reload nginx configuration
nginx -s reload

# Start nginx
nginx

# Stop nginx
nginx -s stop

# Restart nginx
nginx -s restart
```

### Common Configuration Locations
```bash
# Main configuration file
/etc/nginx/nginx.conf

# Site-specific configurations
/etc/nginx/conf.d/*.conf
/etc/nginx/sites-enabled/*
```

### Example Load Balancer Configuration
```nginx
upstream backend {
    server api1:8000;
    server api2:8000;
    # Round-robin is default
}

server {
    listen 80;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Common Configuration Parameters
- `proxy_pass`: Specifies the protocol and address of a proxied server
- `upstream`: Defines a group of servers that can be referenced by `proxy_pass`
- `server_name`: Sets names of a virtual server
- `location`: Sets configuration depending on a request URI
- `proxy_set_header`: Redefines or appends fields to the request header

### Useful Nginx Variables
- `$host`: Request host header
- `$remote_addr`: Client IP address
- `$proxy_add_x_forwarded_for`: Client IP address chain
- `$request_uri`: Full original request URI

### Monitoring and Logs
```bash
# Access log location
/var/log/nginx/access.log

# Error log location
/var/log/nginx/error.log

# Monitor active connections
watch 'nginx -v && echo "" && nginx -t && echo "" && curl http://localhost/nginx_status'
```

For more detailed information, refer to:
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Nginx Beginner's Guide](https://nginx.org/en/docs/beginners_guide.html)
- [Nginx Load Balancing](https://nginx.org/en/docs/http/load_balancing.html)

## Docker
Docker is used to containerize the application and services, providing a consistent and isolated environment that packages all dependencies and can run reliably across different computing environments.

### Container Management
```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop a container
docker stop <container_id>

# Remove a container
docker rm <container_id>

# Start a container
docker start <container_id>

# View container logs
docker logs <container_id>
docker logs -f <container_id>  # Follow log output
```

### Image Management
```bash
# List images
docker images

# Remove an image
docker rmi <image_name>

# Pull an image
docker pull <image_name>

# Build an image
docker build -t <image_name> .
```

### Docker Compose
```bash
# Start services
docker compose up

# Start services in detached mode
docker compose up -d

# Stop services
docker compose down

# Rebuild and start services
docker compose up --build

# View service logs
docker compose logs

# Use a specific compose file
docker compose -f docker-compose.prod.yml up
docker compose -f docker-compose.dev.yml up
```

### Scale specific service
```bash
# Scale specific service
docker compose up --scale api=3
```

### System Management
```bash
# Remove unused data
docker system prune

# Remove all unused images
docker system prune -a

# Show docker disk usage
docker system df

# Show detailed disk usage
docker system df -v

# Remove all unused volumes
docker volume prune

# Show system-wide information
docker info
```

### Troubleshooting Commands
```bash
# Inspect container details
docker inspect <container_id>

# View container resource usage
docker stats

# Check container processes
docker top <container_id>

# View container network settings
docker network ls
docker network inspect <network_name>

# Debug container
docker exec -it <container_id> /bin/bash
```

### Performance Monitoring
```bash
# Monitor all containers
docker stats --all

# Monitor specific container
docker stats <container_id>

# Export container metrics
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Check container events
docker events
```

**References:**
- [Docker Compose CLI reference](https://docs.docker.com/compose/reference/)
- [Docker Compose file reference](https://docs.docker.com/compose/compose-file/)
- [Docker Compose environment variables](https://docs.docker.com/compose/environment-variables/)
- [Docker Compose networking](https://docs.docker.com/compose/networking/)

## MySQL
MySQL is the primary database system used in this project. Here are essential commands and configurations:

### Basic Commands
```sql
# Connect to MySQL
mysql -u <username> -p

# Show databases
SHOW DATABASES;

# Select database
USE <database_name>;

# Show tables
SHOW TABLES;

# Show table structure
DESCRIBE <table_name>;

# Check replication status
SHOW SLAVE STATUS\G
SHOW MASTER STATUS\G

# Check process list
SHOW PROCESSLIST;
```

### Common Configuration Locations
```bash
# Main configuration file
/etc/mysql/my.cnf

# Additional configuration files
/etc/mysql/mysql.conf.d/
/etc/mysql/conf.d/

# Data directory
/var/lib/mysql/
```

### Common Configuration Parameters
- `max_connections`: Maximum number of simultaneous client connections
- `innodb_buffer_pool_size`: Size of InnoDB buffer pool
- `innodb_log_file_size`: Size of InnoDB log files
- `binlog_format`: Format of binary log (ROW, STATEMENT, or MIXED)
- `max_allowed_packet`: Maximum size of one packet/row

### Useful MySQL Variables
```sql
# Show all variables
SHOW VARIABLES;

# Show specific variable
SHOW VARIABLES LIKE 'max_connections';

# Show global status
SHOW GLOBAL STATUS;

# Show session status
SHOW SESSION STATUS;
```

### Monitoring and Logs
```bash
# Error log location
/var/log/mysql/error.log

# Slow query log
/var/log/mysql/mysql-slow.log

# Binary logs
/var/log/mysql/mysql-bin.*

# Monitor MySQL processes
mysqladmin processlist

# Check status
mysqladmin status

# Monitor replication lag
SHOW SLAVE STATUS\G
```

For more detailed information, refer to:
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [MySQL Performance Tuning](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)
- [MySQL Replication](https://dev.mysql.com/doc/refman/8.0/en/replication.html)

## FastAPI
FastAPI is the web framework used to build the API in this project. Here are essential commands and configurations:

### Basic Commands
```bash
# Start the FastAPI server
uvicorn main:app --reload

# Start with specific host and port
uvicorn main:app --host 0.0.0.0 --port 8000

# Start with multiple workers
uvicorn main:app --workers 4

# Start without auto-reload (production)
uvicorn main:app --no-reload
```

### Common Configuration Locations
```bash
# Main application file
./main.py

# Environment variables
./.env

# Configuration files
./config/
./app/core/config.py

# API routes
./app/api/
./app/routers/
```

### Common Configuration Parameters
- `debug`: Enable/disable debug mode
- `workers`: Number of worker processes
- `timeout`: Worker timeout in seconds
- `cors_origins`: Allowed CORS origins
- `allowed_hosts`: List of allowed hosts
- `root_path`: Application root path
- `openapi_url`: OpenAPI schema URL
- `docs_url`: Swagger UI URL

### Useful FastAPI Variables
```python
# Request information
request.client.host  # Client IP
request.headers     # Request headers
request.query_params  # Query parameters
request.path_params  # Path parameters
request.state      # Request state

# Response configuration
response.headers    # Response headers
response.status_code  # Status code
```

### Monitoring and Logs
```bash
# Application logs
./logs/app.log

# Access logs (when using uvicorn)
./logs/access.log

# Monitor application metrics
/metrics  # If prometheus middleware is enabled

# OpenAPI documentation
/docs     # Swagger UI
/redoc    # ReDoc documentation
```

For more detailed information, refer to:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Starlette Documentation](https://www.starlette.io/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)

## Uvicorn
Uvicorn is an ASGI web server implementation used to serve the FastAPI application. Here are essential commands and configurations:

### Basic Commands
```bash
# Start uvicorn with basic configuration
uvicorn main:app --reload

# Start with specific host and port
uvicorn main:app --host 0.0.0.0 --port 8000

# Production deployment with multiple workers
uvicorn main:app --workers 4 --no-reload

# SSL/TLS configuration
uvicorn main:app --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem

# Set log level
uvicorn main:app --log-level debug
```

### Common Configuration Locations
```bash
# Environment variables
.env

# SSL certificates
./certs/

# Log files
./logs/

# Custom config file (when using Config class)
uvicorn_config.py
```

### Common Configuration Parameters
- `workers`: Number of worker processes (default: 1)
- `loop`: Event loop implementation (auto/asyncio/uvloop)
- `timeout_keep_alive`: Keep-alive timeout (default: 5)
- `backlog`: Maximum number of pending connections (default: 2048)
- `limit_concurrency`: Maximum number of concurrent connections
- `limit_max_requests`: Maximum number of requests per worker
- `proxy_headers`: Enable/disable X-Forwarded-* headers

### Useful Uvicorn Variables
```python
# Available through FastAPI app state
app.state.uvicorn_server

# Environment variables
UVICORN_HOST
UVICORN_PORT
UVICORN_WORKERS
UVICORN_LOG_LEVEL
```

### Monitoring and Logs
```bash
# Access logging
uvicorn main:app --access-log

# Enable JSON logging
uvicorn main:app --log-config logging.json

# Monitor worker processes
ps aux | grep uvicorn

# View access logs in real time
tail -f /path/to/access.log

# Common log levels
uvicorn main:app --log-level trace|debug|info|warning|error|critical
```

For more detailed information, refer to:
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [ASGI Specification](https://asgi.readthedocs.io/en/latest/)
- [Uvicorn Settings](https://www.uvicorn.org/settings/)
- [Deployment Guide](https://www.uvicorn.org/deployment/)

## Python
Python is the primary programming language used in this project. Here are essential commands, tools, and configurations:

### Basic Commands
```bash
# Run a Python script
python script.py

# Install packages using pip
pip install package_name
pip install -r requirements.txt

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# List installed packages
pip list

# Generate requirements file
pip freeze > requirements.txt
```

### Common Configuration Locations
```bash
# Virtual environment
./venv/

# Project requirements
./requirements.txt

# Python path configuration
PYTHONPATH
.env

# Configuration files
pyproject.toml
setup.cfg
```

### Common Configuration Parameters
- `PYTHONPATH`: Python module search path
- `PYTHONUNBUFFERED`: Force unbuffered output
- `PYTHONDONTWRITEBYTECODE`: Prevent Python from writing .pyc files
- `PYTHONASYNCIODEBUG`: Enable asyncio debug mode
- `PYTHONWARNINGS`: Warning control

### Useful Python Tools
- `black`: Code formatter
- `flake8`: Style guide enforcer
- `mypy`: Static type checker
- `pytest`: Testing framework
- `isort`: Import sorter
- `pylint`: Code analyzer

### Monitoring and Logs
```bash
# Profile code execution
python -m cProfile script.py

# Memory profiling
python -m memory_profiler script.py

# Debugging
python -m pdb script.py

# Logging configuration
import logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO
)
```

For more detailed information, refer to:
- [Python Documentation](https://docs.python.org/)
- [Python Package Index (PyPI)](https://pypi.org/)
- [Python Enhancement Proposals (PEPs)](https://www.python.org/dev/peps/)
- [Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## Pydantic
Pydantic is a data validation library using Python type annotations. It's used extensively in this project for data modeling and validation. Here are essential concepts and configurations:

### Basic Usage
```python
# Define a basic model
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True

# Create and validate instance
user = User(id=1, name="John", email="john@example.com")

# Export to dictionary/JSON
user_dict = user.model_dump()  # Previously .dict() in v1
user_json = user.model_dump_json()  # Previously .json() in v1
```

### Common Validation Features
```python
from pydantic import BaseModel, Field, EmailStr, validator, constr

class AdvancedUser(BaseModel):
    # Field constraints
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(gt=0, lt=150)
    password: constr(min_length=8)

    # Custom validation
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('must be alphanumeric')
        return v
```

### Configuration Options
```python
from pydantic import BaseModel, ConfigDict

class MyModel(BaseModel):
    model_config = ConfigDict(
        # Common configurations
        validate_assignment=True,
        extra='forbid',
        frozen=False,
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_default=True
    )
```

### Useful Features
```python
# Type aliases
from typing import Dict, List
from pydantic import TypeAdapter

UserList = List[User]
UserDict = Dict[str, User]

# Parse raw data
users = TypeAdapter(UserList).validate_python(data)

# Schema generation
print(User.model_json_schema())  # Previously .schema() in v1

# Data conversion
from pydantic import parse_obj_as
users = parse_obj_as(List[User], data)
```

### Common Patterns
```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# API Request/Response models
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)  # Previously orm_mode=True in v1

# Optional fields
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
```

### Validation and Error Handling
```python
from pydantic import ValidationError

try:
    User(id="not_an_integer", name=123)
except ValidationError as e:
    print(e.errors())
    """
    [
        {
            'loc': ('id',),
            'msg': 'value is not a valid integer',
            'type': 'type_error.integer'
        }
    ]
    """
```

### Integration with FastAPI
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
async def create_item(item: Item):  # Automatic validation
    return item
```

For more detailed information, refer to:
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Pydantic Field Types](https://docs.pydantic.dev/latest/usage/types/)
- [Pydantic Validators](https://docs.pydantic.dev/latest/usage/validators/)
- [Pydantic Settings Management](https://docs.pydantic.dev/latest/usage/settings/)

## SQLAlchemy
SQLAlchemy is the SQL toolkit and Object-Relational Mapping (ORM) library used in this project. Here are essential concepts and configurations:

### Basic Usage
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model
Base = declarative_base()

# Define models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    name = Column(String(50))
    
# Create tables
Base.metadata.create_all(bind=engine)
```

### Common Query Operations
```python
# Create
def create_user(db: Session, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Read
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Update
def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    return db_user

# Delete
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()
```

### Relationship Patterns
```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
```

### Common Configuration Parameters
```python
# Engine configuration
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5,                    # Connection pool size
    max_overflow=10,                # Max extra connections
    pool_timeout=30,                # Connection timeout
    pool_recycle=1800,             # Connection recycle time
    echo=True                       # SQL logging
)

# Session configuration
Session = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=True
)
```

### Query Optimization
```python
# Eager loading
users = (
    db.query(User)
    .options(joinedload(User.posts))
    .all()
)

# Pagination
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

# Complex filters
from sqlalchemy import or_, and_
users = (
    db.query(User)
    .filter(
        and_(
            User.is_active == True,
            or_(
                User.name.like("%John%"),
                User.email.like("%john%")
            )
        )
    )
    .all()
)
```

### FastAPI Integration
```python
from fastapi import Depends
from sqlalchemy.orm import Session

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)
```

### Migration Management (Alembic)
```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Create users table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history
```

### Performance Monitoring
```python
# Enable SQL logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Profile queries
from sqlalchemy import event

@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop()
    print(f"Query took {total}s: {statement}")
```

For more detailed information, refer to:
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Performance](https://docs.sqlalchemy.org/en/14/faq/performance.html)

## Bash
Bash is the shell and command language used in this project for scripting and command-line operations.

### Basic Commands
```bash
# Navigation
pwd                     # Print working directory
cd /path/to/directory   # Change directory
ls -la                  # List files with details
tree                    # Display directory structure

# File viewing
cat file.txt           # Display file content
less file.txt          # View file with pagination
head -n 10 file.txt    # Show first 10 lines
tail -f file.log       # Follow log file updates

# Search
grep "pattern" file    # Search for pattern in file
find . -name "*.py"    # Find files by pattern
```

### File Operations
```bash
# File manipulation
touch file.txt         # Create empty file
cp source dest         # Copy file
mv source dest         # Move/rename file
rm file.txt           # Remove file
rm -rf directory      # Remove directory recursively

# Directory operations
mkdir directory       # Create directory
rmdir directory      # Remove empty directory
```

### System Information
```bash
# System
uname -a              # System information
df -h                 # Disk usage
free -h               # Memory usage
top                   # Process viewer
htop                  # Enhanced process viewer

# Hardware
lscpu                 # CPU information
lsblk                 # Block devices
lsusb                 # USB devices
```

### Process Management
```bash
# Process control
ps aux                # List all processes
kill PID              # Kill process by ID
killall process_name  # Kill process by name
nohup command &       # Run in background
jobs                  # List background jobs

# Resource monitoring
watch command         # Execute command periodically
time command          # Time command execution
```

### Network Commands
```bash
# Network tools
ping host            # Test connectivity
netstat -tulpn       # Show network connections
curl url             # Transfer data
wget url             # Download files
ss -tulpn            # Socket statistics

# Port checking
lsof -i :port        # Check port usage
nc -zv host port     # Test port connection
```

### Text Processing
```bash
# Text manipulation
sed 's/old/new/g'    # Stream editor
awk '{print $1}'     # Pattern scanning
sort file.txt        # Sort lines
uniq                 # Remove duplicates
wc -l file.txt       # Count lines

# File comparison
diff file1 file2     # Compare files
cmp file1 file2      # Compare bytes
```

### Permissions
```bash
# File permissions
chmod 755 file       # Change mode
chown user:group file # Change ownership
umask 022           # Set default permissions
```

## Glossary
- **API**: Application Programming Interface. The API is the interface between the application and the database. FastAPI is used to create the API.
- **Asynchronous Programming**: Asynchronous programming is a programming paradigm that allows for non-blocking, event-driven execution of code. In this project, the replication is done asynchronously.
- **Binlog**: The binary log is a database log that records all changes to the database. In this project, the MySQL shards are configured to use the binlog to replicate the data to the replica.
- **Bufferpool**: The buffer pool is a cache of data blocks that are read from the database. The buffer pool is used to improve the performance of the database by reducing the number of disk reads.
- **Curl**: curl is a command-line tool for transferring data with URLs. In this project, it's used to test the API endpoints.
- **Database**: A structured system for storing, organizing, and retrieving data, which in this project is implemented using MySQL.
- **Docker**: Docker is used to containerize the application and services, providing a consistent and isolated environment that packages all dependencies and can run reliably across different computing environments.
- **Docker Compose**: Docker Compose is used to define and run the multi-container Docker application.
- **Dockerfile**: Dockerfile is a script that contains the instructions for building a Docker image. In this project, it's used to create the Docker image for the FastAPI instances and the testing container.
- **entrypoint**: The entrypoint is the command that is executed when the container starts. In this project, it's used to run the database initialization and replication setup scripts.
- **FastAPI**: FastAPI is the web framework used to create the API.
- **GET**: GET is a request method supported by HTTP used by the API to request data from a specified resource.
- **Load Balancer**: Nginx is used as a load balancer to distribute traffic between the two FastAPI instances.
- **Master**: Another term for the primary database. The primary database is used for write operations (INSERT, UPDATE, DELETE).
- **MySQL**: MySQL is an open-source relational database management system that serves as the backend database in this project, using SQL (Structured Query Language) for managing and querying data.
- **Replica**: The replica database is used for read operations (SELECT).
- **Nginx**: Nginx (pronounced "engine-x") is a powerful open-source web server, reverse proxy, and load balancer. As a web server, it can serve static content with high performance. As a reverse proxy, it sits in front of application servers (like our FastAPI instances) and forwards client requests to them. In our architecture, we're primarily using its load balancing capabilities to distribute incoming traffic across multiple FastAPI instances, which helps improve the application's scalability and reliability. Nginx is known for its high performance, stability, rich feature set, simple configuration, and low resource consumption.
- **POST**: POST is a request method supported by HTTP used by the API to create new resources.
- **Read/Write Splitting**: The application implements database read/write splitting to optimize performance and distribute database load. That means each FastAPI instance will connect to its own MySQL shard, and the requests will be split between the master and replica databases. The write (insert/update/delete) requests will go to the master database, while the read (select) requests will go to the replica database.
- **Replication**: Replication is the process of copying data from one database to another. In this project, the MySQL shards are replicated from the primary to the replica.
- **Round robin**: Round robin is a load balancing algorithm that distributes incoming requests evenly across a group of servers. In this project, Nginx is used to implement round robin load balancing to distribute traffic between the two FastAPI instances.
- **Shard**: A subset of the data that is stored in a database. Each MySQL shard has a master and replica.
- **Swagger UI**: Swagger UI is a tool that allows us to interact with the API and see the available endpoints and their documentation. It's a useful tool for testing and debugging the API.

## Common Issues and Solutions
[Previous troubleshooting section...] 