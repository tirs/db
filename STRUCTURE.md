# Database Structure Reference

Complete visual reference of the FatSecret-like nutrition database.

---

## 📊 Table Relationships Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                            USERS CORE                               │
├─────────────────────────────────────────────────────────────────────┤
│  users (3 fields)                                                   │
│  ├── user_profiles (8 fields)                                       │
│  ├── nutrition_goals (9 fields) ─────┐                             │
│  └── audit_logs (6 fields)           │                             │
└─────────────────────────────────────────────────────────────────────┘
                                        │
┌────────────────────────────────────────┼──────────────────────────┐
│                    MEALS & MEALS TRACKING                         │
├────────────────────────────────────────┼──────────────────────────┤
│  meals (5 fields)                      │                          │
│  ├── meal_entries (8 fields) ───┐     │                          │
│  │   └── foods (8 fields)       │     │                          │
│  │       ├── nutrition_facts    │     │                          │
│  │       │   (30+ fields)       │     │                          │
│  │       ├── food_barcodes      │     │                          │
│  │       └── food_categories    │     │                          │
│  │                              │     │                          │
│  └── daily_nutrition_summary ◄──┴─────┘  (Aggregated totals)      │
│                                                                     │
│  weight_logs (5 fields)                                            │
│  exercise_logs (7 fields)                                          │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                       RECIPES & FAVORITES                           │
├─────────────────────────────────────────────────────────────────────┤
│  recipes (9 fields)                                                 │
│  ├── recipe_ingredients (6 fields)                                  │
│  │   └── foods (references foods table)                             │
│  └── recipe_nutrition_calculated (12 fields)                        │
│                                                                     │
│  user_favorite_foods (3 fields)                                     │
│  user_favorite_recipes (3 fields)                                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Table Definitions

### USER MANAGEMENT (3 tables, 19 fields total)

#### 1. users
```sql
user_id (PK)              INT AUTO_INCREMENT
email                     VARCHAR(255) UNIQUE
username                  VARCHAR(100) UNIQUE
password_hash             VARCHAR(255)
first_name                VARCHAR(100)
last_name                 VARCHAR(100)
created_at                TIMESTAMP DEFAULT NOW
updated_at                TIMESTAMP AUTO UPDATE
is_active                 BOOLEAN DEFAULT TRUE
```

#### 2. user_profiles
```sql
profile_id (PK)           INT AUTO_INCREMENT
user_id (FK)              INT UNIQUE
age                       INT
gender                    ENUM('M', 'F', 'O')
height_cm                 DECIMAL(5,2)
weight_kg                 DECIMAL(5,2)
goal                      VARCHAR(50)
activity_level            VARCHAR(50)
created_at                TIMESTAMP DEFAULT NOW
updated_at                TIMESTAMP AUTO UPDATE
```

#### 3. nutrition_goals
```sql
goal_id (PK)              INT AUTO_INCREMENT
user_id (FK)              INT
goal_type                 ENUM (Weight Loss|Muscle Gain|...)
target_calories           INT
target_protein_g          DECIMAL(8,2)
target_carbohydrates_g    DECIMAL(8,2)
target_fat_g              DECIMAL(8,2)
target_fiber_g            DECIMAL(8,2)
start_date                DATE
end_date                  DATE
created_at                TIMESTAMP DEFAULT NOW
updated_at                TIMESTAMP AUTO UPDATE
```

---

### FOOD DATABASE (3 tables, 43 fields total)

#### 4. food_categories (14 categories)
```sql
category_id (PK)          INT AUTO_INCREMENT
name                      VARCHAR(100) UNIQUE
description               TEXT
created_at                TIMESTAMP DEFAULT NOW
```

**Sample categories:**
- Vegetables
- Fruits
- Grains & Cereals
- Meat & Poultry
- Fish & Seafood
- Dairy & Eggs
- Nuts & Seeds
- Oils & Fats
- Beverages
- Condiments & Sauces
- Snacks
- Desserts
- Prepared Foods
- Fast Food

