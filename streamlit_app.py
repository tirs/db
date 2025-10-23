#!/usr/bin/env python3
"""
Nutrition Database Streamlit Dashboard
Professional nutrition data for clients
"""

import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO
import csv
import json

# Page config
st.set_page_config(
    page_title="Nutrition Database",
    page_icon="leaf",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'meal_plan' not in st.session_state:
    st.session_state.meal_plan = {'breakfast': [], 'lunch': [], 'dinner': [], 'snacks': []}
if 'comparison_foods' not in st.session_state:
    st.session_state.comparison_foods = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Database configuration
def get_db_config():
    """Get database config from secrets or environment"""
    try:
        return {
            'host': st.secrets["database"]["host"],
            'user': st.secrets["database"]["user"],
            'password': st.secrets["database"]["password"],
            'database': st.secrets["database"]["database"],
            'port': st.secrets["database"]["port"]
        }
    except:
        return {
            'host': '82.197.82.46',
            'user': 'u280406916_nutrition',
            'password': 'Mutsokoti08@',
            'database': 'u280406916_nutrition',
            'port': 3306
        }

def get_db_connection():
    """Get fresh database connection (no caching to prevent timeouts)"""
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        if not conn.is_connected():
            conn.reconnect()
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {str(e)}")
        st.stop()

@st.cache_data(ttl=3600)
def get_categories():
    """Get all food categories"""
    conn = get_db_connection()
    try:
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
        return categories
    finally:
        if conn.is_connected():
            conn.close()

@st.cache_data(ttl=3600)
def get_stats():
    """Get database statistics"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM food_categories) as categories,
                (SELECT COUNT(*) FROM foods) as foods,
                (SELECT COUNT(*) FROM nutrition_facts) as nutrition_records,
                (SELECT MAX(created_at) FROM foods) as last_updated
        """)
        stats = cursor.fetchone()
        cursor.close()
        return stats
    finally:
        if conn.is_connected():
            conn.close()

def search_foods(search_term='', category_id='', min_cal='', max_cal='', min_protein='', max_protein='', min_fiber='', max_fiber='', min_sodium='', max_sodium=''):
    """Search for foods with advanced filters"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                f.food_id,
                f.name,
                f.brand,
                f.serving_size,
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
        
        if search_term:
            query += " AND (f.name LIKE %s OR f.description LIKE %s)"
            params.extend([f"%{search_term}%", f"%{search_term}%"])
        
        if category_id:
            query += " AND fc.category_id = %s"
            params.append(category_id)
        
        if min_cal:
            query += " AND nf.calories >= %s"
            params.append(float(min_cal))
        
        if max_cal:
            query += " AND nf.calories <= %s"
            params.append(float(max_cal))
            
        if min_protein:
            query += " AND nf.protein_g >= %s"
            params.append(float(min_protein))
            
        if max_protein:
            query += " AND nf.protein_g <= %s"
            params.append(float(max_protein))
            
        if min_fiber:
            query += " AND nf.fiber_g >= %s"
            params.append(float(min_fiber))
            
        if max_fiber:
            query += " AND nf.fiber_g <= %s"
            params.append(float(max_fiber))
            
        if min_sodium:
            query += " AND nf.sodium_mg >= %s"
            params.append(float(min_sodium))
            
        if max_sodium:
            query += " AND nf.sodium_mg <= %s"
            params.append(float(max_sodium))
        
        query += " ORDER BY f.name LIMIT 500"
        
        cursor.execute(query, params)
        foods = cursor.fetchall()
        cursor.close()
        
        return foods
    finally:
        if conn.is_connected():
            conn.close()

def get_similar_foods(search_term, limit=5):
    """Get similar foods for search suggestions"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT f.name FROM foods f
            WHERE f.name LIKE %s
            LIMIT %s
        """, (f"%{search_term[0]}%", limit))
        results = cursor.fetchall()
        cursor.close()
        return [r['name'] for r in results]
    finally:
        if conn.is_connected():
            conn.close()

@st.cache_data(ttl=3600)
def get_category_stats():
    """Get category statistics"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                fc.name as category,
                COUNT(nf.nutrition_id) as total_foods,
                ROUND(AVG(nf.calories), 2) as avg_calories,
                ROUND(AVG(nf.protein_g), 2) as avg_protein,
                ROUND(AVG(nf.fat_g), 2) as avg_fat,
                ROUND(AVG(nf.carbohydrates_g), 2) as avg_carbs,
                ROUND(AVG(nf.fiber_g), 2) as avg_fiber
            FROM food_categories fc
            LEFT JOIN foods f ON fc.category_id = f.category_id
            LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
            WHERE nf.calories IS NOT NULL
            GROUP BY fc.category_id, fc.name
            ORDER BY avg_calories DESC
        """)
        stats = cursor.fetchall()
        cursor.close()
        return stats
    finally:
        if conn.is_connected():
            conn.close()

@st.cache_data(ttl=3600)
def get_top_foods(metric='calories', category='', limit=10):
    """Get top foods by metric"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        
        if metric == 'calories':
            query = """
                SELECT f.food_id, f.name, fc.name as category, nf.calories as value, f.brand
                FROM foods f
                JOIN food_categories fc ON f.category_id = fc.category_id
                LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
                WHERE nf.calories IS NOT NULL
            """
        elif metric == 'protein':
            query = """
                SELECT f.food_id, f.name, fc.name as category, nf.protein_g as value, f.brand
                FROM foods f
                JOIN food_categories fc ON f.category_id = fc.category_id
                LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
                WHERE nf.protein_g IS NOT NULL
            """
        elif metric == 'fiber':
            query = """
                SELECT f.food_id, f.name, fc.name as category, nf.fiber_g as value, f.brand
                FROM foods f
                JOIN food_categories fc ON f.category_id = fc.category_id
                LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
                WHERE nf.fiber_g IS NOT NULL
            """
        elif metric == 'protein_efficiency':
            query = """
                SELECT f.food_id, f.name, fc.name as category, 
                       ROUND((nf.protein_g / nf.calories) * 4, 3) as value, f.brand
                FROM foods f
                JOIN food_categories fc ON f.category_id = fc.category_id
                LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
                WHERE nf.calories IS NOT NULL AND nf.protein_g IS NOT NULL
            """
        elif metric == 'lowest_calorie':
            query = """
                SELECT f.food_id, f.name, fc.name as category, nf.calories as value, f.brand
                FROM foods f
                JOIN food_categories fc ON f.category_id = fc.category_id
                LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
                WHERE nf.calories IS NOT NULL
            """
        else:
            return []
        
        if category:
            query += f" AND fc.name = %s"
        
        if metric == 'lowest_calorie':
            query += " ORDER BY value ASC"
        else:
            query += " ORDER BY value DESC"
        
        query += f" LIMIT %s"
        
        if category:
            cursor.execute(query, (category, limit))
        else:
            cursor.execute(query, (limit,))
            
        foods = cursor.fetchall()
        cursor.close()
        return foods
    finally:
        if conn.is_connected():
            conn.close()

