import pyodbc
#cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=GWM-PF25ZT8Q;DATABASE=TestMe;Trusted_Connection=yes')
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=127.0.0.1;DATABASE=FC_JBR_DEV;UID=jbruewer@tcp:myserver.database.windows.net;PWD=TotalS€cureAnd0bscure')


cursor = cnxn.cursor()
cursor.execute("select * from dbo.testTabelle1")
rows = cursor.fetchall()
for row in rows:
    print(row)