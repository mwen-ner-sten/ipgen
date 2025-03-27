"""
Input parsers for various IP address formats and file types.
"""
import pandas as pd
import json
import yaml
from typing import List, Union, Dict, Any
from pathlib import Path
from .core import IPGenerator

def parse_csv(filepath: Union[str, Path], ip_column: str = 'ip_address') -> IPGenerator:
    """Parse IP addresses from a CSV file."""
    df = pd.read_csv(filepath)
    generator = IPGenerator()
    
    for ip in df[ip_column]:
        generator.add_ip(ip)
    
    return generator

def parse_excel(filepath: Union[str, Path], ip_column: str = 'ip_address') -> IPGenerator:
    """Parse IP addresses from an Excel file."""
    df = pd.read_excel(filepath)
    generator = IPGenerator()
    
    for ip in df[ip_column]:
        generator.add_ip(ip)
    
    return generator

def parse_json(filepath: Union[str, Path]) -> IPGenerator:
    """Parse IP addresses from a JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    generator = IPGenerator()
    
    if isinstance(data, dict):
        for ip in data.get('ip_addresses', []):
            generator.add_ip(ip)
        for start, end in data.get('ranges', []):
            generator.add_range(start, end)
    elif isinstance(data, list):
        for ip in data:
            generator.add_ip(ip)
    
    return generator

def parse_yaml(filepath: Union[str, Path]) -> IPGenerator:
    """Parse IP addresses from a YAML file."""
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)
    
    generator = IPGenerator()
    
    if isinstance(data, dict):
        for ip in data.get('ip_addresses', []):
            generator.add_ip(ip)
        for start, end in data.get('ranges', []):
            generator.add_range(start, end)
    elif isinstance(data, list):
        for ip in data:
            generator.add_ip(ip)
    
    return generator

def parse_cidr(cidr: str) -> IPGenerator:
    """Parse IP addresses from CIDR notation."""
    generator = IPGenerator()
    generator.add_cidr(cidr)
    return generator

def parse_range(start_ip: str, end_ip: str) -> IPGenerator:
    """Parse IP addresses from a range."""
    generator = IPGenerator()
    generator.add_range(start_ip, end_ip)
    return generator

def parse_wildcard(ip: str, wildcard: str) -> IPGenerator:
    """Parse IP addresses from a wildcard pattern."""
    generator = IPGenerator()
    generator.add_wildcard(ip, wildcard)
    return generator

def parse_gateway_subnet(gateway: str, subnet_mask: str) -> IPGenerator:
    """Parse IP addresses from gateway and subnet mask."""
    generator = IPGenerator()
    generator.add_gateway_subnet(gateway, subnet_mask)
    return generator 