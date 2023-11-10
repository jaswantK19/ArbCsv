from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import dotenv

dotenv.load_dotenv()


user= os.environ["USERNAME"]
password = os.environ['PASSWORD']
host=os.environ['HOST']
port=os.environ["PORT"]
db=os.environ['DATABASE']

connection_str = f'postgresql://{user}:{password}@{host}:{int(port)}/{db}'
engine = create_engine(connection_str)

SessionLocal = sessionmaker(bind=engine)