# FatSecret-like Database Setup Script
# Windows PowerShell setup for MySQL database initialization

param(
    [string]$MySQLPath = "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
    [string]$DatabaseName = "u280406916_nutrition",
    [string]$Username = "u280406916_nutrition",
    [SecureString]$Password = (ConvertTo-SecureString "Mysqlnutrition200" -AsPlainText -Force),
    [string]$DatabaseHost = "srv1539.hstgr.io",
    [int]$Port = 3306
)

# Color output functions
function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

# Convert SecureString to plain text for command-line tools
function ConvertSecureStringToPlainText {
    param([SecureString]$SecureString)
    if ($null -eq $SecureString -or $SecureString.Length -eq 0) {
        return $null
    }
    $ptr = [System.Runtime.InteropServices.Marshal]::SecureStringToGlobalAllocUnicode($SecureString)
    [System.Runtime.InteropServices.Marshal]::PtrToStringUni($ptr)
    [System.Runtime.InteropServices.Marshal]::ZeroFreeGlobalAllocUnicode($ptr)
}

# Verify MySQL is installed
if (-not (Test-Path $MySQLPath)) {
    Write-Error-Custom "MySQL not found at $MySQLPath"
    Write-Info "Please install MySQL or specify correct path using -MySQLPath parameter"
    exit 1
}

Write-Info "Starting database setup..."
Write-Info "Database: $DatabaseName"
Write-Info "Host: ${DatabaseHost}:$Port"

# Create database
Write-Info "Creating database..."
$createDbSQL = "CREATE DATABASE IF NOT EXISTS $DatabaseName CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
$plainPassword = ConvertSecureStringToPlainText -SecureString $Password
$createDbSQL | & $MySQLPath -h $DatabaseHost -P $Port -u $Username $(if ($plainPassword) { "-p$plainPassword" }) 2>&1 | Out-Null

if ($LASTEXITCODE -ne 0) {
    Write-Error-Custom "Failed to create database"
    exit 1
}
Write-Success "Database created"

# Execute schema
Write-Info "Executing schema..."
$schemaPath = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "schema.sql"

if (-not (Test-Path $schemaPath)) {
    Write-Error-Custom "schema.sql not found at $schemaPath"
    exit 1
}

$schemaContent = Get-Content -Path $schemaPath -Raw
$schemaContent | & $MySQLPath -h $DatabaseHost -P $Port -u $Username $(if ($plainPassword) { "-p$plainPassword" }) $DatabaseName 2>&1 | Out-Null

if ($LASTEXITCODE -ne 0) {
    Write-Error-Custom "Failed to execute schema"
    exit 1
}
Write-Success "Schema created successfully"

# Create stored procedures
Write-Info "Creating stored procedures..."

$storedProcsSQL = @"
USE $DatabaseName;

DELIMITER `$`$

CREATE PROCEDURE sp_add_meal_entry(
    IN p_user_id INT,
    IN p_meal_type VARCHAR(50),
    IN p_meal_date DATE,
    IN p_food_id INT,
    IN p_quantity DECIMAL(10,2),
    IN p_unit VARCHAR(50)
)
BEGIN
    DECLARE v_meal_id INT;
    DECLARE v_nutrition_id INT;
    DECLARE v_calories DECIMAL(10,2);
    DECLARE v_protein DECIMAL(10,2);
    DECLARE v_carbs DECIMAL(10,2);
    DECLARE v_fat DECIMAL(10,2);

    SELECT meal_id INTO v_meal_id
    FROM meals
    WHERE user_id = p_user_id AND meal_date = p_meal_date AND meal_type = p_meal_type
    LIMIT 1;

    IF v_meal_id IS NULL THEN
        INSERT INTO meals (user_id, meal_type, meal_date)
        VALUES (p_user_id, p_meal_type, p_meal_date);
        SET v_meal_id = LAST_INSERT_ID();
    END IF;

    SELECT nutrition_id, calories, protein_g, carbohydrates_g, fat_g
    INTO v_nutrition_id, v_calories, v_protein, v_carbs, v_fat
    FROM nutrition_facts
    WHERE food_id = p_food_id;

    INSERT INTO meal_entries (
        meal_id, food_id, quantity, unit,
        calories_consumed, protein_consumed_g, carbs_consumed_g, fat_consumed_g
    ) VALUES (
        v_meal_id, p_food_id, p_quantity, p_unit,
        v_calories * (p_quantity / 100),
        v_protein * (p_quantity / 100),
        v_carbs * (p_quantity / 100),
        v_fat * (p_quantity / 100)
    );

    CALL sp_update_daily_summary(p_user_id, p_meal_date);
