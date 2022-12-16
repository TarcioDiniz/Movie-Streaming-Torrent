import googlesearch
import html
from bs4 import BeautifulSoup
from urllib.request import urlopen


def similar_movies(movie_name):
    result = []
    for i in googlesearch.search(f'filmes tipo {movie_name}', stop=10):
        result.append(i)
    selected_result = []
    for i in range(len(result)):
        if 'https://filmestipo.com/' in result[i]:
            selected_result.append(result[i])

    def filmestipo(movie_link):
        url = movie_link
        page = urlopen(url)
        html_bytes = page.read()
        website = html_bytes.decode("utf-8")
        websiteHtml = BeautifulSoup(website, 'html.parser')
        websiteHtml = websiteHtml.find_all('a', attrs={'class': 'name'})
        listMovie = []
        for j in range(len(websiteHtml)):
            websiteHtml[j] = html.unescape(str(websiteHtml[j])[str(websiteHtml[j]).index('>') + 1: -4]).replace('@',
                                                                                                                'a')
            websiteHtml[j] = websiteHtml[j][:websiteHtml[j].index('(') - 1]  # nome do filme (2020)
            listMovie.append(websiteHtml[j])

        return listMovie

    listMovie = []
    for i in range(len(selected_result)):
        listMovie.append(filmestipo(selected_result[i]))

    new_listMovie = []
    for i in range(len(listMovie)):
        for j in range(len(listMovie[i])):
            new_listMovie.append(listMovie[i][j])

    new_listMovie = list(set(new_listMovie))

    return new_listMovie

# print(similar_movies('rambo'))
