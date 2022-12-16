import time
import sys
import os
import sqlite3

from tabulate import tabulate

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import Scripts.torrent_search.webScraping as webScraping
import Scripts.server_movie.movie as movie
import Scripts.profiles.profile as profile_person


class Player:
    def __init__(self):
        self.movies = None
        self.site_movie = None
        self.movieNews = None
        self.profile = self.checkProfile()
        self.magnet_link = None
        self.full_screen = profile_person.Person().full_screenTrueFalse(self.profile)
        self.recommendation = None

    @property
    def title_art(self):
        title_art = """

░██████╗████████╗██████╗░███████╗░█████╗░███╗░░░███╗████████╗
██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔══██╗████╗░████║╚══██╔══╝
╚█████╗░░░░██║░░░██████╔╝█████╗░░███████║██╔████╔██║░░░██║░░░
░╚═══██╗░░░██║░░░██╔══██╗██╔══╝░░██╔══██║██║╚██╔╝██║░░░██║░░░
██████╔╝░░░██║░░░██║░░██║███████╗██║░░██║██║░╚═╝░██║░░░██║░░░
╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░░░╚═╝░░░
        """
        return title_art

    def checkProfile(self):
        print(self.title_art)
        print('Welcome to your movie streaming.')
        self.profile = profile_person.Person()
        try:
            self.profile.createDataBase()
            self.profile.createProfile()
        except sqlite3.OperationalError:
            pass
        self.profile = self.profile.connectProfile()
        return self.profile

    def searchMovie(self, name_movie):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.title_art)
        print('\nWe will search that movie for you in our system.')
        sys.stdout.write('\r' + '.')
        time.sleep(0.5)
        sys.stdout.write('\r' + '..')
        time.sleep(0.5)
        sys.stdout.write('\r' + '...')
        time.sleep(0.5)
        sys.stdout.write('\r' + '.')
        time.sleep(0.5)
        sys.stdout.write('\r' + '..')
        self.movies = webScraping.searchMovie(name_movie)
        os.system('cls' if os.name == 'nt' else 'clear')
        movie_table = []
        for i in range(len(self.movies)):
            movie_table.append([])
            for j in range(1):
                movie_table[i].append(f'{i}')
                movie_table[i].append(f'{self.movies[i]["TITLE"]}')
        movie_table.insert(0, ['Id', 'Movie'])
        print(tabulate(movie_table, headers='firstrow', tablefmt='grid'))
        if len(self.movies) == 0:
            input("We didn't" + ' find any related movies. click "enter" to return to the menu.')
            return self.launcher()
        choose = input(
            'Choose the id of the movie you want to watch or type "close" to return to the menu. ').lower()
        if choose == 'close':
            os.system('cls' if os.name == 'nt' else 'clear')
            return self.launcher()
        else:
            while not choose.isnumeric():
                choose = input(
                    'Choose the id of the movie you want to watch or type "close" to return to the menu. ').lower()
                if choose == 'close':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    return self.launcher()
            while int(choose) < 0 or int(choose) > len(self.movies) - 1:
                choose = input('Choose the quality id of the movie you want to watch or type "close" to return to '
                               'the menu. ').lower()
                if choose == 'close':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    return self.launcher()
                while not choose.isnumeric():
                    choose = input(
                        'Choose the quality id of the movie you want to watch or type "close" to return to '
                        'the menu. ').lower()
                    if choose == 'close':
                        os.system('cls' if os.name == 'nt' else 'clear')
                        return self.launcher()
        profile_person.Person().updateWatched_movies(self.profile, self.movies[int(choose)]['TITLE'])
        return self.movies[int(choose)]['LINK']

    def movieReleases(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.title_art)
        print('\nLooking for the new list of newly added movies.')
        sys.stdout.write('\r' + '.')
        time.sleep(0.5)
        sys.stdout.write('\r' + '..')
        time.sleep(0.5)
        sys.stdout.write('\r' + '...')
        time.sleep(0.5)
        sys.stdout.write('\r' + '.')
        time.sleep(0.5)
        sys.stdout.write('\r' + '..\n')
        self.movieNews = webScraping.last_releases()
        movieNews_table = []
        for i in range(len(self.movieNews)):
            movieNews_table.append([])
            for j in range(1):
                movieNews_table[i].append(f'{i}')
                movieNews_table[i].append(f"{self.movieNews[i]['TITLE']}")
        movieNews_table.insert(0, ['Id', 'Movie News'])
        print(tabulate(movieNews_table, headers='firstrow', tablefmt='grid'))

        choose = input('Choose the id of the movie you want to watch or type "close" to return to the menu. ').lower()
        if choose == 'close':
            os.system('cls' if os.name == 'nt' else 'clear')
            return self.launcher()
        else:
            while not choose.isnumeric():
                choose = input(
                    'Choose the id of the movie you want to watch or type "close" to return to the menu. ').lower()
                if choose == 'close':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    return self.launcher()

            while int(choose) < 0 or int(choose) > len(self.movieNews) - 1:
                choose = input('Choose the quality id of the movie you want to watch or type "close" to return to '
                               'the menu. ').lower()
                if choose == 'close':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    return self.launcher()
                while not choose.isnumeric():
                    choose = input(
                        'Choose the quality id of the movie you want to watch or type "close" to return to '
                        'the menu. ').lower()
                    if choose == 'close':
                        os.system('cls' if os.name == 'nt' else 'clear')
                        return self.launcher()

            profile_person.Person().updateWatched_movies(self.profile, self.movieNews[int(choose)]['TITLE'])
            return self.movieNews[int(choose)]['LINK']

    def linkTorrent(self):
        print(self.title_art)
        print('\nAbout the quality of your film')
        linkTorrent = webScraping.returnLinkTorrent(self.site_movie)
        if linkTorrent:
            linkTorrent_table = []
            for i in range(len(linkTorrent[1])):
                linkTorrent_table.append([])
                for j in range(1):
                    linkTorrent_table[i].append(f'{i}')
                    linkTorrent_table[i].append(f"{linkTorrent[1][i]['TitleMovie']}")
            linkTorrent_table.insert(0, ['Id', 'Movie Quality'])
            linkTorrent_table.append(['Genre Movie', f'{" ".join(linkTorrent[0]["genreMovie"])}'])
            print(tabulate(linkTorrent_table, headers='firstrow', tablefmt='grid'))

            choose = input('Choose the quality id of the movie you want to watch or type "close" to return to '
                           'the menu. ').lower()
            if choose == 'close':
                os.system('cls' if os.name == 'nt' else 'clear')
                return self.launcher()
            else:
                while not choose.isnumeric():
                    choose = input(
                        'Choose the quality id of the movie you want to watch or type "close" to return to '
                        'the menu. ').lower()
                    if choose == 'close':
                        os.system('cls' if os.name == 'nt' else 'clear')
                        return self.launcher()

                while int(choose) < 0 or int(choose) > len(linkTorrent[1]) - 1:
                    choose = input('Choose the quality id of the movie you want to watch or type "close" to return to '
                                   'the menu. ').lower()
                    if choose == 'close':
                        os.system('cls' if os.name == 'nt' else 'clear')
                        return self.launcher()
                    while not choose.isnumeric():
                        choose = input(
                            'Choose the quality id of the movie you want to watch or type "close" to return to '
                            'the menu. ').lower()
                        if choose == 'close':
                            os.system('cls' if os.name == 'nt' else 'clear')
                            return self.launcher()

                return linkTorrent[1][int(choose)]['LinkMovie']

    def recommendedMovies(self):
        print(self.title_art)
        print('\nLooking for movies similar to what you watched.')
        sys.stdout.write('\r' + '.')
        time.sleep(0.5)
        sys.stdout.write('\r' + '..')
        time.sleep(0.5)
        sys.stdout.write('\r' + '...')
        time.sleep(0.5)
        sys.stdout.write('\r' + '.')
        time.sleep(0.5)
        sys.stdout.write('\r' + '..\n')
        self.recommendation = profile_person.Person().recommendation_movies(self.profile)
        if self.recommendation is None:
            print('We are getting to know you better. Please watch more '
                  'movies so that we can recommend titles that will please you.')
            input('Press any key to go back: ')
            return self.launcher()
        else:
            recommendation_table = []
            for i in range(len(self.recommendation)):
                recommendation_table.append([])
                for j in range(1):
                    recommendation_table[i].append(f'{i}')
                    recommendation_table[i].append(f'{self.recommendation[i]}')
            recommendation_table.insert(0, ['Id', 'Movie Recommendation'])
            print(tabulate(recommendation_table, headers='firstrow', tablefmt='grid'))
            choose = input(
                'Choose the id of the movie you want to watch or type "close" to return to the menu. ').lower()
            if choose == 'close':
                os.system('cls' if os.name == 'nt' else 'clear')
                return self.launcher()
            else:
                while not choose.isnumeric():
                    choose = input(
                        'Choose the id of the movie you want to watch or type "close" to return to the menu. ').lower()
                    if choose == 'close':
                        os.system('cls' if os.name == 'nt' else 'clear')
                        return self.launcher()

                while int(choose) < 0 or int(choose) > len(self.recommendation) - 1:
                    choose = input('Choose the quality id of the movie you want to watch or type "close" to return to '
                                   'the menu. ').lower()
                    if choose == 'close':
                        os.system('cls' if os.name == 'nt' else 'clear')
                        return self.launcher()
                    while not choose.isnumeric():
                        choose = input(
                            'Choose the quality id of the movie you want to watch or type "close" to return to '
                            'the menu. ').lower()
                        if choose == 'close':
                            os.system('cls' if os.name == 'nt' else 'clear')
                            return self.launcher()
                return self.recommendation[int(choose)]

    def playMovie(self):
        try:
            play = movie.Movie()
            play.full_screen = self.full_screen
            play.magnet_link = self.magnet_link
            try:
                play.playMovie()
            except KeyboardInterrupt:  # if the user closes the "Windows media player" before starting the movie
                movie.kill(play.server_cmd.pid)
                return False
            movie.kill(play.server_cmd.pid)
        except AttributeError:
            exit()

    def launcher(self):  # função mãe
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.title_art)
        print(f'\nWelcome {self.profile} to your movie streaming.')

        menu_table = [['Id', 'Menu'], ['0', 'Movie news'], ['1', 'Movie recommendation'],
                      ['2', 'Search movie'], ['3', 'Exit']]
        print(tabulate(menu_table, headers='firstrow', tablefmt='grid'))

        choice_menu = input('Choose an option to continue: ')

        while not choice_menu.isnumeric():
            choice_menu = input('Choose an option to continue: ')

        while int(choice_menu) < 0 or int(choice_menu) > 3:
            choice_menu = input('Choose an option to continue: ')
            while not choice_menu.isnumeric():
                choice_menu = input('Choose an option to continue: ')

        if int(choice_menu) == 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.site_movie = self.movieReleases()
            os.system('cls' if os.name == 'nt' else 'clear')
            self.magnet_link = self.linkTorrent()
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self.title_art)
            print()
            if not self.playMovie():
                return self.launcher()

        elif int(choice_menu) == 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            movieChoose = self.recommendedMovies()
            os.system('cls' if os.name == 'nt' else 'clear')
            self.site_movie = self.searchMovie(movieChoose)
            os.system('cls' if os.name == 'nt' else 'clear')
            self.magnet_link = self.linkTorrent()
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self.title_art)
            print()
            if not self.playMovie():
                return self.launcher()

        elif int(choice_menu) == 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self.title_art)
            choose = input(
                'Search for the movie you want to watch: ').lower()
            if choose == 'close':
                os.system('cls' if os.name == 'nt' else 'clear')
                return self.launcher()
            else:
                self.site_movie = self.searchMovie(choose)
                os.system('cls' if os.name == 'nt' else 'clear')
                self.magnet_link = self.linkTorrent()
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.title_art)
                print()
                if not self.playMovie():
                    return self.launcher()

        elif int(choice_menu) == 3:
            sys.stdout.write('\r' + 'Closing.')
            time.sleep(0.5)
            sys.stdout.write('\r' + 'Closing..')
            time.sleep(0.5)
            sys.stdout.write('\r' + 'Closing...')
            time.sleep(0.5)
            sys.stdout.write('\r' + 'Closing.')
            time.sleep(0.5)
            sys.stdout.write('\r' + 'Closing..')
            movie.Movie().cleardir()


def main():
    pessoa = Player()
    pessoa.launcher()
