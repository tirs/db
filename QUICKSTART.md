# FatSecret Database - Quick Start Guide

Get a production-ready nutrition database running in 15 minutes.

---

## ✅ Prerequisites Check

Before you start, make sure you have:

```powershell
# Check if MySQL is installed
mysql --version

# If not installed:
# Download from https://dev.mysql.com/downloads/mysql/
# Run installer with default settings
```

Expected output: `mysql Ver 8.0.x` or higher

---

## 🚀 Step 1: Navigate to Database Directory

```powershell
cd c:\Users\simba\Desktop\Database
```

Verify files exist:
```powershell
ls  # Should show 9 files including schema.sql, setup.ps1, etc.
```

---

## 🛠️ Step 2: Run Setup Script

**Option A: Default Setup (Recommended)**
```powershell
.\setup.ps1
```

**Option B: Custom Configuration**
```powershell
.\setup.ps1 -Username "root" -Password "your_secure_password" -DatabaseName "nutrition_tracker"
```

**Expected Output:**
```
✓ Database created
✓ Schema created successfully
✓ Stored procedures created
✓ Database setup completed successfully!
```

---

## 📦 Step 3: Load Sample Data (Optional)

Load 37 test foods and sample users:

```powershell
mysql -h localhost -u root nutrition_tracker < sample_data.sql
```

Or with password:
```powershell
mysql -h localhost -u root -p"your_password" nutrition_tracker < sample_data.sql
```

---

## ✔️ Step 4: Verify Installation

Test the database:

```powershell
mysql -h localhost -u root nutrition_tracker -e "SELECT COUNT(*) as foods FROM foods;"
```

Or with password:
```powershell
mysql -h localhost -u root -p"your_password" nutrition_tracker -e "SELECT COUNT(*) as foods FROM foods;"
```

**Expected Output:**
```
foods
37
```

---

## 🔍 Step 5: Test Common Queries

### Get All Foods
```sql
SELECT name, brand, calories FROM nutrition_facts 
JOIN foods ON nutrition_facts.food_id = foods.food_id LIMIT 10;
```

### Get Sample User
```sql
SELECT * FROM users WHERE username = 'johndoe';
```

### Get User's Daily Nutrition
```sql
SELECT * FROM daily_nutrition_summary WHERE user_id = 1 AND summary_date = CURDATE();
```

### Search Foods
```sql
SELECT name, brand FROM foods 
WHERE MATCH(name, brand) AGAINST('chicken' IN BOOLEAN MODE);
```

---

## 🔗 Step 6: Connect Your Application

### Python Example
```python
from sqlalchemy import create_engine

# Create connection
engine = create_engine('mysql+pymysql://root:password@localhost/nutrition_tracker')

# Test connection
with engine.connect() as connection:
    result = connection.execute("SELECT COUNT(*) FROM foods")
    print(result.fetchone())
```

### Node.js Example
```javascript
const mysql = require('mysql2/promise');

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'nutrition_tracker'
});

// Test connection
pool.getConnection().then(conn => {
  conn.query('SELECT COUNT(*) as count FROM foods').then(res => {
    console.log('Foods:', res[0].count);
  });
});
```

### PHP Example
```php
$pdo = new PDO('mysql:host=localhost;dbname=nutrition_tracker', 'root', 'password');
$result = $pdo->query('SELECT COUNT(*) as count FROM foods');
echo $result->fetch()['count'];
```

---

## 📊 Common Tasks

### Add a New User
```sql
INSERT INTO users (email, username, password_hash, first_name, last_name) 
VALUES ('user@example.com', 'newuser', 'hashed_password', 'First', 'Last');
```

### Log a Meal
```sql
CALL sp_add_meal_entry(1, 'Breakfast', CURDATE(), 22, 150, 'g');
```

### Get User's Nutrition Today
```sql
SELECT 
  u.username,
  dns.total_calories,
  dns.total_protein_g,
  dns.total_carbohydrates_g,
  dns.total_fat_g
FROM daily_nutrition_summary dns
JOIN users u ON dns.user_id = u.user_id
WHERE dns.user_id = 1 AND dns.summary_date = CURDATE();
```

### Search for a Food
```sql
SELECT f.name, f.brand, nf.calories, nf.protein_g
FROM foods f
JOIN nutrition_facts nf ON f.food_id = nf.food_id
WHERE MATCH(f.name, f.brand) AGAINST('salmon' IN BOOLEAN MODE)
LIMIT 10;
```

### Get User's Weight History
```sql
SELECT log_date, weight_kg 
FROM weight_logs 
WHERE user_id = 1 
ORDER BY log_date DESC 
LIMIT 30;
```

---

## 🎯 Database Overview

