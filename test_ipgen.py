#!/usr/bin/env python3
"""
Test suite for IPGen package.
"""

import sys
import os
import logging
import pytest
from ipaddress import IPv4Address, IPv6Address, AddressValueError, NetmaskValueError

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add parent directory to path if running directly
if __name__ == "__main__":
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)

from ipgen import IPGenerator, MACGenerator

def test_ip_generator_basic():
    """Test basic IP generator functionality."""
    ip_gen = IPGenerator()
    
    # Test adding single IP
    ip_gen.add_ip("192.168.1.1")
    assert "192.168.1.1" in ip_gen
    assert len(ip_gen) == 1
    
    # Test adding range
    ip_gen.add_range("10.0.0.1", "10.0.0.5")
    assert len(ip_gen) == 6  # 1 single IP + 5 from range
    assert "10.0.0.3" in ip_gen
    
    # Test adding CIDR
    ip_gen.add_cidr("172.16.0.0/30")
    assert len(ip_gen) == 8  # Previous 6 + 2 from CIDR (excluding network and broadcast)
    assert "172.16.0.1" in ip_gen
    
    # Test iteration
    ips = list(ip_gen)
    assert len(ips) == 8
    assert "192.168.1.1" in ips
    assert "10.0.0.3" in ips
    assert "172.16.0.1" in ips

def test_ip_generator_edge_cases():
    """Test edge cases for IP generator."""
    ip_gen = IPGenerator()
    
    # Test invalid IP address
    with pytest.raises(ValueError):
        ip_gen.add_ip("256.256.256.256")
    
    # Test invalid CIDR
    with pytest.raises(ValueError):
        ip_gen.add_cidr("192.168.1.0/33")
    
    # Test invalid range (start > end)
    with pytest.raises(ValueError):
        ip_gen.add_range("192.168.1.10", "192.168.1.1")
    
    # Test empty generator
    assert len(ip_gen) == 0
    assert list(ip_gen) == []
    
    # Test duplicate IPs
    ip_gen.add_ip("192.168.1.1")
    ip_gen.add_ip("192.168.1.1")
    assert len(ip_gen) == 1

def test_ip_generator_special_ranges():
    """Test special IP ranges."""
    ip_gen = IPGenerator()
    
    # Test private ranges
    ip_gen.add_cidr("10.0.0.0/24")  # Class A private
    ip_gen.add_cidr("172.16.0.0/24")  # Class B private
    ip_gen.add_cidr("192.168.0.0/24")  # Class C private
    
    assert "10.0.0.1" in ip_gen
    assert "172.16.0.1" in ip_gen
    assert "192.168.0.1" in ip_gen
    
    # Test loopback
    ip_gen.add_ip("127.0.0.1")
    assert "127.0.0.1" in ip_gen

def test_ip_generator_exclusion():
    """Test IP exclusion functionality."""
    ip_gen = IPGenerator()
    
    # Add some IPs
    ip_gen.add_range("192.168.1.1", "192.168.1.5")
    assert len(ip_gen) == 5
    
    # Exclude specific IPs
    ip_gen.exclude_ips(["192.168.1.2", "192.168.1.4"])
    assert len(ip_gen) == 3
    assert "192.168.1.2" not in ip_gen
    assert "192.168.1.4" not in ip_gen
    
    # Exclude subnet
    ip_gen.exclude_subnet("192.168.1.0/30")
    assert len(ip_gen) == 1
    assert "192.168.1.5" in ip_gen
    
    # Test excluding non-existent IPs
    ip_gen.exclude_ips(["10.0.0.1"])
    assert len(ip_gen) == 1

def test_ip_generator_clear():
    """Test clearing the IP generator."""
    ip_gen = IPGenerator()
    ip_gen.add_ip("192.168.1.1")
    ip_gen.add_range("10.0.0.1", "10.0.0.5")
    
    assert len(ip_gen) == 6
    ip_gen.clear()
    assert len(ip_gen) == 0
    assert list(ip_gen) == []

def test_mac_generator_basic():
    """Test basic MAC generator functionality."""
    mac_gen = MACGenerator()
    
    # Test adding single MAC
    mac_gen.add_mac("00:11:22:33:44:55")
    assert "00:11:22:33:44:55" in mac_gen
    assert len(mac_gen) == 1
    
    # Test adding multiple MACs
    mac_gen.add_macs(["aa:bb:cc:dd:ee:ff", "11:22:33:44:55:66"])
    assert len(mac_gen) == 3
    
    # Test iteration
    macs = list(mac_gen)
    assert len(macs) == 3
    assert "00:11:22:33:44:55" in macs
    assert "aa:bb:cc:dd:ee:ff" in macs
    assert "11:22:33:44:55:66" in macs

def test_mac_generator_edge_cases():
    """Test edge cases for MAC generator."""
    mac_gen = MACGenerator()
    
    # Test invalid MAC format
    with pytest.raises(ValueError):
        mac_gen.add_mac("invalid_mac")
    
    # Test invalid MAC length
    with pytest.raises(ValueError):
        mac_gen.add_mac("00:11:22:33:44")
    
    # Test invalid characters
    with pytest.raises(ValueError):
        mac_gen.add_mac("gg:hh:ii:jj:kk:ll")
    
    # Test empty generator
    assert len(mac_gen) == 0
    assert list(mac_gen) == []
    
    # Test duplicate MACs
    mac_gen.add_mac("00:11:22:33:44:55")
    mac_gen.add_mac("00:11:22:33:44:55")
    assert len(mac_gen) == 1

def test_mac_generator_random():
    """Test random MAC generation."""
    mac_gen = MACGenerator()
    
    # Generate random MACs
    mac_gen.generate_random_macs(5)
    assert len(mac_gen) == 5
    
    # Check format and uniqueness
    macs = list(mac_gen)
    assert len(set(macs)) == 5  # All MACs should be unique
    
    for mac in mac_gen:
        assert MACGenerator._is_valid_mac(mac)
        assert len(mac.split(':')) == 6
        # Check if MAC is properly formatted (all lowercase)
        assert mac.lower() == mac

def test_mac_generator_sequential():
    """Test sequential MAC generation."""
    mac_gen = MACGenerator()
    
    # Generate sequential MACs
    mac_gen.generate_sequential_macs("00:11:22:33:44:55", 3)
    assert len(mac_gen) == 3
    
    # Check sequence
    macs = sorted(list(mac_gen))
    assert macs[0] == "00:11:22:33:44:55"
    assert macs[1] == "00:11:22:33:44:56"
    assert macs[2] == "00:11:22:33:44:57"
    
    # Test overflow
    mac_gen.clear()
    mac_gen.generate_sequential_macs("00:11:22:33:44:ff", 3)
    macs = sorted(list(mac_gen))
    assert macs[0] == "00:11:22:33:44:ff"
    assert macs[1] == "00:11:22:33:45:00"
    assert macs[2] == "00:11:22:33:45:01"

def test_mac_generator_clear():
    """Test clearing the MAC generator."""
    mac_gen = MACGenerator()
    mac_gen.add_mac("00:11:22:33:44:55")
    mac_gen.generate_random_macs(3)
    
    assert len(mac_gen) == 4
    mac_gen.clear()
    assert len(mac_gen) == 0
    assert list(mac_gen) == []

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 