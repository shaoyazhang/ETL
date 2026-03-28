# Python ETL Project

## Overview

A comprehensive Extract-Transform-Load (ETL) pipeline system built with Python, designed to process, validate, and store data from multiple sources (logs, JSON, databases) into target databases and CSV files. The system includes data validation, error handling, transaction management, and metadata tracking for processed files.

## Project Architecture

```
python-etl/
├── simulator/                 # Data simulators for testing
│   └── backend_logs_simulator.py    # Generates test log files
├── config/                    # Configuration management
│   ├── __init__.py
│   ├── project_config.py      # Central configuration (DB, paths, schemas)
│   └── learning/              # Learning/example code
├── model/                     # Data models
│   ├── __init__.py
│   ├── log_model.py          # Log data model
│   ├── barcode_model.py      # Barcode data model
│   └── retail_orders_model.py # Order data model
├── util/                      # Utility modules
│   ├── __init__.py
│   ├── logging_util.py       # Logging initialization and setup
│   ├── mysql_util.py         # MySQL database operations
│   ├── file_util.py          # File system operations
│   ├── str_util.py           # String utilities
│   └── time_util.py          # Time utilities
├── test/                      # Unit tests
│   ├── test_file_util.py
│   ├── test_logging.py
│   ├── test_mysql_util.py
│   ├── test_str_util.py
│   └── test_time_util.py
├── data/                      # Data files (SQL dumps, etc.)
│   └── sys_barcode_2000.sql
├── logs/                      # Generated log outputs
├── logs_service.py           # Main log processing service
├── json_service.py           # JSON data processing service
└── mysql_service.py          # MySQL data processing service
```

## Key Features

### 1. **Log Processing Pipeline** (`logs_service.py`)
- **File Discovery**: Automatically detects new log files in configured directory
- **Deduplication**: Tracks processed files using metadata tables to prevent re-processing
- **Data Parsing**: Parses TSV-formatted log files with validation
- **Multi-Target Output**: 
  - Stores processed data in MySQL database (`logs` table)
  - Exports data to CSV files (UTF-8-sig encoding for Excel compatibility)
- **Error Handling**: Graceful error handling with detailed logging
- **Transaction Management**: Batch inserts with configurable commit intervals

### 2. **Log Simulator** (`backend_logs_simulator.py`)
- Generates realistic test log files with:
  - Timestamps and log levels (INFO, WARN)
  - Module names and response times (10-2000ms)
  - Geographic information (provinces, cities)
  - Diverse log messages
- Configurable file count and lines per file
- TSV format with headers for easy import/export

### 3. **Database Operations** (`util/mysql_util.py`)
- Connection pooling and management
- Automatic table creation based on schema definitions
- Query execution with error handling
- Both transactional (manual commit) and auto-commit modes
- Safe SQL construction with null value handling

### 4. **Metadata Tracking**
- **logs_monitor table**: Tracks which files have been processed
- Stores filename and line count processed
- Prevents duplicate processing of files
- Enables resumable/incremental processing

## Configuration

### Main Configuration File: `config/project_config.py`

```python
# Metadata Database (tracks processed files)
metadata_host = 'localhost'
metadata_database = 'metadata'
metadata_logs_update_monitor_table_name = 'logs_monitor'

# Target Database  
target_host = 'localhost'
target_database = 'retail'
target_logs_table_name = 'logs'

# File Paths
logs_root_path = 'D:/Pythons_studies/logs/'
logs_output_csv_root_path = 'D:/Pythons_studies/logs/csv'

# MySQL Encoding
mysql_charset = 'utf8'
```

### Table Schemas

#### logs_monitor (Metadata Tracking)
```sql
CREATE TABLE logs_monitor (
    id INT PRIMARY KEY AUTO_INCREMENT,
    file_name VARCHAR(255) UNIQUE NOT NULL,
    proces_line INT COMMENT 'Number of records processed',
    process_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### logs (Target Data Storage)
```sql
CREATE TABLE logs (
    timestamp VARCHAR(255),
    log_level VARCHAR(20),
    module VARCHAR(255),
    response_time INT,
    province VARCHAR(50),
    city VARCHAR(50),
    message TEXT
);
```

## Database Setup

### Step 1: Create Databases
```sql
CREATE DATABASE metadata;
CREATE DATABASE retail;
```

### Step 2: Configure Credentials
Update `config/project_config.py` with your MySQL credentials:
```python
metadata_user = 'root'
metadata_password = 'your_password'
```

### Step 3: Verify Connection
The scripts will automatically create required tables on first run.

## Usage

### 1. Generate Test Log Files
```bash
cd simulator
python backend_logs_simulator.py
```
Creates 5 log files with 1024 records each in `D:/Pythons_studies/logs/logs/`

### 2. Process Log Files
```bash
cd ..
python logs_service.py
```
- Discovers new log files
- Parses and validates data
- Stores in MySQL `logs` table
- Exports to CSV file
- Records processed files in `logs_monitor` table

### 3. Run Tests
```bash
python -m pytest test/
```

## Data Flow

```
┌─────────────────────┐
│  Simulator Generates│
│   Log Files (TSV)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  logs_service.py    │
│  1. Discover Files  │
│  2. Check Monitor   │
│  3. Skip Processed  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Parse & Validate  │
│   LogModel Objects  │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌────────┐  ┌──────────┐
│  MySQL │  │   CSV    │
│  logs  │  │  Export  │
└────────┘  └──────────┘
    │             │
    └──────┬──────┘
           │
           ▼
