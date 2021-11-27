import requests
import os
import pathlib
from bs4 import BeautifulSoup
from urllib import parse


def create_nfo(code, response):
    # Get information from response
    soup = BeautifulSoup(response.content, 'html.parser')

    studio: str = f'Nyoshin'
    base_path = f'/mariana/Studio/{studio}/'

    information_table: str = soup.find('table', id='information_table').find_all('tr')

    # title: str = soup.find('p', class_='title_text').text.strip().replace('/', '-')
    full_title: str = soup.find('p', class_='title_text').text.strip()
    title: str = substring_title(full_title)
    release_day: str = information_table[0].find('td', class_='table_right').text.strip()
    actor: str = information_table[1].find('td', class_='table_right').text.strip()
    desc: str = soup.find('div', id='info_comment').text.strip()
    gallerys = soup.find('div', id='gallery').find_all('div', class_='gallery_box')

    # movie folder name
    movie_folder_name: str = f'[{studio}-n{code}] {actor} - {title}'
    print(movie_folder_name)

    # Create Movie folder
    movie_folder_path = os.environ['USERPROFILE'] + f'\Desktop\{movie_folder_name}'
    pathlib.Path(movie_folder_path).mkdir(parents=True, exist_ok=True)

    # Download Images
    print(f'Start Download Landscape and Fanart')
    add_landscape_fanart(movie_folder_path)
    add_extra_fanart(gallerys, movie_folder_path)

    # Download Sample
    print(f'Start Download Sample video')
    add_sample(movie_folder_path)

    # Create NFO file and write
    nfo_filename = f'{movie_folder_path}\{movie_folder_name}.nfo'
    f = open(nfo_filename, 'w', encoding='utf=8')

    # NFO context
    f.write(f'<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
    f.write(f'<movie>\n')
    f.write(f'\t<plot>{desc}</plot>\n')
    f.write(f'\t<outline />\n')
    f.write(f'\t<lockdata>false</lockdata>\n')
    f.write(f'\t<title>[n{code}] {full_title}</title>\n')
    f.write(f'\t<originaltitle>{movie_folder_name}</originaltitle>\n')
    f.write(f'\t<sorttitle>{movie_folder_name}</sorttitle>\n')
    f.write(f'\t<year>{release_day[0:4]}</year>\n')
    f.write(f'\t<mpaa>NC-17</mpaa>\n')
    f.write(f'\t<language>ja</language>\n')
    f.write(f'\t<countrycode>JP</countrycode>\n')
    f.write(f'\t<premiered>{release_day}</premiered>\n')
    f.write(f'\t<releasedate>{release_day}</releasedate>\n')
    f.write(f'\t<studio>{studio}</studio>\n')
    f.write(f'\t<art>\n')
    f.write(f'\t\t<poster>{base_path}{movie_folder_name}/poster.jpg</poster>\n')
    f.write(f'\t\t<fanart>{base_path}{movie_folder_name}/fanart.jpg</fanart>\n')
    for index in range(len(gallerys)):
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


def substring_title(title):
    first_slash: int = title.find('/')
    second_slash: int = title.rfind('/')
    return title[first_slash + 2: second_slash - 1]


def add_landscape_fanart(movie_folder_path):
    # 1. Landscape
    # https://www.nyoshin.com/contents/2200/thum2.jpg
    thumb_image_url: str = f'https://www.nyoshin.com/contents/{code}/thum2.jpg'
    print(f'thumb image url: {thumb_image_url}')
    landscape = f'landscape.jpg'
    landscape_pathname = f'{movie_folder_path}\{landscape}'
    landscape_response = requests.get(thumb_image_url)
    landscape_file = open(landscape_pathname, 'wb')
    landscape_file.write(landscape_response.content)
    landscape_file.close()

    fanart = f'fanart.jpg'
    fanart_pathname = f'{movie_folder_path}\{fanart}'
    fanart_file = open(fanart_pathname, 'wb')
    fanart_file.write(landscape_response.content)
    fanart_file.close()


def add_extra_fanart(gallerys, movie_folder_path):
    # 2. Extra-fanart

    # Create extra-fanart folder
    extra_fanart_path = f'{movie_folder_path}/extrafanart'
    pathlib.Path(extra_fanart_path).mkdir(parents=True, exist_ok=True)

    extra_fanart_base_url: str = f'https://www.nyoshin.com/contents/{code}/'
    print(f'total images: ', len(gallerys))
    fanart_count: int = 0
    for gallery in gallerys:
        fanart_count = fanart_count + 1
        # image = gallery.find('img')
        # print(image['src'])
        extrafanart = f'fanart{fanart_count}.jpg'
        extrafanart_pathname = f'{extra_fanart_path}/{extrafanart}'
        image_concat_url = f'{extra_fanart_base_url}{fanart_count}.jpg'
        image_response = requests.get(image_concat_url)
        extrafanart_file = open(extrafanart_pathname, 'wb')
        extrafanart_file.write(image_response.content)
        extrafanart_file.close()


def add_sample(movie_folder_path):
    # Download Sample Video
    sample_video_url = f'https://www.nyoshin.com/d2p/movie/{code}/sample.mp4'
    print(f'Sample Video URL: {sample_video_url}')
    sample_video_response = requests.head(sample_video_url)
    video_response_location: str = sample_video_response.headers['Location']
    login_domain: str = video_response_location[:29]
    l: str = video_response_location[32:]

    # header define
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    # 通過字典方式定義請求body
    FormData = {
        "V": 1,
        "l": l,
        "EQS": '(none)',
        "NETI_BR_N": 'Chrome',
        "NETI_BR_V": '91.0.4472.114',
        "NETI_DV_B": 'macOS',
        "NETI_DV_T": 'Desktop',
        "NETI_OS_N": 'Mac OS X',
        "NETI_OS_V": '10_15_7',
        "NETI_SC_W": 1680,
        "NETI_SC_H": 1050,
        "FORM_USER": 'sexy70ys@gmail.com',
        "FORM_PASSWD": 'monique610',
        "NETI_SUS": 1,
        "login_btn": 'ログイン(SIGN IN)'}
    # 字典转换k1=v1 & k2=v2 模式
    data = parse.urlencode(FormData)

    sample = f'sample.mp4'
    sample_pathname = f'{movie_folder_path}\{sample}'
    video_response = requests.post(url=login_domain, headers=HEADERS, data=data)
    sample_file = open(sample_pathname, 'wb')
    sample_file.write(video_response.content)
    sample_file.close()


if __name__ == '__main__':
    # code: str = '2200'
    code: str = input('Code (e.g. 2200): ')
    # https://www.nyoshin.com/moviepages/n2200/index.html
    url: str = f'https://www.nyoshin.com/moviepages/n{code}/index.html'
    print(f'url: {url}')

    # call GET API
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        print("Status Code: OK")
        create_nfo(code, response)