#### 5. foods (37 sample foods)
```sql
food_id (PK)              INT AUTO_INCREMENT
category_id (FK)          INT
name                      VARCHAR(255)
description               TEXT
brand                     VARCHAR(255)
serving_size              VARCHAR(100)
serving_weight_g          DECIMAL(8,2)
data_source               VARCHAR(100) [USDA|User|Brand]
is_verified               BOOLEAN DEFAULT FALSE
created_at                TIMESTAMP DEFAULT NOW
updated_at                TIMESTAMP AUTO UPDATE
FULLTEXT INDEX (name, brand, description)
```

#### 6. nutrition_facts (50+ nutrients per food)
```sql
nutrition_id (PK)         INT AUTO_INCREMENT
food_id (FK)              INT UNIQUE
calories                  DECIMAL(8,2) NOT NULL
protein_g                 DECIMAL(8,2)
carbohydrates_g           DECIMAL(8,2)
fiber_g                   DECIMAL(8,2)
sugar_g                   DECIMAL(8,2)
fat_g                     DECIMAL(8,2)
saturated_fat_g           DECIMAL(8,2)
cholesterol_mg            DECIMAL(8,2)
sodium_mg                 DECIMAL(8,2)
potassium_mg              DECIMAL(8,2)
calcium_mg                DECIMAL(8,2)
iron_mg                   DECIMAL(8,2)
magnesium_mg              DECIMAL(8,2)
phosphorus_mg             DECIMAL(8,2)
zinc_mg                   DECIMAL(8,2)
vitamin_a_iu              DECIMAL(10,2)
vitamin_c_mg              DECIMAL(8,2)
vitamin_d_iu              DECIMAL(10,2)
vitamin_e_mg              DECIMAL(8,2)
vitamin_k_mg              DECIMAL(8,2)
thiamine_mg               DECIMAL(8,2)
riboflavin_mg             DECIMAL(8,2)
niacin_mg                 DECIMAL(8,2)
pantothenic_acid_mg       DECIMAL(8,2)
folate_mcg                DECIMAL(8,2)
vitamin_b12_mcg           DECIMAL(8,2)
caffeine_mg               DECIMAL(8,2)
created_at                TIMESTAMP DEFAULT NOW
updated_at                TIMESTAMP AUTO UPDATE
```

---

### MEALS & TRACKING (5 tables, 28 fields total)

#### 7. meals
```sql
meal_id (PK)              INT AUTO_INCREMENT
user_id (FK)              INT NOT NULL
meal_type                 ENUM (Breakfast|Lunch|Dinner|Snack)
meal_date                 DATE NOT NULL
created_at                TIMESTAMP DEFAULT NOW
updated_at                TIMESTAMP AUTO UPDATE
notes                     TEXT
UNIQUE KEY (user_id, meal_date, meal_type)
INDEX (user_id, meal_date)
```

#### 8. meal_entries
```sql
entry_id (PK)             INT AUTO_INCREMENT
meal_id (FK)              INT NOT NULL
food_id (FK)              INT NOT NULL
quantity                  DECIMAL(10,2) NOT NULL
unit                      VARCHAR(50)
calories_consumed         DECIMAL(10,2)
protein_consumed_g        DECIMAL(10,2)
carbs_consumed_g          DECIMAL(10,2)
fat_consumed_g            DECIMAL(10,2)
created_at                TIMESTAMP DEFAULT NOW
INDEX (meal_id)
```

#### 9. daily_nutrition_summary
```sql
summary_id (PK)           INT AUTO_INCREMENT
user_id (FK)              INT NOT NULL
summary_date              DATE NOT NULL
total_calories            DECIMAL(10,2) DEFAULT 0
total_protein_g           DECIMAL(10,2) DEFAULT 0
total_carbohydrates_g     DECIMAL(10,2) DEFAULT 0
total_fiber_g             DECIMAL(10,2) DEFAULT 0
total_sugar_g             DECIMAL(10,2) DEFAULT 0
total_fat_g               DECIMAL(10,2) DEFAULT 0
total_saturated_fat_g     DECIMAL(10,2) DEFAULT 0
total_sodium_mg           DECIMAL(10,2) DEFAULT 0
updated_at                TIMESTAMP DEFAULT NOW
UNIQUE KEY (user_id, summary_date)
INDEX (user_id, summary_date)
```

