from telnetlib import IP
from .download_geosampa import ShpDownloader
from .download_iptu_data import IptuDownloader
from .download_microdados_censo import DadosSetoresCensoDownload
from .download_pesquisa_od import OdDownload
from .download_vinculos_rais import RAISFTPDownloader

def download_all():

    shp = ShpDownloader()
    shp()
    iptu = IptuDownloader()
    iptu()
    censo = DadosSetoresCensoDownload()
    censo()
    od = OdDownload()
    od()
    rais = RAISFTPDownloader()
    rais()