#!/usr/bin/env python3
"""
Check imported food data
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

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    print("\n📊 DATABASE STATISTICS\n")
    
    # Count foods
    cursor.execute("SELECT COUNT(*) FROM foods")
    food_count = cursor.fetchone()[0]
    print(f"✅ Total foods imported: {food_count}")
    
    # Count nutrition entries
    cursor.execute("SELECT COUNT(*) FROM nutrition_facts")
    nutrition_count = cursor.fetchone()[0]
    print(f"✅ Total nutrition entries: {nutrition_count}")
    
    # Count by category
    cursor.execute("SELECT fc.name, COUNT(*) as count FROM food_categories fc LEFT JOIN foods f ON fc.category_id = f.category_id GROUP BY fc.category_id, fc.name ORDER BY count DESC")
    categories = cursor.fetchall()
    print(f"\n📁 Foods by category:")
    for cat_name, count in categories:
        print(f"   {cat_name}: {count} foods")
    
    # Sample foods
    print(f"\n🍗 Sample foods:")
    cursor.execute("SELECT food_id, name, brand FROM foods LIMIT 5")
    foods = cursor.fetchall()
    for food_id, name, brand in foods:
        brand_info = f" ({brand})" if brand else ""
        print(f"   - {name}{brand_info}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)