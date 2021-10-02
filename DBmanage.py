import sqlite3
import datetime
from support import SupportedApps
from os import path

def Creation():
	db = sqlite3.connect("TTW.db")
	cursor = db.cursor()

	first_time = ("""CREATE TABLE IF NOT EXISTS TimedApps (
		'Mixed' varchar(100) primary key NOT NULL,
		'AppName' varchar(200) default Null,
		'AppTitle' varchar(160) default Null,
		'Time' int UNSIGNED NULL DEFAULT NULL,
		'Date' date default Null) 
		""")

	cursor.execute(first_time)

if not path.exists("TTW.db"):
	Creation()

class DBhandle:

	def DateToday():
		Today = datetime.date.today()
		return Today

	def DBstore(AppName, TimeSpent):
		if len(AppName) == 0:
			return

		AppSplit = AppName.split(" - ")

		AppTitle = None
		AppName = AppSplit[-1]

		AppTitle, AppName = SupportedApps.AppCheck(AppTitle, AppName, AppSplit)
		Mixed = f"{DBhandle.DateToday()} / {AppName}"

		db = sqlite3.connect("TTW.db")
		cursor = db.cursor()

		try:
			DBadd = f"INSERT INTO TimedApps (Mixed, AppName, AppTitle, Time, Date) VALUES ('{Mixed}', '{AppName}', '{AppTitle}', '{TimeSpent}', '{DBhandle.DateToday()}')"
			cursor.execute(DBadd)
			db.commit()
		except:
			DBupdate = f"UPDATE TimedApps SET Time = Time + '{TimeSpent}' WHERE Mixed = '{Mixed}'"
			cursor.execute(DBupdate)
			db.commit()

	def DBextract(DateRange):
		db = sqlite3.connect("TTW.db")
		cursor = db.cursor()
		today = DBhandle.DateToday()

		def NoRange(DateRange):
			DBnorange = f"SELECT AppName, AppTitle, Time FROM TimedApps WHERE Date = '{DateRange[0]}'" 
			cursor.execute(DBnorange)
			extracted = cursor.fetchall()
			return extracted

		def Ranged(DateRange):
			DBranged = f"SELECT AppName, AppTitle, Time FROM TimedApps WHERE Date BETWEEN '{DateRange[0]}' and '{DateRange[1]}'" 
			cursor.execute(DBranged)
			extracted = cursor.fetchall()
			return extracted

		def SupportedApp(AppTitle):
			DBranged = f"SELECT AppName, Time FROM TimedApps WHERE AppTitle = '{AppTitle}'" 
			cursor.execute(DBranged)
			extracted = cursor.fetchall()
			return extracted

		def SupportedSorter(Data):
			listed = {}
			for x,y in Data:
				if x in listed:
					listed[x] = listed.get(x) + y
				else:
					listed[x.split(" ")[-1]] = y

			listed_sort = sorted(listed.items(), key=lambda x: x[1])
			output = {}
			for i in range(1, 6):
				try:
					x, y = listed_sort[-i][0], listed_sort[-i][1]
					output[f"{x}"] = (y / 60) / 60
				except:
					break
			return output

		def Sorter(Data):
			listed = {}
			for x,y,z in Data:
				main = SupportedApps.AppSort(x,y,z)
				if main[0] in listed:
					listed[main[0]] = listed.get(main[0]) + main[1]
				else:
					listed[main[0]] = main[1]

			listed_sort = sorted(listed.items(), key=lambda x: x[1])
			output = {}
			for i in range(1, 6):
				try:
					x, y = listed_sort[-i][0], listed_sort[-i][1]
					output[f"{x}"] = (y / 60) / 60
				except:
					break
			return output

		if SupportedApps.AppRetrieve(DateRange) == True:
			Data = SupportedApp(DateRange)
			return SupportedSorter(Data)

		elif DateRange == "Monthly":
			MonthAgo = str(today - datetime.timedelta(days=30))
			Data = Ranged([str(MonthAgo), str(today)])
			return Sorter(Data)

		elif DateRange == "Weekly":
			WeekAgo = str(today - datetime.timedelta(days=7))
			Data = Ranged([str(WeekAgo), str(today)])
			return Sorter(Data)
			
		elif DateRange == "Daily":
			Data = NoRange([str(today)])
			return Sorter(Data)