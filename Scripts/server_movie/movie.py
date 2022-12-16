import os
import subprocess
import sys
import time
import psutil
import win32api
import win32con
import Scripts.server_movie.port_scanning as port_scanning


# https://github.com/mafintosh/peerflix
# npm install -g peerflix


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc_pid in process.children(recursive=True):
        proc_pid.kill()
    process.kill()


# credits clear_data():
# https://pt.stackoverflow.com/questions/421175/como-deletar-arquivos-e-pastas-recursivamente-de-modo-seguro-com-python
def clear_data(locate):
    for raiz, diretorios, arquivos in os.walk(locate):
        for arquivo in arquivos:
            try:
                win32api.SetFileAttributes(os.path.join(raiz, arquivo), win32con.FILE_ATTRIBUTE_NORMAL)
                os.remove(os.path.join(raiz, arquivo))
            except Exception:
                os.system(f'del /q /f /s {locate}')
                pass


class Movie:
    def __init__(self):
        self.listPath = None
        self.dirPath = None
        self.magnet_link = None
        self.server_cmd = None
        self.hostname = port_scanning.hostName()
        self.full_screen = False
        self.PORT = port_scanning.port_scanning()
        self.red = '\033[31m'
        self.green = '\033[32m'
        self.colorReset = "\033[0;0m"
        self.vlc = True

    def cleardir(self):
        self.listPath = ['C:\\Windows\\Prefetch', 'C:\\Windows\\Temp']
        path_temp = os.getenv('temp')
        path_temp = path_temp.replace('Roaming', '\\Local\\Temp')
        self.listPath.append(path_temp)

        for i in self.listPath:
            clear_data(i)

    def playMovie(self):
        try:
            cmd = f'peerflix -p {self.PORT} ' + self.magnet_link + f' --on-listening'
            self.server_cmd = subprocess.Popen(["start/min", "/wait", "cmd", "/k", cmd],
                                               shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            seconds = 0
            print('This can take 1 to 2 minutes.')
            while port_scanning.accessTrue(self.hostname, self.PORT):
                sys.stdout.write('\r' + f'{seconds}s Connecting.')
                seconds += 1
                if seconds == 120:
                    print(f'{self.red}Could not connect.{self.colorReset}')
                    return False
                time.sleep(1)
                sys.stdout.write('\r' + f'{seconds}s Connecting...')

            print(f'{self.green}Connected.{self.colorReset}')

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            try:
                subprocess.check_output(f"cd C:\Program Files\VideoLAN\VLC", shell=True)
            except subprocess.CalledProcessError:
                self.vlc = False

            if self.vlc:
                if self.full_screen:
                    os.system(f"start vlc http://{self.hostname}:{self.PORT}/ –fullscreen")
                    input('Press "ENTER" to go back: ')

                else:
                    os.system(f"start vlc http://{self.hostname}:{self.PORT}/")
                    input('Press "ENTER" to go back: ')
            else:
                if self.full_screen:
                    subprocess.call(f"C:\\Program Files (x86)\\Windows Media Player\\wmplayer.exe /play /close "
                                    f"/fullscreen http://{self.hostname}:{self.PORT}/")
                    input('Press "ENTER" to go back: ')
                else:
                    subprocess.call(f"C:\\Program Files (x86)\\Windows Media Player\\wmplayer.exe /play /close "
                                    f"http://{self.hostname}:{self.PORT}/")
                    input('Press "ENTER" to go back: ')

        except TypeError:
            return False


'''pessoa = Movie()
magnet_link = input()
pessoa.full_screen = True
pessoa.playMovie()
kill(pessoa.server_cmd.pid)'''

# limpar a pasta C:\Users\...\AppData\Local\Temp\torrent-stream  --> ok
