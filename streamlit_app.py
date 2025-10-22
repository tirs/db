#!/usr/bin/env python3
"""
Nutrition Database Streamlit Dashboard
Share your nutrition data with clients
"""

import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO
import csv

# Page config
st.set_page_config(
    page_title="🥗 Nutrition Database",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        # Fallback to hardcoded (for local dev only)
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
        # Verify connection is alive
        if not conn.is_connected():
            conn.reconnect()
        return conn
    except Exception as e:
        st.error(f"❌ Database connection failed: {str(e)}")
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
                (SELECT COUNT(*) FROM nutrition_facts) as nutrition_records
        """)
        stats = cursor.fetchone()
        cursor.close()
        return stats
    finally:
        if conn.is_connected():
            conn.close()

def search_foods(search_term='', category_id='', min_cal='', max_cal=''):
    """Search for foods"""
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
        
        query += " ORDER BY f.name LIMIT 500"
        
        cursor.execute(query, params)
        foods = cursor.fetchall()
        cursor.close()
        
        return foods
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
def get_top_foods(metric='calories', limit=10):
    """Get top foods by metric"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        
        if metric == 'calories':
            query = """
                SELECT f.name, fc.name as category, nf.calories as value, f.brand
                FROM foods f
                JOIN food_categories fc ON f.category_id = fc.category_id
                LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
                WHERE nf.calories IS NOT NULL
                ORDER BY nf.calories DESC
                LIMIT %s
            """
        elif metric == 'protein':
            query = """
                SELECT f.name, fc.name as category, nf.protein_g as value, f.brand
                FROM foods f
                JOIN food_categories fc ON f.category_id = fc.category_id
                LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
                WHERE nf.protein_g IS NOT NULL
                ORDER BY nf.protein_g DESC
                LIMIT %s
            """
        elif metric == 'fiber':
            query = """
                SELECT f.name, fc.name as category, nf.fiber_g as value, f.brand
                FROM foods f
                JOIN food_categories fc ON f.category_id = fc.category_id
                LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
                WHERE nf.fiber_g IS NOT NULL
                ORDER BY nf.fiber_g DESC
                LIMIT %s
            """
        else:
            return []
        
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

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5em;
        font-weight: bold;
        color: #6366f1;
    }
    .metric-label {
        font-size: 0.9em;
        color: #666;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 🥗 Nutrition Database Dashboard")
st.markdown("Professional nutrition data for your clients")

# Stats
stats = get_stats()
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📁 Categories", stats['categories'])
with col2:
    st.metric("🍎 Foods", f"{stats['foods']:,}")
with col3:
    st.metric("📊 Records", f"{stats['nutrition_records']:,}")

st.divider()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search", "📂 Browse", "📊 Analysis", "⭐ Top Foods"])

# TAB 1: SEARCH
with tab1:
    st.subheader("Search & Filter Foods")
    
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("🔎 Search food name", placeholder="e.g., chicken, apple, salmon...")
    with col2:
        categories = get_categories()
        cat_options = {cat['name']: cat['category_id'] for cat in categories}
        cat_options = {"All Categories": ""} | cat_options
        selected_category = st.selectbox("📁 Category", list(cat_options.keys()))
        category_id = cat_options[selected_category]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        min_cal = st.number_input("Min Calories", value=0, min_value=0)
    with col2:
        max_cal = st.number_input("Max Calories", value=0, min_value=0)
    with col3:
        if st.button("🔍 Search", use_container_width=True):
            st.session_state.search_triggered = True
    with col4:
        pass
    
    if st.session_state.get('search_triggered', False) or search_term or category_id:
        foods = search_foods(search_term, category_id, min_cal if min_cal > 0 else '', max_cal if max_cal > 0 else '')
        
        if foods:
            df = pd.DataFrame(foods)
            df['calories'] = df['calories'].fillna(0).astype(float)
            df['protein_g'] = df['protein_g'].fillna(0).astype(float)
            df['fat_g'] = df['fat_g'].fillna(0).astype(float)
            df['carbohydrates_g'] = df['carbohydrates_g'].fillna(0).astype(float)
            
            st.success(f"✅ Found {len(foods)} foods")
            
            # Display table
            display_df = df[['name', 'category', 'calories', 'protein_g', 'fat_g', 'carbohydrates_g', 'fiber_g']].copy()
            display_df.columns = ['Food Name', 'Category', 'Calories', 'Protein (g)', 'Fat (g)', 'Carbs (g)', 'Fiber (g)']
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # CSV export
            csv_buffer = StringIO()
            display_df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_buffer.getvalue(),
                file_name=f"nutrition_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.warning("😕 No foods found. Try a different search or category.")

# TAB 2: BROWSE
with tab2:
    st.subheader("Browse by Category")
    
    categories = get_categories()
    cols = st.columns(3)
    
    for idx, cat in enumerate(categories):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### 📁 {cat['name']}")
                st.metric("Foods", cat['food_count'])
                if st.button("View Details", key=f"cat_{cat['category_id']}"):
                    st.session_state.selected_category = cat['category_id']

# TAB 3: ANALYSIS
with tab3:
    st.subheader("Nutrition Analysis")
    
    overall_stats = get_overall_stats()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Calories", f"{overall_stats['avg_calories']:.0f}")
    with col2:
        st.metric("Avg Protein", f"{overall_stats['avg_protein']:.1f}g")
    with col3:
        st.metric("Avg Fat", f"{overall_stats['avg_fat']:.1f}g")
    with col4:
        st.metric("Avg Carbs", f"{overall_stats['avg_carbs']:.1f}g")
    
    st.divider()
    
    # Category stats chart
    category_stats = get_category_stats()
    df_cat_stats = pd.DataFrame(category_stats)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Average Calories by Category")
        fig = px.bar(df_cat_stats, x='category', y='avg_calories', 
                     labels={'category': 'Category', 'avg_calories': 'Avg Calories'},
                     color='avg_calories', color_continuous_scale='Viridis')
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💪 Average Protein by Category")
        fig = px.bar(df_cat_stats, x='category', y='avg_protein',
                     labels={'category': 'Category', 'avg_protein': 'Avg Protein (g)'},
                     color='avg_protein', color_continuous_scale='Blues')
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Macronutrient distribution
    st.markdown("### 🥘 Overall Macronutrient Distribution")
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
                 color_discrete_sequence=['#FF6B6B', '#FFA07A', '#4ECDC4'])
    st.plotly_chart(fig, use_container_width=True)

# TAB 4: TOP FOODS
with tab4:
    st.subheader("Top Foods Rankings")
    
    metric_type = st.radio("Select Metric:", ["🔥 Highest Calories", "💪 Highest Protein", "🌾 Highest Fiber"], horizontal=True)
    
    col1, col2, col3 = st.columns(3)
    
    if "Calories" in metric_type:
        top_foods_data = get_top_foods('calories', 10)
    elif "Protein" in metric_type:
        top_foods_data = get_top_foods('protein', 10)
    else:
        top_foods_data = get_top_foods('fiber', 10)
    
    df_top = pd.DataFrame(top_foods_data)
    
    # Show as ranking with icons
    for idx, (i, row) in enumerate(df_top.iterrows(), 1):
        with st.container(border=True):
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"### #{idx}")
            with col2:
                st.markdown(f"**{row['name']}**")
                st.caption(f"{row['category']} • {row['value']:.1f}")

st.divider()
st.markdown("---")
st.markdown("📱 Professional Nutrition Database Dashboard | Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))