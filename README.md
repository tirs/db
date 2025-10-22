# FatSecret-like Nutrition Tracking Database

Comprehensive MySQL database structure for a nutrition tracking and meal logging system similar to FatSecret.

## Project Overview

This database is designed to:
- Track user nutrition intake and meals
- Store comprehensive food and nutritional data
- Manage recipes and meal composition
- Log weight and exercise activities
- Support goal tracking and progress monitoring
- Provide audit logging for data integrity

## Database Structure

### Core Modules

#### 1. User Management
- `users` - User accounts and authentication
- `user_profiles` - Extended user information (age, height, weight, goals)
- `user_favorite_foods` - Bookmarked foods for quick access
- `user_favorite_recipes` - Saved recipes

#### 2. Food Database
- `food_categories` - Food classification
- `foods` - Complete food items catalog
- `nutrition_facts` - Detailed nutritional information per food
- `food_barcodes` - Barcode support for mobile scanning

#### 3. Recipes & Meals
- `recipes` - User-created or public recipes
- `recipe_ingredients` - Ingredients in recipes
- `recipe_nutrition_calculated` - Pre-calculated nutrition for recipes
- `meals` - User meals (breakfast, lunch, dinner, snack)
- `meal_entries` - Individual foods in meals

#### 4. Health Tracking
- `daily_nutrition_summary` - Aggregated daily nutrition data
- `weight_logs` - User weight history
- `exercise_logs` - Workout and exercise tracking
- `nutrition_goals` - User nutrition targets

#### 5. System Management
- `audit_logs` - Complete audit trail of data changes

## Installation

### Prerequisites
- MySQL 8.0 or higher
- PowerShell (for setup script)
- Windows OS

### Setup Steps

1. **Clone or download the repository**
```powershell
cd c:\Users\simba\Desktop\Database
```

2. **Run the setup script**
```powershell
.\setup.ps1 -MySQLPath "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -DatabaseName "nutrition_tracker" -Username "root" -Password "your_password"
```

3. **Load sample data (optional)**
```powershell
mysql -h localhost -u root -p nutrition_tracker < sample_data.sql
```

### Setup Script Parameters
- `-MySQLPath` - Path to MySQL executable (default: `C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe`)
- `-DatabaseName` - Database name (default: `nutrition_tracker`)
- `-Username` - MySQL username (default: `root`)
- `-Password` - MySQL password (default: empty)
- `-Host` - Database host (default: `localhost`)
- `-Port` - Database port (default: `3306`)

## Database Schema Details

### Key Tables

#### Users Table
```sql
- user_id (PK)
- email (UNIQUE)
- username (UNIQUE)
- password_hash
- first_name, last_name
- created_at, updated_at
- is_active
```

#### Foods Table
```sql
- food_id (PK)
- category_id (FK)
- name
- description
- brand
- serving_size
- serving_weight_g
- data_source (USDA, User Input, etc.)
- is_verified (Boolean)
```

#### Nutrition Facts Table
```sql
- nutrition_id (PK)
- food_id (FK, UNIQUE)
- Macronutrients: calories, protein, carbs, fat, fiber, sugar
- Micronutrients: vitamins (A, C, D, E, K, B complex), minerals
- Other: cholesterol, sodium, potassium, caffeine
```

#### Meals Table
```sql
- meal_id (PK)
- user_id (FK)
- meal_type (Breakfast, Lunch, Dinner, Snack)
- meal_date
- notes
- UNIQUE constraint on (user_id, meal_date, meal_type)
```

#### Daily Nutrition Summary Table
```sql
- summary_id (PK)
- user_id (FK)
- summary_date
- Aggregated daily totals for all nutrients
- UNIQUE constraint on (user_id, summary_date)
```

## Stored Procedures

### sp_add_meal_entry
Adds a food entry to a meal and automatically updates daily nutrition summary.

**Parameters:**
- `p_user_id` - User ID
- `p_meal_type` - Type of meal
- `p_meal_date` - Date of meal
- `p_food_id` - Food ID
- `p_quantity` - Quantity in grams
- `p_unit` - Unit of measurement

**Usage:**
```sql
CALL sp_add_meal_entry(1, 'Breakfast', CURDATE(), 22, 150, 'g');
```

### sp_update_daily_summary
Recalculates daily nutrition summary for a specific user and date.

**Parameters:**
- `p_user_id` - User ID
- `p_summary_date` - Date to recalculate

