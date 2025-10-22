-- FatSecret-like Database Schema
-- Comprehensive nutrition tracking and meal logging system

-- ============================================================================
-- USERS AND AUTHENTICATION
-- ============================================================================

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_email (email),
    INDEX idx_username (username)
);

CREATE TABLE user_profiles (
    profile_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    age INT,
    gender ENUM('M', 'F', 'O'),
    height_cm DECIMAL(5, 2),
    weight_kg DECIMAL(5, 2),
    goal VARCHAR(50),
    activity_level VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ============================================================================
-- FOOD DATABASE AND NUTRITION
-- ============================================================================

CREATE TABLE food_categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name)
);

CREATE TABLE foods (
    food_id INT PRIMARY KEY AUTO_INCREMENT,
    category_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    brand VARCHAR(255),
    serving_size VARCHAR(100),
    serving_weight_g DECIMAL(8, 2),
    data_source VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (category_id) REFERENCES food_categories(category_id) ON DELETE RESTRICT,
    INDEX idx_name (name),
    INDEX idx_category (category_id),
    INDEX idx_brand (brand),
    FULLTEXT INDEX ft_search (name, brand, description)
);

CREATE TABLE nutrition_facts (
    nutrition_id INT PRIMARY KEY AUTO_INCREMENT,
    food_id INT NOT NULL UNIQUE,
    calories DECIMAL(8, 2) NOT NULL,
    protein_g DECIMAL(8, 2),
    carbohydrates_g DECIMAL(8, 2),
    fiber_g DECIMAL(8, 2),
    sugar_g DECIMAL(8, 2),
    fat_g DECIMAL(8, 2),
    saturated_fat_g DECIMAL(8, 2),
    cholesterol_mg DECIMAL(8, 2),
    sodium_mg DECIMAL(8, 2),
    potassium_mg DECIMAL(8, 2),
    calcium_mg DECIMAL(8, 2),
    iron_mg DECIMAL(8, 2),
    magnesium_mg DECIMAL(8, 2),
    phosphorus_mg DECIMAL(8, 2),
    zinc_mg DECIMAL(8, 2),
    vitamin_a_iu DECIMAL(10, 2),
    vitamin_c_mg DECIMAL(8, 2),
    vitamin_d_iu DECIMAL(10, 2),
    vitamin_e_mg DECIMAL(8, 2),
    vitamin_k_mg DECIMAL(8, 2),
    thiamine_mg DECIMAL(8, 2),
    riboflavin_mg DECIMAL(8, 2),
    niacin_mg DECIMAL(8, 2),
    pantothenic_acid_mg DECIMAL(8, 2),
    folate_mcg DECIMAL(8, 2),
    vitamin_b12_mcg DECIMAL(8, 2),
    caffeine_mg DECIMAL(8, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (food_id) REFERENCES foods(food_id) ON DELETE CASCADE
);

-- ============================================================================
-- RECIPES AND MEAL COMPOSITION
-- ============================================================================

CREATE TABLE recipes (
    recipe_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    servings INT DEFAULT 1,
    prep_time_minutes INT,
    cook_time_minutes INT,
    difficulty_level ENUM('Easy', 'Medium', 'Hard'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_public BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    INDEX idx_user (user_id),
    INDEX idx_name (name)
);

CREATE TABLE recipe_ingredients (
    ingredient_id INT PRIMARY KEY AUTO_INCREMENT,
    recipe_id INT NOT NULL,
    food_id INT NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL,
    unit VARCHAR(50),
    sequence_order INT,
    notes TEXT,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(food_id) ON DELETE RESTRICT,
    INDEX idx_recipe (recipe_id)
);

CREATE TABLE recipe_nutrition_calculated (
    recipe_nutrition_id INT PRIMARY KEY AUTO_INCREMENT,
    recipe_id INT NOT NULL UNIQUE,
    total_calories DECIMAL(10, 2),
    total_protein_g DECIMAL(10, 2),
    total_carbohydrates_g DECIMAL(10, 2),
    total_fiber_g DECIMAL(10, 2),
    total_sugar_g DECIMAL(10, 2),
    total_fat_g DECIMAL(10, 2),
    total_saturated_fat_g DECIMAL(10, 2),
    per_serving_calories DECIMAL(10, 2),
    per_serving_protein_g DECIMAL(10, 2),
    per_serving_carbohydrates_g DECIMAL(10, 2),
    per_serving_fiber_g DECIMAL(10, 2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE
);

-- ============================================================================
-- MEAL LOGGING AND TRACKING
-- ============================================================================

CREATE TABLE meals (
    meal_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    meal_type ENUM('Breakfast', 'Lunch', 'Dinner', 'Snack') NOT NULL,
    meal_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, meal_date),
    INDEX idx_meal_type (meal_type),
    UNIQUE KEY unique_meal (user_id, meal_date, meal_type)
);

CREATE TABLE meal_entries (
    entry_id INT PRIMARY KEY AUTO_INCREMENT,
    meal_id INT NOT NULL,
    food_id INT NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL,
    unit VARCHAR(50),
    calories_consumed DECIMAL(10, 2),
    protein_consumed_g DECIMAL(10, 2),
    carbs_consumed_g DECIMAL(10, 2),
    fat_consumed_g DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (meal_id) REFERENCES meals(meal_id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(food_id) ON DELETE RESTRICT,
    INDEX idx_meal (meal_id)
);

-- ============================================================================
-- DAILY NUTRITION SUMMARY
-- ============================================================================

CREATE TABLE daily_nutrition_summary (
    summary_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    summary_date DATE NOT NULL,
    total_calories DECIMAL(10, 2) DEFAULT 0,
    total_protein_g DECIMAL(10, 2) DEFAULT 0,
    total_carbohydrates_g DECIMAL(10, 2) DEFAULT 0,
    total_fiber_g DECIMAL(10, 2) DEFAULT 0,
    total_sugar_g DECIMAL(10, 2) DEFAULT 0,
    total_fat_g DECIMAL(10, 2) DEFAULT 0,
    total_saturated_fat_g DECIMAL(10, 2) DEFAULT 0,
    total_sodium_mg DECIMAL(10, 2) DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, summary_date),
    UNIQUE KEY unique_daily (user_id, summary_date)
);

-- ============================================================================
-- USER WEIGHT AND HEALTH METRICS
-- ============================================================================

CREATE TABLE weight_logs (
    weight_log_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    weight_kg DECIMAL(5, 2) NOT NULL,
    log_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, log_date),
    UNIQUE KEY unique_weight_date (user_id, log_date)
);

CREATE TABLE exercise_logs (
    exercise_log_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    exercise_type VARCHAR(100),
    duration_minutes INT,
    calories_burned DECIMAL(10, 2),
    exercise_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, exercise_date)
);

