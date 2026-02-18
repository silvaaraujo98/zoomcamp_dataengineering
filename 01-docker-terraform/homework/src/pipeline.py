import pandas as pd
from sqlalchemy import create_engine
def create_connection():
    #Create the connection string
    conn_string = "postgresql://postgres:postgres@localhost:5433/ny_taxi"

    #Create the connection itself
    engine = create_engine(conn_string)

    # Test the connection by reading a simple query
    try:
        with engine.connect() as connection:
            print("Connection successful!")
            return engine
    except Exception as e:
        print(f"Connection failed: {e}")

def send_parquet(engine):
    green_trip_df = pd.read_parquet("data/green_tripdata_2025-11.parquet")
    print("The data was read!!!")

    green_trip_df.to_sql(name='green_taxi_data', 
                         con=engine, 
                         if_exists='replace', 
                         index=False)

def send_csv(engine):
    dtype = {
    'LocationID':'string',
    'Borough':'string',
    'Zone':'string',
    'service_zone': 'string'


    }

    taxi_zone_df = pd.read_csv("data/taxi_zone_lookup.csv",dtype=dtype)
    taxi_zone_df.to_sql(name='taxi_zone', con=engine, if_exists='replace', index=False)

def steps_pipeline():
    engine = create_connection()
    send_csv(engine)
    send_parquet(engine)
# Fazer as queries do trabalho de casa, mas 




