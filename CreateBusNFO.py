import os
import platform

if __name__ == '__main__':
    # MacOS: Darwin
    print(platform.system())
    print('Hello World')
    path = r'smb://Orcinus._smb._tcp.local/Akureyri/[BD]SKYHD-079/'
    print(os.listdir(path))