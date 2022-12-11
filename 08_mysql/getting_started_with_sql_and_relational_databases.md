**Schema (MySQL v8.0)**

    CREATE DATABASE customers_db 
    DEFAULT CHARACTER SET utf8 
    COLLATE utf8_unicode_ci
    ;
    
    
    USE customers_db
    ;
    
    /*********************
     * customers
     *********************/
    CREATE TABLE customers (
      PRIMARY KEY (id)
      , id INT NOT NULL AUTO_INCREMENT
      , name VARCHAR(255)
      , age TINYINT
    )
    ;
    
    
    INSERT INTO customers (
      name
      , age
    )
    VALUES (
      'Harry Poter'
      , 12
    )
    ;
    
    
    -- delete all data
    DELETE FROM customers
    ;
    
    
    INSERT INTO customers (
      name
      , age
    )
    VALUES (
      'Harry Potter'
      , 12
    )
    ;
    
    
    ALTER TABLE customers
    ADD COLUMN(
      email VARCHAR(255) NOT NULL
      , zipcode VARCHAR(5)
    )
    ;
    
    
    CREATE INDEX customers_name_idx
    ON customers (name)
    ;
    
    
    /*
    Unique index:
    Pros: easier to enforce at db level
    Cons: it slows down writes
          So sometimes we prefer not to use unique index
          do it at application side instead.
    */
    CREATE UNIQUE INDEX customers_email_idx
    ON customers (email)
    ;
    
    
    INSERT INTO customers (
      name
      , age
      , email
    )
    VALUES (
      'Luke Skywalker'
      , 20
      , 'ls@universe.com'
    )
    ;
    
    
    INSERT INTO customers (
      name
      , age
      , email
    )
    VALUES (
      'Papa Johns'
      , 100
      , 'pj@test.com' 
    )
    ;
    
    
    DELETE FROM customers
    WHERE name = 'Papa Johns';
    
    
    INSERT INTO customers (
      name
      , age
      , email
    )
    VALUES (
      'John Wick'
      , 40
      , 'jw@test.com'
    )
    ;
    
    
    UPDATE customers
    SET
      email = 'hp@test.com.uk'
      , age = 13
    WHERE id = 2
    ;
    
    
    /*********************
     * products
     *********************/
    CREATE TABLE products (
      PRIMARY KEY (id)
      , id INT NOT NULL AUTO_INCREMENT
      , name VARCHAR(255) NOT NULL
      , price DECIMAL(15, 2) NOT NULL
    )
    ;
    
    
    CREATE UNIQUE INDEX products_name_uidx
    ON products (name)
    ;
    
    
    INSERT INTO products (
      name
      , price
    ) VALUES 
      ('apple', 3.99)
      , ('orang', 2.99)
      , ('grape', 4.99)
      , ('banana', 0.99)
      , ('kiwi', 2.99)
    ;
     
    
    
    /*********************
     * orders
     *********************/
    CREATE TABLE orders (
      id INT NOT NULL AUTO_INCREMENT
      , order_number VARCHAR(255) NOT NULL
      , order_at DATETIME NOT NULL
      , customer_id INT NOT NULL
      , PRIMARY KEY (id)
      , UNIQUE KEY orders_order_number_uidx (order_number)
    )
    ;
    
    
    ALTER TABLE orders
    ADD CONSTRAINT
    orders_customer_fk
    FOREIGN KEY (customer_id)
    REFERENCES customers (id)
    ;
    
    
    INSERT INTO orders (
      order_number
      , order_at
      , customer_id
    ) VALUES
      ('ABC001', current_timestamp, 2)
      , ('ABC002', current_timestamp + 1, 3)
      , ('ABC003', current_timestamp + 2, 2)
    ;
    
    
    /*********************
     * order_items
     *********************/
    CREATE TABLE order_items (
      id INT NOT NULL AUTO_INCREMENT
      , order_id INT NOT NULL
      , product_id INT NOT NULL
      , price DECIMAL(15, 2) NOT NULL
      , quantity INT NOT NULL
      , PRIMARY KEY (id)
      , UNIQUE KEY order_items_order_product_uidx
        (order_id, product_id)
      , CONSTRAINT order_items_order_fk
        FOREIGN KEY (order_id) REFERENCES orders (id)
      , CONSTRAINT order_items_product_fk
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ;
    
    
    INSERT INTO order_items (
      order_id
      , product_id
      , price
      , quantity
    ) VALUES 
      (1, 2, 2.99, 1)
      , (1, 4, 0.99, 1)
      , (2, 2, 2.99, 1)
      , (3, 3, 4.99, 1)
    ;

---

**Query #1**

    USE customers_db
    ;

There are no results to be displayed.

---
**Query #2**

    SELECT * FROM customers
    ;

| id  | name           | age | email           | zipcode |
| --- | -------------- | --- | --------------- | ------- |
| 2   | Harry Potter   | 13  | hp@test.com.uk  |         |
| 3   | Luke Skywalker | 20  | ls@universe.com |         |
| 5   | John Wick      | 40  | jw@test.com     |         |

---
**Query #3**

    SELECT 
      id
      , name
      , age
    FROM customers
    WHERE age > 18
      AND email IS NOT NULL
    ;

| id  | name           | age |
| --- | -------------- | --- |
| 3   | Luke Skywalker | 20  |
| 5   | John Wick      | 40  |

---
**Query #4**

    SELECT COUNT(*)
    FROM customers
    WHERE email LIKE '%@test.com%'
    ;

| COUNT(*) |
| -------- |
| 2        |

---
**Query #5**

    SELECT *
    FROM products
    ORDER BY 
      price
      , name 
    DESC
    LIMIT 2
    ;

| id  | name   | price |
| --- | ------ | ----- |
| 4   | banana | 0.99  |
| 2   | orang  | 2.99  |

---
**Query #6**

    SELECT * 
    FROM orders
    ;

| id  | order_number | order_at            | customer_id |
| --- | ------------ | ------------------- | ----------- |
| 1   | ABC001       | 2022-12-11 04:21:11 | 2           |
| 2   | ABC002       | 2022-12-11 04:21:12 | 3           |
| 3   | ABC003       | 2022-12-11 04:21:13 | 2           |

---
**Query #7**

    SELECT 
      order_id
      , SUM(price * quantity) as total_price
      , sum(quantity) as total_count
    FROM
      order_items
    GROUP BY order_id
    ;

| order_id | total_price | total_count |
| -------- | ----------- | ----------- |
| 1        | 3.98        | 2           |
| 2        | 2.99        | 1           |
| 3        | 4.99        | 1           |

---
**Query #8**

    SELECT * 
    FROM customers
    JOIN orders
    ;

| id  | name           | age | email           | zipcode | id  | order_number | order_at            | customer_id |
| --- | -------------- | --- | --------------- | ------- | --- | ------------ | ------------------- | ----------- |
| 5   | John Wick      | 40  | jw@test.com     |         | 1   | ABC001       | 2022-12-11 04:21:11 | 2           |
| 3   | Luke Skywalker | 20  | ls@universe.com |         | 1   | ABC001       | 2022-12-11 04:21:11 | 2           |
| 2   | Harry Potter   | 13  | hp@test.com.uk  |         | 1   | ABC001       | 2022-12-11 04:21:11 | 2           |
| 5   | John Wick      | 40  | jw@test.com     |         | 2   | ABC002       | 2022-12-11 04:21:12 | 3           |
| 3   | Luke Skywalker | 20  | ls@universe.com |         | 2   | ABC002       | 2022-12-11 04:21:12 | 3           |
| 2   | Harry Potter   | 13  | hp@test.com.uk  |         | 2   | ABC002       | 2022-12-11 04:21:12 | 3           |
| 5   | John Wick      | 40  | jw@test.com     |         | 3   | ABC003       | 2022-12-11 04:21:13 | 2           |
| 3   | Luke Skywalker | 20  | ls@universe.com |         | 3   | ABC003       | 2022-12-11 04:21:13 | 2           |
| 2   | Harry Potter   | 13  | hp@test.com.uk  |         | 3   | ABC003       | 2022-12-11 04:21:13 | 2           |

---
**Query #9**

    SELECT 
      customers.id
      , customers.name
      , orders.order_number
      , order_items.price AS item_price
      , products.name AS product_name
      , products.price AS product_price
    FROM customers
    JOIN orders
      ON customers.id = orders.customer_id
    JOIN order_items
      ON orders.id = order_items.order_id
    JOIN products
      ON order_items.product_id = products.id
    ORDER BY customers.id
    ;

| id  | name           | order_number | item_price | product_name | product_price |
| --- | -------------- | ------------ | ---------- | ------------ | ------------- |
| 2   | Harry Potter   | ABC001       | 2.99       | orang        | 2.99          |
| 2   | Harry Potter   | ABC001       | 0.99       | banana       | 0.99          |
| 2   | Harry Potter   | ABC003       | 4.99       | grape        | 4.99          |
| 3   | Luke Skywalker | ABC002       | 2.99       | orang        | 2.99          |

---
**Query #10**

    SELECT COUNT(DISTINCT customers.id)
    FROM customers
    JOIN orders
      ON customers.id = orders.customer_id
    ;

| COUNT(DISTINCT customers.id) |
| ---------------------------- |
| 2                            |

---
**Query #11**

    SELECT COUNT(DISTINCT customer_id)
    FROM orders
    ;

| COUNT(DISTINCT customer_id) |
| --------------------------- |
| 2                           |

---
**Query #12**

    SELECT 
      customers.id
      , customers.name
      , orders.order_number
      , order_items.price AS item_price
      , products.name AS product_name
      , products.price AS product_price
    FROM customers
    LEFT JOIN orders
      ON customers.id = orders.customer_id
    LEFT JOIN order_items
      ON orders.id = order_items.order_id
    LEFT JOIN products
      ON order_items.product_id = products.id
    ORDER BY customers.id
    ;

| id  | name           | order_number | item_price | product_name | product_price |
| --- | -------------- | ------------ | ---------- | ------------ | ------------- |
| 2   | Harry Potter   | ABC001       | 0.99       | banana       | 0.99          |
| 2   | Harry Potter   | ABC001       | 2.99       | orang        | 2.99          |
| 2   | Harry Potter   | ABC003       | 4.99       | grape        | 4.99          |
| 3   | Luke Skywalker | ABC002       | 2.99       | orang        | 2.99          |
| 5   | John Wick      |              |            |              |               |

---
**Query #13**

    SELECT customers.*
    FROM customers
    LEFT JOIN orders
      ON customers.id = orders.customer_id
    WHERE orders.id is NULL
    ;

| id  | name      | age | email       | zipcode |
| --- | --------- | --- | ----------- | ------- |
| 5   | John Wick | 40  | jw@test.com |         |

---
**Query #14**

    SELECT 
      customers.name
      , SUM(order_items.price * order_items.quantity) AS total_price
    FROM customers
    LEFT JOIN orders
      ON customers.id = orders.customer_id
    LEFT JOIN order_items
      ON orders.id = order_items.order_id
    GROUP BY customers.id
    ORDER BY total_price 
      DESC
    ;

| name           | total_price |
| -------------- | ----------- |
| Harry Potter   | 8.97        |
| Luke Skywalker | 2.99        |
| John Wick      |             |

---
**Query #15**

    SELECT 
      order_items.id
      , products.name
    FROM order_items
    RIGHT JOIN products
      ON order_items.product_id = products.id
    ORDER BY order_items.id
    ;

| id  | name   |
| --- | ------ |
|     | apple  |
|     | kiwi   |
| 1   | orang  |
| 2   | banana |
| 3   | orang  |
| 4   | grape  |

---
**Query #16**

    SELECT 
      customers.name
      , orders.id
    FROM customers
    CROSS JOIN orders
    ;

| name           | id  |
| -------------- | --- |
| Luke Skywalker | 1   |
| John Wick      | 1   |
| Harry Potter   | 1   |
| Luke Skywalker | 3   |
| John Wick      | 3   |
| Harry Potter   | 3   |
| Luke Skywalker | 2   |
| John Wick      | 2   |
| Harry Potter   | 2   |

---

[View on DB Fiddle](https://www.db-fiddle.com/)
