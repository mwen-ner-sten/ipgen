"""
Core IP address generation functionality.
"""
import ipaddress
from typing import Generator, List, Union, Dict, Any
from pathlib import Path
import pandas as pd
import json
import yaml

class IPGenerator:
    """Main class for IP address generation and manipulation."""
    
    def __init__(self):
        self._ip_ranges = []
        self._ip_addresses = set()
    
    def add_ip(self, ip: Union[str, ipaddress.IPv4Address, ipaddress.IPv6Address]) -> None:
        """Add a single IP address."""
        if isinstance(ip, str):
            ip = ipaddress.ip_address(ip)
        self._ip_addresses.add(ip)
    
    def add_range(self, start_ip: str, end_ip: str) -> None:
        """Add a range of IP addresses."""
        start = ipaddress.ip_address(start_ip)
        end = ipaddress.ip_address(end_ip)
        self._ip_ranges.append((start, end))
    
    def add_cidr(self, cidr: str) -> None:
        """Add a CIDR network."""
        network = ipaddress.ip_network(cidr)
        self._ip_ranges.append((network[0], network[-1]))
    
    def add_wildcard(self, ip: str, wildcard: str) -> None:
        """Add IP addresses matching a wildcard pattern."""
        # Convert wildcard to CIDR
        parts = wildcard.split('.')
        cidr = sum(1 for p in parts if p == '255')
        network = ipaddress.ip_network(f"{ip}/{cidr}")
        self._ip_ranges.append((network[0], network[-1]))
    
    def add_gateway_subnet(self, gateway: str, subnet_mask: str) -> None:
        """Add IP addresses based on gateway and subnet mask."""
        network = ipaddress.ip_network(f"{gateway}/{subnet_mask}")
        self._ip_ranges.append((network[0], network[-1]))
    
    def generate(self) -> Generator[Union[ipaddress.IPv4Address, ipaddress.IPv6Address], None, None]:
        """Generate all IP addresses as a generator."""
        # Add individual IPs
        for ip in self._ip_addresses:
            yield ip
        
        # Add ranges
        for start, end in self._ip_ranges:
            current = start
            while current <= end:
                yield current
                current += 1
    
    def to_list(self) -> List[Union[ipaddress.IPv4Address, ipaddress.IPv6Address]]:
        """Convert to list of IP addresses."""
        return list(self.generate())
    
    def to_dict(self) -> Dict[str, List[str]]:
        """Convert to dictionary with string representations."""
        return {
            'ip_addresses': [str(ip) for ip in self._ip_addresses],
            'ranges': [(str(start), str(end)) for start, end in self._ip_ranges]
        }
    
    def to_csv(self, filepath: Union[str, Path]) -> None:
        """Save IP addresses to CSV file."""
        df = pd.DataFrame({'ip_address': [str(ip) for ip in self.generate()]})
        df.to_csv(filepath, index=False)
    
    def to_excel(self, filepath: Union[str, Path]) -> None:
        """Save IP addresses to Excel file."""
        df = pd.DataFrame({'ip_address': [str(ip) for ip in self.generate()]})
        df.to_excel(filepath, index=False)
    
    def to_json(self, filepath: Union[str, Path]) -> None:
        """Save IP addresses to JSON file."""
        data = self.to_dict()
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def to_yaml(self, filepath: Union[str, Path]) -> None:
        """Save IP addresses to YAML file."""
        data = self.to_dict()
        with open(filepath, 'w') as f:
            yaml.dump(data, f) 