@st.cache_data(ttl=3600)
def get_overall_stats():
    """Get overall nutrition statistics"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                ROUND(AVG(calories), 2) as avg_calories,
                ROUND(AVG(protein_g), 2) as avg_protein,
                ROUND(AVG(fat_g), 2) as avg_fat,
                ROUND(AVG(carbohydrates_g), 2) as avg_carbs,
                ROUND(AVG(fiber_g), 2) as avg_fiber,
                ROUND(AVG(sodium_mg), 2) as avg_sodium,
                ROUND(AVG(sugar_g), 2) as avg_sugar
            FROM nutrition_facts
            WHERE calories IS NOT NULL
        """)
        stats = cursor.fetchone()
        cursor.close()
        return stats
    finally:
        if conn.is_connected():
            conn.close()

@st.cache_data(ttl=3600)
def get_extended_stats():
    """Get extended nutrition statistics with min/max/median"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                COUNT(*) as total_foods,
                MIN(calories) as min_calories,
                MAX(calories) as max_calories,
                ROUND(AVG(calories), 2) as avg_calories,
                MIN(protein_g) as min_protein,
                MAX(protein_g) as max_protein,
                ROUND(AVG(protein_g), 2) as avg_protein,
                MIN(fat_g) as min_fat,
                MAX(fat_g) as max_fat,
                ROUND(AVG(fat_g), 2) as avg_fat,
                MIN(carbohydrates_g) as min_carbs,
                MAX(carbohydrates_g) as max_carbs,
                ROUND(AVG(carbohydrates_g), 2) as avg_carbs,
                MIN(fiber_g) as min_fiber,
                MAX(fiber_g) as max_fiber,
                ROUND(AVG(fiber_g), 2) as avg_fiber,
                MIN(sodium_mg) as min_sodium,
                MAX(sodium_mg) as max_sodium,
                ROUND(AVG(sodium_mg), 2) as avg_sodium,
                MIN(sugar_g) as min_sugar,
                MAX(sugar_g) as max_sugar,
                ROUND(AVG(sugar_g), 2) as avg_sugar
            FROM nutrition_facts
            WHERE calories IS NOT NULL
        """)
        stats = cursor.fetchone()
        cursor.close()
        return stats
    finally:
        if conn.is_connected():
            conn.close()

