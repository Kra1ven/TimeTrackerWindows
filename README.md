# TimeTrackerWindows
An app made on Python to track the time you spend on each active window.

Use PyInstaller to compile "ttw.py" into an exe file. Note - After launch, a db file will be created to store data.
```
pyinstaller ttw.py --onefile --name TTW --noconsole --icon icon.ico
```
Or download the latest release -> [here](https://github.com/Kra1ven/TimeTrackerWindows/releases/latest)

![Untitled-3](https://user-images.githubusercontent.com/69338365/135713730-0e150fda-8e72-4377-b364-fb132be3e743.png)

### Features:
* Pause button
* Supported apps, as individual trackers for tabs and projects (Google Chrome, Sublime Text)
* App status
* AutoPause when user afk for more than 20 min (Also sets app status to Running when active again)

## App will not be updated
* Feature-wise updates will not be made
* Fixes and new supported apps will be added rarely

## New integration 
* New web-based app is under development, it will include the functionality of this app
* New features for the current app, such as (sleep tracking, afk time, active time, time spent on each category)
* Check my github profile to see when the first release will come out 
