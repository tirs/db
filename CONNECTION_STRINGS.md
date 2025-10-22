# Database Connection Strings

Connection strings for various programming languages and frameworks.

## Configuration

**Host:** srv1539.hstgr.io  
**Port:** 3306  
**Database:** u280406916_nutrition  
**User:** u280406916_nutrition  
**Password:** Mysqlnutrition200

---

## Python

### MySQLdb
```python
import MySQLdb

conn = MySQLdb.connect(
    host="srv1539.hstgr.io",
    user="u280406916_nutrition",
    passwd="Mysqlnutrition200",
    db="u280406916_nutrition",
    charset="utf8mb4"
)
```

### mysql-connector-python
```python
import mysql.connector

conn = mysql.connector.connect(
    host="srv1539.hstgr.io",
    user="u280406916_nutrition",
    password="Mysqlnutrition200",
    database="u280406916_nutrition",
    charset="utf8mb4",
    use_unicode=True
)
```

### PyMySQL
```python
import pymysql

conn = pymysql.connect(
    host='srv1539.hstgr.io',
    user='u280406916_nutrition',
    password='Mysqlnutrition200',
    database='u280406916_nutrition',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
```

### SQLAlchemy
```python
from sqlalchemy import create_engine

engine = create_engine(
    'mysql+pymysql://u280406916_nutrition:Mysqlnutrition200@srv1539.hstgr.io/u280406916_nutrition',
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600
)
```

### SQLAlchemy with mysql-connector
```python
engine = create_engine(
    'mysql+mysqlconnector://u280406916_nutrition:Mysqlnutrition200@srv1539.hstgr.io/u280406916_nutrition',
    pool_size=10,
    max_overflow=20
)
```

---

## Node.js

### mysql
```javascript
const mysql = require('mysql');

const connection = mysql.createConnection({
    host: 'srv1539.hstgr.io',
    user: 'u280406916_nutrition',
    password: 'Mysqlnutrition200',
    database: 'u280406916_nutrition',
    charset: 'utf8mb4'
});
```

### mysql2/promise
```javascript
const mysql = require('mysql2/promise');

const pool = mysql.createPool({
    host: 'srv1539.hstgr.io',
    user: 'u280406916_nutrition',
    password: 'Mysqlnutrition200',
    database: 'u280406916_nutrition',
    charset: 'utf8mb4',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});
```

### sequelize
```javascript
const Sequelize = require('sequelize');

const sequelize = new Sequelize(
    'u280406916_nutrition',
    'u280406916_nutrition',
    'Mysqlnutrition200',
    {
        host: 'srv1539.hstgr.io',
        port: 3306,
        dialect: 'mysql',
        charset: 'utf8mb4',
        dialectOptions: {
            charset: 'utf8mb4_unicode_ci'
        },
        pool: {
            max: 10,
            min: 0,
            acquire: 30000,
            idle: 10000
        }
    }
);
```

### typeorm
```typescript
import { createConnection } from "typeorm";

const connection = await createConnection({
    type: "mysql",
    host: "srv1539.hstgr.io",
    port: 3306,
    username: "u280406916_nutrition",
    password: "Mysqlnutrition200",
    database: "u280406916_nutrition",
    synchronize: false,
    logging: false,
    charset: "utf8mb4"
});
```

### prisma
```prisma
datasource db {
    provider = "mysql"
    url = "mysql://u280406916_nutrition:Mysqlnutrition200@srv1539.hstgr.io:3306/u280406916_nutrition"
}

model User {
    user_id Int @id @default(autoincrement())
    email String @unique
    username String @unique
    password_hash String
    first_name String?
    last_name String?
    created_at DateTime @default(now())
    updated_at DateTime @updatedAt
    is_active Boolean @default(true)
}
```

---

## PHP

### MySQLi (Procedural)
```php
<?php
$conn = mysqli_connect("srv1539.hstgr.io", "u280406916_nutrition", "Mysqlnutrition200", "u280406916_nutrition");

if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

mysqli_set_charset($conn, "utf8mb4");
```

### MySQLi (Object-Oriented)
```php
<?php
$conn = new mysqli("srv1539.hstgr.io", "u280406916_nutrition", "Mysqlnutrition200", "u280406916_nutrition");

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$conn->set_charset("utf8mb4");
```

### PDO
```php
<?php
$dsn = "mysql:host=srv1539.hstgr.io;dbname=u280406916_nutrition;charset=utf8mb4";
$user = "u280406916_nutrition";
$password = "Mysqlnutrition200";

try {
    $conn = new PDO($dsn, $user, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Connection failed: " . $e->getMessage());
}
```