#### 10. weight_logs
```sql
weight_log_id (PK)        INT AUTO_INCREMENT
user_id (FK)              INT NOT NULL
weight_kg                 DECIMAL(5,2) NOT NULL
log_date                  DATE NOT NULL
created_at                TIMESTAMP DEFAULT NOW
notes                     TEXT
UNIQUE KEY (user_id, log_date)
INDEX (user_id, log_date)
```

#### 11. exercise_logs
```sql
exercise_log_id (PK)      INT AUTO_INCREMENT
user_id (FK)              INT NOT NULL
exercise_type             VARCHAR(100)
duration_minutes          INT
calories_burned           DECIMAL(10,2)
exercise_date             DATE NOT NULL
created_at                TIMESTAMP DEFAULT NOW
notes                     TEXT
INDEX (user_id, exercise_date)
```

---

### RECIPES & FAVORITES (4 tables, 28 fields total)

#### 12. recipes
```sql
recipe_id (PK)            INT AUTO_INCREMENT
user_id (FK)              INT
name                      VARCHAR(255) NOT NULL
description               TEXT
servings                  INT DEFAULT 1
prep_time_minutes         INT
cook_time_minutes         INT
difficulty_level          ENUM (Easy|Medium|Hard)
created_at                TIMESTAMP DEFAULT NOW
updated_at                TIMESTAMP AUTO UPDATE
is_public                 BOOLEAN DEFAULT FALSE
INDEX (user_id)
INDEX (name)
```

#### 13. recipe_ingredients
```sql
ingredient_id (PK)        INT AUTO_INCREMENT
recipe_id (FK)            INT NOT NULL
food_id (FK)              INT NOT NULL
quantity                  DECIMAL(10,2) NOT NULL
unit                      VARCHAR(50)
sequence_order            INT
notes                     TEXT
INDEX (recipe_id)
```

#### 14. recipe_nutrition_calculated
```sql
recipe_nutrition_id (PK)  INT AUTO_INCREMENT
recipe_id (FK)            INT UNIQUE
total_calories            DECIMAL(10,2)
total_protein_g           DECIMAL(10,2)
total_carbohydrates_g     DECIMAL(10,2)
total_fiber_g             DECIMAL(10,2)
total_sugar_g             DECIMAL(10,2)
total_fat_g               DECIMAL(10,2)
total_saturated_fat_g     DECIMAL(10,2)
per_serving_calories      DECIMAL(10,2)
per_serving_protein_g     DECIMAL(10,2)
per_serving_carbohydrates_g DECIMAL(10,2)
per_serving_fiber_g       DECIMAL(10,2)
updated_at                TIMESTAMP DEFAULT NOW
```

#### 15. user_favorite_foods
```sql
favorite_id (PK)          INT AUTO_INCREMENT
user_id (FK)              INT NOT NULL
food_id (FK)              INT NOT NULL
created_at                TIMESTAMP DEFAULT NOW
UNIQUE KEY (user_id, food_id)
INDEX (user_id)
```

#### 16. user_favorite_recipes
```sql
favorite_recipe_id (PK)   INT AUTO_INCREMENT
user_id (FK)              INT NOT NULL
recipe_id (FK)            INT NOT NULL
created_at                TIMESTAMP DEFAULT NOW
UNIQUE KEY (user_id, recipe_id)
INDEX (user_id)
```

---

### FOOD LOOKUP & AUDIT (2 tables, 8 fields total)

#### 17. food_barcodes
```sql
barcode_id (PK)           INT AUTO_INCREMENT
food_id (FK)              INT NOT NULL
barcode_code              VARCHAR(20) UNIQUE
barcode_type              VARCHAR(20)
created_at                TIMESTAMP DEFAULT NOW
INDEX (barcode_code)
INDEX (food_id)
```