### What You Get
- **15 tables** - Users, foods, recipes, meals, tracking
- **37 foods** - Complete nutrition data
- **50+ nutrients** - Macros and micros
- **3 users** - Sample data
- **Stored procedures** - Auto-calculations
- **Indexes** - Performance optimized
- **Security** - Data integrity checks

### Key Tables
```
users              → User accounts
user_profiles      → User info (age, weight, goals)
foods              → Food database (37 items)
nutrition_facts    → Nutrition per food
meals              → Daily meal logs
meal_entries       → Foods in meals
daily_nutrition_summary → Daily totals
weight_logs        → Weight tracking
exercise_logs      → Workout tracking
recipes            → Saved recipes
nutrition_goals    → User targets
```

---

## 🐛 Troubleshooting

### Problem: "Access denied for user 'root'"
**Solution:** 
```powershell
# Try without password if you didn't set one
mysql -h localhost -u root nutrition_tracker -e "SELECT 1;"

# Or use the password you set
mysql -h localhost -u root -p"YourPassword" nutrition_tracker -e "SELECT 1;"
```

### Problem: "Database 'nutrition_tracker' doesn't exist"
**Solution:**
```powershell
# Run setup script again
.\setup.ps1 -Password "your_password"

# Verify database was created
mysql -h localhost -u root -e "SHOW DATABASES LIKE 'nutrition_tracker';"
```

### Problem: "Table 'foods' doesn't exist"
**Solution:**
```powershell
# Schema wasn't loaded, run it manually
mysql -h localhost -u root nutrition_tracker < schema.sql

# Or load sample data which includes schema
mysql -h localhost -u root nutrition_tracker < sample_data.sql
```

### Problem: Connection timeout
**Solution:**
```powershell
# Check MySQL is running
Get-Service -Name MySQL80

# Or for MySQL 5.7
Get-Service -Name MySQL57

# Start service if stopped
Start-Service -Name MySQL80
```

---

## 📚 Next Steps

1. **Read Full Documentation** → Open `README.md`
2. **See Integration Examples** → Check `IMPLEMENTATION_GUIDE.md`
3. **Connection Strings** → Browse `CONNECTION_STRINGS.md`
4. **Copy Queries** → Use queries from `queries.sql`
5. **Configure App** → Copy `config.example.json` to `config.json`

---

## 🔐 Security Notes

### For Development
- Default user: `root`
- Default password: (none - set your own)
- Database: `nutrition_tracker`

### For Production
1. Create dedicated database user:
   ```sql
   CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'strong_password';
   GRANT SELECT, INSERT, UPDATE, DELETE ON nutrition_tracker.* TO 'app_user'@'localhost';
   ```

2. Disable root remote access:
   ```sql
   DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
   ```

3. Enable SSL/TLS (optional but recommended)

4. Set up backups

---

## 📞 Quick Support

**Check this first:**
1. Is MySQL running? → `Get-Service -Name MySQL80`
2. Can you connect? → `mysql -h localhost -u root -e "SELECT 1;"`
3. Does database exist? → `mysql -h localhost -u root -e "SHOW DATABASES;"`
4. Are tables there? → `mysql -h localhost -u root nutrition_tracker -e "SHOW TABLES;"`

**Still stuck?**
- Check ERROR messages carefully - they're descriptive
- Try with `-v` flag for verbose output
- See IMPLEMENTATION_GUIDE.md "Troubleshooting" section

---

## 💡 Pro Tips

### 1. Use MySQL Workbench (GUI)
Download free MySQL Workbench for visual database management

### 2. Keep Sample Data
- Great for testing queries
- Reference for data structure
- Demo to stakeholders

### 3. Regular Backups
```powershell
# Weekly backup script
mysqldump -h localhost -u root nutrition_tracker > backup_$(date +%Y%m%d).sql
```

### 4. Export Reports
```sql
SELECT * FROM daily_nutrition_summary 
WHERE user_id = 1 AND summary_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
INTO OUTFILE '/tmp/nutrition_report.csv' 
FIELDS TERMINATED BY ',' ENCLOSED BY '"';
```

### 5. Monitor Performance
```sql
-- Check slow queries
SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;

-- Check table sizes
SELECT TABLE_NAME, ROUND(((data_length + index_length) / 1024 / 1024), 2) as size_mb
FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = 'nutrition_tracker';
```

---

## ✨ You're All Set!

Your nutrition database is ready. Next:
1. Start logging meals
2. Connect your application
3. Add your own foods
4. Build your feature

---

**Questions? Check the documentation or run:**
```powershell
# List all files
Get-ChildItem

# View any file
type README.md
type IMPLEMENTATION_GUIDE.md
```

**Happy coding! 🚀**