-- ============================================================================
-- FAVORITES AND PREFERENCES
-- ============================================================================

CREATE TABLE user_favorite_foods (
    favorite_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    food_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(food_id) ON DELETE CASCADE,
    UNIQUE KEY unique_favorite (user_id, food_id),
    INDEX idx_user (user_id)
);

CREATE TABLE user_favorite_recipes (
    favorite_recipe_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    UNIQUE KEY unique_favorite_recipe (user_id, recipe_id),
    INDEX idx_user (user_id)
);

-- ============================================================================
-- GOALS AND TRACKING
-- ============================================================================

CREATE TABLE nutrition_goals (
    goal_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    goal_type ENUM('Weight Loss', 'Muscle Gain', 'Maintenance', 'Athletic') NOT NULL,
    target_calories INT,
    target_protein_g DECIMAL(8, 2),
    target_carbohydrates_g DECIMAL(8, 2),
    target_fat_g DECIMAL(8, 2),
    target_fiber_g DECIMAL(8, 2),
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user (user_id)
);

-- ============================================================================
-- BARCODE SUPPORT
-- ============================================================================

CREATE TABLE food_barcodes (
    barcode_id INT PRIMARY KEY AUTO_INCREMENT,
    food_id INT NOT NULL,
    barcode_code VARCHAR(20) NOT NULL UNIQUE,
    barcode_type VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (food_id) REFERENCES foods(food_id) ON DELETE CASCADE,
    INDEX idx_barcode (barcode_code),
    INDEX idx_food (food_id)
);

-- ============================================================================
-- AUDIT AND LOGGING
-- ============================================================================

CREATE TABLE audit_logs (
    audit_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    table_name VARCHAR(100),
    action ENUM('INSERT', 'UPDATE', 'DELETE'),
    record_id INT,
    old_values JSON,
    new_values JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    INDEX idx_user (user_id),
    INDEX idx_created (created_at)
);

-- ============================================================================
-- INDEXES FOR COMMON QUERIES
-- ============================================================================

CREATE INDEX idx_nutrition_facts_calories ON nutrition_facts(calories);
CREATE INDEX idx_meals_user_date ON meals(user_id, meal_date);
CREATE INDEX idx_meal_entries_meal ON meal_entries(meal_id);
CREATE INDEX idx_weight_logs_user_date ON weight_logs(user_id, log_date);
CREATE INDEX idx_daily_summary_user_date ON daily_nutrition_summary(user_id, summary_date);