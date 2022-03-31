import pyodbc
server = 'Azure-Web.database.windows.net'
database = '8451_The_Complete_Journey_2_Sample'
username = 'teamMeow'
password = '{meowmeowmeow1!}'   
driver= '{ODBC Driver 17 for SQL Server}'

# QUERY FROM AZURE DATABASE
TOTALSALES = '''select dbo.[400_transactions].YEAR, SUM(CAST(dbo.[400_transactions].SPEND as float))
FROM dbo.[400_transactions]
where dbo.[400_transactions].YEAR in (2019,2020) AND dbo.[400_transactions].WEEK_NUM < 32
GROUP BY dbo.[400_transactions].YEAR
'''

TOTALSALESCHILDFEW = '''select dbo.[400_transactions].YEAR, SUM(CAST(dbo.[400_transactions].SPEND as float))
FROM dbo.[400_transactions]
Inner Join dbo.[400_products] ON dbo.[400_transactions].PRODUCT_NUM = dbo.[400_products].PRODUCT_NUM
Inner Join dbo.[400_households] ON dbo.[400_transactions].HSHD_NUM = dbo.[400_households].HSHD_NUM
where dbo.[400_transactions].YEAR in (2019) AND (dbo.[400_products].COMMODITY = 'BABY' OR dbo.[400_products].COMMODITY = 'TOYS') AND dbo.[400_households].CHILDREN != '3+' AND dbo.[400_households].CHILDREN != 'null'
GROUP BY dbo.[400_transactions].YEAR
'''

TOTALSALESCHILDMANY = '''select dbo.[400_transactions].YEAR, SUM(CAST(dbo.[400_transactions].SPEND as float))
FROM dbo.[400_transactions]
Inner Join dbo.[400_products] ON dbo.[400_transactions].PRODUCT_NUM = dbo.[400_products].PRODUCT_NUM
Inner Join dbo.[400_households] ON dbo.[400_transactions].HSHD_NUM = dbo.[400_households].HSHD_NUM
where dbo.[400_transactions].YEAR in (2019) AND (dbo.[400_products].COMMODITY = 'BABY' OR dbo.[400_products].COMMODITY = 'TOYS') AND dbo.[400_households].CHILDREN = '3+'
GROUP BY dbo.[400_transactions].YEAR
'''

COUNTCHILDFEW = '''select dbo.[400_transactions].YEAR, COUNT(DISTINCT dbo.[400_households].HSHD_NUM)
FROM dbo.[400_transactions]
Inner Join dbo.[400_households] ON dbo.[400_transactions].HSHD_NUM = dbo.[400_households].HSHD_NUM
where dbo.[400_transactions].YEAR in (2019) AND dbo.[400_households].CHILDREN != '3+' AND dbo.[400_households].CHILDREN != 'null'
GROUP BY dbo.[400_transactions].YEAR
'''

COUNTCHILDMANY = '''select dbo.[400_transactions].YEAR, COUNT(DISTINCT dbo.[400_households].HSHD_NUM)
FROM dbo.[400_transactions]
Inner Join dbo.[400_households] ON dbo.[400_transactions].HSHD_NUM = dbo.[400_households].HSHD_NUM
where dbo.[400_transactions].YEAR in (2019) AND dbo.[400_households].CHILDREN = '3+'
GROUP BY dbo.[400_transactions].YEAR
'''

HSHDDATA = '''SELECT * FROM dbo.[400_transactions]
INNER JOIN dbo.[400_products] ON dbo.[400_transactions].PRODUCT_NUM = dbo.[400_products].PRODUCT_NUM
INNER JOIN dbo.[400_households] ON dbo.[400_transactions].HSHD_NUM = dbo.[400_households].HSHD_NUM
where dbo.[400_transactions].HSHD_NUM = (?)
ORDER BY dbo.[400_transactions].HSHD_NUM, dbo.[400_transactions].BASKET_NUM, dbo.[400_transactions].PRODUCT_NUM, dbo.[400_products].DEPARTMENT, dbo.[400_products].COMMODITY;
'''

class DB():
	def getHouseHoldData(self, hshd_num):
		vals = self.cur.execute(HSHDDATA, [hshd_num])
		if vals is not None:
			rows = []
			for row in vals:
				rows.append(row)
			return rows
		else:
			return None

	def getTotalSales(self):
		val = self.cur.execute(TOTALSALES)
		rows = []
		for row in val:
			rows.append(row)
		return rows

	def getTotalSalesChildFew(self):
		val = self.cur.execute(TOTALSALESCHILDFEW)
		rows = []
		for row in val:
			rows.append(row)
		return rows

	def getTotalSalesChildMany(self):
		val = self.cur.execute(TOTALSALESCHILDMANY)
		rows = []
		for row in val:
			rows.append(row)
		return rows

	def getCountChildFew(self):
		val = self.cur.execute(COUNTCHILDFEW)
		rows = []
		for row in val:
			rows.append(row)
		return rows

	def getCountSalesChildMany(self):
		val = self.cur.execute(COUNTCHILDMANY)
		rows = []
		for row in val:
			rows.append(row)
		return rows

	def __init__(self):
		self.cur = object
		with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
			self.cur = conn.cursor()
			
			
			