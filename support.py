
class SupportedApps(object):

	"""
	Class for supported apps:
	AppCheck = Checks for AppName and AppTitle to save
	AppSort = Check for AppTitle to seein what way to display data
	AppRetrieve = Display data from specific app
	"""

	@staticmethod
	def AppCheck(AppTitle, AppName, AppSplit):
		if AppName == "Google Chrome":
			AppName = AppSplit[-2].split(" ")[-1]
			AppTitle = AppSplit[-1]

		elif AppName == "Sublime Text":
			try:
				AppName = AppSplit[0].split(" ")[1]
				if AppName == "•":
					AppName == "NoProject"
			except:
				AppName = "NoProject"
			AppTitle = AppSplit[-1]
		elif AppName == "Apply SQL Script to Database":
			AppName = "MySQL Workbench"

		return AppTitle, AppName

	@staticmethod
	def AppSort(x,y,z):
		if y == "Sublime Text":
			return (y, z)
		elif y == "Google Chrome":
			return (y, z)
		else:
			return (x, z)

	def AppRetrieve(App):
		check = ["Google Chrome", "Sublime Text"]
		if App in check:
			return True
		else:
			return False
