import shutil
import pathlib
import requests
from bs4 import BeautifulSoup

n = f'238'
#source = f'\\\\ORCINUS\\Akureyri\\936-1165\\gachi{n}.wmv'
source = r'\\ORCINUS\Fancy\JDownloader2\GirlsDelta\better gachinco-gachip238\better_gachinco-gachip238.wmv'
#code: str = f'GACHI-{n}'
code: str = f'GACHIP-{n}'



javbus = f'https://www.javbus.com'
movie_url = f'{javbus}/{code}'
base_path = r'\\ORCINUS\Mariana'
nfo_base = '/mariana'


def create_nfo(url):
    print(f'URL: {url}')

    # If response == OK, create NFO
    response = requests.get(url)

    if response.status_code == requests.codes.ok:
        print("Status Code: OK")

        # Get information from response
        soup = BeautifulSoup(response.content, 'html.parser')
        big_image = soup.find('a', class_='bigImage').find('img')
        info = soup.find('div', class_='col-md-3 info')
        star = soup.find('a', class_='avatar-box')

        print('### Movie Info. ###')
        # Title
        title = big_image['title']
        image = big_image['src']
        print(f'*Title: {title}')
        print(f'*Image URL: {image}')

        # Code
        info_code = info.find_all('p')[0].find_all('span')[1].text.strip()
        print(f'*Code: {info_code}')

        # Release Date
        info.find_all('p')[1].find('span').extract()
        release_date = info.find_all('p')[1].text.strip()
        print(f'*Release Date: {release_date}')

        # Studio
        studio = info.find_all('p')[3].find('a').text.strip()
        print(f'*Studio: {studio}')

        # Series
        series = info.find_all('p')[4].find('a').text.strip()
        print(f'*Series: {series}')

        # Genre
        genres_tag = info.find_all('p')[6].find_all('a')
        genres = []
        for genre_tag in genres_tag:
            genres.append(genre_tag.text.strip())
        print('*Genres: ')
        print(genres)

        # Actress
        actress = star.text.strip()
        print(f'*Actress: {actress}')

        # movie folder name
        movie_folder_name: str = f'[{studio}-{code}] {title}'
        print(f'Movie folder Name: {movie_folder_name}')

        # Create Movie folder
        movie_folder_path = None
        if studio == 'Gachinco':
            print('% Match Gachinco %')
            gachinco_path = r'\Studio\Gachinco'
            movie_folder_path = f'{base_path}{gachinco_path}\{movie_folder_name}'
            nfo_folder_path = f'{nfo_base}/Studio/Gachinco/{movie_folder_name}/'
            print(f'The full path: {movie_folder_path}')

        if movie_folder_path:
            pathlib.Path(movie_folder_path).mkdir(parents=True, exist_ok=True)

            # Copy movie file to movie folder
            destination = f'{movie_folder_path}\{movie_folder_name}.wmv'
            dest = shutil.copyfile(source, destination)

            # Download Images
            print(f'Start Download Landscape and Fanart')
            # 1. Landscape
            thumb_image_url: str = f'{javbus}{image}'
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

            # Create NFO file and write
            nfo_filename = f'{movie_folder_path}\{movie_folder_name}.nfo'
            f = open(nfo_filename, 'w', encoding='utf=8')

            # NFO context
            f.write(f'<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
            f.write(f'<movie>\n')
            f.write(f'\t<outline />\n')
            f.write(f'\t<lockdata>false</lockdata>\n')
            f.write(f'\t<title>[{code}] {title}</title>\n')
            f.write(f'\t<originaltitle>{movie_folder_name}</originaltitle>\n')
            f.write(f'\t<sorttitle>{movie_folder_name}</sorttitle>\n')
            f.write(f'\t<year>{release_date[0:4]}</year>\n')
            f.write(f'\t<mpaa>NC-17</mpaa>\n')
            f.write(f'\t<language>ja</language>\n')
            f.write(f'\t<countrycode>JP</countrycode>\n')
            f.write(f'\t<premiered>{release_date}</premiered>\n')
            f.write(f'\t<releasedate>{release_date}</releasedate>\n')
            if series:
                f.write(f'\t<genre>{series}</genre>\n')
            for genre in genres:
                f.write(f'\t<genre>{genre}</genre>\n')
            f.write(f'\t<studio>{studio}</studio>\n')
            f.write(f'\t<art>\n')
            f.write(f'\t\t<poster>{nfo_folder_path}poster.jpg</poster>\n')
            f.write(f'\t\t<fanart>{nfo_folder_path}fanart.jpg</fanart>\n')
            f.write(f'\t</art>\n')
            f.write(f'\t<actor>\n')
            f.write(f'\t\t<name>{actress}</name>\n')
            f.write(f'\t\t<role>{actress}</role>\n')
            f.write(f'\t\t<type>Actor</type>\n')
            f.write(f'\t</actor>\n')
            f.write(f'\t<artist>{actress}</artist>\n')
            f.write(f'</movie>\n')
            f.close()


if __name__ == '__main__':
    # MacOS: Darwin
    # print(platform.system())
    # print('Start c')
    create_nfo(movie_url)
