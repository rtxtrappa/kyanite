import json, os, sys, subprocess
import random, string, time, threading
from pynput import keyboard
from termcolor import colored

def change_title():
    while True:
        random_title = ''.join(random.choices(string.ascii_letters + string.digits, k=15))

        os.system(f"title {random_title}")

        time.sleep(0.001)

threading.Thread(target=change_title, daemon=True).start()

def install_packages(packages):
    try:
        for package in packages:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def main():
    packages = ["json", "os", "sys", "subprocess", "random", "string", "time", "threading"]  # List your required packages here
    missing_packages = []

    for package in packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("Missing packages:", ", ".join(missing_packages))
        choice = input("The required packages aren't installed, would you like to install them? [Y/N] ")

        if choice.lower() == 'y':
            if install_packages(missing_packages):
                print("Packages installed.")
            else:
                print("Failed to install the required packages.")
            sys.exit()
        else:
            print("Exiting script.")
            sys.exit()

if __name__ == "__main__":
    main()


def on_release(key):
    try:
        if key == keyboard.Key.f1:
            Aimbot.update_status_aimbot()
        if key == keyboard.Key.f2:
            Aimbot.clean_up()
    except NameError:
        pass

def main():
    global lunar
    lunar = Aimbot(collect_data = "collect_data" in sys.argv)
    lunar.start()

def setup():
    path = "lib/config"
    if not os.path.exists(path):
        os.makedirs(path)

    print("[INFO] In-game X and Y axis sensitivity should be the same")
    def prompt(str):
        valid_input = False
        while not valid_input:
            try:
                number = float(input(str))
                valid_input = True
            except ValueError:
                print("[!] Invalid Input. Make sure to enter only the number (e.g. 6.9)")
        return number

    xy_sens = prompt("X-Axis and Y-Axis Sensitivity (from in-game settings): ")
    targeting_sens = prompt("Targeting Sensitivity (from in-game settings): ")

    print("[INFO] Your in-game targeting sensitivity must be the same as your scoping sensitivity")
    sensitivity_settings = {"xy_sens": xy_sens, "targeting_sens": targeting_sens, "xy_scale": 10/xy_sens, "targeting_scale": 1000/(targeting_sens * xy_sens)}

    with open('lib/config/config.json', 'w') as outfile:
        json.dump(sensitivity_settings, outfile)
    print("[INFO] Sensitivity configuration complete")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

    print(colored('''

	    	 ██ ▄█▀▓██   ██▓ ▄▄▄       ███▄    █  ██▓▄▄▄█████▓▓█████ 
	    	 ██▄█▒  ▒██  ██▒▒████▄     ██ ▀█   █ ▓██▒▓  ██▒ ▓▒▓█   ▀ 
	    	▓███▄░   ▒██ ██░▒██  ▀█▄  ▓██  ▀█ ██▒▒██▒▒ ▓██░ ▒░▒███   
	    	▓██ █▄   ░ ▐██▓░░██▄▄▄▄██ ▓██▒  ▐▌██▒░██░░ ▓██▓ ░ ▒▓█  ▄ 
	    	▒██▒ █▄  ░ ██▒▓░ ▓█   ▓██▒▒██░   ▓██░░██░  ▒██▒ ░ ░▒████▒
	    	▒ ▒▒ ▓▒   ██▒▒▒  ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░▓    ▒ ░░   ░░ ▒░ ░
	    	░ ░▒ ▒░ ▓██ ░▒░   ▒   ▒▒ ░░ ░░   ░ ▒░ ▒ ░    ░     ░ ░  ░
	    	░ ░░ ░  ▒ ▒ ░░    ░   ▒      ░   ░ ░  ▒ ░  ░         ░   
	    	░  ░    ░ ░           ░  ░         ░  ░              ░  ░
            	░ ░                                                                                                              
      ''', "magenta"))
    
    print(colored('Welcome to Kyanite, ' + os.getlogin(), "magenta"))

    path_exists = os.path.exists("lib/config/config.json")
    if not path_exists or ("setup" in sys.argv):
        if not path_exists:
            print("[!] Sensitivity configuration is not set")
        setup()
    path_exists = os.path.exists("lib/data")
    if "collect_data" in sys.argv and not path_exists:
        os.makedirs("lib/data")
    from lib.aimbot import Aimbot
    listener = keyboard.Listener(on_release=on_release)
    listener.start()
    main()
