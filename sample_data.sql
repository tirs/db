-- Sample Data for FatSecret-like Nutrition Database
-- Use this to populate initial data for testing

USE u280406916_nutrition;

-- ============================================================================
-- FOOD CATEGORIES
-- ============================================================================

INSERT INTO food_categories (name, description) VALUES
('Vegetables', 'Fresh vegetables and legumes'),
('Fruits', 'Fresh fruits and berries'),
('Grains & Cereals', 'Bread, rice, pasta, cereals'),
('Meat & Poultry', 'Beef, chicken, turkey, pork'),
('Fish & Seafood', 'Fish, shrimp, shellfish'),
('Dairy & Eggs', 'Milk, cheese, yogurt, eggs'),
('Nuts & Seeds', 'Nuts, seeds, nut butters'),
('Oils & Fats', 'Oils, butter, margarine'),
('Beverages', 'Water, juice, coffee, tea'),
('Condiments & Sauces', 'Sauces, dressings, condiments'),
('Snacks', 'Chips, crackers, bars'),
('Desserts', 'Cakes, cookies, ice cream'),
('Prepared Foods', 'Ready-to-eat meals, frozen foods'),
('Fast Food', 'Restaurant and fast food items');

-- ============================================================================
-- VEGETABLES
-- ============================================================================

INSERT INTO foods (category_id, name, description, brand, serving_size, serving_weight_g, data_source, is_verified)
VALUES
(1, 'Broccoli, raw', 'Fresh raw broccoli florets', NULL, '1 cup (91g)', 91, 'USDA', TRUE),
(1, 'Carrot, raw', 'Fresh raw carrot', NULL, '1 medium (61g)', 61, 'USDA', TRUE),
(1, 'Spinach, raw', 'Fresh raw spinach leaves', NULL, '1 cup (30g)', 30, 'USDA', TRUE),
(1, 'Tomato, raw', 'Fresh ripe tomato', NULL, '1 medium (123g)', 123, 'USDA', TRUE),
(1, 'Lettuce, raw', 'Romaine lettuce leaves', NULL, '2 cups (94g)', 94, 'USDA', TRUE),
(1, 'Bell Pepper, red', 'Fresh red bell pepper', NULL, '1 large (186g)', 186, 'USDA', TRUE),
(1, 'Chicken Peas, cooked', 'Cooked chickpeas', NULL, '1 cup (164g)', 164, 'USDA', TRUE),
(1, 'Beans, black cooked', 'Cooked black beans', NULL, '1 cup (172g)', 172, 'USDA', TRUE);

-- ============================================================================
-- FRUITS
-- ============================================================================

INSERT INTO foods (category_id, name, description, brand, serving_size, serving_weight_g, data_source, is_verified)
VALUES
(2, 'Apple, medium', 'Raw medium apple with skin', NULL, '1 medium (182g)', 182, 'USDA', TRUE),
(2, 'Banana, medium', 'Raw medium banana', NULL, '1 medium (118g)', 118, 'USDA', TRUE),
(2, 'Orange, medium', 'Raw medium orange', NULL, '1 medium (131g)', 131, 'USDA', TRUE),
(2, 'Strawberry, fresh', 'Fresh raw strawberries', NULL, '1 cup (152g)', 152, 'USDA', TRUE),
(2, 'Blueberry, fresh', 'Fresh raw blueberries', NULL, '1 cup (148g)', 148, 'USDA', TRUE),
(2, 'Grapes, red', 'Raw red grapes', NULL, '1 cup (160g)', 160, 'USDA', TRUE),
(2, 'Watermelon', 'Fresh watermelon pieces', NULL, '1 cup (152g)', 152, 'USDA', TRUE);

-- ============================================================================
-- GRAINS & CEREALS
-- ============================================================================

