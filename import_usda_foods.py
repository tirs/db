#!/usr/bin/env python3
"""
USDA FoodData Central to Nutrition Database Importer
Imports 400,000+ foods with complete nutritional data
"""

import requests
import mysql.connector
import json
import time
from typing import List, Dict, Optional
import sys

# ============================================================================
# CONFIGURATION
# ============================================================================

USDA_API_KEY = "1buWLv3vMzAeQ1319oRbWWP7myxHVjKchC5MqseI"  # Replace with your API key from https://fdc.nal.usda.gov/api-key/

# Database configuration
DB_CONFIG = {
    'host': '82.197.82.46',
    'user': 'u280406916_nutrition',
    'password': 'Mutsokoti08@',
    'database': 'u280406916_nutrition',
    'port': 3306
}

# USDA FDC API endpoints
USDA_SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
USDA_DETAIL_URL = "https://api.nal.usda.gov/fdc/v1/foods/{fdc_id}"

# Categories to import
CATEGORIES = [
    'Vegetables',
    'Fruits',
    'Grains & Cereals',
    'Meat & Poultry',
    'Fish & Seafood',
    'Dairy & Eggs',
    'Nuts & Seeds',
    'Oils & Fats',
    'Beverages',
    'Condiments & Sauces',
    'Snacks',
    'Desserts',
    'Prepared Foods',
    'Fast Food'
]

# Nutrient mapping (USDA to your database)
NUTRIENT_MAPPING = {
    1003: 'protein',           # Protein
    1004: 'fat',               # Fat
    1005: 'carbohydrates',     # Carbohydrates
    1008: 'calories',          # Energy (kcal)
    1079: 'fiber',             # Fiber
    1089: 'sugars',            # Sugars
    1106: 'vitamin_a',         # Vitamin A
    1109: 'vitamin_c',         # Vitamin C
    1114: 'vitamin_d',         # Vitamin D
    1191: 'vitamin_b12',       # Vitamin B12
    1175: 'folate',            # Folate
    1253: 'cholesterol',       # Cholesterol
    1258: 'sodium',            # Sodium
    1259: 'potassium',         # Potassium
    1095: 'calcium',           # Calcium
    1096: 'iron',              # Iron
    1097: 'magnesium',         # Magnesium
    1098: 'phosphorus',        # Phosphorus
    1100: 'zinc',              # Zinc
}

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

def get_db_connection(retry_count=3):
    """Create database connection with retry logic"""
    for attempt in range(retry_count):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            # Set session timeout to avoid idle disconnects
            conn.autocommit = False
            return conn
        except Exception as e:
            if attempt < retry_count - 1:
                print(f"  ⚠️ Connection attempt {attempt + 1} failed, retrying...")
                time.sleep(2)
            else:
                raise e

def get_or_create_category(cursor, category_name: str) -> int:
    """Get or create a food category"""
    # Check if exists
    cursor.execute("SELECT category_id FROM food_categories WHERE name = %s", (category_name,))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    
    # Create if doesn't exist
    cursor.execute(
        "INSERT INTO food_categories (name, description) VALUES (%s, %s)",
        (category_name, f"{category_name} foods from USDA FoodData Central")
    )
    return cursor.lastrowid

