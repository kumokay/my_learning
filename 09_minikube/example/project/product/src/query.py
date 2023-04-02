from typing import List, NamedTuple

from mysql.connector.connection import MySQLConnection

MYSQL_USER = "root"
MYSQL_PASSWORD = "mypassword"
MYSQL_HOST = "product-mysql"
MYSQL_PORT = 3306

DB_NAME = "product_db"

QUERY_INSERT_PRODUCT = """
INSERT INTO products (
  name
  , price
  , seller_id
) VALUES
  (%s, %s, %s)
;
"""

QUERY_SELECT_PRODUCT = """
SELECT
  products.id as product_id
  , products.name as product_name
  , products.price as product_price
  , users.name as seller_name
FROM
  products
JOIN users
  ON products.seller_id = users.id
WHERE products.id >= %s
  AND is_active = true
ORDER BY products.id
LIMIT %s
;
"""

class ProductObj(NamedTuple):
    product_id: int
    product_name: str
    product_price: float
    seller_name: str


class QueryExecutor:

    @staticmethod
    def _start_connection() -> MySQLConnection:
        return MySQLConnection(
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            database=DB_NAME,
        )

    @classmethod
    def list_product(
        cls,
        product_name: str,
        seller_id: int,
        price: float
    ) -> int:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        cursor.execute(QUERY_INSERT_PRODUCT, (product_name, price, seller_id))
        cnx.commit()
        cnx.close()

        count = cursor.rowcount
        cursor.close()

        return count
    
    @classmethod
    def get_catalogue(
        cls,
        next_product_id: int,
        limit: int,
    ) -> List[ProductObj]:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        cursor.execute(QUERY_SELECT_PRODUCT, (next_product_id, limit))
        rows = cursor.fetchall()

        result = [
            ProductObj(
                product_id=product_id,
                product_name=product_name,
                product_price=product_price,
                seller_name=seller_name,
            ) for (product_id, product_name, product_price, seller_name) in rows
        ]

        cursor.close()
        cnx.close()

        return result