INSERT INTO foods (category_id, name, description, brand, serving_size, serving_weight_g, data_source, is_verified)
VALUES
(3, 'Bread, whole wheat', 'Whole wheat bread slice', NULL, '1 slice (28g)', 28, 'USDA', TRUE),
(3, 'Brown Rice, cooked', 'Cooked brown rice', NULL, '1 cup (195g)', 195, 'USDA', TRUE),
(3, 'Pasta, whole wheat cooked', 'Cooked whole wheat pasta', NULL, '1 cup (174g)', 174, 'USDA', TRUE),
(3, 'Oatmeal, dry', 'Dry oatmeal', NULL, '1 cup (150g)', 150, 'USDA', TRUE),
(3, 'Cereal, cornflakes', 'Cornflakes cereal', NULL, '1 cup (28g)', 28, 'USDA', TRUE),
(3, 'White Rice, cooked', 'Cooked white rice', NULL, '1 cup (158g)', 158, 'USDA', TRUE);

-- ============================================================================
-- MEAT & POULTRY
-- ============================================================================

INSERT INTO foods (category_id, name, description, brand, serving_size, serving_weight_g, data_source, is_verified)
VALUES
(4, 'Chicken Breast, cooked', 'Cooked boneless skinless chicken breast', NULL, '3 oz (85g)', 85, 'USDA', TRUE),
(4, 'Ground Beef, lean', 'Cooked lean ground beef', NULL, '3 oz (85g)', 85, 'USDA', TRUE),
(4, 'Pork Tenderloin, cooked', 'Cooked pork tenderloin', NULL, '3 oz (85g)', 85, 'USDA', TRUE),
(4, 'Turkey Breast, cooked', 'Cooked turkey breast', NULL, '3 oz (85g)', 85, 'USDA', TRUE),
(4, 'Bacon, crispy', 'Cooked crispy bacon', NULL, '2 slices (16g)', 16, 'USDA', TRUE),
(4, 'Beef Steak', 'Cooked beef sirloin steak', NULL, '3 oz (85g)', 85, 'USDA', TRUE);

-- ============================================================================
-- FISH & SEAFOOD
-- ============================================================================

INSERT INTO foods (category_id, name, description, brand, serving_size, serving_weight_g, data_source, is_verified)
VALUES
(5, 'Salmon, cooked', 'Cooked Atlantic salmon', NULL, '3 oz (85g)', 85, 'USDA', TRUE),
(5, 'Tuna, canned', 'Canned tuna in water, drained', NULL, '3 oz (85g)', 85, 'USDA', TRUE),
(5, 'Shrimp, cooked', 'Cooked large shrimp', NULL, '3 oz (85g)', 85, 'USDA', TRUE),
(5, 'Cod, cooked', 'Cooked Atlantic cod', NULL, '3 oz (85g)', 85, 'USDA', TRUE),
(5, 'Tilapia, cooked', 'Cooked tilapia fillet', NULL, '3 oz (85g)', 85, 'USDA', TRUE);

-- ============================================================================
-- DAIRY & EGGS
-- ============================================================================

INSERT INTO foods (category_id, name, description, brand, serving_size, serving_weight_g, data_source, is_verified)
VALUES
(6, 'Egg, whole cooked', 'Boiled large egg', NULL, '1 egg (50g)', 50, 'USDA', TRUE),
(6, 'Milk, 2% fat', '2% reduced fat milk', NULL, '1 cup (244g)', 244, 'USDA', TRUE),
(6, 'Yogurt, plain', 'Plain nonfat yogurt', NULL, '1 cup (227g)', 227, 'USDA', TRUE),
(6, 'Cheese, cheddar', 'Cheddar cheese', NULL, '1 oz (28g)', 28, 'USDA', TRUE),
(6, 'Cottage Cheese', 'Cottage cheese 2% fat', NULL, '1/2 cup (113g)', 113, 'USDA', TRUE);

-- ============================================================================
-- NUTRITION FACTS - Sample Foods
-- ============================================================================

