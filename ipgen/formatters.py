"""
Output formatters for writing IP addresses to various formats.
"""
import pandas as pd
import json
import yaml
from typing import List, Dict, Any, Union
from pathlib import Path
import ipaddress

def to_list(ips) -> List[str]:
    """Convert IP generator to a list of IP strings."""
    return [str(ip) for ip in ips]

def to_dict(ips) -> Dict[str, List[str]]:
    """Convert IP generator to a dictionary structure."""
    return {
        'ip_addresses': [str(ip) for ip in ips]
    }

def to_csv(ips, filepath: Union[str, Path]) -> None:
    """Save IP addresses to a CSV file."""
    df = pd.DataFrame({'ip_address': [str(ip) for ip in ips]})
    df.to_csv(filepath, index=False)

def to_excel(ips, filepath: Union[str, Path]) -> None:
    """Save IP addresses to an Excel file."""
    df = pd.DataFrame({'ip_address': [str(ip) for ip in ips]})
    df.to_excel(filepath, index=False)

def to_json(ips, filepath: Union[str, Path]) -> None:
    """Save IP addresses to a JSON file."""
    data = {'ip_addresses': [str(ip) for ip in ips]}
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def to_yaml(ips, filepath: Union[str, Path]) -> None:
    """Save IP addresses to a YAML file."""
    data = {'ip_addresses': [str(ip) for ip in ips]}
    with open(filepath, 'w') as f:
        yaml.dump(data, f) 