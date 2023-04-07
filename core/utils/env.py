import os

def load_env_variable(variable_name:str)->str:

    return os.environ.get(variable_name)
