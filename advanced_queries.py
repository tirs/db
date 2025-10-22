#!/usr/bin/env python3
"""
Advanced Database Query and Analysis Script
Comprehensive analysis of imported nutrition data
"""

import mysql.connector
import json
from typing import List, Dict, Any
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': '82.197.82.46',
    'user': 'u280406916_nutrition',
    'password': 'Mutsokoti08@',
    'database': 'u280406916_nutrition',
    'port': 3306
}

class NutritionAnalyzer:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Connect to database"""
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(dictionary=True)
        print("✓ Database connected\n")
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def print_section(self, title):
        """Print formatted section header"""
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    
    def print_results(self, results: List[Dict], max_rows: int = 10):
        """Pretty print query results"""
        if not results:
            print("   No results")
            return
        
        results = results[:max_rows]
        
        # Get column names
        if isinstance(results[0], dict):
            columns = list(results[0].keys())
        else:
            columns = [f"col_{i}" for i in range(len(results[0]))]
        
        # Calculate column widths
        col_widths = {}
        for col in columns:
            col_widths[col] = max(len(str(col)), max(len(str(row.get(col, ''))) for row in results))
        
        # Print header
        header = " | ".join(f"{col:{col_widths[col]}}" for col in columns)
        print(f"   {header}")
        print(f"   {'-' * len(header)}")
        
        # Print rows
        for row in results:
            row_str = " | ".join(f"{str(row.get(col, '')):{col_widths[col]}}" for col in columns)
            print(f"   {row_str}")
        
        if len(results) == max_rows:
            print(f"   ... (showing {max_rows} of {len(results)} results)")
    
    # ========================================================================
    # 1. OVERVIEW QUERIES
    # ========================================================================
    
    def database_overview(self):
        """Overall database statistics"""
        self.print_section("1. DATABASE OVERVIEW")
        
        # Total counts
        self.cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM food_categories) as total_categories,
                (SELECT COUNT(*) FROM foods) as total_foods,
                (SELECT COUNT(*) FROM nutrition_facts) as total_nutrition_records,
                (SELECT COUNT(*) FROM nutrition_facts WHERE calories IS NOT NULL) as foods_with_calories,
                (SELECT COUNT(*) FROM nutrition_facts WHERE calories IS NULL) as foods_without_calories
        """)
        results = self.cursor.fetchall()
        for row in results:
            print(f"   Total Categories:              {row['total_categories']}")
            print(f"   Total Foods:                   {row['total_foods']}")
            print(f"   Total Nutrition Records:       {row['total_nutrition_records']}")
            print(f"   Foods with Calorie Data:       {row['foods_with_calories']}")
            print(f"   Foods without Calorie Data:    {row['foods_without_calories']}")
    
    def category_breakdown(self):
        """Foods per category"""
        self.print_section("2. FOODS PER CATEGORY")
        
        self.cursor.execute("""
            SELECT 
                fc.name,
                COUNT(f.food_id) as food_count,
                COUNT(nf.nutrition_id) as nutrition_records
            FROM food_categories fc
            LEFT JOIN foods f ON fc.category_id = f.category_id
            LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
            GROUP BY fc.category_id, fc.name
            ORDER BY food_count DESC
        """)
        results = self.cursor.fetchall()
        self.print_results(results, max_rows=20)
    
    # ========================================================================
    # 2. NUTRITIONAL EXTREMES
    # ========================================================================
    
    def highest_calorie_foods(self, limit: int = 10):
        """Foods with highest calorie content"""
        self.print_section(f"3. TOP {limit} HIGHEST CALORIE FOODS")
        
        self.cursor.execute(f"""
            SELECT 
                f.name,
                fc.name as category,
                nf.calories,
                nf.fat_g,
                nf.protein_g
            FROM foods f
            JOIN food_categories fc ON f.category_id = fc.category_id
            JOIN nutrition_facts nf ON f.food_id = nf.food_id
            WHERE nf.calories IS NOT NULL
            ORDER BY nf.calories DESC
            LIMIT {limit}
        """)
        results = self.cursor.fetchall()
        self.print_results(results)
    
    def highest_protein_foods(self, limit: int = 10):
        """Foods with highest protein content"""
        self.print_section(f"4. TOP {limit} HIGHEST PROTEIN FOODS")
        
        self.cursor.execute(f"""
            SELECT 
                f.name,
                fc.name as category,
                nf.protein_g,
                nf.calories,
                ROUND((nf.protein_g * 4) / nf.calories * 100, 2) as protein_percent
            FROM foods f
            JOIN food_categories fc ON f.category_id = fc.category_id
            JOIN nutrition_facts nf ON f.food_id = nf.food_id
            WHERE nf.protein_g IS NOT NULL AND nf.calories IS NOT NULL
            ORDER BY nf.protein_g DESC
            LIMIT {limit}
        """)
        results = self.cursor.fetchall()
        self.print_results(results)
    
    def lowest_sodium_foods(self, limit: int = 10):
        """Foods with lowest sodium content"""
        self.print_section(f"5. TOP {limit} LOWEST SODIUM FOODS")
        
        self.cursor.execute(f"""
            SELECT 
                f.name,
                fc.name as category,
                nf.sodium_mg,
                nf.calories
            FROM foods f
            JOIN food_categories fc ON f.category_id = fc.category_id
            JOIN nutrition_facts nf ON f.food_id = nf.food_id
            WHERE nf.sodium_mg IS NOT NULL
            ORDER BY nf.sodium_mg ASC
            LIMIT {limit}
        """)
        results = self.cursor.fetchall()
        self.print_results(results)
    
    def highest_fiber_foods(self, limit: int = 10):
        """Foods with highest fiber content"""
        self.print_section(f"6. TOP {limit} HIGHEST FIBER FOODS")
        
        self.cursor.execute(f"""
            SELECT 
                f.name,
                fc.name as category,
                nf.fiber_g,
                nf.carbohydrates_g,
                nf.calories
            FROM foods f
            JOIN food_categories fc ON f.category_id = fc.category_id
            JOIN nutrition_facts nf ON f.food_id = nf.food_id
            WHERE nf.fiber_g IS NOT NULL
            ORDER BY nf.fiber_g DESC
            LIMIT {limit}
        """)
        results = self.cursor.fetchall()
        self.print_results(results)
    
    # ========================================================================
    # 3. CATEGORY ANALYSIS
    # ========================================================================
    
    def category_nutrition_stats(self):
        """Average nutrition values per category"""
        self.print_section("7. AVERAGE NUTRITION BY CATEGORY")
        
        self.cursor.execute("""
            SELECT 
                fc.name as category,
                ROUND(AVG(nf.calories), 2) as avg_calories,
                ROUND(AVG(nf.protein_g), 2) as avg_protein,
                ROUND(AVG(nf.fat_g), 2) as avg_fat,
                ROUND(AVG(nf.carbohydrates_g), 2) as avg_carbs,
                ROUND(AVG(nf.fiber_g), 2) as avg_fiber,
                COUNT(nf.nutrition_id) as records_count
            FROM food_categories fc
            LEFT JOIN foods f ON fc.category_id = f.category_id
            LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
            WHERE nf.calories IS NOT NULL
            GROUP BY fc.category_id, fc.name
            ORDER BY avg_calories DESC
        """)
        results = self.cursor.fetchall()
        self.print_results(results, max_rows=20)
    
    def category_with_most_sugar(self):
        """Which category has most sugar on average"""
        self.print_section("8. SUGAR CONTENT BY CATEGORY")
        
        self.cursor.execute("""
            SELECT 
                fc.name as category,
                ROUND(AVG(nf.sugar_g), 2) as avg_sugar,
                ROUND(MAX(nf.sugar_g), 2) as max_sugar,
                COUNT(nf.nutrition_id) as foods_with_sugar_data
            FROM food_categories fc
            LEFT JOIN foods f ON fc.category_id = f.category_id
            LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
            WHERE nf.sugar_g IS NOT NULL
            GROUP BY fc.category_id, fc.name
            ORDER BY avg_sugar DESC
        """)
        results = self.cursor.fetchall()
        self.print_results(results, max_rows=20)
    
    # ========================================================================
    # 4. NUTRIENT DENSITY & MACROS
    # ========================================================================
    
    def best_protein_to_calorie_ratio(self, limit: int = 10):
        """Most efficient protein per calorie"""
        self.print_section(f"9. BEST PROTEIN EFFICIENCY (highest protein per calorie) - TOP {limit}")
        
        self.cursor.execute(f"""
            SELECT 
                f.name,
                fc.name as category,
                nf.protein_g,
                nf.calories,
                ROUND((nf.protein_g / nf.calories), 4) as protein_per_calorie,
                ROUND((nf.protein_g * 4) / nf.calories * 100, 2) as protein_percent
            FROM foods f
            JOIN food_categories fc ON f.category_id = fc.category_id
            JOIN nutrition_facts nf ON f.food_id = nf.food_id
            WHERE nf.protein_g IS NOT NULL AND nf.calories > 0
            ORDER BY protein_per_calorie DESC
            LIMIT {limit}
        """)
        results = self.cursor.fetchall()
        self.print_results(results)
    
    def macronutrient_distribution(self):
        """Average macronutrient distribution by category"""
        self.print_section("10. MACRONUTRIENT DISTRIBUTION BY CATEGORY (% of calories)")
        
        self.cursor.execute("""
            SELECT 
                fc.name as category,
                ROUND(AVG((nf.protein_g * 4) / nf.calories * 100), 2) as protein_percent,
                ROUND(AVG((nf.fat_g * 9) / nf.calories * 100), 2) as fat_percent,
                ROUND(AVG((nf.carbohydrates_g * 4) / nf.calories * 100), 2) as carb_percent
            FROM food_categories fc
            LEFT JOIN foods f ON fc.category_id = f.category_id
            LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
            WHERE nf.calories > 0 AND nf.protein_g IS NOT NULL 
                AND nf.fat_g IS NOT NULL AND nf.carbohydrates_g IS NOT NULL
            GROUP BY fc.category_id, fc.name
            ORDER BY protein_percent DESC
        """)
        results = self.cursor.fetchall()
        self.print_results(results, max_rows=20)
    
    # ========================================================================
    # 5. DATA QUALITY ANALYSIS
    # ========================================================================
    
    def data_completeness(self):
        """How complete is the nutrition data"""
        self.print_section("11. DATA COMPLETENESS ANALYSIS")
        
        self.cursor.execute("""
            SELECT 
                COUNT(*) as total_records,
                ROUND(COUNT(CASE WHEN calories IS NOT NULL THEN 1 END) / COUNT(*) * 100, 2) as calories_percent,
                ROUND(COUNT(CASE WHEN protein_g IS NOT NULL THEN 1 END) / COUNT(*) * 100, 2) as protein_percent,
                ROUND(COUNT(CASE WHEN fat_g IS NOT NULL THEN 1 END) / COUNT(*) * 100, 2) as fat_percent,
                ROUND(COUNT(CASE WHEN carbohydrates_g IS NOT NULL THEN 1 END) / COUNT(*) * 100, 2) as carbs_percent,
                ROUND(COUNT(CASE WHEN fiber_g IS NOT NULL THEN 1 END) / COUNT(*) * 100, 2) as fiber_percent,
                ROUND(COUNT(CASE WHEN sodium_mg IS NOT NULL THEN 1 END) / COUNT(*) * 100, 2) as sodium_percent,
                ROUND(COUNT(CASE WHEN vitamin_c_mg IS NOT NULL THEN 1 END) / COUNT(*) * 100, 2) as vitamin_c_percent
            FROM nutrition_facts
        """)
        results = self.cursor.fetchall()
        for row in results:
            print(f"   Total Records:        {row['total_records']}")
            print(f"   Calories:             {row['calories_percent']}%")
            print(f"   Protein:              {row['protein_percent']}%")
            print(f"   Fat:                  {row['fat_percent']}%")
            print(f"   Carbohydrates:        {row['carbs_percent']}%")
            print(f"   Fiber:                {row['fiber_percent']}%")
            print(f"   Sodium:               {row['sodium_percent']}%")
            print(f"   Vitamin C:            {row['vitamin_c_percent']}%")
    
    def nutrient_ranges(self):
        """Min, max, average for key nutrients"""
        self.print_section("12. NUTRIENT RANGES (Min/Max/Average)")
        
        self.cursor.execute("""
            SELECT 
                'Calories' as nutrient,
                ROUND(MIN(calories), 2) as min_val,
                ROUND(MAX(calories), 2) as max_val,
                ROUND(AVG(calories), 2) as avg_val
            FROM nutrition_facts
            WHERE calories IS NOT NULL
            UNION ALL
            SELECT 'Protein (g)', ROUND(MIN(protein_g), 2), ROUND(MAX(protein_g), 2), ROUND(AVG(protein_g), 2)
            FROM nutrition_facts WHERE protein_g IS NOT NULL
            UNION ALL
            SELECT 'Fat (g)', ROUND(MIN(fat_g), 2), ROUND(MAX(fat_g), 2), ROUND(AVG(fat_g), 2)
            FROM nutrition_facts WHERE fat_g IS NOT NULL
            UNION ALL
            SELECT 'Carbs (g)', ROUND(MIN(carbohydrates_g), 2), ROUND(MAX(carbohydrates_g), 2), ROUND(AVG(carbohydrates_g), 2)
            FROM nutrition_facts WHERE carbohydrates_g IS NOT NULL
            UNION ALL
            SELECT 'Fiber (g)', ROUND(MIN(fiber_g), 2), ROUND(MAX(fiber_g), 2), ROUND(AVG(fiber_g), 2)
            FROM nutrition_facts WHERE fiber_g IS NOT NULL
            UNION ALL
            SELECT 'Sodium (mg)', ROUND(MIN(sodium_mg), 2), ROUND(MAX(sodium_mg), 2), ROUND(AVG(sodium_mg), 2)
            FROM nutrition_facts WHERE sodium_mg IS NOT NULL
            UNION ALL
            SELECT 'Vitamin C (mg)', ROUND(MIN(vitamin_c_mg), 2), ROUND(MAX(vitamin_c_mg), 2), ROUND(AVG(vitamin_c_mg), 2)
            FROM nutrition_facts WHERE vitamin_c_mg IS NOT NULL
        """)
        results = self.cursor.fetchall()
        self.print_results(results)
    
    # ========================================================================
    # 6. SEARCH & FILTER EXAMPLES
    # ========================================================================
    
    def search_foods(self, keyword: str, limit: int = 5):
        """Search for foods by keyword"""
        self.print_section(f"13. SEARCH: '{keyword}'")
        
        search_term = f"%{keyword}%"
        self.cursor.execute(f"""
            SELECT 
                f.name,
                fc.name as category,
                nf.calories,
                nf.protein_g,
                nf.fat_g,
                nf.carbohydrates_g
            FROM foods f
            JOIN food_categories fc ON f.category_id = fc.category_id
            LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
            WHERE f.name LIKE %s OR f.description LIKE %s
            LIMIT {limit}
        """, (search_term, search_term))
        results = self.cursor.fetchall()
        self.print_results(results)
    
    def foods_in_calorie_range(self, min_cal: int, max_cal: int, limit: int = 10):
        """Find foods in specific calorie range"""
        self.print_section(f"14. FOODS IN {min_cal}-{max_cal} CALORIE RANGE")
        
        self.cursor.execute(f"""
            SELECT 
                f.name,
                fc.name as category,
                nf.calories,
                nf.protein_g,
                nf.fat_g,
                nf.carbohydrates_g
            FROM foods f
            JOIN food_categories fc ON f.category_id = fc.category_id
            JOIN nutrition_facts nf ON f.food_id = nf.food_id
            WHERE nf.calories BETWEEN %s AND %s
            ORDER BY nf.calories
            LIMIT {limit}
        """, (min_cal, max_cal))
        results = self.cursor.fetchall()
        self.print_results(results)
    
    def low_carb_high_protein(self, limit: int = 10):
        """Find low-carb, high-protein foods"""
        self.print_section(f"15. LOW-CARB, HIGH-PROTEIN FOODS (top {limit})")
        
        self.cursor.execute(f"""
            SELECT 
                f.name,
                fc.name as category,
                nf.protein_g,
                nf.carbohydrates_g,
                nf.fat_g,
                nf.calories,
                ROUND((nf.protein_g / nf.carbohydrates_g), 2) as protein_carb_ratio
            FROM foods f
            JOIN food_categories fc ON f.category_id = fc.category_id
            JOIN nutrition_facts nf ON f.food_id = nf.food_id
            WHERE nf.protein_g IS NOT NULL AND nf.carbohydrates_g IS NOT NULL 
                AND nf.carbohydrates_g > 0 AND nf.protein_g > nf.carbohydrates_g
            ORDER BY protein_carb_ratio DESC
            LIMIT {limit}
        """)
        results = self.cursor.fetchall()
        self.print_results(results)
    
    # ========================================================================
    # RUN ALL ANALYSES
    # ========================================================================
    
    def run_all(self):
        """Run all analyses"""
        print("\n")
        print("╔" + "="*78 + "╗")
        print("║" + " "*20 + "NUTRITION DATABASE ADVANCED ANALYSIS" + " "*22 + "║")
        print("║" + " "*30 + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " "*15 + "║")
        print("╚" + "="*78 + "╝")
        
        try:
            # Overview
            self.database_overview()
            self.category_breakdown()
            
            # Extremes
            self.highest_calorie_foods(10)
            self.highest_protein_foods(10)
            self.lowest_sodium_foods(10)
            self.highest_fiber_foods(10)
            
            # Category Analysis
            self.category_nutrition_stats()
            self.category_with_most_sugar()
            
            # Nutrient Efficiency
            self.best_protein_to_calorie_ratio(10)
            self.macronutrient_distribution()
            
            # Data Quality
            self.data_completeness()
            self.nutrient_ranges()
            
            # Search Examples
            self.search_foods('chicken', 5)
            self.foods_in_calorie_range(100, 150, 10)
            self.low_carb_high_protein(10)
            
            print("\n" + "="*80)
            print("✓ Analysis complete!")
            print("="*80 + "\n")
            
        except Exception as e:
            print(f"\n❌ Error during analysis: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.close()


if __name__ == "__main__":
    analyzer = NutritionAnalyzer()
    analyzer.run_all()