### Eloquent (Laravel)
```php
// config/database.php
'mysql' => [
    'driver' => 'mysql',
    'host' => env('DB_HOST', 'srv1539.hstgr.io'),
    'port' => env('DB_PORT', 3306),
    'database' => env('DB_DATABASE', 'u280406916_nutrition'),
    'username' => env('DB_USERNAME', 'u280406916_nutrition'),
    'password' => env('DB_PASSWORD', 'Mysqlnutrition200'),
    'unix_socket' => env('DB_SOCKET', ''),
    'charset' => 'utf8mb4',
    'collation' => 'utf8mb4_unicode_ci',
    'prefix' => '',
    'prefix_indexes' => true,
    'strict' => true,
    'engine' => null,
    'options' => extension_loaded('pdo_mysql') ? array_filter([
        PDO::MYSQL_ATTR_SSL_CA => env('MYSQL_ATTR_SSL_CA'),
    ]) : [],
],
```

### Doctrine (Symfony)
```yaml
# .env
DATABASE_URL="mysql://u280406916_nutrition:Mysqlnutrition200@srv1539.hstgr.io:3306/u280406916_nutrition?charset=utf8mb4"
```

---

## Java

### JDBC
```java
String url = "jdbc:mysql://srv1539.hstgr.io:3306/u280406916_nutrition?useSSL=false&serverTimezone=UTC&characterEncoding=utf8mb4";
String user = "u280406916_nutrition";
String password = "Mysqlnutrition200";

Connection conn = DriverManager.getConnection(url, user, password);
```

### Hibernate
```xml
<!-- hibernate.cfg.xml -->
<hibernate-configuration>
    <session-factory>
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.connection.url">jdbc:mysql://srv1539.hstgr.io:3306/u280406916_nutrition?characterEncoding=utf8mb4</property>
        <property name="hibernate.connection.username">u280406916_nutrition</property>
        <property name="hibernate.connection.password">Mysqlnutrition200</property>
        <property name="hibernate.dialect">org.hibernate.dialect.MySQL8Dialect</property>
        <property name="hibernate.connection.useUnicode">true</property>
        <property name="hibernate.connection.characterEncoding">utf8mb4</property>
    </session-factory>
</hibernate-configuration>
```

### Spring Boot
```properties
# application.properties
spring.datasource.url=jdbc:mysql://srv1539.hstgr.io:3306/u280406916_nutrition?useSSL=false&serverTimezone=UTC&characterEncoding=utf8mb4
spring.datasource.username=u280406916_nutrition
spring.datasource.password=Mysqlnutrition200
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.jpa.hibernate.ddl-auto=validate
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect
spring.jpa.properties.hibernate.connection.useUnicode=true
spring.jpa.properties.hibernate.connection.characterEncoding=utf8mb4
```

### MyBatis
```xml
<!-- SqlMapConfig.xml -->
<dataSource type="POOLED">
    <property name="driver" value="com.mysql.cj.jdbc.Driver" />
    <property name="url" value="jdbc:mysql://srv1539.hstgr.io:3306/u280406916_nutrition?characterEncoding=utf8mb4" />
    <property name="username" value="u280406916_nutrition" />
    <property name="password" value="Mysqlnutrition200" />
</dataSource>
```

---

## C# / .NET

### SQL Server Syntax (for MySQL)
```csharp
string connectionString = "Server=srv1539.hstgr.io;Port=3306;Database=u280406916_nutrition;User Id=u280406916_nutrition;Password=Mysqlnutrition200;CharSet=utf8mb4;";

using (MySqlConnection conn = new MySqlConnection(connectionString))
{
    conn.Open();
    // Use connection
}
```

### Entity Framework
```csharp
// DbContext
protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
{
    optionsBuilder.UseMySql(
        "Server=srv1539.hstgr.io;Port=3306;Database=u280406916_nutrition;User Id=u280406916_nutrition;Password=Mysqlnutrition200;CharSet=utf8mb4;",
        new MySqlServerVersion(new Version(8, 0, 0))
    );
}
```

### Dapper
```csharp
string connectionString = "Server=srv1539.hstgr.io;Port=3306;Database=u280406916_nutrition;User Id=u280406916_nutrition;Password=Mysqlnutrition200;CharSet=utf8mb4;";

using (var connection = new MySqlConnection(connectionString))
{
    connection.Open();
    var results = connection.Query<User>("SELECT * FROM users");
}
```

