#!/usr/bin/env python3
"""
Simple test to verify database connection
"""

import mysql.connector
import sys

DB_CONFIG = {
    'host': '82.197.82.46',
    'user': 'u280406916_nutrition',
    'password': 'Mutsokoti08@',
    'database': 'u280406916_nutrition',
    'port': 3306
}

print(f"🔗 Testing connection to {DB_CONFIG['host']}...")
print(f"   User: {DB_CONFIG['user']}")
print(f"   Database: {DB_CONFIG['database']}")

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Test query
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"✅ SUCCESS! Connected to MySQL version: {version[0]}")
    
    # Check tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"✅ Tables found: {len(tables)}")
    for table in tables:
        print(f"   - {table[0]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)