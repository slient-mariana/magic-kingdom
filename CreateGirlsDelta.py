import requests
from bs4 import BeautifulSoup
import os
import pathlib


def girlsdelta():

    ######################################################
    # Web
    ######################################################
    code: str = '714'

    url: str = f'https://girlsdelta.com/product/{code}'
    print(f'url: {url}')

    # call GET API
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        print("Status Code: OK")
        create_nfo(code, response)


def create_nfo(code, response):

    ######################################################
    # MetaData
    ######################################################
    studio: str = f'GirlsDelta'
    base_path = f'/mariana/Studio/{studio}/'
    release: str = f'2021-01-16'

    # Get information from response
    soup = BeautifulSoup(response.content, 'html.parser')

    web_title: str = soup.find('title').text.strip()
    web_title_trim_position = web_title.find('のワレメ')
    web_title = web_title[:web_title_trim_position]
    print(web_title)

    product_detail = soup.find('div', id='product-detail').find_all('div',class_='product-detail')[1]
    product_detail_list = product_detail.find_all('li')
    actor = product_detail_list[0].find('p').text.strip();
    body_size = product_detail_list[1].find('p').text.strip();
    tags = product_detail_list[2].find_all('a')

    sample_video = soup.find('video', id='sample-video')
    poster_url = sample_video.get('poster')
    sample_video_url = sample_video.get('src')
    pid = poster_url[36:68]

    # movie folder name
    movie_folder_name: str = f'[{studio}][{code}] {web_title}'
    print(movie_folder_name)

    # Create Movie folder
    movie_folder_path = os.environ['USERPROFILE'] + f'\Desktop\{movie_folder_name}'
    pathlib.Path(movie_folder_path).mkdir(parents=True, exist_ok=True)

    # Download Images
    print(f'Start Download Landscape and Fanart')
    add_landscape_fanart(movie_folder_path, poster_url)
    add_extra_fanart(movie_folder_path, pid)

    # Download Sample
    print(f'Start Download Sample video')
    add_sample(movie_folder_path, movie_folder_name ,sample_video_url)

    # Create NFO file and write
    nfo_filename = f'{movie_folder_path}\{movie_folder_name}.nfo'
    f = open(nfo_filename, 'w', encoding='utf=8')

    # NFO context
    f.write(f'<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
    f.write(f'<movie>\n')
    f.write(f'\t<plot>サイズ: {body_size}</plot>\n')
    f.write(f'\t<outline />\n')
    f.write(f'\t<lockdata>false</lockdata>\n')
    f.write(f'\t<title>{movie_folder_name}</title>\n')
    f.write(f'\t<originaltitle>{movie_folder_name}</originaltitle>\n')
    f.write(f'\t<sorttitle>{movie_folder_name}</sorttitle>\n')
    f.write(f'\t<year>{release[:4]}</year>\n')
    f.write(f'\t<mpaa>NC-17</mpaa>\n')
    f.write(f'\t<language>ja</language>\n')
    f.write(f'\t<countrycode>JP</countrycode>\n')
    f.write(f'\t<premiered>{release}</premiered>\n')
    f.write(f'\t<releasedate>{release}</releasedate>\n')
    f.write(f'\t<genre>{studio}</genre>\n')
    f.write(f'\t<studio>{studio}</studio>\n')
    for tag in tags:
        tag_text = tag.text.strip()
        f.write(f'\t<tag>{tag_text}</tag>\n')
    f.write(f'\t<art>\n')
    f.write(f'\t\t<poster>{base_path}{movie_folder_name}/poster.jpg</poster>\n')
    f.write(f'\t\t<fanart>{base_path}{movie_folder_name}/fanart.jpg</fanart>\n')
    for index in range(20):
        f.write(f'\t\t<fanart>{base_path}{movie_folder_name}/extrafanart/fanart{index + 1}.jpg</fanart>\n')
    f.write(f'\t</art>\n')
    f.write(f'\t<actor>\n')
    f.write(f'\t\t<name>{actor}</name>\n')
    f.write(f'\t\t<role>{actor}</role>\n')
    f.write(f'\t\t<type>Actor</type>\n')
    f.write(f'\t</actor>\n')
    f.write(f'\t<artist>{actor}</artist>\n')
    f.write(f'</movie>\n')
    f.close()


def add_landscape_fanart(movie_folder_path, poster_url):
    # 1. Landscape
    print(f'poster url: {poster_url}')
    landscape = f'landscape.jpg'
    landscape_pathname = f'{movie_folder_path}\{landscape}'
    landscape_response = requests.get(poster_url)
    landscape_file = open(landscape_pathname, 'wb')
    landscape_file.write(landscape_response.content)
    landscape_file.close()

    fanart = f'fanart.jpg'
    fanart_pathname = f'{movie_folder_path}\{fanart}'
    fanart_file = open(fanart_pathname, 'wb')
    fanart_file.write(landscape_response.content)
    fanart_file.close()


def add_extra_fanart(movie_folder_path, pid):
    # 2. Extra-fanart

    # Create extra-fanart folder
    extra_fanart_path = f'{movie_folder_path}/extrafanart'
    pathlib.Path(extra_fanart_path).mkdir(parents=True, exist_ok=True)

    extra_fanart_base_url: str = f'http://cash.girlsdelta.com/gallery/delta/images/prod/{pid}/sample/'
    print(f'gallery base url: {extra_fanart_base_url}')
    for i in range(20):
        fanart_count = i + 1
        extrafanart = f'fanart{fanart_count}.jpg'
        extrafanart_pathname = f'{extra_fanart_path}/{extrafanart}'
        image_concat_url = f'{extra_fanart_base_url}{fanart_count}.jpg'
        image_response = requests.get(image_concat_url)
        extrafanart_file = open(extrafanart_pathname, 'wb')
        extrafanart_file.write(image_response.content)
        extrafanart_file.close()


def add_sample(movie_folder_path, movie_folder_name, sample_video_url):
    # Download Sample Video
    print(f'Sample Video URL: {sample_video_url}')
    video_response = requests.get(sample_video_url)
    sample = f'{movie_folder_name} - trailer.mp4'
    sample_pathname = f'{movie_folder_path}\{sample}'
    sample_file = open(sample_pathname, 'wb')
    sample_file.write(video_response.content)
    sample_file.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    girlsdelta()
