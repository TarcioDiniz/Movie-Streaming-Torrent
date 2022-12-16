import requests

import unidecode
from bs4 import BeautifulSoup


def searchMovie(search):
    search = search.lower()
    search = unidecode.unidecode(search)
    if ' ' in search:
        search = search.replace(' ', '+')
    link = f'https://vacatorrent.com/index.php?campo1={search}&nome_campo1=pesquisa&categoria=lista'
    website = requests.get(link)
    websiteHtml = BeautifulSoup(website.content, 'html.parser')
    links_by_category = websiteHtml.find('ul', attrs={'class': 'list-inline'})
    links_by_category = links_by_category.find_all('div', attrs={'class': 'col-sm-4 col-xs-12'})
    links_by_category = str(links_by_category).split('col-sm-4 col-xs-12')
    links_by_category = links_by_category[1:]
    links_by_category = str(links_by_category).split('</a>')
    for i in range(len(links_by_category)):
        if 'class="centraliza" ' in links_by_category[i]:
            links_by_category[i] = links_by_category[i].replace(
                links_by_category[i][:links_by_category[i].index('class="centraliza" ')], '')
    _dictionary = []
    for i in range(len(links_by_category)):
        links_by_category[i] = links_by_category[i][9:].split(' ')
        try:
            _dictionary.append({
                'LINK': str(links_by_category[i][1: links_by_category[i].index('alt="Filme')])[8:-8],
                'TITLE': ' '.join(links_by_category[i][links_by_category[i].index('title="Filme') + 1: -1])
            })
        except ValueError:
            pass

    dictionary = []
    for i in range(len(_dictionary)):
        if '4k' not in _dictionary[i]['TITLE'].lower():
            dictionary.append(_dictionary[i])

    return dictionary


# https://vacatorrent.com/orfa-2-a-origem-torrent for test of returnLinkTorrent()

def returnLinkTorrent(link):
    try:
        website = requests.get(link)
    except requests.exceptions.MissingSchema:
        return False
    websiteHtml = BeautifulSoup(website.content, 'html.parser')
    links_by_category = websiteHtml.find_all('ul', attrs={'class': 'list-group'})
    links_by_category = ''.join(list(str(links_by_category))[5:-8]).split('</a>')

    # --------------------------Genre--------------------------------------------
    genreMovieList = []
    genreMovie = websiteHtml.find('div', attrs={'class': 'infos'})
    genreMovie = genreMovie.find_all('a')
    for i in range(len(genreMovie)):
        if 'itemprop="genre"' in str(genreMovie[i]):
            genreMovieList.append(str(genreMovie[i])[
                                  str(genreMovie[i]).index('itemprop="genre">') + len('itemprop="genre">'):
                                  str(genreMovie[i]).index('</span></a>')].replace(' ', ''))

    # -----------------------------Links + Genre----------------------------------

    _dicionary = [{'genreMovie': genreMovieList}, []]

    for i in range(len(links_by_category)):
        if 'list-group-item-success newdawn" ' in links_by_category[i]:
            links_by_category[i] = links_by_category[i].replace(
                links_by_category[i][:links_by_category[i].index('list-group-item-success newdawn" ')], '')
    for i in range(len(links_by_category)):
        links_by_category[i] = (links_by_category[i]).split(' ')

        if 'LEGENDAS' not in links_by_category[i]:
            if 'list-group-item-success"' not in links_by_category[i]:
                TitleMovie = ' '.join(links_by_category[i][
                                      4:links_by_category[i].index('</span>') - 4]).replace('title="', '')
                LinkMovie = str(links_by_category[i][2:3])[8:-3]

                _dicionary[1].append({
                    'TitleMovie': TitleMovie,
                    'LinkMovie': LinkMovie
                })
    return _dicionary


def last_releases():
    link = 'https://vacatorrent.com/lancamentos-filmes'
    website = requests.get(link)
    websiteHtml = BeautifulSoup(website.content, 'html.parser')
    websiteHtml = websiteHtml.find('ul', attrs={'class', 'list-inline'})
    websiteHtml = websiteHtml.find_all('li')
    dicionary = []
    for i in range(len(websiteHtml)):
        websiteHtml[i] = str(websiteHtml).split(' ')
        websiteHtml[i] = ' '.join(websiteHtml[i])
        websiteHtml[i] = websiteHtml[i][websiteHtml[i].index('href=') + 6:websiteHtml[i].index('src="')]
        link = websiteHtml[i][:websiteHtml[i].index(' ') - 1]
        title = websiteHtml[i][websiteHtml[i].index('title="') + 7: websiteHtml[i].index('Torrent')]
        dicionary.append({
            'TITLE': title,
            'LINK': link
        })

    return dicionary
