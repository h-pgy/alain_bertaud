import os
from ..utils.file_path import solve_dir, solve_path, check_dir_exists, list_files_recursive, delete_existing_files
from ..utils.io import download_binary_file, unzip_file
from ..config import URIS_CAMADAS, SHP_FOLDER, ZIP_FOLDER


class ShpDownloader:
    
    
    domain = 'http://download.geosampa.prefeitura.sp.gov.br/PaginasPublicas/'
    zip_folder = ZIP_FOLDER
    shp_folder = SHP_FOLDER
    aliases = URIS_CAMADAS

    def get_file_uri(self, alias):

        fname = self.aliases[alias]

        uri = f'downloadArquivo.aspx?orig=DownloadCamadas&arq={fname}&arqTipo=Shapefile'

        return self.domain + uri
    
    def download_shp_zip(self, alias):

        uri = self.get_file_uri(alias)
        fname = solve_path(f'{alias}.zip', parent=self.zip_folder)

        download_binary_file(uri, fname)

        return fname
    
    def shp_path(self, alias):

        return solve_dir(solve_path(alias, self.shp_folder))
    
    def unzip_shp(self, zip_path, alias):

        dir_name = self.shp_path(alias)

        unzip_file(zip_path, dir_name)


    def check_shp_exists(self, shp_folder):
        
        checagem = check_dir_exists(shp_folder)
        if checagem:
            shp = list_files_recursive(shp_folder, '.shp')
            if shp:
                return True
        return False

    def pipe_download_shp(self, alias, check=True):

        shp_path = self.shp_path(alias)
        if check:
            checagem = self.check_shp_exists(shp_path)
            if checagem:
                print(f'Shape {shp_path} já salvo')
                return shp_path

        zip_path = self.download_shp_zip(alias)

        self.unzip_shp(zip_path, alias)

        return shp_path

    def download_all_shapes(self, check=True, delete_zips=True):

        for alias in self.aliases.keys():
            self.pipe_download_shp(alias, check)

        if delete_zips:
            delete_existing_files(self.zip_folder, extension='.zip')
    
    def __call__(self, check=True):

        self.download_all_shapes(check)





        
        


    