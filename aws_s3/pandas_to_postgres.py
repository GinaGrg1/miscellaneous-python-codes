import pandas as pd
import psycopg2 as pg


def make_conn():
    try:
        conn = pg.connect(database="postgres", user="reginagurung", password="***")
        cursor = conn.cursor()
    except Exception as e:
        raise e
    return conn, cursor


filepath = '/Users/reginagurung/Downloads/tx_deathrow_full.csv'

columns = 'Execution Date_of_Birth Date_of_Offence Highest_Education_Level Last_Name First_Name TDCJ_Number Age_at_Execution Date_Received Execution_Date Race County Eye_Color Weight Height Native_County Native_State Last_Statement'.split()

df = pd.read_csv(filepath, header=None)
df.columns = columns
df.fillna('N/A', axis=0, inplace=True)

conn, cur = make_conn()
cols_psql = ",".join([str(i) for i in columns])

for _, row in df.iterrows():
    sql = "INSERT INTO public.prisoners (" + cols_psql + ") VALUES (" + "%s," * (len(row) - 1) + "%s)"
    cur.execute(sql, tuple(row))
    conn.commit()

conn.close()
