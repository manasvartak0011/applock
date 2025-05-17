import psutil
import os
import threading
import time
import datetime
import PySimpleGUI as sg
from pystray import Icon, MenuItem as item, Menu
from PIL import Image

PASSWORD_FILE = 'password.txt'
locked_apps = ['opera.exe', 'vlc.exe', 'notepad.exe']
lock_status = True  # Global flag to control locking

def get_today_password():
    return datetime.datetime.now().strftime('%d%m%Y')

def get_custom_password():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as file:
            return file.read().strip()
    return None

def monitor_and_lock_apps():
    global lock_status
    while True:
        if lock_status:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] in locked_apps:
                        print(f"🔒 {proc.info['name']} blocked.")
                        os.system(f"taskkill /f /pid {proc.info['pid']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        time.sleep(1)

def unlock_apps():
    global lock_status

    layout = [
        [sg.Text('Enter password to unlock apps:')],
        [sg.Input(key='-PASS-', password_char='*')],
        [sg.Button('Unlock'), sg.Button('Cancel')]
    ]
    window = sg.Window('Unlock Apps', layout, keep_on_top=True, modal=True, finalize=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        entered_password = values['-PASS-'].strip()
        today_password = get_today_password()
        custom_password = get_custom_password()

        if entered_password == today_password or (custom_password and entered_password == custom_password):
            sg.popup('✅ Apps Unlocked!', keep_on_top=True)
            lock_status = False
            break
        else:
            sg.popup('❌ Incorrect password. Try again.', keep_on_top=True)
            window['-PASS-'].update('')

    window.close()

def set_custom_password():
    layout = [
        [sg.Text('Enter new custom password:')],
        [sg.Input(key='-NEWPASS-', password_char='*')],
        [sg.Button('Set Password'), sg.Button('Cancel')]
    ]
    window = sg.Window('Set Custom Password', layout, keep_on_top=True, modal=True, finalize=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        new_password = values['-NEWPASS-'].strip()
        if new_password:
            with open(PASSWORD_FILE, 'w') as file:
                file.write(new_password)
            sg.popup('✅ Custom password set successfully.', keep_on_top=True)
            break
        else:
            sg.popup('⚠️ Password cannot be empty.', keep_on_top=True)

    window.close()

def run_tray_icon():
    menu = Menu(
        item('Unlock Apps', lambda icon, item: threading.Thread(target=unlock_apps, daemon=True).start()),
        item('Set Custom Password', lambda icon, item: threading.Thread(target=set_custom_password, daemon=True).start()),
        item('Exit', lambda icon, item: icon.stop())
    )
    # Load icon relative to script
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, 'lock.ico')
    icon_image = Image.open(icon_path)

    icon = Icon("AppLock", icon_image, "App Lock", menu)
    icon.run()

def start_app_lock_tray():
    threading.Thread(target=monitor_and_lock_apps, daemon=True).start()
    run_tray_icon()

if __name__ == '__main__':
    start_app_lock_tray()
