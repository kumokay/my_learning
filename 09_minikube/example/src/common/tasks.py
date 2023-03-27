import socket
import time

from celery import Celery


app = Celery('tasks',
             broker='redis://redis-leader:6379/0',
             backend='redis://redis-leader:6379/1')


# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)


HOSTNAME = socket.gethostname()
EXECTIME = 3
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

@app.task
def place_bid(product_id: int, bidder_id: int, price: float, bid_at: str) -> str:
    from mysql.connector.connection import MySQLConnection

    cnx = MySQLConnection(
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            database=MYSQL_DB)

    cursor = cnx.cursor()
    cursor.execute(QUERY_INSERT_BID, (product_id, bidder_id, price, bid_at))
    cnx.commit()
    cnx.close()

    count = cursor.rowcount
    cursor.close()

    # add delay
    time.sleep(EXECTIME)

    return f"[{HOSTNAME}] user-{bidder_id} bid ${price} for product-{product_id}"


@app.task
def list_product(product_name: str, seller_id: int, price: float) -> str:
    from mysql.connector.connection import MySQLConnection

    cnx = MySQLConnection(
            user=MYSQL_USER, 
            password=MYSQL_PASSWORD,
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            database=MYSQL_DB)

    cursor = cnx.cursor()
    cursor.execute(QUERY_INSERT_PRODUCT, (product_name, price, seller_id))
    cnx.commit()
    cnx.close()

    count = cursor.rowcount
    cursor.close()

    return f"[{HOSTNAME}] user-{seller_id} listed {count} product-{product_name} at ${price}"
    

