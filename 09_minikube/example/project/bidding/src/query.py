from typing import List, NamedTuple

from mysql.connector.connection import MySQLConnection

MYSQL_USER = "root"
MYSQL_PASSWORD = "mypassword"
MYSQL_HOST = "wordpress-mysql"
MYSQL_PORT = 3306

BIDDING_DB = "bidding_db"
PRODUCT_DB = "product_db"

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

class BidObj(NamedTuple):
    bid_id: int
    product_id: int
    bidder_id: int
    bid_price: float
    bid_at: str


QUERY_SELECT_BID = """
SELECT
  id as bid_id
  , product_id
  , bidder_id
  , price as bid_price
  , bid_at
FROM
  bids
WHERE product_id = %s
  AND id >= %s
ORDER BY price DESC, bid_at ASC
LIMIT %s
;
"""


class QueryExecutor:

    @staticmethod
    def _start_connection(dbname: str) -> MySQLConnection:
        return MySQLConnection(
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            database=dbname,
        )

    @classmethod
    def place_bid(
        cls,
        product_id: int,
        bidder_id: int,
        price: float,
        bid_at: str
    ) -> int:
        cnx = cls._start_connection(BIDDING_DB)
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
        cnx = cls._start_connection(PRODUCT_DB)
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
        cnx = cls._start_connection(PRODUCT_DB)
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

    @classmethod
    def _get_bid(
        cls,
        product_id_filter: int,
        next_bid_id: int,
        limit: int
    ) -> List[BidObj]:
        cnx = cls._start_connection(BIDDING_DB)
        cursor = cnx.cursor()
        cursor.execute(QUERY_SELECT_BID, (product_id_filter, next_bid_id, limit))
        rows = cursor.fetchall()

        result = [
            BidObj(
                bid_id=bid_id,
                product_id=product_id,
                bidder_id=bidder_id,
                bid_price=float(bid_price),  # convert Decimal to float
                bid_at=str(bid_at),  # convert datetime to string
            ) for (bid_id, product_id, bidder_id, bid_price, bid_at) in rows
        ]

        cursor.close()
        cnx.close()

        return result
    
    @classmethod
    def get_winner(
        cls,
        product_id_filter: int,
    ) -> List[BidObj]:
        return cls._get_bid(product_id_filter, 0, 1)
        
    
    @classmethod
    def get_bid_history(
        cls,
        product_id_filter: int,
        next_bid_id: int,
        limit: int
    ) -> List[BidObj]:
        return cls._get_bid(product_id_filter, next_bid_id, limit)