END`$`$

CREATE PROCEDURE sp_update_daily_summary(
    IN p_user_id INT,
    IN p_summary_date DATE
)
BEGIN
    DECLARE v_total_calories DECIMAL(10,2);
    DECLARE v_total_protein DECIMAL(10,2);
    DECLARE v_total_carbs DECIMAL(10,2);
    DECLARE v_total_fiber DECIMAL(10,2);
    DECLARE v_total_sugar DECIMAL(10,2);
    DECLARE v_total_fat DECIMAL(10,2);
    DECLARE v_total_sat_fat DECIMAL(10,2);
    DECLARE v_total_sodium DECIMAL(10,2);

    SELECT
        COALESCE(SUM(me.calories_consumed), 0),
        COALESCE(SUM(me.protein_consumed_g), 0),
        COALESCE(SUM(me.carbs_consumed_g), 0),
        COALESCE(SUM(COALESCE(nf.fiber_g, 0) * (me.quantity / 100)), 0),
        COALESCE(SUM(COALESCE(nf.sugar_g, 0) * (me.quantity / 100)), 0),
        COALESCE(SUM(me.fat_consumed_g), 0),
        COALESCE(SUM(COALESCE(nf.saturated_fat_g, 0) * (me.quantity / 100)), 0),
        COALESCE(SUM(COALESCE(nf.sodium_mg, 0) * (me.quantity / 100)), 0)
    INTO
        v_total_calories, v_total_protein, v_total_carbs, v_total_fiber,
        v_total_sugar, v_total_fat, v_total_sat_fat, v_total_sodium
    FROM meal_entries me
    JOIN meals m ON me.meal_id = m.meal_id
    LEFT JOIN nutrition_facts nf ON me.food_id = nf.food_id
    WHERE m.user_id = p_user_id AND m.meal_date = p_summary_date;

    INSERT INTO daily_nutrition_summary (
        user_id, summary_date, total_calories, total_protein_g, total_carbohydrates_g,
        total_fiber_g, total_sugar_g, total_fat_g, total_saturated_fat_g, total_sodium_mg
    ) VALUES (
        p_user_id, p_summary_date, v_total_calories, v_total_protein, v_total_carbs,
        v_total_fiber, v_total_sugar, v_total_fat, v_total_sat_fat, v_total_sodium
    )
    ON DUPLICATE KEY UPDATE
        total_calories = v_total_calories,
        total_protein_g = v_total_protein,
        total_carbohydrates_g = v_total_carbs,
        total_fiber_g = v_total_fiber,
        total_sugar_g = v_total_sugar,
        total_fat_g = v_total_fat,
        total_saturated_fat_g = v_total_sat_fat,
        total_sodium_mg = v_total_sodium,
        updated_at = CURRENT_TIMESTAMP;
END`$`$

DELIMITER ;
"@

$storedProcsSQL | & $MySQLPath -h $DatabaseHost -P $Port -u $Username $(if ($plainPassword) { "-p$plainPassword" }) 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Success "Stored procedures created"
} else {
    Write-Error-Custom "Warning: Some stored procedures may have failed"
}

Write-Success "Database setup completed successfully!"
Write-Info "Database name: $DatabaseName"
Write-Info "Connection: $DatabaseHost`:$Port"
Write-Info ""
Write-Info "Next: Load sample data with:"
Write-Info "mysql -h $DatabaseHost -u $Username -p $DatabaseName < sample_data.sql"