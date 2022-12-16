import subprocess
import sys
import os
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import Scripts.setup as setup

if __name__ == "__main__":

    if os.name == 'nt':
        try:
            check_node_intall = subprocess.check_output('node -v', shell=True)
        except subprocess.CalledProcessError:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('NodeJS not installed.')
            time.sleep(2)
            os.system('start https://nodejs.org/en/download/')
            input('After installation, run the "npm install -g peerflix".')
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            setup.main()

    else:
        print('This version is only available for windows. We apologize.')
