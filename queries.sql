-- Common Queries and Reports for Nutrition Database

USE nutrition_tracker;

-- ============================================================================
-- USER QUERIES
-- ============================================================================

-- Get user profile with goals
SELECT 
    u.user_id, u.username, u.email,
    up.age, up.gender, up.height_cm, up.weight_kg,
    up.goal, up.activity_level,
    ng.goal_type, ng.target_calories, ng.target_protein_g
FROM users u
LEFT JOIN user_profiles up ON u.user_id = up.user_id
LEFT JOIN nutrition_goals ng ON u.user_id = ng.user_id AND ng.end_date IS NULL
WHERE u.user_id = 1;

-- Get active users with their latest weight
SELECT 
    u.user_id, u.username,
    wl.weight_kg, wl.log_date,
    ROW_NUMBER() OVER (PARTITION BY u.user_id ORDER BY wl.log_date DESC) as rn
FROM users u
LEFT JOIN weight_logs wl ON u.user_id = wl.user_id
WHERE u.is_active = TRUE
ORDER BY u.user_id, wl.log_date DESC;

-- ============================================================================
-- NUTRITION TRACKING QUERIES
-- ============================================================================

-- Get today's nutrition summary for a user
SELECT 
    u.username,
    dns.summary_date,
    dns.total_calories,
    dns.total_protein_g,
    dns.total_carbohydrates_g,
    dns.total_fat_g,
    dns.total_fiber_g,
    ng.target_calories,
    (ng.target_calories - dns.total_calories) as calories_remaining
FROM daily_nutrition_summary dns
JOIN users u ON dns.user_id = u.user_id
LEFT JOIN nutrition_goals ng ON u.user_id = ng.user_id AND ng.end_date IS NULL
WHERE dns.user_id = 1 AND dns.summary_date = CURDATE();

-- Get weekly nutrition average
SELECT 
    u.username,
    WEEK(dns.summary_date) as week_num,
    YEAR(dns.summary_date) as year,
    ROUND(AVG(dns.total_calories), 0) as avg_calories,
    ROUND(AVG(dns.total_protein_g), 2) as avg_protein,
    ROUND(AVG(dns.total_carbohydrates_g), 2) as avg_carbs,
    ROUND(AVG(dns.total_fat_g), 2) as avg_fat,
    COUNT(*) as days_logged
FROM daily_nutrition_summary dns
JOIN users u ON dns.user_id = u.user_id
WHERE dns.user_id = 1 
    AND dns.summary_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY u.user_id, WEEK(dns.summary_date), YEAR(dns.summary_date)
ORDER BY YEAR(dns.summary_date) DESC, WEEK(dns.summary_date) DESC;

-- Get today's meals breakdown
SELECT 
    m.meal_type,
    GROUP_CONCAT(f.name, ' (', me.quantity, 'g)' SEPARATOR ', ') as foods,
    SUM(me.calories_consumed) as total_calories,
    SUM(me.protein_consumed_g) as total_protein,
    SUM(me.carbs_consumed_g) as total_carbs,
    SUM(me.fat_consumed_g) as total_fat,
    COUNT(*) as food_count
FROM meals m
JOIN meal_entries me ON m.meal_id = me.meal_id
JOIN foods f ON me.food_id = f.food_id
WHERE m.user_id = 1 AND m.meal_date = CURDATE()
GROUP BY m.meal_id, m.meal_type
ORDER BY m.meal_type;

-- ============================================================================
-- FOOD DATABASE QUERIES
-- ============================================================================

-- Search foods by full-text index
SELECT 
    f.food_id, f.name, f.brand, f.category_id,
    fc.name as category,
    nf.calories, nf.protein_g, nf.carbohydrates_g, nf.fat_g,
    ROUND(CHAR_LENGTH(f.name) - CHAR_LENGTH(REPLACE(f.name, ' ', '')) + 1) as word_count
FROM foods f
JOIN food_categories fc ON f.category_id = fc.category_id
JOIN nutrition_facts nf ON f.food_id = nf.food_id
WHERE MATCH(f.name, f.brand, f.description) AGAINST('chicken' IN BOOLEAN MODE)
ORDER BY f.is_verified DESC, f.name
LIMIT 20;

