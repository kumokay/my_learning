from typing import List, NamedTuple

from mysql.connector.connection import MySQLConnection

MYSQL_USER = "root"
MYSQL_PASSWORD = "mypassword"
MYSQL_HOST = "bidding-mysql"
MYSQL_PORT = 3306

DB_NAME = "bidding_db"

QUERY_INSERT_BID = """
INSERT INTO bids (
  auction_id
  , bidder_id
  , price
  , bid_at
) VALUES
  (%s, %s, %s, %s)
;
"""

class BidObj(NamedTuple):
    bid_id: int
    auction_id: int
    bidder_id: int
    bid_price: float
    bid_at: str


QUERY_SELECT_BID = """
SELECT
  id as bid_id
  , auction_id
  , bidder_id
  , price as bid_price
  , bid_at
FROM
  bids
WHERE auction_id = %s
  AND id >= %s
ORDER BY price DESC, bid_at ASC
LIMIT %s
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
            database=DB_NAME,
        )

    @classmethod
    def place_bid(
        cls,
        auction_id: int,
        bidder_id: int,
        price: float,
        bid_at: str
    ) -> int:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        cursor.execute(
            QUERY_INSERT_BID,
            (auction_id, bidder_id, price, bid_at)
        )
        cnx.commit()
        cnx.close()

        count = cursor.rowcount
        cursor.close()

        return count

    @classmethod
    def _get_bid(
        cls,
        auction_id_filter: int,
        next_bid_id: int,
        limit: int
    ) -> List[BidObj]:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        cursor.execute(QUERY_SELECT_BID, (auction_id_filter, next_bid_id, limit))
        rows = cursor.fetchall()

        result = [
            BidObj(
                bid_id=bid_id,
                auction_id=auction_id,
                bidder_id=bidder_id,
                bid_price=float(bid_price),  # convert Decimal to float
                bid_at=str(bid_at),  # convert datetime to string
            ) for (bid_id, auction_id, bidder_id, bid_price, bid_at) in rows
        ]

        cursor.close()
        cnx.close()

        return result
    
    @classmethod
    def get_winner(
        cls,
        auction_id_filter: int,
    ) -> List[BidObj]:
        return cls._get_bid(auction_id_filter, 0, 1)
        
    
    @classmethod
    def get_bid_history(
        cls,
        auction_id_filter: int,
        next_bid_id: int,
        limit: int
    ) -> List[BidObj]:
        return cls._get_bid(auction_id_filter, next_bid_id, limit)

