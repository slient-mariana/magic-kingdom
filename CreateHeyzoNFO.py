# This is a Python script:
# 1. Download Heyzo video metadata
# 2. Download gallery with phpauto

import requests
import os
import pathlib
from bs4 import BeautifulSoup

def create_nfo(code, response):

    # Get information from response
    soup = BeautifulSoup(response.content, 'html.parser')

    movid_info = soup.find('table', class_='movieInfo')
    studio: str = f'HEYZO'
    base_path = f'/mariana/Movies/'
    title: str = soup.find('div', id='movie') .find('h1').text.strip().split()[0]
    actor: str = movid_info.find('tr', class_='table-actor').find_all('td')[1].find('a').text.strip()
    release_day = movid_info.find('tr', class_='table-release-day').find_all('td')[1].text.strip()
    year: str = release_day[0:4]
    desc: str = f''
    if movid_info.find('p', class_='memo'):
        desc = movid_info.find('p', class_='memo').text.strip()
    series: str = movid_info.find('tr', class_='table-series').find_all('td')[1].text.strip()
    tags = movid_info.find('tr', class_='table-tag-keyword-big').find_all('a')
    # movie folder name
    movie_folder_name: str = f'{actor} - [{year}] {title} [{studio}-{code}]'

    # Create Actress folder
    parent_path = os.environ['USERPROFILE'] + f'\Desktop\{actor}'
    pathlib.Path(parent_path).mkdir(parents=True, exist_ok=True)

    # Create Movie folder
    movie_folder_path = f'{parent_path}\{movie_folder_name}'
    pathlib.Path(movie_folder_path).mkdir(parents=True, exist_ok=True)

    # Download Images
    print(f'Start Download Landscape and Fanart')
    # 1. Landscape
    landscape = f'landscape.jpg'
    landscape_pathname = f'{movie_folder_path}\{landscape}'
    landscape_response = requests.get(f'https://www.heyzo.com/contents/3000/{code}/images/player_thumbnail.jpg')
    landscape_file = open(landscape_pathname, 'wb')
    landscape_file.write(landscape_response.content)
    landscape_file.close()

    fanart = f'fanart.jpg'
    fanart_pathname = f'{movie_folder_path}\{fanart}'
    fanart_file = open(fanart_pathname, 'wb')
    fanart_file.write(landscape_response.content)
    fanart_file.close()

    # 2. Get extra-fanart
    # Get from https://www.tubetubetube.com/pics/heyzo/airi-miun/2513/airi-miun-21.jpg
    extrafanart_base_url: str = f'https://www.tubetubetube.com/pics/heyzo/'
    actor_english_name: str = f''
    image_amount: int = 21
    en_url: str = f'https://en.heyzo.com/moviepages/{code}/index.html'
    en_response = requests.get(en_url)
    if en_response.status_code == requests.codes.ok:
        en_soup = BeautifulSoup(en_response.content, 'html.parser')
        actor_english_name: str = en_soup.find('table', class_='movieInfo').find_all('a')[0].text.strip()

        if len(actor_english_name) != 0:
            print(f'Actor English Name found: {actor_english_name}')

            input_actor_english_name_code:str = input(f'Please input replace actor name for fanart: ')
            if input_actor_english_name_code:
                actor_english_name_code = input_actor_english_name_code
            else:
                actor_english_name_code: str = actor_english_name.lower().replace(' ','-')
            #actor_english_name_code: str = f'jyuri-haruka'
            image_concat_url: str = f'{extrafanart_base_url}{actor_english_name_code}/{code}/{actor_english_name_code}'

            # Create extra-fanart folder
            extra_fanart_path = f'{movie_folder_path}/extrafanart'
            pathlib.Path(extra_fanart_path).mkdir(parents=True, exist_ok=True)

            print(f'Start download extra-fanart, url: {image_concat_url}')
            for fanart_count in range(image_amount):
                # Create Movie folder
                extrafanart = f'fanart{fanart_count+1}.jpg'
                extrafanart_pathname = f'{extra_fanart_path}/{extrafanart}'
                current_url = f'{image_concat_url}-{fanart_count + 1}.jpg'
                #image_concat_url: str = f'{actor_english_name_code}'
                image_response = requests.get(current_url)
                extrafanart_file = open(extrafanart_pathname, 'wb')
                extrafanart_file.write(image_response.content)
                extrafanart_file.close()

    #3. Download trailer
    # https://m.heyzo.com/contents/3000/2513/sample.mp4
    sample_file_url: str = f'https://heyzo.com/contents/3000/{code}/sample.mp4'
    print(f'Start download trailer, url: {sample_file_url}')
    trailer = f'trailer.mp4'
    trailer_pathname = f'{movie_folder_path}\{trailer}'
    trailer_response = requests.get(sample_file_url)
    trailer_file = open(trailer_pathname, 'wb')
    trailer_file.write(trailer_response.content)
    trailer_file.close()

    # Create NFO file and write
    nfo_filename = f'{movie_folder_path}\{movie_folder_name}.nfo'
    f = open(nfo_filename, 'w', encoding='utf=8')

    # NFO context
    f.write(f'<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
    f.write(f'<movie>\n')
    f.write(f'\t<plot>{desc}</plot>\n')
    f.write(f'\t<outline />\n')
    f.write(f'\t<lockdata>false</lockdata>\n')
    f.write(f'\t<title>{title}</title>\n')
    f.write(f'\t<originaltitle>{movie_folder_name}</originaltitle>\n')
    f.write(f'\t<sorttitle>{movie_folder_name}</sorttitle>\n')
    f.write(f'\t<year>{year}</year>\n')
    f.write(f'\t<mpaa>NC-17</mpaa>\n')
    f.write(f'\t<language>ja</language>\n')
    f.write(f'\t<countrycode>JP</countrycode>\n')
    f.write(f'\t<premiered>{release_day}</premiered>\n')
    f.write(f'\t<releasedate>{release_day}</releasedate>\n')
    if series != '-----':
        f.write(f'\t<genre>{series}</genre>\n')
    f.write(f'\t<studio>{studio}</studio>\n')
    for tag in tags:
        f.write(f'\t<tag>{tag.text.strip()}</tag>\n')
    f.write(f'\t<art>\n')
    f.write(f'\t\t<poster>{base_path}{actor}/{movie_folder_name}/poster.jpg</poster>\n')
    f.write(f'\t\t<fanart>{base_path}{actor}/{movie_folder_name}/fanart.jpg</fanart>\n')
    for index in range(image_amount):
        f.write(f'\t\t<fanart>{base_path}{actor}/{movie_folder_name}/extrafanart/fanart{index + 1}.jpg</fanart>\n')
    f.write(f'\t</art>\n')
    #for actress in actresses_ja:
    f.write(f'\t<actor>\n')
    f.write(f'\t\t<name>{actor}</name>\n')
    f.write(f'\t\t<role>{actor}</role>\n')
    f.write(f'\t\t<type>Actor</type>\n')
    f.write(f'\t</actor>\n')
    #for actress in actresses_ja:
    f.write(f'\t<artist>{actor}</artist>\n')
    f.write(f'</movie>\n')
    f.close()
if __name__ == '__main__':

    # Basic Inforamtion
    code: str = input('code (e.g.2500):')
    url: str = f'https://www.heyzo.com/moviepages/{code}/index.html'
    print(f'code: {code}')
    print(f'url: {url}')

    # If response == OK, create NFO
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        print("Status Code: OK")
        create_nfo(code, response)

