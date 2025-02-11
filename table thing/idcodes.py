import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

url = "https://dcs.rutgers.edu/classrooms/building-identification-codes"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table")
rows = table.find_all("tr")
headers = [cell.text.strip() for cell in rows[0].find_all("td")]
data = []
for row in rows[1:]:  # Skip the first row since it's the header
    cells = [cell.text.strip() for cell in row.find_all("td")]
    data.append(cells)
df = pd.DataFrame(data, columns=headers)
brr_row = {"Abbr.":"BRR","Building Name":"Buisness Rockefeller Road","Campus": "LIV", "Number": "0"}
df.loc[len(df)] = brr_row
df = df[df["Building Name"] != "Rutgers Cinema"]
df = df[df["Building Name"] != "Rutgers Academic Building"]
df["Building Name"] = df["Building Name"].replace("Rutgers Academic Building - East Wing", "Rutgers Academic Building (East Wing)")
df["Building Name"] = df["Building Name"].replace("Rutgers Academic Building - West Wing", "Rutgers Academic Building (West Wing)")
df["Building Name"] = df["Building Name"].replace("Science & Engineering Resource Center (T. Alexander Pond)", "Science & Engineering Resource Center")
print(df)
df.to_json("idcodes.json", orient="records")
# Create a connection to SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect('my_database.db')  # 'example.db' is the name of the database file

# Convert the DataFrame to an SQL table
df.to_sql('Abbrs', conn, if_exists='replace', index=False)

# Close the connection
conn.close()