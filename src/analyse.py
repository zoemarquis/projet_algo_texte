
def get_join(genome, bornes):

    chaines = []
    chaine_globale = ''
    
    for borne in bornes:
        chaine = ''
        for nucl in genome[borne[0] : borne[1]]:
            if nucl not in ('A', 'C', 'G', 'T'):
                return 0
            chaine += nucl
        chaine_globale += chaine
        chaines += [chaine]

    return [chaine_globale] + chaines


def get_complement_join(bornes, genome):

    complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}

    chaines = []
    chaine_globale = ''
    
    for borne in bornes:
        chaine = ''
        for nucl in genome[borne[0] : borne[1]]:
            if nucl not in ('A', 'C', 'G', 'T'):
                return 0
            chaine = complement[nucl] + chaine
        chaine_globale = chaine + chaine_globale
        chaines = [chaine] + chaines

    return [chaine_globale] + chaines


def get_complement(bornes, genome):
    borne = bornes[0]
    
    complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}

    chaine = ''

    for nucl in genome[borne[0] : borne[1]]:
        if nucl not in ('A', 'C', 'G', 'T'):
            return 0
        chaine = complement[nucl] + chaine

    return [chaine]


def get_bornes(bornes, genome):
    borne = bornes[0]

    chaine = ''

    for nucl in genome[borne[0] : borne[1]]:
        if nucl not in ('A', 'C', 'G', 'T'):
            return 0
        chaine += nucl

    return [chaine]



def transforme_bornes(txt, borne_min, borne_max):
    tmp = txt[1:-4].split(':')
    if len(tmp) != 2:
        return 0
    try:
        borne_inf = int(tmp[0])
        borne_sup = int(tmp[1])
    except:
        print("Parsing Error")
        return 0

    if borne_min < borne_inf < borne_sup < borne_max:
        # print("borne_inf", borne_inf, " borne_sup", borne_sup)
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


def analyse_bornes(txt, genome):
    borne_max = len(genome)
    bornes = []
    if txt[:4] == 'join':
        bornes = analyse_join(txt, borne_max)
        if bornes:
            return get_join(bornes, genome)
        
    elif txt[:15] == 'complement(join':
        bornes = analyse_complement_join(txt, borne_max)
        if bornes:
            return get_complement_join(bornes, genome)
            
    elif txt[:10] == 'complement':
        bornes = analyse_complement(txt, borne_max)
        if bornes:
            return get_complement(bornes, genome)
            
    else:
        bornes = transforme_bornes(txt, 0, borne_max)
        if bornes:
            return get_bornes(bornes, genome)