INSERT INTO nutrition_facts (food_id, calories, protein_g, carbohydrates_g, fiber_g, sugar_g, fat_g, saturated_fat_g, cholesterol_mg, sodium_mg, potassium_mg, calcium_mg, iron_mg, vitamin_c_mg)
VALUES
-- Broccoli
(1, 34, 2.8, 7, 1.5, 1.5, 0.4, 0.1, 0, 64, 288, 47, 0.7, 89),
-- Carrot
(2, 25, 0.6, 6, 1.7, 3.6, 0.1, 0, 0, 42, 195, 20, 0.3, 6),
-- Spinach
(3, 7, 0.9, 1.1, 0.7, 0.1, 0.1, 0, 0, 24, 167, 30, 0.8, 8),
-- Tomato
(4, 22, 1.1, 5, 1.5, 3.2, 0.2, 0, 0, 12, 292, 12, 0.3, 17),
-- Lettuce
(5, 15, 1.2, 3, 2, 0.6, 0.3, 0.1, 0, 8, 244, 36, 0.4, 6),
-- Bell Pepper Red
(6, 37, 1.5, 9, 1.9, 6.3, 0.3, 0, 0, 3, 314, 11, 0.3, 190),
-- Chickpeas Cooked
(7, 269, 15, 45, 12, 8, 4.3, 0.4, 0, 191, 477, 80, 4.3, 1),
-- Black Beans Cooked
(8, 132, 8.9, 24, 6.4, 0.3, 0.5, 0.1, 0, 2, 305, 46, 1.8, 1),
-- Apple Medium
(9, 95, 0.5, 25, 4.4, 19, 0.3, 0.1, 0, 2, 195, 11, 0.2, 5),
-- Banana Medium
(10, 105, 1.3, 27, 3.1, 14, 0.3, 0.1, 0, 1, 358, 5, 0.3, 8),
-- Orange Medium
(11, 62, 1.2, 15, 3, 12, 0.3, 0, 0, 0, 237, 52, 0.1, 53),
-- Strawberry
(12, 49, 1, 12, 3, 7, 0.5, 0.1, 0, 2, 233, 27, 0.6, 98),
-- Blueberry
(13, 57, 0.7, 14, 2.4, 10, 0.3, 0, 0, 1, 148, 9, 0.3, 10),
-- Grapes Red
(14, 104, 1.1, 28, 1.5, 23, 0.2, 0.1, 0, 2, 191, 15, 0.4, 3),
-- Watermelon
(15, 46, 0.9, 12, 0.6, 9, 0.2, 0, 0, 28, 170, 11, 0.2, 12),
-- Bread Whole Wheat
(16, 80, 4, 14, 2.4, 1, 1, 0.2, 0, 149, 71, 20, 1.4, 0),
-- Brown Rice Cooked
(17, 215, 5, 45, 3.5, 0.5, 1.8, 0.4, 0, 10, 168, 20, 0.8, 0),
-- Pasta Whole Wheat Cooked
(18, 174, 7.4, 37, 6.3, 0.5, 0.8, 0.2, 0, 7, 61, 21, 2.5, 0),
-- Oatmeal Dry
(19, 389, 17, 66, 11, 0, 6.9, 1.2, 0, 2, 429, 55, 5.7, 0),
-- Cornflakes Cereal
(20, 100, 2, 24, 1, 2, 0.3, 0, 0, 279, 21, 0, 1.8, 0),
-- White Rice Cooked
(21, 206, 4.3, 45, 0.6, 0.1, 0.3, 0.1, 0, 2, 55, 16, 0.2, 0),
-- Chicken Breast Cooked
(22, 165, 31, 0, 0, 0, 3.6, 1, 85, 74, 220, 15, 1.1, 0),
-- Ground Beef Lean Cooked
(23, 215, 23, 0, 0, 0, 12, 5, 75, 75, 287, 19, 2.6, 0),
-- Pork Tenderloin Cooked
(24, 139, 26, 0, 0, 0, 4.1, 1.4, 73, 55, 382, 21, 1, 0),
-- Turkey Breast Cooked
(25, 134, 25, 0, 0, 0, 3, 1, 59, 54, 212, 19, 1.3, 0),
-- Bacon Crispy
(26, 90, 6, 0.4, 0, 0, 7, 2.3, 16, 310, 57, 4, 0.3, 0),
-- Beef Steak Cooked
(27, 271, 25, 0, 0, 0, 19, 7.6, 88, 75, 318, 19, 2.1, 0),
-- Salmon Cooked
(28, 280, 19, 0, 0, 0, 21, 4.9, 55, 75, 363, 13, 0.8, 0),
-- Tuna Canned in Water
(29, 99, 22, 0, 0, 0, 0.7, 0.2, 42, 320, 201, 17, 1.3, 0),
-- Shrimp Cooked
(30, 84, 18, 0, 0, 0, 0.9, 0.3, 166, 190, 155, 54, 0.3, 2),
-- Cod Cooked
(31, 82, 18, 0, 0, 0, 0.7, 0.1, 47, 77, 413, 12, 0.4, 0),
-- Tilapia Cooked
(32, 128, 26, 0, 0, 0, 2.7, 0.9, 56, 75, 302, 13, 0.7, 0),
-- Egg Whole Cooked
(33, 78, 6.3, 0.6, 0, 0.1, 5.3, 1.6, 212, 62, 63, 50, 0.9, 0),
-- Milk 2% Fat
(34, 122, 8, 12, 0, 12, 4.8, 3, 18, 195, 366, 285, 0.1, 2),
-- Yogurt Plain
(35, 100, 3.5, 7, 0, 7, 3.3, 2, 12, 75, 208, 448, 0.1, 2),
-- Cheese Cheddar
(36, 402, 25, 1.3, 0, 0.7, 33, 21, 105, 621, 98, 721, 0.7, 0),
-- Cottage Cheese
(37, 110, 14, 4, 0, 4, 5, 3, 17, 390, 142, 138, 0.2, 0);