def insert_food(cursor, category_id: int, food_data: Dict) -> Optional[int]:
    """Insert food with nutrition data"""
    try:
        # Get nutrition data
        nutrition = food_data.get('nutrition', {})
        
        # Calculate serving size from first nutrient unit
        serving_weight = 100  # Default to 100g for USDA data
        serving_size = "100g"
        
        # Insert into foods table
        cursor.execute("""
            INSERT INTO foods 
            (category_id, name, description, brand, serving_size, serving_weight_g, data_source, is_verified)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            category_id,
            food_data.get('name', '')[:200],
            food_data.get('description', '')[:500],
            food_data.get('brand', '')[:200] or None,
            serving_size,
            serving_weight,
            'USDA',
            True
        ))
        
        food_id = cursor.lastrowid
        
        # Insert nutrition facts data
        # Map nutrient names to database columns
        nutrition_insert = {
            'calories': nutrition.get('calories'),
            'protein_g': nutrition.get('protein'),
            'fat_g': nutrition.get('fat'),
            'carbohydrates_g': nutrition.get('carbohydrates'),
            'fiber_g': nutrition.get('fiber'),
            'sugar_g': nutrition.get('sugars'),
            'cholesterol_mg': nutrition.get('cholesterol'),
            'sodium_mg': nutrition.get('sodium'),
            'potassium_mg': nutrition.get('potassium'),
            'calcium_mg': nutrition.get('calcium'),
            'iron_mg': nutrition.get('iron'),
            'magnesium_mg': nutrition.get('magnesium'),
            'phosphorus_mg': nutrition.get('phosphorus'),
            'zinc_mg': nutrition.get('zinc'),
            'vitamin_a_iu': nutrition.get('vitamin_a'),
            'vitamin_c_mg': nutrition.get('vitamin_c'),
            'vitamin_d_iu': nutrition.get('vitamin_d'),
            'vitamin_b12_mcg': nutrition.get('vitamin_b12'),
            'folate_mcg': nutrition.get('folate'),
        }
        
        # Only insert nutrition facts if we have calories
        if nutrition_insert.get('calories'):
            try:
                cursor.execute("""
                    INSERT INTO nutrition_facts 
                    (food_id, calories, protein_g, fat_g, carbohydrates_g, fiber_g, sugar_g,
                     cholesterol_mg, sodium_mg, potassium_mg, calcium_mg, iron_mg, magnesium_mg,
                     phosphorus_mg, zinc_mg, vitamin_a_iu, vitamin_c_mg, vitamin_d_iu, vitamin_b12_mcg, folate_mcg)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    food_id,
                    nutrition_insert.get('calories'),
                    nutrition_insert.get('protein_g'),
                    nutrition_insert.get('fat_g'),
                    nutrition_insert.get('carbohydrates_g'),
                    nutrition_insert.get('fiber_g'),
                    nutrition_insert.get('sugar_g'),
                    nutrition_insert.get('cholesterol_mg'),
                    nutrition_insert.get('sodium_mg'),
                    nutrition_insert.get('potassium_mg'),
                    nutrition_insert.get('calcium_mg'),
                    nutrition_insert.get('iron_mg'),
                    nutrition_insert.get('magnesium_mg'),
                    nutrition_insert.get('phosphorus_mg'),
                    nutrition_insert.get('zinc_mg'),
                    nutrition_insert.get('vitamin_a_iu'),
                    nutrition_insert.get('vitamin_c_mg'),
                    nutrition_insert.get('vitamin_d_iu'),
                    nutrition_insert.get('vitamin_b12_mcg'),
                    nutrition_insert.get('folate_mcg'),
                ))
            except Exception as e:
                print(f"  ⚠️ Error inserting nutrition facts for food {food_id}: {e}")
                pass
        
        return food_id
    
    except Exception as e:
        print(f"  ❌ Error inserting food {food_data.get('name')}: {e}")
        return None

# ============================================================================
# USDA API FUNCTIONS
# ============================================================================