-- Get high-protein foods
SELECT 
    f.name, f.brand,
    fc.name as category,
    nf.calories, nf.protein_g,
    ROUND((nf.protein_g * 4) / nf.calories * 100, 1) as protein_percentage
FROM foods f
JOIN food_categories fc ON f.category_id = fc.category_id
JOIN nutrition_facts nf ON f.food_id = nf.food_id
WHERE nf.protein_g > 20
    AND nf.calories > 0
ORDER BY (nf.protein_g / nf.calories) DESC
LIMIT 20;

-- Get low-calorie options by category
SELECT 
    fc.name as category,
    f.name, f.brand,
    nf.calories, nf.protein_g,
    ROW_NUMBER() OVER (PARTITION BY fc.category_id ORDER BY nf.calories ASC) as rank
FROM foods f
JOIN food_categories fc ON f.category_id = fc.category_id
JOIN nutrition_facts nf ON f.food_id = nf.food_id
WHERE nf.calories < 100
HAVING rank <= 5;

-- Foods scanned by barcode
SELECT 
    fb.barcode_code,
    f.name, f.brand,
    fc.name as category,
    nf.calories, nf.protein_g
FROM food_barcodes fb
JOIN foods f ON fb.food_id = f.food_id
JOIN food_categories fc ON f.category_id = fc.category_id
JOIN nutrition_facts nf ON f.food_id = nf.food_id
WHERE fb.barcode_code = '012345678905';

-- ============================================================================
-- RECIPE QUERIES
-- ============================================================================

-- Get recipe with calculated nutrition
SELECT 
    r.recipe_id, r.name, r.description,
    r.servings, r.prep_time_minutes, r.cook_time_minutes,
    rnc.total_calories, rnc.total_protein_g, rnc.total_carbohydrates_g,
    rnc.total_fat_g, rnc.total_fiber_g,
    rnc.per_serving_calories, rnc.per_serving_protein_g,
    COUNT(ri.ingredient_id) as ingredient_count
FROM recipes r
LEFT JOIN recipe_nutrition_calculated rnc ON r.recipe_id = rnc.recipe_id
LEFT JOIN recipe_ingredients ri ON r.recipe_id = ri.recipe_id
WHERE r.recipe_id = 1
GROUP BY r.recipe_id;

-- Get recipe ingredients with nutrition details
SELECT 
    ri.recipe_id,
    ri.sequence_order,
    f.name, f.brand,
    ri.quantity, ri.unit,
    nf.calories, nf.protein_g, nf.carbohydrates_g, nf.fat_g,
    (nf.calories * ri.quantity / 100) as calories_in_recipe,
    ri.notes
FROM recipe_ingredients ri
JOIN foods f ON ri.food_id = f.food_id
JOIN nutrition_facts nf ON f.food_id = nf.food_id
WHERE ri.recipe_id = 1
ORDER BY ri.sequence_order;

-- User's favorite recipes
SELECT 
    fr.favorite_recipe_id,
    r.name, r.description,
    rnc.per_serving_calories,
    rnc.total_calories,
    COUNT(ri.ingredient_id) as ingredients,
    fr.created_at
FROM user_favorite_recipes fr
JOIN recipes r ON fr.recipe_id = r.recipe_id
LEFT JOIN recipe_nutrition_calculated rnc ON r.recipe_id = rnc.recipe_id
LEFT JOIN recipe_ingredients ri ON r.recipe_id = ri.recipe_id
WHERE fr.user_id = 1
GROUP BY r.recipe_id
ORDER BY fr.created_at DESC;

-- ============================================================================
-- EXERCISE AND WEIGHT TRACKING
-- ============================================================================