-- ============================================================================
-- SAMPLE USERS
-- ============================================================================

INSERT INTO users (email, username, password_hash, first_name, last_name, is_active)
VALUES
('john.doe@example.com', 'johndoe', 'hashed_password_1', 'John', 'Doe', TRUE),
('jane.smith@example.com', 'janesmith', 'hashed_password_2', 'Jane', 'Smith', TRUE),
('mike.wilson@example.com', 'mikewilson', 'hashed_password_3', 'Mike', 'Wilson', TRUE);

-- ============================================================================
-- USER PROFILES
-- ============================================================================

INSERT INTO user_profiles (user_id, age, gender, height_cm, weight_kg, goal, activity_level)
VALUES
(1, 30, 'M', 180, 85, 'Weight Loss', 'Moderate Exercise'),
(2, 28, 'F', 165, 65, 'Muscle Gain', 'Regular Exercise'),
(3, 35, 'M', 175, 90, 'Maintenance', 'Light Exercise');

-- ============================================================================
-- NUTRITION GOALS
-- ============================================================================

INSERT INTO nutrition_goals (user_id, goal_type, target_calories, target_protein_g, target_carbohydrates_g, target_fat_g, target_fiber_g, start_date, end_date)
VALUES
(1, 'Weight Loss', 2000, 150, 200, 65, 30, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 12 WEEK)),
(2, 'Muscle Gain', 2800, 200, 280, 95, 35, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 12 WEEK)),
(3, 'Maintenance', 2400, 180, 240, 80, 30, CURDATE(), NULL);

-- ============================================================================
-- SAMPLE RECIPES
-- ============================================================================

INSERT INTO recipes (user_id, name, description, servings, prep_time_minutes, cook_time_minutes, difficulty_level, is_public)
VALUES
(1, 'Grilled Chicken Salad', 'Fresh garden salad with grilled chicken breast', 1, 15, 15, 'Easy', TRUE),
(1, 'Vegetable Stir Fry', 'Mixed vegetables with brown rice', 2, 10, 20, 'Easy', TRUE),
(2, 'Protein Smoothie Bowl', 'Oatmeal with yogurt, berries and nuts', 1, 5, 0, 'Easy', TRUE);

-- ============================================================================
-- RECIPE INGREDIENTS
-- ============================================================================

