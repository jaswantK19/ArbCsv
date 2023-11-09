import os
import csv
import dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from schemas import get_schema
import pandas as pd

dotenv.load_dotenv()

use= os.environ["USERNAME"]
password = os.environ['PASSWORD']
host=os.environ['HOST']
port=os.environ["PORT"]
db=os.environ['DATABASE']

connection_str = f'postgresql://{user}:{password}@{host}:{int(port)}/{db}'
engine = create_engine(connection_str)
Base = declarative_base()
try:
    with engine.connect() as connection_str:
        print('Successfully connected to the PostgreSQL database')
except Exception as ex:
    print(f'Sorry failed to connect: {ex}')

metadata = MetaData()
def create_table(file_path:str):
    df = get_schema(file_path)
    df.to_sql('Some Table', con=engine, index=True, index_label='id', if_exists='replace')
    metadata.create_all(engine)

create_table("./sample.csv")
