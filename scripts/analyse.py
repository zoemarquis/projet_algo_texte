def transforme_bornes(txt, borne_min, borne_max):
    tmp = txt.split(':')
    if len(tmp) != 2:
        return 0
    try:
        borne_inf = int(tmp[0])
        borne_sup = int(tmp[1])
    except:
        print("Parsing Error")
        return 0

    if borne_inf < borne_sup and borne_inf > borne_min and borne_sup < borne_max:
        print("borne_inf", borne_inf, " borne_sup", borne_sup)
        return [(borne_inf, borne_sup)]
    else:
        return 0


def analyse_join(txt, borne_max):
    print("Parsing Join")
    tmp = txt.split('join(')
    if len(tmp) != 2:
        return 0
    tmp = tmp[1].split(')')
    if len(tmp) != 2:
        return 0
    txt = tmp[0]

    bornes = []
    borne_courante = 0

    for borne in txt.split(','):
        res = transforme_bornes(borne, borne_courante, borne_max)
        if not res: return 0

        bornes += res
        borne_courante = res[0][1]

    return bornes


def analyse_complement(txt, borne_max):
    print("Parsing Complement")
    tmp = txt.split('complement(')
    if len(tmp) != 2:
        return 0
    tmp = tmp[1].split(')')
    if len(tmp) != 2:
        return 0
    txt = tmp[0]

    res = transforme_bornes(txt, 0, borne_max)
    if not res: return 0

    return res


def analyse_complement_join(txt, borne_max):
    print("Parsing Complement Join")
    tmp = txt.split('complement(join(')
    if len(tmp) != 2:
        return 0
    tmp = tmp[1].split('))')
    if len(tmp) != 2:
        return 0
    txt = tmp[0]

    bornes = []
    borne_courante = 0

    for borne in txt.split(','):
        res = transforme_bornes(borne, borne_courante, borne_max)
        if not res: return 0

        bornes += res
        borne_courante = res[0][1]

    return bornes


def analyse_bornes(txt, borne_max):
    bornes = []
    if txt[:4] == 'join':
        bornes = analyse_join(txt, borne_max)
        if bornes:
            # get_join(bornes)
            return bornes
    elif txt[:15] == 'complement(join':
        bornes = analyse_complement_join(txt, borne_max)
        if bornes:
            # get_complement_join(bornes)
            return bornes
    elif txt[:10] == 'complement':
        bornes = analyse_complement(txt, borne_max)
        if bornes:
            # get_complement(bornes)
            return bornes
    else:
        bornes = transforme_bornes(txt, 0, borne_max)
        if bornes:
            # get_bornes(bornes)
            return bornes
