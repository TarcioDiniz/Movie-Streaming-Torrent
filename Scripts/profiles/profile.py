import sqlite3
from tabulate import tabulate
import Scripts.recommendation.recommendation as recommendation
import getpass


class Person:
    def __init__(self):
        self.name = None
        self.password = None
        self.movies_category = None
        self.full_screen = 0
        self.database = sqlite3.connect('Scripts/profiles/database/profile.db')
        # 0self.database = sqlite3.connect('./database/profile.db')
        self.cursor = self.database.cursor()
        self.Watched_movies = None

    def createDataBase(self):
        self.cursor.execute("CREATE TABLE profile ("
                            "name TEXT, "
                            "password TEXT, "
                            "movies_category TEXT, "
                            "full_screen INTEGER, Watched_movies TEXT)")

    def createProfile(self):
        categoryMovieList = ['Action', 'Adventure', 'Comedy', 'Crime', 'Animation',
                             'Documentary', 'Drama', 'Western', 'War', 'Thriller',
                             'Sci-Fi', 'Mystery', 'Fantasy', 'Romance', 'Horror']
        tableCategory = []
        for i in range(len(categoryMovieList)):
            tableCategory.append([])
            for j in range(1):
                tableCategory[i].append(f'{i}')
                tableCategory[i].append(categoryMovieList[i])

        tableCategory.insert(0, ['Id', 'Movies Category'])

        self.name = input('Inform your name: ')

        while self.name == '':
            self.name = input('Please add a name to your profile: ')

        self.password = input('Create your password: ')
        print(tabulate(tableCategory, headers='firstrow', tablefmt='grid'))

        choice_Category = []

        self.movies_category = input('Choose your category. To exit press "Enter": ')

        while self.movies_category != '':
            if not self.movies_category.isnumeric() or int(self.movies_category) < 0 or \
                    int(self.movies_category) > len(categoryMovieList) - 1:

                print(f'Please enter number between 0 and {len(categoryMovieList) - 1}')
                self.movies_category = input('Choose your category. To exit press "Enter": ')

                if self.movies_category == '':
                    break
            else:
                choice_Category.append(self.movies_category)
                self.movies_category = input('Choose your category. To exit press "Enter": ')

        category_movie = []
        for i in range(len(choice_Category)):
            category_movie.append(categoryMovieList[int(choice_Category[i])])
        self.movies_category = ', '.join(category_movie)

        fullscreen_option = input('Want to enable full screen option [Y/N]: ').upper()

        while fullscreen_option != 'Y':
            if fullscreen_option == 'N':
                break
            else:
                fullscreen_option = input('Want to enable full screen option [Y/N]: ').upper()

        if fullscreen_option == 'Y':
            self.full_screen = 1
        else:
            self.full_screen = 0

        self.cursor.execute(f"INSERT INTO profile "
                            f"VALUES('{self.name}', "
                            f"'{self.password}', "
                            f"'{self.movies_category}', "
                            f"{self.full_screen}, '')")

        self.database.commit()

    def deleteProfile(self):
        self.cursor.execute("SELECT *FROM profile")
        table_profile = []
        fetchall = self.cursor.fetchall()
        for i in range(len(fetchall)):
            table_profile.append([])
            for j in range(1):
                table_profile[i].append(f'{i}')
                table_profile[i].append(f'{fetchall[i][0]}')
        table_profile.insert(0, ['Id', 'Profile'])
        print(tabulate(table_profile, headers='firstrow', tablefmt='grid'))
        self.database.commit()

        deleteSelector = input('Enter the id of the profile you want to delete. Press "Enter" to exit. ')
        if deleteSelector == '':
            return self.connectProfile()

        while not deleteSelector.isnumeric() or int(deleteSelector) > len(fetchall) or int(deleteSelector) < 0:
            deleteSelector = input('Enter the id of the profile you want to delete. Press "Enter" to exit. ')
            if deleteSelector == '':
                return self.connectProfile()
        print(fetchall[int(deleteSelector)][0])
        self.cursor.execute(f"DELETE from profile WHERE name='{fetchall[int(deleteSelector)][0]}'")
        self.database.commit()

    def updateWatched_movies(self, name_profile, title_movie):
        self.cursor.execute("SELECT *FROM profile")
        fetchall = self.cursor.fetchall()

        for i in range(len(fetchall)):
            try:
                if fetchall[i][0] == name_profile:
                    fetchall = fetchall[i]
            except IndexError:
                pass

        watched_movies = fetchall[-1]
        if watched_movies == '':
            watched_movies = title_movie
        else:
            watched_movies = watched_movies.split(', ')
            list_watched_movies = []
            for i in range(len(watched_movies)):
                if title_movie not in watched_movies[i]:
                    list_watched_movies.append(watched_movies[i])
            list_watched_movies = ', '.join(list_watched_movies)
            watched_movies = f'{list_watched_movies}, {title_movie}'

        self.database.commit()
        try:
            self.cursor.execute(f"UPDATE profile SET Watched_movies='{watched_movies}' WHERE name='{fetchall[0]}'")
            self.database.commit()
        except sqlite3.OperationalError:
            print('Name not found.')

    def connectProfile(self):
        self.cursor.execute("SELECT *FROM profile")
        table_profile = []
        fetchall = self.cursor.fetchall()
        for i in range(len(fetchall)):
            table_profile.append([])
            for j in range(1):
                table_profile[i].append(f'{i}')
                table_profile[i].append(f'{fetchall[i][0]}')
        table_profile.insert(0, ['Id', 'Profile'])
        table_profile.insert(len(table_profile), [f'{len(table_profile) - 1}', 'Create profile'])
        table_profile.insert(len(table_profile), [f'{len(table_profile) - 1}', 'Delete profile'])
        print(tabulate(table_profile, headers='firstrow', tablefmt='grid'))

        table_profile = table_profile[1:]

        def login():
            answerPlayer = input('Choose any id to continue: ')

            while not answerPlayer.isnumeric():
                answerPlayer = input('please enter a number equivalent to the id in the table above: ')

            while int(answerPlayer) < 0 or int(answerPlayer) > len(table_profile) - 1:
                answerPlayer = input('Choose any id to continue: ')
                while not answerPlayer.isnumeric():
                    answerPlayer = input('please enter a number equivalent to the id in the table above: ')

            if int(answerPlayer) == len(table_profile) - 2:
                self.createProfile()
                return self.connectProfile()
            else:
                if int(answerPlayer) == len(table_profile) - 1:
                    self.deleteProfile()
                    return self.connectProfile()
                else:
                    self.database.commit()

                    user = table_profile[int(answerPlayer)][1]
                    password = getpass.getpass(f'{user} inform your password: ')

                    verify_user = self.cursor.execute('SELECT * FROM profile WHERE name = ? AND password = ?',
                                                      (user, password)).fetchall()
                    while not verify_user:
                        print('Login error! Try again!')
                        return login()
                    return user

        return login()

    def recommendation_movies(self, name_profile):
        self.cursor.execute("SELECT *FROM profile")
        fetchall = self.cursor.fetchall()

        for i in range(len(fetchall)):
            try:
                if fetchall[i][0] == name_profile:
                    fetchall = fetchall[i]
            except IndexError:
                pass

        watched_movies = fetchall[-1]
        if watched_movies == '':
            return None
        else:
            watched_movies = watched_movies.split(', ')
            watched_movies = watched_movies[-1]
            return recommendation.similar_movies(watched_movies)

    def full_screenTrueFalse(self, name_profile):
        self.cursor.execute("SELECT *FROM profile")
        fetchall = self.cursor.fetchall()

        for i in range(len(fetchall)):
            try:
                if fetchall[i][0] == name_profile:
                    fetchall = fetchall[i]
            except IndexError:
                pass

        full_screen = fetchall[-2]

        if full_screen == 1:
            return True
        else:
            return False
