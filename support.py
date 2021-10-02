
class SupportedApps():

	def AppCheck(AppTitle, AppName, AppSplit):
		if "Google Chrome" in AppName:
			AppName = AppSplit[-2].split(" ")[-1]
			AppTitle = "Google Chrome"

		elif "Sublime Text" in AppName:
			try:
				AppName = AppSplit[0].split(" ")[1].replace("(", "").replace(")", "")
				if AppName == "•":
					AppName == "NoProject"
			except:
				AppName = "NoProject"
			AppTitle = "Sublime Text"
		elif "Apply SQL Script to Database" in AppName:
			AppName = "MySQL Workbench"

		return AppTitle, AppName

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
