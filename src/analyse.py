
verbose = 0
print_errors = 0


def get_bornes(borne, genome):
    if verbose > 1: print('Analyse genome')
    
    chaine = ''

    for nucl in genome[borne[0] : borne[1]]:
        if nucl not in ('A', 'C', 'G', 'T'):
            if print_errors: print(f'Analyse Error: {nucl} not in A,C,G,T')
            return 0
        chaine += nucl

    return [chaine]


def get_join(bornes, genome):
    if verbose: print('Analyse join genome')

    chaines = []
    chaine_globale = ''
    
    for borne in bornes:
        chaine = get_bornes(borne, genome)[0]
        chaine_globale += chaine
        chaines += [chaine]

    if verbose: print(f'Join: {len(chaines) + 1}')
    return [chaine_globale] + chaines


def get_complement(borne, genome):
    if verbose: print('Analyse complement genome')
    
    complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}

    chaine = ''

    for nucl in genome[borne[0] : borne[1]]:
        if nucl not in ('A', 'C', 'G', 'T'):
            if print_errors: print(f'Analyse Error: {nucl} not in A,C,G,T')
            return 0
        chaine = complement[nucl] + chaine

    if verbose: print(f'Complement: {len(chaines) + 1}')
    return [chaine]


def get_complement_join(bornes, genome):
    if verbose: print('Analyse complement join genome')

    chaines = []
    chaine_globale = ''
    
    for borne in bornes:
        chaine = get_complement(borne, genome)[0]
        chaine_globale = chaine + chaine_globale
        chaines = [chaine] + chaines

    if verbose: print(f'Complement-Join: {len(chaines) + 1}')
    return [chaine_globale] + chaines


#-------------------------------------------------------------------------------


def transforme_bornes_simple(txt, borne_min, borne_max, sep):
    if verbose > 1: print('Parsing single bornes')
    
    tmp = txt[1:-4].split(sep)
    if len(tmp) != 2:
        if print_errors: print(f'Parsing Error: {sep} ne sépare pas en 2 ({txt})')
        return 0
    try:
        borne_inf = int(tmp[0])
        borne_sup = int(tmp[1])
    except:
        if print_errors: print(f'Parsing Error: {tmp[0]} ou {tmp[1]} non entier ({txt})')
        return 0

    if borne_min < borne_inf < borne_sup < borne_max:
        if verbose > 1: print('borne_inf', borne_inf, ' borne_sup ', borne_sup)
        return (borne_inf, borne_sup)
    else:
        if print_errors: print(f'Parsing Error: Bornes non ordonnées ({borne_min} < {borne_inf} < {borne_sup} < {borne_max}) ({txt})')
        return 0


def transforme_bornes_multiple(txt, borne_max):
    if verbose: print('Parsing multiple bornes')

    bornes = []
    borne_courante = 0

    for borne in txt.split(', '):
        res = transforme_bornes_simple(borne, borne_courante, borne_max, ':')
        if not res: return 0
        
        bornes += [res]
        borne_courante = res[1]

    return bornes



def transforme_borne_intron(txt, borne_max):
    if verbose: print('Parsing bornes intron')

    bornes = []
    borne_courante = 0

    for borne in txt.split(':')[1:-1]:
        res = transforme_bornes_simple(borne, borne_courante, borne_max, sep=', ')
        if not res: return 0

        bornes += [res]
        borne_courante = res[1]

    return bornes
    

#-------------------------------------------------------------------------------


def enleve_entete(txt, entete, fin):
    if verbose: print(txt)

    tmp = txt.split(entete)
    
    if len(tmp) != 2:
        if print_errors: print(f'Parsing Error: Entête ({entete}) non conforme ({txt})')
        return 0
    tmp = tmp[1].split(fin)
    if len(tmp) != 2:
        if print_errors: print(f'Parsing Error: Fin ({fin}) non conforme ({txt})')
        return 0
    elif len(tmp[1]) > 0:
        if print_errors: print(f'Parsing Error: Fin ({fin}) non conforme ({txt})')
        return 0
    
    return tmp[0]


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------


def analyse_bornes(txt, genome, intron):
    if verbose > 1: print('Analyse')
    
    borne_max = len(genome)
    bornes = []
    if txt[:4] == 'join':
        txt = enleve_entete(txt, 'join{', '}')
        if not txt:
            return 0
        if intron:
            bornes = transforme_borne_intron(txt, borne_max)
        else:
            bornes = transforme_bornes_multiple(txt, borne_max)
        if bornes:
            return get_join(bornes, genome)
        else:
            return 0
        
    elif txt[:15] == 'complement{join':
        txt = enleve_entete(txt, 'complement{join{', '}}')
        if intron:
            bornes = transforme_borne_intron(txt, borne_max)
        else:
            bornes = transforme_bornes_multiple(txt, borne_max)
        if bornes:
            return get_complement_join(bornes, genome)
        else:
            return 0
            
    elif txt[:10] == 'complement' and not intron:
        txt = enleve_entete(txt, 'complement{', '}')
        borne = transforme_bornes_simple(txt, borne_max)
        if borne:
            return get_complement(borne, genome)
        else:
            return 0
            
    elif not intron:
        bornes = transforme_bornes_simple(txt, 0, borne_max, ':')
        if bornes:
            return get_bornes(bornes, genome)
        else:
            return 0

    else:
        return 0



#join{[702268:702511](+), [0:1023](+)} -> (0 < 702268 < 702511 < 702511)
#join{[5631972:5632216](+), [5632215:5633123](+)} -> (5632216 < 5632215 < 5633123 < 6000087)