-- User's weight progress over time
SELECT 
    wl.log_date,
    wl.weight_kg,
    LAG(wl.weight_kg) OVER (ORDER BY wl.log_date) as prev_weight,
    wl.weight_kg - LAG(wl.weight_kg) OVER (ORDER BY wl.log_date) as daily_change,
    AVG(wl.weight_kg) OVER (
        ORDER BY wl.log_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7day,
    wl.notes
FROM weight_logs wl
WHERE wl.user_id = 1
    AND wl.log_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
ORDER BY wl.log_date;

-- Weekly weight change summary
SELECT 
    YEAR(wl.log_date) as year,
    WEEK(wl.log_date) as week_num,
    MIN(wl.weight_kg) as min_weight,
    MAX(wl.weight_kg) as max_weight,
    ROUND(AVG(wl.weight_kg), 2) as avg_weight,
    ROUND(MAX(wl.weight_kg) - MIN(wl.weight_kg), 2) as weekly_fluctuation,
    COUNT(*) as weight_entries
FROM weight_logs wl
WHERE wl.user_id = 1
GROUP BY YEAR(wl.log_date), WEEK(wl.log_date)
ORDER BY YEAR(wl.log_date) DESC, WEEK(wl.log_date) DESC;

-- Recent exercise activity
SELECT 
    el.exercise_date,
    GROUP_CONCAT(
        CONCAT(el.exercise_type, ' (', el.duration_minutes, 'min, ', 
               COALESCE(el.calories_burned, 0), 'cal)')
        SEPARATOR ', '
    ) as activities,
    SUM(COALESCE(el.calories_burned, 0)) as total_calories_burned,
    COUNT(*) as exercise_count
FROM exercise_logs el
WHERE el.user_id = 1
    AND el.exercise_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY el.exercise_date
ORDER BY el.exercise_date DESC;

-- ============================================================================
-- FAVORITES AND RECOMMENDATIONS
-- ============================================================================

-- User's favorite foods nutrition comparison
SELECT 
    ufl.favorite_id,
    f.name, f.brand,
    fc.name as category,
    nf.calories, nf.protein_g, nf.carbohydrates_g, nf.fat_g, nf.fiber_g,
    COUNT(DISTINCT me.meal_id) as times_consumed
FROM user_favorite_foods ufl
JOIN foods f ON ufl.food_id = f.food_id
JOIN food_categories fc ON f.category_id = fc.category_id
JOIN nutrition_facts nf ON f.food_id = nf.food_id
LEFT JOIN meal_entries me ON f.food_id = me.food_id
    AND me.meal_id IN (SELECT meal_id FROM meals WHERE user_id = ufl.user_id)
WHERE ufl.user_id = 1
GROUP BY ufl.favorite_id
ORDER BY ufl.created_at DESC;

-- Most frequently consumed foods
SELECT 
    f.food_id, f.name, f.brand,
    fc.name as category,
    COUNT(DISTINCT me.meal_id) as times_consumed,
    SUM(me.quantity) as total_quantity_consumed_g,
    ROUND(AVG(me.quantity), 2) as avg_serving_size
FROM meal_entries me
JOIN foods f ON me.food_id = f.food_id
JOIN food_categories fc ON f.category_id = fc.category_id
JOIN meals m ON me.meal_id = m.meal_id
WHERE m.user_id = 1
GROUP BY f.food_id
ORDER BY times_consumed DESC
LIMIT 20;

-- ============================================================================
-- COMPLIANCE AND GOAL TRACKING
-- ============================================================================

-- Goal adherence report
SELECT 
    dns.summary_date,
    ng.target_calories,
    dns.total_calories,
    ROUND(((dns.total_calories / ng.target_calories) * 100), 1) as calorie_adherence_pct,
    ng.target_protein_g,
    dns.total_protein_g,
    ROUND(((dns.total_protein_g / ng.target_protein_g) * 100), 1) as protein_adherence_pct,
    CASE 
        WHEN dns.total_calories > ng.target_calories * 1.1 THEN 'Over'
        WHEN dns.total_calories < ng.target_calories * 0.9 THEN 'Under'
        ELSE 'On Target'
    END as calorie_status
FROM daily_nutrition_summary dns
JOIN nutrition_goals ng ON dns.user_id = ng.user_id 
    AND ng.end_date IS NULL
WHERE dns.user_id = 1
    AND dns.summary_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY dns.summary_date DESC;

-- Goal completion summary
SELECT 
    ng.goal_id, ng.goal_type,
    ng.start_date, ng.end_date,
    COUNT(DISTINCT dns.summary_date) as days_tracked,
    ROUND(AVG(dns.total_calories), 0) as avg_calories,
    MIN(wl.weight_kg) as starting_weight,
    MAX(wl.weight_kg) as current_weight,
    MAX(wl.weight_kg) - MIN(wl.weight_kg) as total_change
FROM nutrition_goals ng
LEFT JOIN daily_nutrition_summary dns ON ng.user_id = dns.user_id
    AND dns.summary_date BETWEEN ng.start_date AND COALESCE(ng.end_date, CURDATE())
LEFT JOIN weight_logs wl ON ng.user_id = wl.user_id
    AND wl.log_date BETWEEN ng.start_date AND COALESCE(ng.end_date, CURDATE())
WHERE ng.user_id = 1
GROUP BY ng.goal_id
ORDER BY ng.start_date DESC;

-- ============================================================================
-- AUDIT AND DATA QUALITY
-- ============================================================================

-- Audit trail for a specific user
SELECT 
    al.audit_id,
    al.action,
    al.table_name,
    al.record_id,
    al.created_at,
    al.old_values,
    al.new_values
FROM audit_logs al
WHERE al.user_id = 1
ORDER BY al.created_at DESC
LIMIT 100;

-- Foods without complete nutrition data
SELECT 
    f.food_id, f.name, f.brand,
    CASE 
        WHEN nf.nutrition_id IS NULL THEN 'No nutrition data'
        WHEN nf.protein_g IS NULL OR nf.carbohydrates_g IS NULL OR nf.fat_g IS NULL THEN 'Incomplete'
        ELSE 'Complete'
    END as data_status,
    COUNT(DISTINCT fb.barcode_id) as barcode_count,
    COUNT(DISTINCT me.entry_id) as times_used
FROM foods f
LEFT JOIN nutrition_facts nf ON f.food_id = nf.food_id
LEFT JOIN food_barcodes fb ON f.food_id = fb.food_id
LEFT JOIN meal_entries me ON f.food_id = me.food_id
GROUP BY f.food_id
HAVING data_status IN ('No nutrition data', 'Incomplete')
ORDER BY times_used DESC;

-- ============================================================================
-- REPORTING AND ANALYTICS
-- ============================================================================

-- Monthly nutrition report
SELECT 
    YEAR(dns.summary_date) as year,
    MONTH(dns.summary_date) as month,
    COUNT(DISTINCT dns.summary_date) as days_tracked,
    ROUND(AVG(dns.total_calories), 0) as avg_daily_calories,
    ROUND(AVG(dns.total_protein_g), 1) as avg_daily_protein,
    ROUND(AVG(dns.total_carbohydrates_g), 1) as avg_daily_carbs,
    ROUND(AVG(dns.total_fat_g), 1) as avg_daily_fat,
    MIN(wl.weight_kg) as min_weight,
    MAX(wl.weight_kg) as max_weight
FROM daily_nutrition_summary dns
LEFT JOIN weight_logs wl ON dns.user_id = wl.user_id
    AND wl.log_date BETWEEN 
        DATE_FORMAT(dns.summary_date, '%Y-%m-01')
        AND LAST_DAY(dns.summary_date)
WHERE dns.user_id = 1
GROUP BY YEAR(dns.summary_date), MONTH(dns.summary_date)
ORDER BY year DESC, month DESC;

-- Nutrient distribution analysis
SELECT 
    dns.summary_date,
    dns.total_calories,
    ROUND((dns.total_protein_g * 4) / dns.total_calories * 100, 1) as protein_pct,
    ROUND((dns.total_carbohydrates_g * 4) / dns.total_calories * 100, 1) as carb_pct,
    ROUND((dns.total_fat_g * 9) / dns.total_calories * 100, 1) as fat_pct
FROM daily_nutrition_summary dns
WHERE dns.user_id = 1
    AND dns.summary_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY dns.summary_date DESC;