from ..utils.file_path import solve_path, list_files_recursive, delete_existing_files
from ..utils.io import download_binary_file, unzip_file
from ..config import OD_DATA_FOLDER


class OdDownload:

    link = 'https://transparencia.metrosp.com.br/sites/default/files/OD-2017.zip'
    folder = OD_DATA_FOLDER

    def download_od_zip(self):

        fname = solve_path('od.zip', self.folder)
        zipfile = download_binary_file(self.link, fname = fname)
        
        return fname

    def check_od_data_exists(self):

        #arquivos de dados estão em .xlsx
        arquivos = list_files_recursive(self.folder, '.xlsx')

        return len(arquivos)>0

    def download_od_pipeline(self, delete_zip = True):

        if self.check_od_data_exists():
            print('Dados pesquisa OD já salvos')
            return
        
        zipfile = self.download_od_zip()
        unzip_file(zipfile, self.folder)

        if delete_zip:
            delete_existing_files(self.folder, extension='.zip')


    def __call__(self, delete_zip = True):

        self.download_od_pipeline(delete_zip)
        
        



