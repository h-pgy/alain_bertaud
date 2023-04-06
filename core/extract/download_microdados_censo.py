from ..utils.file_path import solve_path, list_files_recursive, delete_existing_files
from ..utils.io import download_binary_file, unzip_file
from ..config import CENSO_DATA_FOLDER


class DadosSetoresCensoDownload:

    #NA VERDADE QUERO OS DADOS AGREGADOS POR SETOR CENSITARIO
    link = 'https://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios/SP_Capital_20190823.zip'
    folder = CENSO_DATA_FOLDER

    def download_census_zip(self):

        fname = solve_path('microdados_censo.zip', self.folder)
        download_binary_file(self.link, fname = fname)
        
        return fname

    def check_census_data_exists(self):

        #arquivos de dados estão em txt
        arquivos = list_files_recursive(self.folder, '.csv')

        return len(arquivos)>0

    def download_census_pipeline(self, delete_zip = True):

        if self.check_census_data_exists():
            print('Dados censo já salvos')
            return
        
        zipfile = self.download_census_zip()
        unzip_file(zipfile, self.folder)

        if delete_zip:
            delete_existing_files(self.folder, extension='.zip')


    def __call__(self, delete_zip = True):

        self.download_census_pipeline(delete_zip)


