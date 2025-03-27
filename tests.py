#!/usr/bin/env python3
"""
Test script for IPGen functionality.
"""
import os
import tempfile
import ipaddress
from ipgen import (
    IPGenerator,
    parse_cidr,
    parse_range,
    parse_wildcard,
    parse_gateway_subnet,
)

def test_single_ip():
    """Test adding a single IP."""
    generator = IPGenerator()
    generator.add_ip("192.168.1.1")
    ips = list(generator.generate())
    assert len(ips) == 1
    assert str(ips[0]) == "192.168.1.1"
    print("✓ Single IP test passed")

def test_ip_range():
    """Test adding an IP range."""
    generator = IPGenerator()
    generator.add_range("192.168.1.1", "192.168.1.10")
    ips = list(generator.generate())
    assert len(ips) == 10
    assert str(ips[0]) == "192.168.1.1"
    assert str(ips[-1]) == "192.168.1.10"
    print("✓ IP range test passed")

def test_cidr():
    """Test adding a CIDR network."""
    generator = parse_cidr("192.168.1.0/30")
    ips = list(generator.generate())
    assert len(ips) == 4  # 4 IPs in a /30 network
    assert str(ips[0]) == "192.168.1.0"
    assert str(ips[-1]) == "192.168.1.3"
    print("✓ CIDR test passed")

def test_wildcard():
    """Test adding a wildcard pattern."""
    # 0.0.0.255 means the last octet can be 0-255
    generator = parse_wildcard("192.168.1.0", "0.0.0.255")
    ips = list(generator.generate())
    assert len(ips) == 256  # 256 IPs in the range
    assert str(ips[0]) == "192.168.1.0"
    assert str(ips[-1]) == "192.168.1.255"
    print("✓ Wildcard test passed")

def test_gateway_subnet():
    """Test adding a gateway/subnet."""
    generator = parse_gateway_subnet("192.168.1.1", "255.255.255.0")
    ips = list(generator.generate())
    assert len(ips) == 256  # 256 IPs in a /24 network
    assert str(ips[0]) == "192.168.1.0"
    assert str(ips[-1]) == "192.168.1.255"
    print("✓ Gateway/subnet test passed")

def test_output_formats():
    """Test output to various formats."""
    generator = parse_cidr("192.168.1.0/28")  # 16 IPs
    
    # Test list output
    ip_list = generator.to_list()
    assert len(ip_list) == 16
    
    # Test file outputs
    with tempfile.TemporaryDirectory() as tmpdir:
        # CSV output
        csv_file = os.path.join(tmpdir, "test.csv")
        generator.to_csv(csv_file)
        assert os.path.exists(csv_file)
        
        # Excel output
        excel_file = os.path.join(tmpdir, "test.xlsx")
        generator.to_excel(excel_file)
        assert os.path.exists(excel_file)
        
        # JSON output
        json_file = os.path.join(tmpdir, "test.json")
        generator.to_json(json_file)
        assert os.path.exists(json_file)
        
        # YAML output
        yaml_file = os.path.join(tmpdir, "test.yaml")
        generator.to_yaml(yaml_file)
        assert os.path.exists(yaml_file)
    
    print("✓ Output formats test passed")

def main():
    """Run all tests."""
    print("Running IPGen tests...\n")
    
    try:
        test_single_ip()
        test_ip_range()
        test_cidr()
        test_wildcard()
        test_gateway_subnet()
        test_output_formats()
        
        print("\nAll tests passed successfully!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {str(e)}")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 