@st.cache_data(ttl=3600)
def get_calorie_distribution():
    """Get calorie distribution for histogram"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT calories
            FROM nutrition_facts
            WHERE calories IS NOT NULL
            ORDER BY calories
        """)
        data = cursor.fetchall()
        cursor.close()
        return [row['calories'] for row in data]
    finally:
        if conn.is_connected():
            conn.close()

@st.cache_data(ttl=3600)
def get_nutrition_by_category_detailed():
    """Get detailed nutrition stats by category"""
    conn = get_db_connection()
    try:
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
                ROUND(AVG(nf.sodium_mg), 2) as avg_sodium,
                ROUND(AVG(nf.sugar_g), 2) as avg_sugar,
                ROUND(AVG(nf.protein_g) / AVG(nf.calories) * 4, 4) as protein_ratio,
                ROUND(AVG(nf.fiber_g) / AVG(nf.sugar_g), 4) as fiber_sugar_ratio
            FROM food_categories fc
            LEFT JOIN foods f ON fc.category_id = f.category_id
            LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
            WHERE nf.calories IS NOT NULL
            GROUP BY fc.category_id, fc.name
            ORDER BY avg_calories DESC
        """)
        stats = cursor.fetchall()
        cursor.close()
        return stats
    finally:
        if conn.is_connected():
            conn.close()

def get_food_details(food_id):
    """Get detailed nutrition info for a food"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                f.food_id,
                f.name,
                f.brand,
                f.serving_size,
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
            WHERE f.food_id = %s
        """, (food_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    finally:
        if conn.is_connected():
            conn.close()

# Theme CSS
if st.session_state.dark_mode:
    st.markdown("""
        <style>
        .metric-card { background-color: #1e1e1e; padding: 20px; border-radius: 10px; text-align: center; }
        .metric-value { font-size: 2.5em; font-weight: bold; color: #64B5F6; }
        .metric-label { font-size: 0.9em; color: #aaa; margin-top: 10px; }
        body { background-color: #0d1117; color: #e1e4e8; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .metric-card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; }
        .metric-value { font-size: 2.5em; font-weight: bold; color: #6366f1; }
        .metric-label { font-size: 0.9em; color: #666; margin-top: 10px; }
        </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Settings & Tools")
    
    # Dark mode toggle
    st.session_state.dark_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode)
    
    # Favorites section
    st.markdown("### Bookmarks")
    if st.session_state.favorites:
        for fav in st.session_state.favorites:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.caption(fav['name'])
            with col2:
                if st.button("x", key=f"remove_fav_{fav['food_id']}"):
                    st.session_state.favorites = [f for f in st.session_state.favorites if f['food_id'] != fav['food_id']]
                    st.rerun()
    else:
        st.caption("No bookmarks yet")
    
    st.divider()
    
    # Quick presets
    st.markdown("### Search Presets")
    preset = st.radio("Quick Filters:", 
        ["None", "High Protein (>20g)", "Low Calorie (<100)", "High Fiber (>5g)"],
        label_visibility="collapsed")
    
    st.divider()
    
    # Keyboard shortcuts help
    st.markdown("### Keyboard Shortcuts")
    st.caption("Press 'S' to focus search")
    st.caption("Press 'C' to open comparison tool")
    st.caption("Press 'M' to open meal planner")
    
    st.divider()
    
    # Database info
    stats = get_stats()
    st.markdown("### Database Information")
    st.caption(f"Total Foods: {stats['foods']:,}")
    st.caption(f"Categories: {stats['categories']}")
    if stats.get('last_updated'):
        st.caption(f"Last Updated: {stats['last_updated'].strftime('%Y-%m-%d')}")
    st.caption("Powered by USDA FoodData Central")

# Header
st.markdown("# Nutrition Database Dashboard")
st.markdown("Professional nutrition data for your clients")

# Stats
stats = get_stats()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Categories", stats['categories'])
with col2:
    st.metric("Foods", f"{stats['foods']:,}")
with col3:
    st.metric("Records", f"{stats['nutrition_records']:,}")
with col4:
    st.metric("Last Updated", stats.get('last_updated', 'N/A').strftime('%Y-%m-%d') if stats.get('last_updated') else 'N/A')

st.divider()

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Search", "Browse", "Analysis", "Top Foods", "Comparison", "Meal Planner", "Bookmarks"])

# TAB 1: SEARCH
with tab1:
    st.subheader("Search and Filter Foods")
    
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("Food name", placeholder="e.g., chicken, apple, salmon...")
    with col2:
        categories = get_categories()
        cat_options = {cat['name']: cat['category_id'] for cat in categories}
        cat_options = {"All Categories": ""} | cat_options
        selected_category = st.selectbox("Category", list(cat_options.keys()))
        category_id = cat_options[selected_category]
    
    # Apply preset if selected
    if preset == "High Protein (>20g)":
        preset_min_protein = 20
        preset_max_protein = 1000
        preset_min_cal = 0
        preset_max_cal = 1000
        preset_min_fiber = 0
        preset_max_fiber = 100
        preset_min_sodium = 0
        preset_max_sodium = 10000
    elif preset == "Low Calorie (<100)":
        preset_min_protein = 0
        preset_max_protein = 100
        preset_min_cal = 0
        preset_max_cal = 100
        preset_min_fiber = 0
        preset_max_fiber = 100
        preset_min_sodium = 0
        preset_max_sodium = 10000
    elif preset == "High Fiber (>5g)":
        preset_min_protein = 0
        preset_max_protein = 100
        preset_min_cal = 0
        preset_max_cal = 1000
        preset_min_fiber = 5
        preset_max_fiber = 100
        preset_min_sodium = 0
        preset_max_sodium = 10000
    else:
        preset_min_protein = 0
        preset_max_protein = 100
        preset_min_cal = 0
        preset_max_cal = 1000
        preset_min_fiber = 0
        preset_max_fiber = 100
        preset_min_sodium = 0
        preset_max_sodium = 10000
    
    with st.expander("Advanced Filters"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Calories**")
            min_cal = st.slider("Min Calories", 0, 1000, preset_min_cal, key="cal_min")
            max_cal = st.slider("Max Calories", 0, 1000, preset_max_cal, key="cal_max")
        with col2:
            st.markdown("**Protein (g)**")
            min_protein = st.slider("Min Protein", 0, 100, preset_min_protein, key="protein_min")
            max_protein = st.slider("Max Protein", 0, 100, preset_max_protein, key="protein_max")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Fiber (g)**")
            min_fiber = st.slider("Min Fiber", 0, 100, preset_min_fiber, key="fiber_min")
            max_fiber = st.slider("Max Fiber", 0, 100, preset_max_fiber, key="fiber_max")
        with col2:
            st.markdown("**Sodium (mg)**")
            min_sodium = st.slider("Min Sodium", 0, 5000, preset_min_sodium, key="sodium_min")
            max_sodium = st.slider("Max Sodium", 0, 5000, preset_max_sodium, key="sodium_max")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Search", use_container_width=True):
            st.session_state.search_triggered = True
    
    if st.session_state.get('search_triggered', False) or search_term or category_id:
        foods = search_foods(search_term, category_id, 
                           min_cal if min_cal > 0 else '', 
                           max_cal if max_cal > 0 else '',
                           min_protein if min_protein > 0 else '',
                           max_protein if max_protein < 100 else '',
                           min_fiber if min_fiber > 0 else '',
                           max_fiber if max_fiber < 100 else '',
                           min_sodium if min_sodium > 0 else '',
                           max_sodium if max_sodium < 5000 else '')
        
        if foods:
            st.success(f"Found {len(foods)} foods")
            
            df = pd.DataFrame(foods)
            df['calories'] = df['calories'].fillna(0).astype(float)
            df['protein_g'] = df['protein_g'].fillna(0).astype(float)
            df['fat_g'] = df['fat_g'].fillna(0).astype(float)
            df['carbohydrates_g'] = df['carbohydrates_g'].fillna(0).astype(float)
            df['fiber_g'] = df['fiber_g'].fillna(0).astype(float)
            
            display_df = df[['name', 'category', 'calories', 'protein_g', 'fat_g', 'carbohydrates_g', 'fiber_g']].copy()
            display_df.columns = ['Food Name', 'Category', 'Calories', 'Protein (g)', 'Fat (g)', 'Carbs (g)', 'Fiber (g)']
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Add to comparison
            for idx, food in enumerate(foods[:3]):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col2:
                    if st.button("Compare", key=f"comp_{idx}"):
                        st.session_state.comparison_foods.append(food)
                with col3:
                    if st.button("Bookmark", key=f"fav_{idx}"):
                        st.session_state.favorites.append({
                            'food_id': food['food_id'],
                            'name': food['name']
                        })
                        st.success("Added to bookmarks!")
            
            # CSV export
            csv_buffer = StringIO()
            display_df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="Download CSV",
                data=csv_buffer.getvalue(),
                file_name=f"nutrition_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.warning("No foods found")
            if search_term:
                suggestions = get_similar_foods(search_term, 5)
                if suggestions:
                    st.info("Did you mean:")
                    for suggestion in suggestions:
                        st.caption(f"- {suggestion}")

# TAB 2: BROWSE
with tab2:
    st.subheader("Browse by Category")
    
    categories = get_categories()
    cols = st.columns(3)
    
    for idx, cat in enumerate(categories):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {cat['name']}")
                st.metric("Foods", cat['food_count'])
                if st.button("View Details", key=f"cat_{cat['category_id']}", use_container_width=True):
                    st.session_state.selected_category = cat['category_id']
    
    st.divider()
    
    if st.session_state.get('selected_category'):
        selected_cat_id = st.session_state.selected_category
        selected_cat_name = next((cat['name'] for cat in categories if cat['category_id'] == selected_cat_id), "Unknown")
        
        st.markdown(f"## {selected_cat_name} - All Foods")
        
        foods = search_foods('', selected_cat_id, '', '', '', '', '', '', '', '')
        
        if foods:
            df = pd.DataFrame(foods)
            df['calories'] = df['calories'].fillna(0).astype(float)
            df['protein_g'] = df['protein_g'].fillna(0).astype(float)
            df['fat_g'] = df['fat_g'].fillna(0).astype(float)
            df['carbohydrates_g'] = df['carbohydrates_g'].fillna(0).astype(float)
            
            st.success(f"Found {len(foods)} foods in this category")
            
            display_df = df[['name', 'brand', 'calories', 'protein_g', 'fat_g', 'carbohydrates_g', 'fiber_g']].copy()
            display_df.columns = ['Food Name', 'Brand', 'Calories', 'Protein (g)', 'Fat (g)', 'Carbs (g)', 'Fiber (g)']
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            csv_buffer = StringIO()
            display_df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="Download CSV",
                data=csv_buffer.getvalue(),
                file_name=f"{selected_cat_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info(f"No foods available in {selected_cat_name} at this time.")

# TAB 3: ANALYSIS
with tab3:
    st.subheader("Comprehensive Nutrition Analysis")
    
    extended_stats = get_extended_stats()
    overall_stats = get_overall_stats()
    df_detailed = pd.DataFrame(get_nutrition_by_category_detailed())
    calorie_dist = get_calorie_distribution()
    
    st.markdown("## Key Metrics Overview")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Avg Calories", f"{overall_stats['avg_calories']:.0f}", 
                  f"Min: {extended_stats['min_calories']:.0f} | Max: {extended_stats['max_calories']:.0f}")
    with col2:
        st.metric("Avg Protein", f"{overall_stats['avg_protein']:.1f}g",
                  f"Min: {extended_stats['min_protein']:.1f}g | Max: {extended_stats['max_protein']:.1f}g")
    with col3:
        st.metric("Avg Fat", f"{overall_stats['avg_fat']:.1f}g",
                  f"Min: {extended_stats['min_fat']:.1f}g | Max: {extended_stats['max_fat']:.1f}g")
    with col4:
        st.metric("Avg Carbs", f"{overall_stats['avg_carbs']:.1f}g",
                  f"Min: {extended_stats['min_carbs']:.1f}g | Max: {extended_stats['max_carbs']:.1f}g")
    with col5:
        st.metric("Avg Fiber", f"{overall_stats['avg_fiber']:.1f}g",
                  f"Min: {extended_stats['min_fiber']:.1f}g | Max: {extended_stats['max_fiber']:.1f}g")
    with col6:
        st.metric("Avg Sodium", f"{overall_stats['avg_sodium']:.0f}mg",
                  f"Min: {extended_stats['min_sodium']:.0f}mg | Max: {extended_stats['max_sodium']:.0f}mg")
    
    st.metric("Avg Sugar", f"{overall_stats['avg_sugar']:.1f}g",
              f"Min: {extended_stats['min_sugar']:.1f}g | Max: {extended_stats['max_sugar']:.1f}g")
    
    st.divider()
    
    st.markdown("## Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Calorie Distribution")
        fig = go.Figure(data=[go.Histogram(x=calorie_dist, nbinsx=50, 
                                           marker_color='#667eea',
                                           opacity=0.7)])
        fig.update_layout(
            xaxis_title="Calories per Serving",
            yaxis_title="Number of Foods",
            height=400,
            showlegend=False,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Macronutrient Distribution (Avg)")
        macro_data = {
            'Macronutrient': ['Protein', 'Fat', 'Carbs'],
            'Grams': [
                overall_stats['avg_protein'],
                overall_stats['avg_fat'],
                overall_stats['avg_carbs']
            ]
        }
        df_macro = pd.DataFrame(macro_data)
        fig = px.pie(df_macro, values='Grams', names='Macronutrient',
                     color_discrete_sequence=['#FF6B6B', '#FFA07A', '#4ECDC4'],
                     hole=0.3)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    st.markdown("## Category Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Average Calories by Category")
        fig = px.bar(df_detailed, x='category', y='avg_calories',
                     labels={'category': 'Category', 'avg_calories': 'Avg Calories'},
                     color='avg_calories', color_continuous_scale='Viridis',
                     text='avg_calories')
        fig.update_traces(textposition='auto')
        fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Average Protein by Category")
        fig = px.bar(df_detailed, x='category', y='avg_protein',
                     labels={'category': 'Category', 'avg_protein': 'Avg Protein (g)'},
                     color='avg_protein', color_continuous_scale='Blues',
                     text='avg_protein')
        fig.update_traces(textposition='auto')
        fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Average Fiber by Category")
        fig = px.bar(df_detailed, x='category', y='avg_fiber',
                     labels={'category': 'Category', 'avg_fiber': 'Avg Fiber (g)'},
                     color='avg_fiber', color_continuous_scale='Greens',
                     text='avg_fiber')
        fig.update_traces(textposition='auto')
        fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Average Sodium by Category")
        fig = px.bar(df_detailed, x='category', y='avg_sodium',
                     labels={'category': 'Category', 'avg_sodium': 'Avg Sodium (mg)'},
                     color='avg_sodium', color_continuous_scale='Reds',
                     text='avg_sodium')
        fig.update_traces(textposition='auto')
        fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    st.markdown("## Nutrition Quality Scores by Category")
    st.markdown("*Protein Efficiency: Higher = More protein per calorie | Health Score: Higher = Healthier*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Protein Efficiency (g per calorie)")
        fig = px.bar(df_detailed.sort_values('protein_ratio', ascending=False), 
                     x='category', y='protein_ratio',
                     labels={'category': 'Category', 'protein_ratio': 'Protein/Calorie Ratio'},
                     color='protein_ratio', color_continuous_scale='Reds',
                     text='protein_ratio')
        fig.update_traces(textposition='auto', texttemplate='%{y:.3f}')
        fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Health Score (Fiber-to-Sugar Ratio)")
        fig = px.bar(df_detailed.sort_values('fiber_sugar_ratio', ascending=False),
                     x='category', y='fiber_sugar_ratio',
                     labels={'category': 'Category', 'fiber_sugar_ratio': 'Fiber/Sugar Ratio'},
                     color='fiber_sugar_ratio', color_continuous_scale='Greens',
                     text='fiber_sugar_ratio')
        fig.update_traces(textposition='auto', texttemplate='%{y:.3f}')
        fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    st.markdown("## Complete Category Nutrition Summary")
    
    summary_df = df_detailed.copy()
    summary_df = summary_df.round(2)
    
    display_cols = {
        'category': 'Category',
        'total_foods': 'Foods',
        'avg_calories': 'Avg Cal',
        'avg_protein': 'Avg Protein (g)',
        'avg_fat': 'Avg Fat (g)',
        'avg_carbs': 'Avg Carbs (g)',
        'avg_fiber': 'Avg Fiber (g)',
        'avg_sodium': 'Avg Na (mg)',
        'avg_sugar': 'Avg Sugar (g)',
        'protein_ratio': 'Protein Ratio',
        'fiber_sugar_ratio': 'Fiber/Sugar'
    }
    
    summary_df = summary_df.rename(columns=display_cols)
    summary_df = summary_df[list(display_cols.values())]
    
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    csv_buffer = StringIO()
    summary_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="Download Analysis Summary (CSV)",
        data=csv_buffer.getvalue(),
        file_name=f"nutrition_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# TAB 4: TOP FOODS
with tab4:
    st.subheader("Top Foods Rankings")
    
    col1, col2 = st.columns(2)
    with col1:
        metric_type = st.radio("Select Metric:", ["Highest Calories", "Highest Protein", "Highest Fiber", "Protein Efficiency", "Lowest Calorie"], horizontal=False)
    with col2:
        categories = get_categories()
        cat_options = {cat['name']: cat['name'] for cat in categories}
        cat_options = {"All Categories": ""} | cat_options
        selected_top_category = st.selectbox("Filter by Category", list(cat_options.keys()), key="top_cat")
    
    metric_map = {
        "Highest Calories": "calories",
        "Highest Protein": "protein",
        "Highest Fiber": "fiber",
        "Protein Efficiency": "protein_efficiency",
        "Lowest Calorie": "lowest_calorie"
    }
    
    top_foods_data = get_top_foods(metric_map[metric_type], cat_options[selected_top_category], 15)
    
    if top_foods_data:
        df_top = pd.DataFrame(top_foods_data)
        
        for idx, (i, row) in enumerate(df_top.iterrows(), 1):
            with st.container(border=True):
                col1, col2, col3 = st.columns([0.5, 3, 1])
                with col1:
                    st.markdown(f"### #{idx}")
                with col2:
                    st.markdown(f"**{row['name']}**")
                    st.caption(f"{row['category']} | {row.get('brand', 'N/A')}")
                with col3:
                    st.metric("Value", f"{row['value']:.1f}")
    else:
        st.info("No top foods data available for selected criteria")

# TAB 5: FOOD COMPARISON
with tab5:
    st.subheader("Compare Foods Side-by-Side")
    
    st.markdown("### Add Foods to Compare")
    
    col1, col2 = st.columns(2)
    with col1:
        search_for_comp = st.text_input("Search food to add", key="comp_search")
    with col2:
        if st.button("Add Food"):
            if search_for_comp:
                foods = search_foods(search_for_comp, '', '', '', '', '', '', '', '', '')
                if foods:
                    st.session_state.comparison_foods.append(foods[0])
                    st.success(f"Added {foods[0]['name']} to comparison")
                    st.rerun()
    
    if st.session_state.comparison_foods:
        st.markdown("### Selected Foods")
        
        comp_foods = st.session_state.comparison_foods
        
        for idx, food in enumerate(comp_foods):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.caption(f"{food['name']} ({food.get('brand', 'N/A')})")
            with col2:
                if st.button("Remove", key=f"remove_comp_{idx}"):
                    st.session_state.comparison_foods.pop(idx)
                    st.rerun()
        
        if len(comp_foods) >= 2:
            st.divider()
            st.markdown("### Comparison Results")
            
            comp_data = {
                'Nutrient': ['Calories', 'Protein (g)', 'Fat (g)', 'Carbs (g)', 'Fiber (g)', 'Sodium (mg)', 'Sugar (g)']
            }
            
            for food in comp_foods:
                comp_data[food['name']] = [
                    f"{food['calories']:.0f}",
                    f"{food['protein_g']:.1f}",
                    f"{food['fat_g']:.1f}",
                    f"{food['carbohydrates_g']:.1f}",
                    f"{food['fiber_g']:.1f}",
                    f"{food['sodium_mg']:.0f}",
                    f"{food['sugar_g']:.1f}"
                ]
            
            df_comp = pd.DataFrame(comp_data)
            st.dataframe(df_comp, use_container_width=True, hide_index=True)
            
            # Radar chart comparison
            if len(comp_foods) <= 3:
                fig = go.Figure()
                
                nutrients = ['Calories', 'Protein', 'Fat', 'Carbs', 'Fiber', 'Sodium', 'Sugar']
                
                for food in comp_foods:
                    values = [
                        food['calories'],
                        food['protein_g'] * 20,
                        food['fat_g'] * 20,
                        food['carbohydrates_g'] * 20,
                        food['fiber_g'] * 20,
                        food['sodium_mg'] / 10,
                        food['sugar_g'] * 20
                    ]
                    
                    fig.add_trace(go.Scatterpolar(
                        r=values,
                        theta=nutrients,
                        fill='toself',
                        name=food['name']
                    ))
                
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add at least 2 foods to see comparison charts")
    else:
        st.info("No foods selected yet. Search and add foods from other tabs or search above.")

# TAB 6: MEAL PLANNER
with tab6:
    st.subheader("Daily Meal Planner")
    
    meal_type = st.radio("Select Meal Type:", ["Breakfast", "Lunch", "Dinner", "Snacks"], horizontal=True)
    meal_key = meal_type.lower()
    
    col1, col2 = st.columns(2)
    with col1:
        meal_search = st.text_input(f"Add food to {meal_type}", key=f"meal_search_{meal_key}")
    with col2:
        if st.button(f"Add to {meal_type}"):
            if meal_search:
                foods = search_foods(meal_search, '', '', '', '', '', '', '', '', '')
                if foods:
                    st.session_state.meal_plan[meal_key].append(foods[0])
                    st.success(f"Added {foods[0]['name']}")
                    st.rerun()
    
    st.divider()
    
    st.markdown("### Your Daily Plan")
    
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    total_fiber = 0
    total_sodium = 0
    total_sugar = 0
    
    meal_order = ['breakfast', 'lunch', 'dinner', 'snacks']
    
    for meal in meal_order:
        with st.expander(f"{meal.capitalize()} ({len(st.session_state.meal_plan[meal])} items)"):
            if st.session_state.meal_plan[meal]:
                for idx, food in enumerate(st.session_state.meal_plan[meal]):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.caption(f"{food['name']} - {food['calories']:.0f} cal, {food['protein_g']:.1f}g protein")
                    with col2:
                        if st.button("x", key=f"remove_meal_{meal}_{idx}"):
                            st.session_state.meal_plan[meal].pop(idx)
                            st.rerun()
                    
                    total_calories += food['calories']
                    total_protein += food['protein_g']
                    total_carbs += food['carbohydrates_g']
                    total_fat += food['fat_g']
                    total_fiber += food['fiber_g']
                    total_sodium += food['sodium_mg']
                    total_sugar += food['sugar_g']
            else:
                st.caption("No foods added")
    
    st.divider()
    
    st.markdown("### Daily Totals")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Calories", f"{total_calories:.0f}")
    with col2:
        st.metric("Protein (g)", f"{total_protein:.1f}")
    with col3:
        st.metric("Carbs (g)", f"{total_carbs:.1f}")
    with col4:
        st.metric("Fat (g)", f"{total_fat:.1f}")
    with col5:
        st.metric("Fiber (g)", f"{total_fiber:.1f}")
    with col6:
        st.metric("Sodium (mg)", f"{total_sodium:.0f}")
    
    if total_calories > 0:
        st.markdown("### Daily Summary Chart")
        
        daily_summary = {
            'Nutrient': ['Protein', 'Fat', 'Carbs'],
            'Grams': [total_protein, total_fat, total_carbs]
        }
        
        df_daily = pd.DataFrame(daily_summary)
        fig = px.bar(df_daily, x='Nutrient', y='Grams',
                    color='Nutrient',
                    color_discrete_sequence=['#FF6B6B', '#FFA07A', '#4ECDC4'])
        st.plotly_chart(fig, use_container_width=True)
        
        # Export meal plan
        meal_export = []
        for meal in meal_order:
            for food in st.session_state.meal_plan[meal]:
                meal_export.append({
                    'Meal': meal.capitalize(),
                    'Food': food['name'],
                    'Calories': food['calories'],
                    'Protein': food['protein_g'],
                    'Carbs': food['carbohydrates_g'],
                    'Fat': food['fat_g'],
                    'Fiber': food['fiber_g']
                })
        
        meal_export.append({
            'Meal': 'TOTAL',
            'Food': '',
            'Calories': total_calories,
            'Protein': total_protein,
            'Carbs': total_carbs,
            'Fat': total_fat,
            'Fiber': total_fiber
        })
        
        df_export = pd.DataFrame(meal_export)
        csv_buffer = StringIO()
        df_export.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download Meal Plan (CSV)",
            data=csv_buffer.getvalue(),
            file_name=f"meal_plan_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# TAB 7: BOOKMARKS
with tab7:
    st.subheader("Your Bookmarked Foods")
    
    if st.session_state.favorites:
        st.markdown(f"### Total Bookmarks: {len(st.session_state.favorites)}")
        
        for idx, fav in enumerate(st.session_state.favorites):
            food_details = get_food_details(fav['food_id'])
            
            if food_details:
                with st.container(border=True):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{food_details['name']}**")
                        st.caption(f"{food_details['category']} | {food_details.get('brand', 'N/A')}")
                        st.caption(f"{food_details['calories']:.0f} cal | {food_details['protein_g']:.1f}g protein | {food_details['fiber_g']:.1f}g fiber")
                    with col2:
                        if st.button("Remove", key=f"unbookmark_{idx}"):
                            st.session_state.favorites.pop(idx)
                            st.rerun()
    else:
        st.info("No bookmarks yet. Browse foods and click 'Bookmark' to add them here.")

st.divider()
st.markdown("---")

stats = get_stats()
last_updated = stats.get('last_updated', datetime.now()).strftime('%Y-%m-%d %H:%M:%S') if stats.get('last_updated') else 'N/A'
st.markdown(f"Professional Nutrition Database | Last Updated: {last_updated}")