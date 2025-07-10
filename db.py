import pandas as pd
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit
import mysql.connector
import os
from dotenv import load_dotenv
import plotly.express as px

# Connect to MySQL
load_dotenv()

# try:
#     conn = mysql.connector.connect(
#     host=os.getenv("DB_HOST"),
#     user=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASSWORD"),
#     database=os.getenv("DB_NAME")
# )

#     if conn.is_connected():
#         print("Connection successful!")
#     else:
#         print("Connection failed.")
# except mysql.connector.Error as err:
#     print(f"Error: {err}")


# from urllib.parse import quote_plus
# from dotenv import load_dotenv
# import os
# from sqlalchemy import create_engine

# load_dotenv()

# host = os.getenv("DB_HOST")
# user = os.getenv("DB_USER")
# raw_password = os.getenv("DB_PASSWORD")
# password = quote_plus(raw_password) 
# database = os.getenv("DB_NAME")

# engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:3306/{database}")


def load_dataframe(table):
    # q_agg_insu = f"SELECT * FROM {table}"
    # dataframe = pd.read_sql(q_agg_insu, conn)
    dataframe = pd.read_csv(f"{table}.csv")
    dataframe = dataframe[dataframe["state"] != "india"]
    # print(dataframe.head())
    dataframe["state"] = dataframe["state"].str.replace("andaman-&-nicobar-islands" , "Andaman & Nicobar")
    dataframe["state"] = dataframe["state"].str.replace("-" ," ")
    dataframe["state"] = dataframe["state"].str.replace("dadra-&-nagar-haveli-&-daman-&-diu" , "Dadra and Nagar Haveli and Daman and Diu")
    dataframe["state"] = dataframe["state"].str.title()
    # print(dataframe["state"].unique())
    return dataframe


df_aggregated_insurance = load_dataframe("aggregated_insurance")
df_aggregated_transaction = load_dataframe("aggregated_transaction")
df_aggregated_user = load_dataframe("aggregated_user")
df_map_insurance = load_dataframe("map_insurance")
df_map_insurance.rename(columns={"name": "district"}, inplace=True)
df_map_transaction = load_dataframe("map_transaction")
df_map_transaction.rename(columns={"name": "district"}, inplace=True)
df_map_user = load_dataframe("map_user")
df_map_user.rename(columns={"name": "district"}, inplace=True)

df_top_insurance = load_dataframe("top_insurance")

df_top_insurance_district = df_top_insurance[df_top_insurance["level"] == "district"].reset_index(drop=True)
df_top_insurance_pincode = df_top_insurance[df_top_insurance["level"] == "pincode"].reset_index(drop=True)

df_top_insurance_district.rename(columns={"name": "district"}, inplace=True)
df_top_insurance_pincode.rename(columns={"name": "pincode"}, inplace=True)

df_top_insurance_district.drop(["level" ,"type" ] , axis = 1 , inplace = True )
df_top_insurance_pincode.drop(["level" ,"type"], axis = 1 , inplace = True )

df_top_insurance_pincode["pincode"] = df_top_insurance_pincode["pincode"].astype(str)

df_top_transaction = load_dataframe("top_transaction")

df_top_transaction_district = df_top_transaction[df_top_transaction["level"] == "district"].reset_index(drop=True)
df_top_transaction_pincode = df_top_transaction[df_top_transaction["level"] == "pincode"].reset_index(drop=True)

df_top_transaction_district.rename(columns={"name": "district"}, inplace=True)
df_top_transaction_pincode.rename(columns={"name": "pincode"}, inplace=True)

df_top_transaction_district.drop(["level" ,"type" ] , axis = 1 , inplace = True )
df_top_transaction_pincode.drop(["level" ,"type"], axis = 1 , inplace = True )

df_top_transaction_pincode["pincode"] = df_top_transaction_pincode["pincode"].astype(str)


df_top_user = load_dataframe("top_user")
# df_top_user = pd.read_csv("E:/IITKanpur/Labmentix/2PhonePe/project/csvs/top_user.csv")

df_top_user_district = df_top_user[df_top_user["level"] == "district"].reset_index(drop=True)
df_top_user_pincode = df_top_user[df_top_user["level"] == "pincode"].reset_index(drop=True)

df_top_user_district.rename(columns={"name": "district"}, inplace=True)
df_top_user_pincode.rename(columns={"name": "pincode"}, inplace=True)

df_top_user_district.drop(["level"] , axis = 1 , inplace = True )
df_top_user_pincode.drop(["level"], axis = 1 , inplace = True )

df_top_user_pincode["pincode"] = df_top_user_pincode["pincode"].astype(str)


