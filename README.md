# IPGen

A flexible IP address generator supporting multiple input and output formats. This package is designed for network scanning and device discovery tasks, allowing you to generate IP addresses from various sources and output them in different formats.

## Features

- Multiple input formats:
  - Single IP addresses
  - IP ranges
  - CIDR notation
  - Wildcard patterns
  - Gateway and subnet mask
  - CSV files
  - Excel files
  - JSON files
  - YAML files

- Multiple output formats:
  - Python generator (memory efficient)
  - Python list
  - Python dictionary
  - CSV files
  - Excel files
  - JSON files
  - YAML files

## Installation

```bash
pip install -r requirements.txt
```

## Usage Examples

### Basic Usage

```python
from ipgen import IPGenerator, parse_cidr, parse_range

# Create a generator from CIDR notation
generator = parse_cidr("192.168.1.0/24")

# Add a range
generator.add_range("10.0.0.1", "10.0.0.10")

# Generate IPs as a generator (memory efficient)
for ip in generator.generate():
    print(ip)

# Convert to list
ip_list = generator.to_list()

# Save to CSV
generator.to_csv("output.csv")

# Save to Excel
generator.to_excel("output.xlsx")

# Save to JSON
generator.to_json("output.json")

# Save to YAML
generator.to_yaml("output.yaml")
```

### Reading from Files

```python
from ipgen import parse_csv, parse_excel, parse_json, parse_yaml

# Read from CSV
generator = parse_csv("input.csv", ip_column="ip_address")

# Read from Excel
generator = parse_excel("input.xlsx", ip_column="ip_address")

# Read from JSON
generator = parse_json("input.json")

# Read from YAML
generator = parse_yaml("input.yaml")
```

### Using Wildcards and Gateway/Subnet

```python
from ipgen import parse_wildcard, parse_gateway_subnet

# Using wildcard pattern
generator = parse_wildcard("192.168.1.0", "255.255.255.0")

# Using gateway and subnet mask
generator = parse_gateway_subnet("192.168.1.1", "255.255.255.0")
```

## Input File Formats

### CSV/Excel
The files should contain a column with IP addresses (default column name is 'ip_address').

### JSON
```json
{
    "ip_addresses": ["192.168.1.1", "192.168.1.2"],
    "ranges": [
        ["10.0.0.1", "10.0.0.10"]
    ]
}
```

### YAML
```yaml
ip_addresses:
  - 192.168.1.1
  - 192.168.1.2
ranges:
  - ["10.0.0.1", "10.0.0.10"]
```
