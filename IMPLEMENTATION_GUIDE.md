# FatSecret Database Implementation Guide

Complete guide for deploying, integrating, and maintaining the nutrition tracking database.

## Quick Start (5 minutes)

### 1. Install MySQL
Download from https://dev.mysql.com/downloads/mysql/

### 2. Run Setup
```powershell
cd c:\Users\simba\Desktop\Database
.\setup.ps1 -Password "your_secure_password"
```

### 3. Load Sample Data
```powershell
mysql -h localhost -u root -pYourPassword nutrition_tracker < sample_data.sql
```

### 4. Verify Installation
```sql
SELECT COUNT(*) as food_count FROM foods;
SELECT COUNT(*) as user_count FROM users;
```

## Architecture Overview

### Database Layers

```
┌─────────────────────────────────────────────────────────┐
│         Web Application / API Layer                      │
├─────────────────────────────────────────────────────────┤
│     Connection Pooling + ORM/Query Builder              │
├─────────────────────────────────────────────────────────┤
│     Stored Procedures + Transactions                     │
├─────────────────────────────────────────────────────────┤
│              MySQL Database Core                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Users | Food DB | Recipes | Tracking | Audit    │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Table Relationships

```
users
├── user_profiles
├── user_favorite_foods ──→ foods
├── user_favorite_recipes ──→ recipes
├── nutrition_goals
├── meals
│   └── meal_entries ──→ foods ──→ nutrition_facts
├── weight_logs
├── exercise_logs
└── recipes
    ├── recipe_ingredients ──→ foods
    └── recipe_nutrition_calculated
```

## Integration Examples

### Python (Using SQLAlchemy)

```python
from sqlalchemy import create_engine
from datetime import date

# Connect to database
engine = create_engine('mysql+pymysql://root:password@localhost/nutrition_tracker')
connection = engine.connect()

# Add meal entry using stored procedure
def log_meal(user_id, meal_type, food_id, quantity_g):
    query = """
    CALL sp_add_meal_entry(%s, %s, %s, %s, %s, %s)
    """
    connection.execute(query, (
        user_id, meal_type, date.today(), food_id, quantity_g, 'g'
    ))

# Get today's nutrition
def get_daily_summary(user_id):
    query = """
    SELECT total_calories, total_protein_g, total_carbohydrates_g, total_fat_g
    FROM daily_nutrition_summary
    WHERE user_id = %s AND summary_date = %s
    """
    result = connection.execute(query, (user_id, date.today())).fetchone()
    return result
```

### Node.js (Using mysql2)

```javascript
const mysql = require('mysql2/promise');

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'nutrition_tracker',
  waitForConnections: true,
  connectionLimit: 10
});

// Log meal
async function logMeal(userId, mealType, foodId, quantity) {
  const conn = await pool.getConnection();
  try {
    await conn.query(
      'CALL sp_add_meal_entry(?, ?, ?, ?, ?, ?)',
      [userId, mealType, new Date(), foodId, quantity, 'g']
    );
  } finally {
    conn.release();
  }
}

// Search foods
async function searchFoods(query) {
  const conn = await pool.getConnection();
  const [rows] = await conn.query(
    `SELECT f.*, nf.calories, nf.protein_g 
     FROM foods f
     JOIN nutrition_facts nf ON f.food_id = nf.food_id
     WHERE MATCH(f.name, f.brand) AGAINST(? IN BOOLEAN MODE)
     LIMIT 20`,
    [query]
  );
  conn.release();
  return rows;
}
```

### PHP (Using PDO)

```php
<?php
$pdo = new PDO(
    'mysql:host=localhost;dbname=nutrition_tracker',
    'root',
    'password'
);

// Log meal entry
function logMeal($userId, $mealType, $foodId, $quantity) {
    global $pdo;
    $stmt = $pdo->prepare(
        'CALL sp_add_meal_entry(?, ?, ?, ?, ?, ?)'
    );
    $stmt->execute([
        $userId, 
        $mealType, 
        date('Y-m-d'), 
        $foodId, 
        $quantity, 
        'g'
    ]);
}

