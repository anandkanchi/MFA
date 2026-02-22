#!/usr/bin/env python
"""Test script for mutual fund handler"""

from app.mutual_fund_handler import MutualFundHandler

if __name__ == '__main__':
    print("Testing Mutual Fund Handler...")
    mfh = MutualFundHandler()
    
    print("\n1. Testing fund data fetching...")
    result = mfh.fetch_fund_data('HDFC', '2024-01-01', '2024-01-31')
    
    if result['success']:
        print(f"✓ Success! Fetched {result['record_count']} records")
        print(f"✓ Found {result['funds_found']} matching funds")
        if result['data']:
            print(f"✓ Sample data: {result['data'][0]}")
    else:
        print(f"✗ Error: {result['message']}")
    
    print("\nTest complete!")
