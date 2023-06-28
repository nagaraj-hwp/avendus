import requests
from bs4 import BeautifulSoup
import mysql.connector
from requests_html import *

url = 'https://www.bseindia.com/markets/equity/EQReports/bulk_deals.aspx'

response = requests.get(url)
print(response.content)
soup = BeautifulSoup(response.content, "html.parser")

# session = HTMLSession()
# r = session.get(url)

# print(r)
# print(r.html.links)

# asession = AsyncHTMLSession()
# async def get_htmlcontent():
#     r = await asession.get(url)

# result = session.run(get_htmlcontent)


table = soup.find("table")
print(table)
headers = [header.text for header in table.find_all("th")]

rows = []
for row in table.find_all("tr")[1:]:
    row_data = [data.text for data in row.find_all("td")]
    rows.append(row_data)

print(headers)
for row in rows:
    print(row)

db = mysql.connector.connect(
    host="<host>",
    user="<user>",
    password="<password>",
    database="<database>"
)
cursor = db.cursor()


query = "INSERT INTO table_name (deal_date, security_name, quantity) VALUES (%s, %s, %s)"

values = [(deal_date, security_name, quantity), (deal_date, security_name, quantity), ...]  # List of tuples with the extracted data

cursor.executemany(query, values)
db.commit()

cursor.close()
db.close()

