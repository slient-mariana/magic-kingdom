# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from pyexiv2 import Image
import os
import sys

image_description: str = f'三橋詠美 EIMI'
image_tilte : str = f''
studio: str = f'GirlsDelta'

def photo_manipulation(folder, file):

    if studio == f'GirlsDelta':
        filename: str = file.replace('3500_','')
        filename = filename.upper()
        # Exif Data
        exif_data = {
            'Exif.Image.ImageDescription': '[GirlsDelta 1568] 三橋詠美 EIMI'
        }
        # Xmp Data
        xmp_data = {
            'Xmp.dc.title': f'lang="x-default" [GirlsDelta 1568] {filename}',
            'Xmp.xmp.Label': 'GirlsDelta'
        }
    if studio == 'Pacific Girls':
        # Exif Data
        exif_data = {
            'Exif.Image.ImageDescription': 'めい 第1066弾「めいのパイパンあなたにあげる！オイシイョ♪」',
            'Exif.Photo.DateTimeOriginal': '2016:05:11 00:00:00',
            'Exif.Photo.DateTimeDigitized': '2016:05:11 00:00:00'
        }
        # Xmp Data
        xmp_data = {
            'Xmp.dc.title': f'lang="x-default" [Pacific Girls 1066] {file.upper()}',
            'Xmp.xmp.Label': 'Pacific Girls'
        }
    full_path = os.path.join(folder, file)
    image = Image(full_path)
    image.modify_exif(exif_data)
    image.modify_xmp(xmp_data)
    image.close()
    print(f'{file} Done')


def list_files():

    ######################################
    # Information session
    ######################################
    #folder_str: str = f'/Users/carlyle/Documents/Temp Work/Photo_Manipulation/1066 Mei/'
    # \\ORCINUS\Mariana\Studio\GirlsDeltaGallery\1568\
    #folder_str: str = r'\\ORCINUS\Mariana\Studio\GirlsDeltaGallery\1568'
    folder_str: str = r'C:\Users\carlyle\Desktop\temp\1568'

    # Start List files
    print(f'Start Get photos from the folder...')
    os.chdir(folder_str)
    folder: str = os.getcwd()
    print(f'folder: {folder}')
    file_count = len(os.listdir())
    print(f'Total: {file_count} file(s)')

    for file in os.listdir():
        photo_manipulation(folder, file)

    print(f'End Get photos from the folder...')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(f'Start Photo Manipulation Program')
    list_files()
    print(f'End Photo Manipulation Program')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
