#!/usr/bin/env python3
"""
Nutrition Database Web Dashboard
Share your nutrition data with clients via browser
"""

from flask import Flask, render_template, request, jsonify, send_file
import mysql.connector
from datetime import datetime
import json
import csv
from io import StringIO, BytesIO
import os

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Database configuration
DB_CONFIG = {
    'host': '82.197.82.46',
    'user': 'u280406916_nutrition',
    'password': 'Mutsokoti08@',
    'database': 'u280406916_nutrition',
    'port': 3306
}

def get_db():
    """Get database connection"""
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def index():
    """Main dashboard page"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        # Get stats
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM food_categories) as categories,
                (SELECT COUNT(*) FROM foods) as foods,
                (SELECT COUNT(*) FROM nutrition_facts) as nutrition_records
        """)
        stats = cursor.fetchone()
        
        # Get categories
        cursor.execute("SELECT category_id, name FROM food_categories ORDER BY name")
        categories = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('index.html', stats=stats, categories=categories)
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/api/foods', methods=['GET'])
def api_foods():
    """Search and filter foods"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        # Get parameters
        search = request.args.get('search', '').strip()
        category_id = request.args.get('category', '')
        min_cal = request.args.get('min_cal', '')
        max_cal = request.args.get('max_cal', '')
        page = int(request.args.get('page', 1))
        limit = 20
        offset = (page - 1) * limit
        
        # Build query
        query = """
            SELECT 
                f.food_id,
                f.name,
                fc.name as category,
                nf.calories,
                nf.protein_g,
                nf.fat_g,
                nf.carbohydrates_g,
                nf.fiber_g,
                nf.sodium_mg,
                nf.sugar_g
            FROM foods f
            JOIN food_categories fc ON f.category_id = fc.category_id
            LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
            WHERE 1=1
        """
        
        params = []
        
        if search:
            query += " AND (f.name LIKE %s OR f.description LIKE %s)"
            params.extend([f"%{search}%", f"%{search}%"])
        
        if category_id:
            query += " AND fc.category_id = %s"
            params.append(category_id)
        
        if min_cal:
            query += " AND nf.calories >= %s"
            params.append(min_cal)
        
        if max_cal:
            query += " AND nf.calories <= %s"
            params.append(max_cal)
        
        # Get total count (without ORDER BY)
        count_query = query.replace(
            "SELECT f.food_id, f.name, fc.name as category, nf.calories, nf.protein_g, nf.fat_g, nf.carbohydrates_g, nf.fiber_g, nf.sodium_mg, nf.sugar_g",
            "SELECT COUNT(*) as total"
        )
        cursor.execute(count_query, params)
        total = cursor.fetchone()['total']
        
        # Get results with ORDER BY and LIMIT
        query += " ORDER BY f.name"
        query += f" LIMIT {limit} OFFSET {offset}"
        cursor.execute(query, params)
        foods = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'foods': foods,
            'total': total,
            'page': page,
            'limit': limit,
            'pages': (total + limit - 1) // limit
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/food/<int:food_id>')
def api_food_details(food_id):
    """Get detailed nutrition info for a food"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                f.food_id,
                f.name,
                f.description,
                f.brand,
                fc.name as category,
                f.serving_size,
                f.serving_weight_g,
                nf.*
            FROM foods f
            JOIN food_categories fc ON f.category_id = fc.category_id
            LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
            WHERE f.food_id = %s
        """, (food_id,))
        
        food = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not food:
            return jsonify({'success': False, 'error': 'Food not found'}), 404
        
        return jsonify({'success': True, 'food': food})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/categories')
def api_categories():
    """Get all categories"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                fc.category_id,
                fc.name,
                COUNT(f.food_id) as food_count
            FROM food_categories fc
            LEFT JOIN foods f ON fc.category_id = f.category_id
            GROUP BY fc.category_id, fc.name
            ORDER BY fc.name
        """)
        
        categories = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, 'categories': categories})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/category-stats/<int:category_id>')
def api_category_stats(category_id):
    """Get category nutrition statistics"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                fc.name as category,
                COUNT(nf.nutrition_id) as total_foods,
                ROUND(AVG(nf.calories), 2) as avg_calories,
                ROUND(AVG(nf.protein_g), 2) as avg_protein,
                ROUND(AVG(nf.fat_g), 2) as avg_fat,
                ROUND(AVG(nf.carbohydrates_g), 2) as avg_carbs,
                ROUND(AVG(nf.fiber_g), 2) as avg_fiber,
                ROUND(MAX(nf.calories), 2) as max_calories,
                ROUND(MIN(nf.calories), 2) as min_calories
            FROM food_categories fc
            LEFT JOIN foods f ON fc.category_id = f.category_id
            LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
            WHERE fc.category_id = %s AND nf.calories IS NOT NULL
            GROUP BY fc.category_id, fc.name
        """, (category_id,))
        
        stats = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not stats:
            return jsonify({'success': False, 'error': 'Category not found'}), 404
        
        return jsonify({'success': True, 'stats': stats})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export-csv', methods=['GET'])
def export_csv():
    """Export search results as CSV"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        search = request.args.get('search', '').strip()
        category_id = request.args.get('category', '')
        
        query = """
            SELECT 
                f.name,
                fc.name as category,
                nf.calories,
                nf.protein_g,
                nf.fat_g,
                nf.carbohydrates_g,
                nf.fiber_g,
                nf.sugar_g,
                nf.sodium_mg,
                nf.cholesterol_mg,
                nf.calcium_mg,
                nf.iron_mg,
                nf.vitamin_c_mg
            FROM foods f
            JOIN food_categories fc ON f.category_id = fc.category_id
            LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
            WHERE 1=1
        """
        
        params = []
        
        if search:
            query += " AND (f.name LIKE %s OR f.description LIKE %s)"
            params.extend([f"%{search}%", f"%{search}%"])
        
        if category_id:
            query += " AND fc.category_id = %s"
            params.append(category_id)
        
        query += " ORDER BY f.name LIMIT 5000"
        
        cursor.execute(query, params)
        foods = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Create CSV
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=foods[0].keys() if foods else [])
        writer.writeheader()
        writer.writerows(foods)
        
        output.seek(0)
        return send_file(
            BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'nutrition_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/api/top-foods', methods=['GET'])
def api_top_foods():
    """Get top foods by various metrics"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        metric = request.args.get('metric', 'calories')
        limit = int(request.args.get('limit', 10))
        
        if metric == 'calories':
            query = """
                SELECT f.name, fc.name as category, nf.calories
                FROM foods f
                JOIN food_categories fc ON f.category_id = fc.category_id
                LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
                WHERE nf.calories IS NOT NULL
                ORDER BY nf.calories DESC
                LIMIT %s
            """
        elif metric == 'protein':
            query = """
                SELECT f.name, fc.name as category, nf.protein_g
                FROM foods f
                JOIN food_categories fc ON f.category_id = fc.category_id
                LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
                WHERE nf.protein_g IS NOT NULL
                ORDER BY nf.protein_g DESC
                LIMIT %s
            """
        elif metric == 'fiber':
            query = """
                SELECT f.name, fc.name as category, nf.fiber_g
                FROM foods f
                JOIN food_categories fc ON f.category_id = fc.category_id
                LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
                WHERE nf.fiber_g IS NOT NULL
                ORDER BY nf.fiber_g DESC
                LIMIT %s
            """
        else:
            return jsonify({'success': False, 'error': 'Invalid metric'}), 400
        
        cursor.execute(query, (limit,))
        foods = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, 'foods': foods})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Development
    app.run(debug=True, host='0.0.0.0', port=5000)