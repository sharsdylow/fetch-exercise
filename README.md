# Fetch Health Check Monitor

This is the solution for Fetch's SRE take home exercise that implements a continuous health check monitoring system for web endpoints.

# Install Requirements

Python 3.6 or higher is required. Install the required packages using:

```shell
pip install -r requirements.txt
```

# Usage

### Command Line Interface

Run the monitor with command-line arguments:

```shell
python healthCheck.py [-h] [-c FILE_PATH] [-s SECOND]
```

Options:

- `-h, --help`: Show help message and exit
- `-c FILE_PATH`: Path to the YAML config file containing endpoint definitions
- `-s SECOND`: Health check test cycle length in seconds (default: 15)

### Interactive Mode

```shell
python healthCheck.py
Please input config file path:[enter your path]
```

## Output

The monitor will display real-time results showing the availability percentage for each domain:

```
Health Check Results (Last Updated: 2024-11-11 10:30:15):
--------------------------------------------------
fetch.com has 33% availability percentage
www.fetchrewards.com has 100% availability percentage
```

## Exiting

Press Ctrl+C to gracefully exit the monitor.

## License

This project is part of a technical exercise and is not licensed for public use.
