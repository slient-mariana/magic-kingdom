import shutil

from bs4 import BeautifulSoup
import requests
import os
import pathlib
import zipfile

if __name__ == '__main__':

    # Information:
    #code: str = f'050921-001'
    code: str = input('Code (e.g. 091719-001):')

    # Let Program do it
    studio: str = f'Carib'
    url: str = f'https://www.caribbeancom.com/moviepages/{code}/index.html'
    print(f'URL: {url}')
    title_actor: str = f''
    series: str =f''
    base_path = f'/mariana/Movies/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    movie_info = soup.find('div',{'class':'movie-info section'})

    # Movie Info
    title: str = movie_info.find('div',{'class':'heading'}).find('h1', itemprop='name').string
    desc: str = movie_info.find('p', itemprop='description').string

    actresses = movie_info.find_all('a', {'class':'spec__tag'},itemprop='actor')
    for actress in actresses:
        title_actor = title_actor + actress.string + ', '
    title_actor = title_actor[:-2]

    date = movie_info.find('span', {'class':'spec-content'},itemprop='datePublished').string
    year:str = date[:4]
    release = f'{date[:4]}-{date[5:-3]}-{date[8:]}'

    movie_spec = movie_info.find_all('li',{'class':'movie-spec'})
    for spec in movie_spec:
        if spec.find('span',{'class':'spec-title'}).string == f'シリーズ':
            series: str = spec.find('span',{'class':'spec-content'}).string
        elif spec.find('span',{'class':'spec-title'}).string == f'タグ':
            tags = spec.find('span',{'class':'spec-content'}).find_all('a', {'class':'spec-item'},itemprop='url')
            genres = spec.find('span',{'class':'spec-content'}).find_all('a', {'class':'spec-item'},itemprop='genre')

    # movie folder name
    movie_folder_name: str = f'{title_actor} - [{year}] {title} [{studio}-{code}]'
    print(f'Movie Name: {movie_folder_name}')

    # Create Actress folder
    parent_path = os.environ['USERPROFILE'] + f'\Desktop\{title_actor}'
    pathlib.Path(parent_path).mkdir(parents=True, exist_ok=True)

    # Create Movie folder
    movie_folder_path = f'{parent_path}\{movie_folder_name}'
    pathlib.Path(movie_folder_path).mkdir(parents=True, exist_ok=True)

    # Download Images
    # 1. Landscape
    landscape_url = f'https://www.caribbeancom.com/moviepages/{code}/images/l_l.jpg'
    print(f'Landscape URL: {landscape_url}')
    landscape = f'landscape.jpg'
    landscape_pathname = f'{movie_folder_path}\{landscape}'
    landscape_response = requests.get(landscape_url)
    landscape_file = open(landscape_pathname, 'wb')
    landscape_file.write(landscape_response.content)
    landscape_file.close()

    fanart = f'fanart.jpg'
    fanart_pathname = f'{movie_folder_path}\{fanart}'
    fanart_file = open(fanart_pathname, 'wb')
    fanart_file.write(landscape_response.content)
    fanart_file.close()

    # 2. gallery.zip
    gallery_url = f'https://www.caribbeancom.com/moviepages/{code}/images/gallery.zip'
    print(f'Gallery URL: {gallery_url}')
    gallery:str = f'gallery.zip'
    gallery_pathname = f'{movie_folder_path}\{gallery}'
    gallery_response = requests.get(gallery_url)
    gallery_file = open(gallery_pathname,'wb')
    gallery_file.write(gallery_response.content)
    gallery_file.close()

    # Unzip gallery.zip
    extrafanart_path: str = f'{movie_folder_path}\extrafanart'
    with zipfile.ZipFile(gallery_pathname, 'r') as zip_ref:
        zip_ref.extractall(extrafanart_path)

    # Remove gallery.zip
    os.remove(gallery_pathname)

    # Check Gallery folder exists
    extrafanart_sub_folders = os.listdir(extrafanart_path)
    for sub_folder in extrafanart_sub_folders:
        sub_folder_path: str = f'{extrafanart_path}\{sub_folder}'
        if os.path.isdir(sub_folder_path):
            file_names = os.listdir(sub_folder_path)
            for file_name in file_names:
                shutil.move(os.path.join(sub_folder_path, file_name), extrafanart_path)
            shutil.rmtree(sub_folder_path)

    # Rename all extra-fanact
    fanart_count = 0
    for path in pathlib.Path(f'{movie_folder_path}\extrafanart').iterdir():
        fanart_count = fanart_count + 1
        if path.is_file():
            directory = path.parent
            new_name = f'fanart{fanart_count}.jpg'
            path.rename(pathlib.Path(directory, new_name))

    # 3. trailer
    trailer = f'trailer.mp4'
    trailer_pathname = f'{movie_folder_path}\{trailer}'
    trailer_response = requests.get(f'https://smovie.caribbeancom.com/sample/movies/{code}/1080p.mp4')
    trailer_file = open(trailer_pathname, 'wb')
    trailer_file.write(trailer_response.content)
    trailer_file.close()

    # Create NFO file and write
    nfo_filename = f'{movie_folder_path}\{movie_folder_name}.nfo'
    f = open(nfo_filename, 'w', encoding='utf=8')

    # NFO context
    f.write(f'<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
    f.write(f'<musicvideo>\n')
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
    for genre in genres:
        f.write(f'\t<genre>{genre.string}</genre>\n')
    f.write(f'\t<studio>カリビアンコム</studio>\n')
    for tag in tags:
        f.write(f'\t<tag>{tag.string}</tag>\n')
    f.write(f'\t<art>\n')
    f.write(f'\t\t<poster>{base_path}{title_actor}/{movie_folder_name}/poster.jpg</poster>\n')
    f.write(f'\t\t<fanart>{base_path}{title_actor}/{movie_folder_name}/fanart.jpg</fanart>\n')
    for index in range(fanart_count):
        f.write(f'\t\t<fanart>{base_path}{title_actor}/{movie_folder_name}/extrafanart/fanart{index + 1}.jpg</fanart>\n')
    f.write(f'\t</art>\n')
    for actress in actresses:
        f.write(f'\t<actor>\n')
        f.write(f'\t\t<name>{actress.string}</name>\n')
        f.write(f'\t\t<role>{actress.string}</role>\n')
        f.write(f'\t\t<type>Actor</type>\n')
        f.write(f'\t</actor>\n')
    for actress in actresses:
        f.write(f'\t<artist>{actress.string}</artist>\n')
    f.write(f'</musicvideo>\n')
    f.close()