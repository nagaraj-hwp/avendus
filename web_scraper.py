from requests_html import HTMLSession
import pandas as pd
import sqlite3

with HTMLSession() as s:

    r = s.get(
        'https://www.bseindia.com/markets/equity/EQReports/bulk_deals.aspx')
    hiddens = r.html.find('input[name=__VIEWSTATE]',
                          first=True).attrs.get('value')

    payload = {
        '__EVENTTARGET': '',
        '_VIEWSTATE': hiddens,
        'obsSwitcher:ddlObsUnits': 'usunits',
        'tbStation1': 'MD-BL-13',
        'ucDateRangeFilter:dcStartDate': '8/1/2019',
        'ucDateRangeFilter_dcStartDate_p': '2019-8-1-0-0-0-0',
        'ucDateRangeFilter:dcEndDate': '8/10/2019',
        'ucDateRangeFilter_dcEndDate_p': '2019-8-10-0-0-0-0',
        'btnSubmit': 'Get Summary'
    }

    r = s.post(
        'https://www.bseindia.com/markets/equity/EQReports/bulk_deals.aspx', data=payload)
    table = r.html.find('#ContentPlaceHolder1_gvbulk_deals', first=True)
    df = pd.read_html(table.html, header=0)[0]
    df.rename(columns={'Deal Date': 'deal_date', 'Security Code': 'security_code', 'Security Name': 'security_name',
              'Client Name': 'client_name', 'Deal Type': 'deal_type', 'Quantity': 'quantity', 'Price **': 'price'}, inplace=True)
    print(list(df.columns))
    print(df)


conn = sqlite3.connect('test_database')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS deals (deal_date text, security_code text, security_name text, client_name text, deal_type text, quantity number, price number)')
conn.commit()

df.to_sql('deals', conn, if_exists='replace', index=False)

c.execute('''  
		SELECT * FROM deals
          ''')

df = pd.DataFrame(c.fetchall(), columns=[
                  'deal_date', 'security_code', 'security_name', 'client_name', 'deal_type', 'quantity', 'price'])
print("Here is the complete data")
print(df)

c.execute('''  
		SELECT * FROM deals
        WHERE price = (SELECT max(price) FROM deals)
          ''')
df = pd.DataFrame(c.fetchall(), columns=[
                  'deal_date', 'security_code', 'security_name', 'client_name', 'deal_type', 'quantity', 'price'])
print("Data according to your query")
print(df)
