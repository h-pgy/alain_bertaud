from ftplib import FTP
from core.config import RAIS_YEARS, RAIS_FOLDER
from core.utils.file_path import solve_path

class RAISFTPDownloader:
    
    
    host = 'ftp.mtps.gov.br'
    
    
    def __init__(self, years=RAIS_YEARS, folder=RAIS_FOLDER)->None:
        
        self.ftp = FTP(self.host)
        self.ftp.login()
        self.years = years
        self.folder = folder
        
    def chdir_microdados_rais(self)->None:
        
        self.ftp.cwd('pdet/microdados/RAIS')
    
    def get_folder_years(self)->list:
        
        folders = self.ftp.nlst()
        set_years = set(str(year) for year in self.years)
        return [int(f) for f in folders if f in set_years]
    
    def get_vinculos_sp_file(self, year)->str:
        
        if year < 2018:
            fname = f'SP{year}.7z'
            assert fname in self.ftp.nlst(str(year))
        else:
            fname = 'RAIS_VINC_PUB_SP.7z'
            assert fname in self.ftp.nlst(str(year))
        
        return fname
    
    def new_fname(self, year)->str:
        
        new_fname = f'microdados_vinculos_rais{year}.7z'
        
        return solve_path(new_fname, self.folder)
    
    def download_file(self, year)->None:
        
        og_fname = self.get_vinculos_sp_file(year)
        new_fname = self.new_fname(year)
        self.ftp.cwd(str(year))
        with open(new_fname, 'wb') as f:
            self.ftp.retrbinary(f'RETR {og_fname}', f.write)
        self.ftp.cwd('..')
            
    def __call__(self):
        
        self.chdir_microdados_rais()
        years = self.get_folder_years()
        for year in years:
            print(f'Downloading {year} microdata file')
            self.download_file(year)