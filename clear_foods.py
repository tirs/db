#!/usr/bin/env python3
"""Clear old food data for fresh import"""

import mysql.connector

DB_CONFIG = {
    'host': '82.197.82.46',
    'user': 'u280406916_nutrition',
    'password': 'Mutsokoti08@',
    'database': 'u280406916_nutrition',
    'port': 3306
}

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    print("🗑️  Clearing old food data...")
    
    # Delete in correct order (respecting foreign keys)
    cursor.execute("DELETE FROM nutrition_facts")
    print(f"   Deleted nutrition_facts")
    
    cursor.execute("DELETE FROM foods")
    print(f"   Deleted foods")
    
    cursor.execute("DELETE FROM food_categories")
    print(f"   Deleted food_categories")
    
    conn.commit()
    print("✅ All food data cleared successfully!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ ERROR: {e}")