#### 18. audit_logs
```sql
audit_id (PK)             INT AUTO_INCREMENT
user_id (FK)              INT
table_name                VARCHAR(100)
action                    ENUM (INSERT|UPDATE|DELETE)
record_id                 INT
old_values                JSON
new_values                JSON
created_at                TIMESTAMP DEFAULT NOW
INDEX (user_id)
INDEX (created_at)
```

---

## 🔑 Primary Keys (18 total)

All use AUTO_INCREMENT for automatic ID generation:
- users (user_id)
- user_profiles (profile_id)
- nutrition_goals (goal_id)
- food_categories (category_id)
- foods (food_id)
- nutrition_facts (nutrition_id)
- meals (meal_id)
- meal_entries (entry_id)
- daily_nutrition_summary (summary_id)
- weight_logs (weight_log_id)
- exercise_logs (exercise_log_id)
- recipes (recipe_id)
- recipe_ingredients (ingredient_id)
- recipe_nutrition_calculated (recipe_nutrition_id)
- user_favorite_foods (favorite_id)
- user_favorite_recipes (favorite_recipe_id)
- food_barcodes (barcode_id)
- audit_logs (audit_id)

---

## 🔗 Foreign Keys (18 total)

| Table | FK | References | Delete Rule |
|-------|----|-----------:|------------|
| user_profiles | user_id | users | CASCADE |
| nutrition_goals | user_id | users | CASCADE |
| meals | user_id | users | CASCADE |
| weight_logs | user_id | users | CASCADE |
| exercise_logs | user_id | users | CASCADE |
| recipes | user_id | users | SET NULL |
| user_favorite_foods | user_id | users | CASCADE |
| user_favorite_foods | food_id | foods | CASCADE |
| user_favorite_recipes | user_id | users | CASCADE |
| user_favorite_recipes | recipe_id | recipes | CASCADE |
| foods | category_id | food_categories | RESTRICT |
| nutrition_facts | food_id | foods | CASCADE |
| meal_entries | meal_id | meals | CASCADE |
| meal_entries | food_id | foods | RESTRICT |
| recipe_ingredients | recipe_id | recipes | CASCADE |
| recipe_ingredients | food_id | foods | RESTRICT |
| recipe_nutrition_calculated | recipe_id | recipes | CASCADE |
| food_barcodes | food_id | foods | CASCADE |

---

## 📊 Indexes (30+ total)

### Performance Indexes
```
meals(user_id, meal_date)           - For daily meal retrieval
daily_nutrition_summary(user_id, summary_date)  - For daily summaries
weight_logs(user_id, log_date)      - For weight tracking
nutrition_facts(calories)            - For sorting by calories
foods(name)                          - For food lookups
foods(brand)                         - For brand filtering
```

### Full-Text Search Indexes
```
foods(name, brand, description)     - For food search functionality
```

### Foreign Key Indexes
```
Automatically created for all foreign keys
```

### Unique Indexes
```
users(email)                        - Prevent duplicate emails
users(username)                     - Prevent duplicate usernames
user_profiles(user_id)              - One profile per user
nutrition_facts(food_id)            - One nutrition record per food
meals(user_id, meal_date, meal_type) - One meal per type per day
daily_nutrition_summary(user_id, summary_date) - One summary per day
weight_logs(user_id, log_date)      - One weight per day
user_favorite_foods(user_id, food_id) - Prevent duplicate favorites
user_favorite_recipes(user_id, recipe_id) - Prevent duplicate favorites
food_barcodes(barcode_code)         - Unique barcodes
```

---

## 📈 Data Types Used

| Type | Usage | Examples |
|------|-------|----------|
| INT | IDs, counts | user_id, quantity, age |
| VARCHAR | Text fields | name, email, brand |
| DECIMAL(8,2) | Numbers with precision | weight, calories |
| DATE | Date only | meal_date, log_date |
| TIMESTAMP | Date + time | created_at, updated_at |
| TEXT | Long text | description, notes |
| BOOLEAN | True/false | is_active, is_verified |
| ENUM | Fixed options | gender, meal_type |
| JSON | Complex data | old_values, new_values |

---

## 🔐 Constraints

