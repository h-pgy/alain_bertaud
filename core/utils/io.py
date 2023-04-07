import requests
import zipfile


def download_binary_file(url, fname):

    with requests.get(url) as r:
        content = r.content

    with open(fname, 'wb') as f:
        f.write(content)
        print(f'File {fname} saved')

def download_text_file(url, fname):

    with requests.get(url) as r:
        text = r.text

    with open(fname, 'wt') as f:
        f.write(text)
        print(f'File {fname} saved')


def unzip_file(zip_file_path, target_dir):

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)
        print(f'Zipfile: {zip_file_path} extracted.')

