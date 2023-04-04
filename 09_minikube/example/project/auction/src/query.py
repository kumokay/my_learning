from typing import List, NamedTuple

from mysql.connector.connection import MySQLConnection

MYSQL_USER = "root"
MYSQL_PASSWORD = "mypassword"
MYSQL_HOST = "auction-mysql"
MYSQL_PORT = 3306

DB_NAME = "auction_db"

QUERY_INSERT_AUCTION = """
INSERT INTO auctions (
  name
  , start_price
  , seller_id
  , start_at
  , end_at
  , status
) VALUES
  (%s, %s, %s, %s, %s, %s)
;
"""

QUERY_SELECT_AUCTION = """
SELECT
  auctions.id as auction_id
  , auctions.name as auction_name
  , auctions.start_price as start_price
  , users.name as seller_name
  , auctions.start_at as start_at
  , auctions.end_at as end_at
  , auctions.status as status
FROM
  auctions
JOIN users
  ON auctions.seller_id = users.id
WHERE auctions.id >= %s
  AND status = 'ongoing'
ORDER BY auctions.id
LIMIT %s
;
"""

QUERY_UPDATE_PAYMENT="""
UPDATE payments
SET
  status = %s
WHERE
  id = %s
"""

class AuctionObj(NamedTuple):
    auction_id: int
    auction_name: str
    start_price: float
    seller_name: str
    start_at: str
    end_at: str
    status: str


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
    def create_auction(
        cls,
        auction_name: str,
        seller_id: int,
        start_price: float,
        start_at: str,
        end_at: str,
        status: str
    ) -> int:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        cursor.execute(
            QUERY_INSERT_AUCTION, 
            (
                auction_name, 
                start_price,
                seller_id,
                start_at,
                end_at,
                status,
            ),
        )
        cnx.commit()
        cnx.close()

        count = cursor.rowcount
        cursor.close()

        return count
    
    @classmethod
    def get_auctions(
        cls,
        next_auction_id: int,
        limit: int,
    ) -> List[AuctionObj]:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        cursor.execute(QUERY_SELECT_AUCTION, (next_auction_id, limit))
        rows = cursor.fetchall()

        result = [
            AuctionObj(
                auction_id=auction_id,
                auction_name=auction_name,
                start_price=float(start_price),  # convert Decimal to float,
                seller_name=seller_name,
                start_at=str(start_at),  # convert Datetime to str,
                end_at=str(end_at),  # convert Datetime to str,
                status=status,
            ) for (
                auction_id, 
                auction_name, 
                start_price,
                seller_name, 
                start_at, 
                end_at, 
                status,
            ) in rows
        ]

        cursor.close()
        cnx.close()

        return result
    
    @classmethod
    def update_payment(
        cls,
        payment_id,
        status,
    ) -> int:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        cursor.execute(
            QUERY_UPDATE_PAYMENT, (status, payment_id),
        )
        cnx.commit()
        cnx.close()

        count = cursor.rowcount
        cursor.close()

        return count
