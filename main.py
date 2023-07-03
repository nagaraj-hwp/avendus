import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from db import get_db_connection
app = FastAPI()


def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )
    return connection


class DealData(BaseModel):
    deal_date: str
    security_code: str
    security_name: str
    client_name: str
    deal_type: str
    quantity: int
    price: float


@app.post("/deals")
async def create_deal(deal_data: DealData):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO deals (deal_date, security_code, security_name, client_name, deal_type, quantity, price) " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (
        deal_data.deal_date,
        deal_data.security_code,
        deal_data.security_name,
        deal_data.client_name,
        deal_data.deal_type,
        deal_data.quantity,
        deal_data.price
    )
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

    return {"message": "Deal created successfully"}
