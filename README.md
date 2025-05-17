# AppLocker

A simple **Python desktop app locker** with a system tray icon that automatically locks specified applications by killing their processes.  
The unlock password changes daily based on the current date, and users can also set a custom password.

---

## Features

- Automatically locks specified apps by terminating their processes.
- Daily default password is today’s date in `ddmmyyyy` format.
- Option to set and use a custom password stored securely in a local file.
- System tray icon with a menu to:
  - Unlock apps by entering password
  - Set or change custom password
  - Exit the app
- Unlock dialog supports masked password input.
- Runs silently in the system tray.

---

## Supported Apps

You can customize the apps to lock by modifying the `locked_apps` list in `applock.py`, for example:

```python
locked_apps = ['opera.exe', 'notepad.exe']

