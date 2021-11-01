from typing import Dict, final


def make_vars_dict(file_path: str) -> Dict[str, str]:
    """
    Genera un diccionario con las variables del archivo enviado por 
    parametro parseadas con sus respectivas variables de ambiente
    """
    with open(file_path, 'r') as archivo:
        lines_file = archivo.readlines()

    vars_dict = {}
    for line in lines_file:

        if line.startswith('#') or line == '\n':
            continue

        key, value = line.split('=')

        if '#' in value:
            value = value[:value.index('#')].strip()

        final_value = value.replace('\n', '')
        if final_value == 'true' or final_value == 'false':
            final_value = bool(final_value)

        vars_dict[key] = final_value

    return vars_dict