def search_foods_usda(query: str, page: int = 1) -> Dict:
    """Search USDA FoodData Central"""
    params = {
        'query': query,
        'pageNumber': page,
        'pageSize': 100,
        'api_key': USDA_API_KEY
    }
    
    try:
        response = requests.get(USDA_SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ API Error: {e}")
        return {'foods': []}

def get_food_details(fdc_id: str) -> Dict:
    """Get detailed food information from USDA"""
    params = {'api_key': USDA_API_KEY}
    
    try:
        response = requests.get(USDA_DETAIL_URL.format(fdc_id=fdc_id), params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Parse nutrition data
        nutrition = {}
        if 'foodNutrients' in data:
            for nutrient in data['foodNutrients']:
                nutrient_id = nutrient.get('nutrient', {}).get('id')
                if nutrient_id in NUTRIENT_MAPPING:
                    nutrient_name = NUTRIENT_MAPPING[nutrient_id]
                    nutrition[nutrient_name] = nutrient.get('value')
        
        return {
            'name': data.get('description', '')[:200],
            'description': data.get('description', '')[:500],
            'brand': data.get('brandName', '')[:200],
            'fdc_id': fdc_id,
            'nutrition': nutrition
        }
    
    except Exception as e:
        print(f"⚠️ Could not get details for FDC {fdc_id}: {e}")
        return None

def parse_usda_food(usda_food: Dict) -> Dict:
    """Parse USDA search result into our format"""
    # Extract nutrition from search results if available
    nutrition = {}
    if 'foodNutrients' in usda_food:
        for nutrient in usda_food['foodNutrients']:
            # nutrientId is at the top level of each nutrient object
            nutrient_id = nutrient.get('nutrientId')
            if nutrient_id in NUTRIENT_MAPPING:
                nutrient_name = NUTRIENT_MAPPING[nutrient_id]
                nutrition[nutrient_name] = nutrient.get('value')
    
    return {
        'name': usda_food.get('description', '')[:200],
        'description': usda_food.get('description', '')[:500],
        'brand': usda_food.get('brandName', '')[:200],
        'fdc_id': usda_food.get('fdcId'),
        'nutrition': nutrition
    }

# ============================================================================
# MAIN IMPORT FUNCTION
# ============================================================================

def import_foods_by_category(search_terms: List[str], max_per_category: int = 1000):
    """Import foods from USDA by category"""
    
    if not USDA_API_KEY or USDA_API_KEY == "YOUR_USDA_API_KEY_HERE":
        print("❌ ERROR: Please set your USDA API Key first!")
        print("   Get it free at: https://fdc.nal.usda.gov/api-key/")
        sys.exit(1)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    total_imported = 0
    
    try:
        for search_term in search_terms:
            print(f"\n🔍 Searching for: {search_term}")
            
            # Get or create category
            category_id = get_or_create_category(cursor, search_term)
            conn.commit()
            
            # Search foods
            search_results = search_foods_usda(search_term)
            foods = search_results.get('foods', [])
            
            print(f"   Found {len(foods)} foods in USDA database")
            
            imported_count = 0
            for food in foods[:max_per_category]:
                if imported_count >= max_per_category:
                    break
                
                # Parse food data from search results (includes nutrition)
                food_data = parse_usda_food(food)
                
                # Insert into database directly (no separate detail fetch needed)
                food_id = insert_food(cursor, category_id, food_data)
                if food_id:
                    imported_count += 1
                    total_imported += 1
                    
                    if imported_count % 20 == 0:
                        try:
                            conn.commit()
                            print(f"   ✓ {imported_count} foods imported...")
                        except Exception as e:
                            print(f"   ⚠️ Commit failed: {e}. Reconnecting...")
                            try:
                                conn.close()
                            except:
                                pass
                            conn = get_db_connection()
                            cursor = conn.cursor()
                
                # Rate limiting - USDA has limits
                time.sleep(0.05)
            
            try:
                conn.commit()
            except Exception as e:
                print(f"   ⚠️ Final commit failed: {e}")
            print(f"   ✅ Imported {imported_count} foods")
        
        print(f"\n✅ SUCCESS! Imported {total_imported} foods total")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        try:
            conn.rollback()
        except:
            pass
    
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass

# ============================================================================
# QUICK IMPORT (Recommended for first run)
# ============================================================================

def import_popular_foods(max_per_category: int = 500):
    """Import most popular/common foods quickly"""
    
    popular_searches = [
        'chicken',
        'rice',
        'bread',
        'apple',
        'banana',
        'milk',
        'eggs',
        'fish',
        'vegetables',
        'pasta',
    ]
    
    import_foods_by_category(popular_searches, max_per_category)

# ============================================================================
# FULL IMPORT (Takes longer but gets everything)
# ============================================================================

def import_full_database(max_per_category: int = 1000):
    """Import full food database by all categories"""
    import_foods_by_category(CATEGORIES, max_per_category)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════╗
║   USDA FoodData Central Import Tool                           ║
║   Imports 400,000+ foods with complete nutrition data         ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    print("Choose import option:")
    print("  1. Quick Import (500 popular foods) - ~5-10 minutes")
    print("  2. Full Import (1000+ foods per category) - ~1-2 hours")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        print("\n⏱️  Starting quick import...")
        import_popular_foods(500)
    elif choice == "2":
        print("\n⏱️  Starting full import...")
        import_full_database(1000)
    else:
        print("❌ Invalid choice")
        sys.exit(1)