---

## Ruby

### mysql2 gem
```ruby
require 'mysql2'

client = Mysql2::Client.new(
    host: "srv1539.hstgr.io",
    username: "u280406916_nutrition",
    password: "Mysqlnutrition200",
    database: "u280406916_nutrition",
    charset: "utf8mb4"
)
```

### Rails
```ruby
# config/database.yml
default: &default
    adapter: mysql2
    encoding: utf8mb4
    pool: 5
    username: u280406916_nutrition
    password: Mysqlnutrition200
    host: srv1539.hstgr.io
    port: 3306

development:
    <<: *default
    database: u280406916_nutrition

test:
    <<: *default
    database: u280406916_nutrition

production:
    <<: *default
    database: u280406916_nutrition
    username: <%= ENV['DATABASE_USERNAME'] %>
    password: <%= ENV['DATABASE_PASSWORD'] %>
    host: <%= ENV['DATABASE_HOST'] %>
```

### ActiveRecord
```ruby
ActiveRecord::Base.establish_connection(
    adapter: "mysql2",
    host: "srv1539.hstgr.io",
    username: "u280406916_nutrition",
    password: "Mysqlnutrition200",
    database: "u280406916_nutrition",
    charset: "utf8mb4"
)
```

---

## Go

### go-sql-driver/mysql
```go
import "database/sql"
import _ "github.com/go-sql-driver/mysql"

dsn := "root:your_password@tcp(localhost:3306)/nutrition_tracker?charset=utf8mb4&parseTime=True&loc=Local"
db, err := sql.Open("mysql", dsn)
if err != nil {
    log.Fatal(err)
}
defer db.Close()
```

### GORM
```go
import "gorm.io/driver/mysql"
import "gorm.io/gorm"

dsn := "root:your_password@tcp(localhost:3306)/nutrition_tracker?charset=utf8mb4&parseTime=True&loc=Local"
db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
if err != nil {
    log.Fatal(err)
}
```

---

## Environment Variables (.env file)

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=nutrition_tracker
DB_USER=root
DB_PASSWORD=your_password
DB_CHARSET=utf8mb4

# Connection Pool
DB_POOL_MIN=5
DB_POOL_MAX=20
DB_POOL_TIMEOUT=30

# Security
DB_SSL_ENABLED=false
DB_SSL_CA_PATH=
DB_SSL_CERT_PATH=
DB_SSL_KEY_PATH=

# Performance
DB_SLOW_QUERY_THRESHOLD=1000
DB_QUERY_TIMEOUT=30
```

---

## Connection Test Commands

### PowerShell
```powershell
mysql -h localhost -u root -pYourPassword nutrition_tracker -e "SELECT 1 as connection_test;"
```

### Command Line
```bash
mysql -h localhost -u root -p nutrition_tracker -e "SELECT 1 as connection_test;"
```

### MySQL CLI
```sql
mysql> SELECT DATABASE();
mysql> SHOW TABLES;
mysql> SELECT COUNT(*) FROM users;
```

---

## SSL/TLS Connection (Production)

### Connection String with SSL
```
mysql+pymysql://root:your_password@localhost/nutrition_tracker?ssl_ca=/path/to/ca.pem&ssl_cert=/path/to/client-cert.pem&ssl_key=/path/to/client-key.pem
```

### Generate Self-Signed Certificates
```bash
# Generate CA certificate
openssl req -new -x509 -days 365 -keyout ca-key.pem -out ca-cert.pem

# Generate server certificate
openssl req -new -keyout server-key.pem -out server.csr
openssl x509 -req -in server.csr -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -days 365 -out server-cert.pem

# Generate client certificate
openssl req -new -keyout client-key.pem -out client.csr
openssl x509 -req -in client.csr -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -days 365 -out client-cert.pem
```

---

## Troubleshooting Connection Issues

### Connection Refused
- Check MySQL service is running
- Verify host and port are correct
- Check firewall settings

### Authentication Failed
- Verify username and password
- Check user privileges: `SHOW GRANTS FOR 'root'@'localhost';`
- Reset password if forgotten

### Charset Issues
- Always use `charset=utf8mb4`
- Set collation to `utf8mb4_unicode_ci`
- Verify client charset matches server

### Performance Issues
- Enable connection pooling
- Set appropriate pool size (typically 10-20)
- Use connection recycling (max 3600 seconds)