**Usage:**
```sql
CALL sp_update_daily_summary(1, CURDATE());
```

## Performance Optimization

### Indexes
- Full-text search index on foods(name, brand, description)
- Composite indexes on frequently queried columns:
  - meals(user_id, meal_date)
  - daily_nutrition_summary(user_id, summary_date)
  - weight_logs(user_id, log_date)
  - exercise_logs(user_id, exercise_date)

### Query Optimization Tips
1. Use indexes for date range queries
2. Pre-aggregate data in daily_nutrition_summary table
3. Archive old data periodically
4. Use stored procedures for complex calculations

## Security Features

1. **Data Integrity**
   - Foreign key constraints prevent orphaned data
   - Unique constraints prevent duplicates
   - Check constraints ensure valid data

2. **Access Control**
   - Password hashing (application-level)
   - User isolation (user_id filtering on all queries)
   - Audit logging for compliance

3. **Data Protection**
   - Character set: UTF8MB4 for international support
   - Collation: utf8mb4_unicode_ci for proper sorting

## Sample Data

The database includes:
- 14 food categories
- 37 common foods with complete nutrition facts
- 3 sample users with profiles
- 3 nutrition goals
- 3 recipes with ingredients
- Sample meal entries and exercise logs
- Weight tracking history

## Querying Examples

### Get Daily Nutrition Summary
```sql
SELECT * FROM daily_nutrition_summary 
WHERE user_id = 1 AND summary_date = CURDATE();
```

### Find Foods by Search
```sql
SELECT * FROM foods 
WHERE MATCH(name, brand, description) AGAINST('salmon' IN BOOLEAN MODE)
LIMIT 10;
```

### Get User's Favorite Foods Nutrition
```sql
SELECT f.name, f.brand, nf.calories, nf.protein_g, nf.carbohydrates_g
FROM user_favorite_foods uff
JOIN foods f ON uff.food_id = f.food_id
JOIN nutrition_facts nf ON f.food_id = nf.food_id
WHERE uff.user_id = 1
ORDER BY uff.created_at DESC;
```

### Get Recipe Nutrition
```sql
SELECT rn.recipe_id, r.name, rn.total_calories, 
       rn.per_serving_calories, r.servings
FROM recipe_nutrition_calculated rn
JOIN recipes r ON rn.recipe_id = r.recipe_id
WHERE r.user_id = 1;
```

### User Weekly Progress
```sql
SELECT log_date, weight_kg, 
       LAG(weight_kg) OVER (ORDER BY log_date) AS prev_weight,
       weight_kg - LAG(weight_kg) OVER (ORDER BY log_date) AS daily_change
FROM weight_logs
WHERE user_id = 1 AND log_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
ORDER BY log_date;
```

## Maintenance

### Regular Tasks
1. **Backup** - Daily incremental, weekly full backups
2. **Optimize** - Weekly table optimization (`OPTIMIZE TABLE`)
3. **Archive** - Monthly archive of old meal logs
4. **Update Nutrition Data** - Quarterly updates from USDA database

### Scaling Considerations
1. Partition large tables by date (meal_entries, meals)
2. Use read replicas for reporting queries
3. Implement caching layer for nutrition_facts
4. Consider sharding by user_id for multi-region deployments

## Integration Guide

### Web Application Integration
1. Use connection pooling for efficiency
2. Implement prepared statements to prevent SQL injection
3. Cache nutrition_facts table in application
4. Use transactions for meal logging operations

### API Endpoints (Suggested)
- `POST /api/meals` - Log a meal
- `POST /api/foods/search` - Search foods
- `GET /api/daily-summary` - Get daily nutrition
- `POST /api/recipes` - Create recipe
- `POST /api/weight` - Log weight
- `GET /api/progress` - Get progress charts

## File Structure

```
c:\Users\simba\Desktop\Database\
├── schema.sql              # Main database schema (550 lines)
├── sample_data.sql         # Sample data for testing (400+ lines)
├── setup.ps1              # PowerShell setup script (200 lines)
└── README.md              # This file
```

## Support & Documentation

- Database Design: See schema.sql for complete structure with comments
- Setup Instructions: Follow setup.ps1 for automated installation
- Sample Queries: Check README.md examples section

## License

This database structure is provided as-is for educational and commercial use.

## Version History

- **v1.0** - Initial release with core functionality
  - Complete schema with 15 tables
  - 37 sample foods with full nutrition facts
  - 3 stored procedures
  - Full-text search support
  - Audit logging