INSERT INTO recipe_ingredients (recipe_id, food_id, quantity, unit, sequence_order, notes)
VALUES
-- Grilled Chicken Salad
(1, 22, 150, 'g', 1, 'Grilled chicken breast'),
(1, 5, 200, 'g', 2, 'Mixed lettuce leaves'),
(1, 6, 1, 'medium', 3, 'Red bell pepper, sliced'),
(1, 4, 2, 'medium', 4, 'Cherry tomatoes'),
-- Vegetable Stir Fry
(2, 1, 200, 'g', 1, 'Broccoli florets'),
(2, 2, 200, 'g', 2, 'Carrots, sliced'),
(2, 3, 100, 'g', 3, 'Spinach'),
(2, 17, 200, 'g', 4, 'Cooked brown rice'),
-- Protein Smoothie Bowl
(3, 19, 50, 'g', 1, 'Dry oatmeal'),
(3, 34, 200, 'ml', 2, 'Milk 2%'),
(3, 35, 100, 'g', 3, 'Plain yogurt'),
(3, 12, 150, 'g', 4, 'Fresh strawberries'),
(3, 13, 100, 'g', 5, 'Fresh blueberries');

-- ============================================================================
-- SAMPLE MEALS
-- ============================================================================

INSERT INTO meals (user_id, meal_type, meal_date, notes)
VALUES
(1, 'Breakfast', CURDATE(), 'Good breakfast'),
(1, 'Lunch', CURDATE(), 'Healthy lunch'),
(1, 'Dinner', CURDATE(), NULL),
(2, 'Breakfast', CURDATE(), NULL),
(2, 'Lunch', CURDATE(), 'After workout meal');

-- ============================================================================
-- SAMPLE MEAL ENTRIES
-- ============================================================================

INSERT INTO meal_entries (meal_id, food_id, quantity, unit, calories_consumed, protein_consumed_g, carbs_consumed_g, fat_consumed_g)
VALUES
(1, 19, 50, 'g', 195, 8.5, 33, 3.45),
(1, 34, 244, 'ml', 122, 8, 12, 4.8),
(1, 12, 152, 'g', 49, 1, 12, 0.5),
(2, 22, 150, 'g', 248, 46.5, 0, 5.4),
(2, 5, 150, 'g', 23, 1.8, 4.5, 0.45),
(2, 6, 100, 'g', 20, 0.8, 5, 0.16),
(5, 28, 120, 'g', 336, 22.8, 0, 25.2),
(5, 3, 100, 'g', 7, 0.9, 1.1, 0.1);

-- ============================================================================
-- FAVORITE FOODS
-- ============================================================================

INSERT INTO user_favorite_foods (user_id, food_id)
VALUES
(1, 22),
(1, 28),
(1, 12),
(2, 22),
(2, 28),
(2, 34);

-- ============================================================================
-- WEIGHT LOGS
-- ============================================================================

INSERT INTO weight_logs (user_id, weight_kg, log_date, notes)
VALUES
(1, 85, DATE_SUB(CURDATE(), INTERVAL 14 DAY), 'Starting weight'),
(1, 84.5, DATE_SUB(CURDATE(), INTERVAL 7 DAY), 'Week 1'),
(1, 84, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 'Progress'),
(1, 83.5, CURDATE(), 'This week'),
(2, 65, DATE_SUB(CURDATE(), INTERVAL 14 DAY), 'Starting weight'),
(2, 65.2, DATE_SUB(CURDATE(), INTERVAL 7 DAY), 'Muscle gain expected'),
(2, 65.5, CURDATE(), 'Week 2');

-- ============================================================================
-- EXERCISE LOGS
-- ============================================================================

INSERT INTO exercise_logs (user_id, exercise_type, duration_minutes, calories_burned, exercise_date, notes)
VALUES
(1, 'Running', 30, 300, CURDATE(), 'Morning run'),
(1, 'Weight Training', 45, 350, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 'Upper body'),
(2, 'Weight Training', 60, 450, CURDATE(), 'Full body workout'),
(2, 'Cardio', 20, 200, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 'Treadmill');

-- ============================================================================
-- FOOD BARCODES
-- ============================================================================

INSERT INTO food_barcodes (food_id, barcode_code, barcode_type)
VALUES
(22, '012345678905', 'UPC-A'),
(28, '012345678912', 'UPC-A'),
(34, '012345678929', 'UPC-A'),
(35, '012345678936', 'UPC-A'),
(36, '012345678943', 'UPC-A');