### Not Null
- All primary keys
- user_id in all user-related tables
- food_id in nutrition_facts
- name in foods and recipes
- quantity in meal_entries

### Check Constraints
- age >= 0
- weight_kg > 0
- height_cm > 0
- All decimal values >= 0

### Unique Constraints
- emails
- usernames
- barcodes
- Composite: user+date combinations

---

## 📝 Default Values

| Field | Default |
|-------|---------|
| created_at | CURRENT_TIMESTAMP |
| updated_at | CURRENT_TIMESTAMP |
| is_active | TRUE |
| is_verified | FALSE |
| is_public | FALSE |
| servings | 1 |
| total_calories | 0 |
| (All totals) | 0 |

---

## 📋 Charset & Collation

**Database Level:**
- Charset: `utf8mb4` (supports emojis, multilingual)
- Collation: `utf8mb4_unicode_ci` (case-insensitive, unicode-aware)

**All Tables:**
- Charset: Inherited from database
- Collation: Inherited from database

---

## 🔄 Stored Procedures (2 total)

### sp_add_meal_entry
- **Purpose:** Add food to meal and update daily summary
- **Parameters:** user_id, meal_type, meal_date, food_id, quantity, unit
- **Actions:** 
  1. Gets or creates meal
  2. Calculates nutrition for quantity
  3. Adds entry to meal
  4. Updates daily summary

### sp_update_daily_summary
- **Purpose:** Recalculate daily nutrition totals
- **Parameters:** user_id, summary_date
- **Actions:**
  1. Sums all meal entries for day
  2. Updates or inserts daily summary
  3. Handles INSERT/UPDATE with ON DUPLICATE KEY

---

## 📊 Sample Data Included

- **14 food categories**
- **37 foods** with complete nutrition
- **3 users** with profiles
- **3 nutrition goals** (weight loss, muscle gain, maintenance)
- **3 recipes** with ingredients
- **5 sample meals** with entries
- **7 weight log entries**
- **4 exercise log entries**
- **6 favorite food entries**

---

## 🎯 Query Performance

### Fast Queries (< 100ms)
```sql
SELECT * FROM daily_nutrition_summary WHERE user_id = 1 AND summary_date = CURDATE();
SELECT * FROM meals WHERE user_id = 1 AND meal_date = CURDATE();
SELECT * FROM nutrition_facts WHERE calories > 100;
```

### Moderate Queries (100-500ms)
```sql
SELECT * FROM foods WHERE MATCH(name, brand) AGAINST('chicken' IN BOOLEAN MODE);
SELECT * FROM weight_logs WHERE user_id = 1 ORDER BY log_date DESC;
SELECT * FROM exercise_logs WHERE exercise_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY);
```

### Complex Queries (500ms-1s)
```sql
SELECT WEEK(summary_date), AVG(total_calories) FROM daily_nutrition_summary GROUP BY WEEK(summary_date);
SELECT f.name, COUNT(*) FROM meal_entries me JOIN foods f GROUP BY f.food_id;
```

---

## 📐 Size Estimates

| Table | Row Size | Sample Rows | Storage |
|-------|----------|-------------|---------|
| users | 300B | 3 | 1KB |
| user_profiles | 150B | 3 | 1KB |
| foods | 500B | 37 | 20KB |
| nutrition_facts | 800B | 37 | 30KB |
| meals | 200B | 5 | 1KB |
| meal_entries | 150B | 8 | 2KB |
| recipes | 400B | 3 | 2KB |
| **Total** | - | - | **~100KB** |

**Note:** Grows with user data. Expect 1-10MB per 1,000 users (depending on meal logging frequency).

---

## ✅ Data Integrity Features

1. **Foreign Key Constraints** - Prevent orphaned data
2. **Unique Constraints** - Prevent duplicates
3. **Not Null Constraints** - Ensure required fields
4. **Check Constraints** - Validate value ranges
5. **Cascade Deletes** - Auto-cleanup related data
6. **Audit Logging** - Track all changes
7. **Referential Integrity** - Maintain relationships

---

**Reference completed! See README.md for usage examples.**