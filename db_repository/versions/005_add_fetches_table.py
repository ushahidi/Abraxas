import datetime

from sqlalchemy import *
from migrate import *

from sqlalchemy.databases import mysql

metadata = MetaData(migrate_engine)


# New tables
fetch_table = Table('fetch', metadata,
    Column('id', mysql.MSBigInteger(unsigned=True), autoincrement=True, primary_key=True, nullable=False),
    Column('feed_id', mysql.MSBigInteger(unsigned=True), nullable=False),
    Column('result', VARCHAR(512), server_default="", nullable=False),                   
    # Note: SQLAlchemy doesnt seem to have a way to create a current_timestamp col
    # So see upgrade script 6 where we do it with raw sql.
    #Column('created', TIMESTAMP, default='current_timestamp')
)                                                                                                                    
                                                                                                                    

def upgrade():
    fetch_table.create()

def downgrade():
    fetch_table.drop()

