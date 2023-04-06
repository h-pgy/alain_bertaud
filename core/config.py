from dotenv import load_dotenv, find_dotenv
import json
from core.utils.env import load_env_variable
from core.utils.file_path import solve_dir, solve_path

load_dotenv(find_dotenv())

ORIGINAL_DATA_FOLDER = solve_dir(load_env_variable('original_data_folder'))
GENERATED_DATA_FOLDER = solve_dir(load_env_variable('generated_data_folder'))

def solve_folder(env_variable:str, parent=ORIGINAL_DATA_FOLDER)->str:

    folder_name = load_env_variable(env_variable)
    path = solve_path(folder_name, parent=parent)

    return solve_dir(path)
    

SHP_FOLDER = solve_folder('shp_folder')
ZIP_FOLDER = solve_folder('zip_folder')
IPTU_DATA_FOLDER = solve_folder('iptu_data_folder')
OD_DATA_FOLDER = solve_folder('od_data_folder')
CENSO_DATA_FOLDER = solve_folder('censo_data_folder')

IPTU_YEARS=[int(load_env_variable('iptu_ini')), int(load_env_variable('iptu_fim'))]

uris_camadas_json=solve_path(load_env_variable('uris_camadas_fname'))

with open(uris_camadas_json) as f:
    URIS_CAMADAS=json.load(f)
