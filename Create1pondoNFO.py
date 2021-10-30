# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import os
import pathlib

def create_nfo(movie_json):

    # Get metadata from movie json file
    studio = f'1pondo'
    base_path = f'/mariana/Movies/'
    actor = movie_json['Actor']
    actresses_ja = movie_json['ActressesJa']
    desc = movie_json['Desc']
    movie_id = movie_json['MovieID']
    movie_thumb = movie_json['MovieThumb']
    title = movie_json['Title']
    release = movie_json['Release']
    year = movie_json['Year']
    uc_name = movie_json['UCNAME']
    series = movie_json['Series']
    movie_thumb_ultra = movie_json['ThumbUltra']
    sample_files = movie_json['SampleFiles']
    sample_file_url = f''
    sample_file_size = 0
    for sampleFile in sample_files:
        if sampleFile['FileSize'] > sample_file_size:
            sample_file_size = sampleFile['FileSize']
            sample_file_url = sampleFile['URL']

    # movie folder name
    movie_folder_name: str = f'{actor} - [{year}] {title} [{studio}-{movie_id}]'

    # Create Actress folder
    parent_path = os.environ['USERPROFILE'] + f'\Desktop\{actor}'
    pathlib.Path(parent_path).mkdir(parents=True, exist_ok=True)

    # Create Movie folder
    movie_folder_path = f'{parent_path}\{movie_folder_name}'
    pathlib.Path(movie_folder_path).mkdir(parents=True, exist_ok=True)

    # Download Images
    # 1. Poster
    if movie_thumb:
        print(f'movie thumb: {movie_thumb}')
        poster = f'poster.jpg'
        movie_thumb_pathname = f'{movie_folder_path}\{poster}'
        movie_thumb_response = requests.get(movie_thumb)
        movie_thumb_file = open(movie_thumb_pathname, 'wb')
        movie_thumb_file.write(movie_thumb_response.content)
        movie_thumb_file.close()

    # 2. Landscape
    if movie_thumb_ultra:
        print(f'Landscape: {movie_thumb_ultra}')
        landscape = f'landscape.jpg'
        landscape_pathname = f'{movie_folder_path}\{landscape}'
        landscape_response = requests.get(movie_thumb_ultra)
        landscape_file = open(landscape_pathname, 'wb')
        landscape_file.write(landscape_response.content)
        landscape_file.close()

        fanart = f'fanart.jpg'
        fanart_pathname = f'{movie_folder_path}\{fanart}'
        fanart_file = open(fanart_pathname, 'wb')
        fanart_file.write(landscape_response.content)
        fanart_file.close()

    # 3. Extra-fanart
    movie_gallery_url = f'https://www.1pondo.tv/dyn/dla/json/movie_gallery/{movie_id}.json'
    print(f'movie gallery URL: {movie_gallery_url}')
    movie_gallery_response = requests.get(movie_gallery_url)
    if movie_gallery_response.status_code == requests.codes.ok:
        print(f'get movie gallery from: {movie_gallery_url} success!')
        movie_gallery_base_url = f'https://www.1pondo.tv/dyn/dla/images/'
        movie_gallery_json = movie_gallery_response.json()
        images = movie_gallery_json['Rows']
        print(f'total images: ', len(images))

        # Create extra-fanart folder
        extra_fanart_path = f'{movie_folder_path}/extrafanart'
        pathlib.Path(extra_fanart_path).mkdir(parents=True, exist_ok=True)

        # Download extrafanart Images
        fanart_count: int = 0
        for image in images:
            fanart_count = fanart_count + 1
            extrafanart = f'fanart{fanart_count}.jpg'
            extrafanart_pathname = f'{extra_fanart_path}/{extrafanart}'
            image_url = image['Img']
            image_concat_url = f'{movie_gallery_base_url}{image_url}'
            image_response = requests.get(image_concat_url)
            extrafanart_file = open(extrafanart_pathname, 'wb')
            extrafanart_file.write(image_response.content)
            extrafanart_file.close()

    movie_gallery_url = f'https://www.1pondo.tv/dyn/phpauto/movie_galleries/movie_id/{movie_id}.json'
    print(f'movie gallery URL: {movie_gallery_url}')
    movie_gallery_response = requests.get(movie_gallery_url)
    if movie_gallery_response.status_code == requests.codes.ok:
        print(f'get movie gallery from: {movie_gallery_url} success!')
        movie_gallery_base_url = f'https://www.1pondo.tv/assets/'
        movie_gallery_json = movie_gallery_response.json()
        images = movie_gallery_json['Rows']
        print(f'total images: ', len(images))

        # Create extra-fanart folder
        extra_fanart_path = f'{movie_folder_path}/extrafanart'
        pathlib.Path(extra_fanart_path).mkdir(parents=True, exist_ok=True)

        # Download extrafanart Images
        fanart_count: int = 0
        for image in images:
            fanart_count = fanart_count + 1
            extrafanart = f'fanart{fanart_count}.jpg'
            extrafanart_pathname = f'{extra_fanart_path}/{extrafanart}'
            image_url = image['Filename']
            if image['Protected']:
                image_concat_url = f'{movie_gallery_base_url}member/{movie_id}/popu/{image_url}'
            else:
                image_concat_url = f'{movie_gallery_base_url}sample/{movie_id}/popu/{image_url}'
            image_response = requests.get(image_concat_url)
            extrafanart_file = open(extrafanart_pathname, 'wb')
            extrafanart_file.write(image_response.content)
            extrafanart_file.close()

    # 4. Trailer
    if sample_file_url:
        print(f'trailer url: {sample_file_url}')
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
    f.write(f'\t<premiered>{release}</premiered>\n')
    f.write(f'\t<releasedate>{release}</releasedate>\n')
    if series:
        f.write(f'\t<genre>{series}</genre>\n')
    f.write(f'\t<studio>{studio}</studio>\n')
    for uc in uc_name:
        f.write(f'\t<tag>{uc}</tag>\n')
    f.write(f'\t<art>\n')
    f.write(f'\t\t<poster>{base_path}{actor}/{movie_folder_name}/poster.jpg</poster>\n')
    f.write(f'\t\t<fanart>{base_path}{actor}/{movie_folder_name}/fanart.jpg</fanart>\n')
    for index in range(len(images)):
        f.write(f'\t\t<fanart>{base_path}{actor}/{movie_folder_name}/extrafanart/fanart{index+1}.jpg</fanart>\n')
    f.write(f'\t</art>\n')
    for actress in actresses_ja:
        f.write(f'\t<actor>\n')
        f.write(f'\t\t<name>{actress}</name>\n')
        f.write(f'\t\t<role>{actress}</role>\n')
        f.write(f'\t\t<type>Actor</type>\n')
        f.write(f'\t</actor>\n')
    for actress in actresses_ja:
        f.write(f'\t<artist>{actress}</artist>\n')
    f.write(f'</movie>\n')
    f.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #code: str = '070219_867'
    code: str = input('Code (e.g.: 082219_889): ')
    url: str = f'https://www.1pondo.tv/dyn/phpauto/movie_details/movie_id/{code}.json'
    print(f'url: {url}')

    # call GET API
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        print("Status Code: OK")

        create_nfo(response.json())
