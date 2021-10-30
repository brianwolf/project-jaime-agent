from typing import Dict


def make_vars_dict(file_path: str) -> Dict[str, str]:
    """
    Genera un diccionario con las variables del archivo enviado por 
    parametro parseadas con sus respectivas variables de ambiente
    """
    with open(file_path, 'r') as archivo:
        renglones_archivo = archivo.readlines()

    diccionario_variables = {}
    for renglon in renglones_archivo:

        if renglon.startswith('#') or renglon == '\n':
            continue

        clave, valor = renglon.split('=')

        if '#' in valor:
            valor = valor[:valor.index('#')].strip()

        diccionario_variables[clave] = valor.replace('\n', '')

    return diccionario_variables
