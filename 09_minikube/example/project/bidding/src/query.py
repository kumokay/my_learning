from mysql.connector.connection import MySQLConnection

MYSQL_USER = "root"
MYSQL_PASSWORD = "mypassword"
MYSQL_HOST = "wordpress-mysql"
MYSQL_PORT = 3306
MYSQL_DB = "bidding_db"

QUERY_INSERT_PRODUCT = """
INSERT INTO products (
  name
  , price
  , seller_id
) VALUES
  (%s, %s, %s)
;
"""

QUERY_INSERT_BID = """
INSERT INTO bids (
  product_id
  , bidder_id
  , price
  , bid_at
) VALUES
  (%s, %s, %s, %s)
;
"""


class QueryExecutor:

    @staticmethod
    def _start_connection() -> MySQLConnection:
        return MySQLConnection(
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                database=MYSQL_DB)

    @classmethod
    def place_bid(
        cls,
        product_id: int,
        bidder_id: int,
        price: float,
        bid_at: str
    ) -> int:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        cursor.execute(
            QUERY_INSERT_BID,
            (product_id, bidder_id, price, bid_at)
        )
        cnx.commit()
        cnx.close()

        count = cursor.rowcount
        cursor.close()

        return count

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
