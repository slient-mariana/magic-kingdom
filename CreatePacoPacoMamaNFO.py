import requests
import pathlib
import shutil

# code: e.g. 053117_002
code: str = '091412_738'
source = r'\\ORCINUS\Akureyri\pacopacomama.2009-2012.Pack.HD720Px29.WMV-MTwy\12\pacopacomama-091412_738-HD\091412_738-paco-whole.wmv'

# Parameter
pacopacomama: str = 'https://www.pacopacomama.com/'
movie_details_url = f'{pacopacomama}dyn/phpauto/movie_details/movie_id/{code}.json'
studio = 'Pacopacomama'
base_path = r'\\ORCINUS\Mariana'
pacopacomama_path = r'\Studio\Pacopacomama'
nfo_folder_path = f'/mariana/Studio/{studio}/'

def create_NFO():
    print('Start Create Pacopacomama NFO...')
    print(f'Movie Details URL: {movie_details_url}')

    # call GET API
    response = requests.get(movie_details_url)
    if response.status_code == requests.codes.ok:
        print("Status Code: OK")

        movie_details_json = response.json()

        # Actor
        actor = movie_details_json['Actor']
        print(f'Actor: {actor}')

        # ActressesJa
        actresses_ja = movie_details_json['ActressesJa']
        print(f'Actresses Ja: {actresses_ja}')

        # Description
        desc = movie_details_json['Desc']
        print(f'Description: {desc}')

        # Description Eng
        desc_en = movie_details_json['DescEn']
        print(f'English Description: {desc_en}')

        # Movie ID
        movie_id = movie_details_json['MovieID']
        print(f'Movie Id: {movie_id}')

        # Movie Thumb url
        movie_thumb = movie_details_json['MovieThumb']
        print(f'Movie Thumb URL: {movie_thumb}')

        # Title
        title = movie_details_json['Title']
        print(f'Title: {title}')

        # Release Day
        release = movie_details_json['Release']
        print(f'Release Day: {release}')

        # Year
        year = movie_details_json['Year']
        print(f'Year: {year}')

        # UC Name
        uc_name = movie_details_json['UCNAME']
        print(f'UC Name: {uc_name}')

        # Series
        series = movie_details_json['Series']
        print(f'Series: {series} ')

        # Movie Thumb Ultra
        movie_thumb_ultra = movie_details_json['ThumbUltra']
        print(f'Movie Thumb Ultra: {movie_thumb_ultra}')

        # Sample File
        sample_files = movie_details_json['SampleFiles']
        print(f'Sample Files: {sample_files}')
        sample_file_url = f''
        sample_file_size = 0
        for sampleFile in sample_files:
            if sampleFile['FileSize'] > sample_file_size:
                sample_file_size = sampleFile['FileSize']
                sample_file_url = sampleFile['URL']

        # movie folder name
        movie_folder_name: str = f'[{studio}-{movie_id}] {actor} {title}'
        print(f'Movie folder Name: {movie_folder_name}')

        # Create Movie folder
        movie_folder_path = f'{base_path}{pacopacomama_path}\{movie_folder_name}'
        print(f'The full path: {movie_folder_path}')

        if movie_folder_path:
            pathlib.Path(movie_folder_path).mkdir(parents=True, exist_ok=True)

            # 0. Copy movie file to movie folder
            destination = f'{movie_folder_path}\{movie_folder_name}.wmv'
            dest = shutil.copyfile(source, destination)

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
            images = None
            #https://www.pacopacomama.com/dyn/phpauto/movie_galleries/movie_id/053117_002.json
            movie_gallery_url = f'https://www.pacopacomama.com/dyn/dla/json/movie_gallery/{movie_id}.json'
            print(f'movie gallery URL: {movie_gallery_url}')
            movie_gallery_response = requests.get(movie_gallery_url)
            if movie_gallery_response.status_code == requests.codes.ok:
                print(f'get movie gallery from: {movie_gallery_url} success!')
                movie_gallery_base_url = f'https://www.pacopacomama.com/dyn/dla/images/'
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

            #https://www.pacopacomama.com/dyn/phpauto/movie_galleries/movie_id/053117_002.json
            movie_gallery_url = f'https://www.pacopacomama.com/dyn/phpauto/movie_galleries/movie_id/{movie_id}.json'
            print(f'movie gallery URL: {movie_gallery_url}')
            movie_gallery_response = requests.get(movie_gallery_url)
            if movie_gallery_response.status_code == requests.codes.ok:
                print(f'get movie gallery from: {movie_gallery_url} success!')
                movie_gallery_base_url = f'https://www.pacopacomama.com/assets/'
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
                        # https://www.pacopacomama.com/assets/member/053117_002/l/4.jpg
                        image_concat_url = f'{movie_gallery_base_url}member/{movie_id}/l/{image_url}'
                    else:
                        image_concat_url = f'{movie_gallery_base_url}sample/{movie_id}/l/{image_url}'
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
            f.write(f'\t<plot>{desc}\n{desc_en}</plot>\n')
            f.write(f'\t<outline />\n')
            f.write(f'\t<lockdata>false</lockdata>\n')
            f.write(f'\t<title>[{movie_id}] {actor} {title}</title>\n')
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
            f.write(f'\t\t<poster>{nfo_folder_path}{movie_folder_name}/poster.jpg</poster>\n')
            f.write(f'\t\t<fanart>{nfo_folder_path}{movie_folder_name}/fanart.jpg</fanart>\n')
            if images != None:
                for index in range(len(images)):
                    f.write(
                        f'\t\t<fanart>{nfo_folder_path}{movie_folder_name}/extrafanart/fanart{index + 1}.jpg</fanart>\n')
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
    create_NFO()