┌─────────────────────┐
│  Update Monitor     │
│  Mark as Processed  │
└─────────────────────┘
```

## Error Handling

The system includes comprehensive error handling:
- **File Reading Errors**: Logged and skipped, processing continues
- **Data Parsing Errors**: Invalid lines are logged as warnings
- **Database Errors**: Transaction rolled back on failure
- **Connection Errors**: Detailed error messages for troubleshooting

Example error handling in log parsing:
```python
try:
    response_time = int(response_time)
except Exception:
    logger.warning(f"Failed to parse response time: {response_time_raw}")
    response_time = 0
```

## Performance Optimizations

1. **Batch Processing**: Inserts grouped into transactions (1000 records per batch)
2. **Deduplication**: Only processes new files, skips already-processed ones
3. **File I/O**: Efficient streaming of large files
4. **Database Indexing**: Indexed tables for faster queries
5. **Memory Management**: Line-by-line parsing to minimize memory footprint

## Logging

Logs are written to: `D:/Pythons_studies/logs/pyetl-{YYYYMMDD-HH}.log`

Log levels configured per module:
- `logging_util.py`: Initializes logging with timestamps and levels
- All messages include module name, function, and line number

Example log output:
```
2025-01-15 10:30:45,123 - INFO - logs_service.py - Found 3 log files for processing
2025-01-15 10:30:46,234 - WARNING - logs_service.py - Invalid log line format, skipping
2025-01-15 10:30:47,345 - INFO - logs_service.py - Processed 1024 records from file 1.log
```

## Data Models

### LogModel (`model/log_model.py`)
Represents a single log entry with:
- `timestamp`: When the event occurred
- `log_level`: Severity level (INFO, WARN, etc.)
- `module`: Source module/service
- `response_time`: API response time in milliseconds
- `province`: Geographic location - province
- `city`: Geographic location - city
- `message`: Log message content

Methods:
- `to_csv()`: Convert to CSV row format
- `generate_insert_sql()`: Generate SQL insert statement

## Utility Modules

### MySQLUtil (`util/mysql_util.py`)
- Connection management with configurable host/port/credentials
- `execute_with_autocommit()`: Run query with auto-commit
- `execute_without_autocommit()`: Run query for manual transaction control
- `check_table_existes()`: Verify table existence
- `create_table()`: Create table from schema definition
- `query()`: Execute SELECT queries and return results

### FileUtil (`util/file_util.py`)
- `get_dir_files_list()`: Recursively list files in directory
- `get_new_by_compare_lists()`: Find new files by comparing lists

### StringUtil (`util/str_util.py`)
- `check_str_null_and_transform_to_sql_null()`: Convert Python None to SQL NULL
- `check_number_null_and_transform_to_sql_null()`: Handle numeric nulls
- `check_null()`: General null checking

## Future Enhancements

- [ ] Support for additional data formats (JSON lines, Parquet)
- [ ] Real-time processing with message queues (Kafka, RabbitMQ)
- [ ] Advanced data validation with schema enforcement
- [ ] Distributed processing for large-scale data
- [ ] Web UI for monitoring and configuration
- [ ] Automated data quality checks and alerts
- [ ] Support for incremental updates and deletes
- [ ] Compression for archived log files

## Troubleshooting

### Issue: "No files found to process"
- Check that files exist in configured `logs_root_path`
- Verify file format is TSV with correct headers
- Check `logs_monitor` table - files may already be processed

### Issue: "Database connection refused"
- Verify MySQL is running: `mysql -u root -p`
- Check credentials in `project_config.py`
- Verify databases exist: `SHOW DATABASES;`

### Issue: "CSV file encoding issues in Excel"
- System uses UTF-8-sig (with BOM) for Excel compatibility
- If still having issues, try opening in Excel with explicit UTF-8 encoding

## Dependencies

```
Python 3.8+
pymysql >= 1.0.0
```

Install with:
```bash
pip install pymysql
```

## License

Internal project - All rights reserved

## Support

For issues or questions, check the log files for detailed error messages and consult the code comments for implementation details.