// Get user nutrition goals
function getUserGoals($userId) {
    global $pdo;
    $stmt = $pdo->prepare(
        'SELECT target_calories, target_protein_g, target_carbohydrates_g 
         FROM nutrition_goals 
         WHERE user_id = ? AND end_date IS NULL'
    );
    $stmt->execute([$userId]);
    return $stmt->fetch(PDO::FETCH_ASSOC);
}
?>
```

## API Design (REST)

### User Management
```
POST   /api/users                    - Register new user
GET    /api/users/{id}               - Get user profile
PUT    /api/users/{id}               - Update profile
GET    /api/users/{id}/goals         - Get nutrition goals
POST   /api/users/{id}/goals         - Set new goal
```

### Meal Logging
```
POST   /api/meals                    - Log new meal
GET    /api/meals?date=YYYY-MM-DD    - Get meals for date
POST   /api/meals/{id}/entries       - Add food to meal
DELETE /api/meals/{id}/entries/{id}  - Remove food from meal
GET    /api/daily-summary            - Get today's nutrition
```

### Food Database
```
GET    /api/foods/search?q=query     - Search foods
GET    /api/foods/{id}               - Get food details
POST   /api/foods/scan?barcode=...   - Scan barcode
GET    /api/categories               - Get food categories
```

### Recipes
```
GET    /api/recipes                  - List user recipes
POST   /api/recipes                  - Create recipe
PUT    /api/recipes/{id}             - Update recipe
GET    /api/recipes/{id}/nutrition   - Get recipe nutrition
POST   /api/recipes/{id}/favorite    - Save as favorite
```

### Health Tracking
```
POST   /api/weight                   - Log weight
GET    /api/weight?days=30           - Get weight history
POST   /api/exercise                 - Log exercise
GET    /api/exercise?days=7          - Get exercise log
```

## Database Tuning

### Connection Pool Configuration
```
Pool Size: 10-20 connections
Max Wait Time: 30 seconds
Connection Timeout: 5 seconds
Idle Timeout: 900 seconds (15 minutes)
```

### Query Optimization

#### 1. Common Queries (Should use indexes)
```sql
-- These queries are optimized with indexes
SELECT * FROM daily_nutrition_summary 
WHERE user_id = 1 AND summary_date = CURDATE();

SELECT * FROM meals 
WHERE user_id = 1 AND meal_date = CURDATE();
```

#### 2. Full-Text Search
```sql
-- Uses FULLTEXT index on foods(name, brand, description)
SELECT * FROM foods 
WHERE MATCH(name, brand, description) AGAINST('salmon' IN BOOLEAN MODE);
```

#### 3. Pagination for Large Result Sets
```sql
SELECT * FROM foods 
LIMIT 20 OFFSET 0;  -- First page
LIMIT 20 OFFSET 20; -- Second page
```

### Performance Tips

1. **Use EXPLAIN to analyze queries**
   ```sql
   EXPLAIN SELECT * FROM meals WHERE user_id = 1 AND meal_date = CURDATE();
   ```

2. **Batch operations**
   ```sql
   -- Insert multiple entries at once
   INSERT INTO meal_entries (meal_id, food_id, quantity, unit) VALUES
   (1, 22, 150, 'g'),
   (1, 5, 200, 'g'),
   (1, 34, 244, 'ml');
   ```

3. **Use transactions for consistency**
   ```sql
   START TRANSACTION;
   INSERT INTO meals ... ;
   INSERT INTO meal_entries ... ;
   COMMIT;
   ```

## Security Implementation

### 1. User Authentication
```sql
-- Store passwords securely (application-level)
-- Use bcrypt or similar hashing algorithm
-- Never store plain text passwords

UPDATE users SET password_hash = bcrypt(password, 12);
```

### 2. Query Parameterization (Prevent SQL Injection)
```python
# GOOD - Use parameterized queries
query = "SELECT * FROM foods WHERE food_id = ?"
cursor.execute(query, (food_id,))

# BAD - Vulnerable to SQL injection
query = f"SELECT * FROM foods WHERE food_id = {food_id}"
```

### 3. Access Control
```sql
-- Always filter by user_id for user-specific data
SELECT * FROM meals WHERE user_id = ? AND meal_date = ?;

