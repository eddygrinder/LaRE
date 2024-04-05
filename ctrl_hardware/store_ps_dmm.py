# Arquivo para armazenar os valores ps e dmm
# Não esquecer de documentar a escolha do módulo para manter e aceder aos valores de ps e dmm
ps = None
dmm = None

def set_values(ps_value, dmm_value):
    global ps, dmm
    ps = ps_value
    dmm = dmm_value

def get_values():
    return ps, dmm

def clear_values():
    global ps, dmm
    ps = None
    dmm = None