-- Use database roles for access control
CREATE ROLE app_user;
GRANT SELECT ON nutrition_tracker.* TO app_user;
```

### 4. Data Encryption
```sql
-- Encrypt sensitive fields at application layer
-- Consider AES encryption for:
-- - Email addresses
-- - Weight logs (if sensitive)
-- - Health metrics
```

## Backup & Recovery

### Backup Strategy

```powershell
# Full backup daily
mysqldump -h localhost -u root -p nutrition_tracker > backup_$(date +%Y%m%d).sql

# Incremental backup (binary logs)
mysqlbinlog --start-date="2024-01-01" mysql.000001 > incremental.sql
```

### Restore from Backup

```powershell
# Full restore
mysql -h localhost -u root -p nutrition_tracker < backup_20240101.sql

# Point-in-time recovery
mysql -h localhost -u root -p nutrition_tracker < incremental.sql
```

## Monitoring & Maintenance

### Check Database Health

```sql
-- Check table sizes
SELECT 
    TABLE_NAME,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) as size_mb
FROM INFORMATION_SCHEMA.TABLES
WHERE table_schema = 'nutrition_tracker'
ORDER BY size_mb DESC;

-- Check for missing indexes
SELECT * FROM INFORMATION_SCHEMA.STATISTICS
WHERE TABLE_SCHEMA = 'nutrition_tracker'
ORDER BY TABLE_NAME;
```

### Regular Maintenance Tasks

```sql
-- Weekly: Optimize tables
OPTIMIZE TABLE foods;
OPTIMIZE TABLE meals;
OPTIMIZE TABLE nutrition_facts;

-- Monthly: Analyze statistics
ANALYZE TABLE daily_nutrition_summary;

-- Quarterly: Archive old data
DELETE FROM meal_entries 
WHERE meal_id IN (
    SELECT meal_id FROM meals 
    WHERE meal_date < DATE_SUB(CURDATE(), INTERVAL 2 YEAR)
);
```

## Scaling Strategies

### 1. Read Replicas (for reporting)
```
Primary Server (writes)
    ├── Replica 1 (reporting queries)
    ├── Replica 2 (backups)
    └── Replica 3 (analytics)
```

### 2. Partitioning (for large tables)
```sql
-- Partition meals by date
ALTER TABLE meals
PARTITION BY RANGE(YEAR(meal_date)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025)
);
```

### 3. Caching Layer
```python
# Redis caching for nutrition facts
cache.set(f'food:{food_id}', food_data, ttl=86400)  # 24 hours
cached_food = cache.get(f'food:{food_id}')
```

### 4. Database Sharding (for extreme scale)
```
User 1-1M    → DB Shard 1
User 1M-2M   → DB Shard 2
User 2M-3M   → DB Shard 3
...
```

## File Reference

| File | Purpose | Size |
|------|---------|------|
| `schema.sql` | Database structure with 15 tables | ~550 lines |
| `sample_data.sql` | Test data (users, foods, meals) | ~400 lines |
| `setup.ps1` | Automated installation script | ~200 lines |
| `queries.sql` | Common queries and reports | ~400 lines |
| `README.md` | Overview and documentation | ~400 lines |
| `IMPLEMENTATION_GUIDE.md` | This file | ~500 lines |

## Troubleshooting

### Connection Issues
```powershell
# Test connection
mysql -h localhost -u root -pPassword -e "SELECT 1"

# Check MySQL service status
Get-Service -Name MySQL80
```

### Performance Issues
```sql
-- Find slow queries
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

-- Check query execution plan
EXPLAIN SELECT * FROM meals WHERE user_id = 1;
```

### Data Integrity
```sql
-- Check for orphaned records
SELECT m.* FROM meals m
LEFT JOIN users u ON m.user_id = u.user_id
WHERE u.user_id IS NULL;

-- Verify foreign key constraints
SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'nutrition_tracker' AND REFERENCED_TABLE_NAME IS NOT NULL;
```

## Support Resources

- MySQL Documentation: https://dev.mysql.com/doc/
- Query Optimization: https://dev.mysql.com/doc/refman/8.0/en/optimization.html
- Best Practices: https://dev.mysql.com/doc/refman/8.0/en/optimization.html

## Version Updates

### Upgrading from v1.0 to v1.1 (Future)
1. Backup existing database
2. Run migration scripts
3. Update application code
4. Test thoroughly
5. Deploy to production

---

**Last Updated:** 2024
**Version:** 1.0