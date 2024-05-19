from src.resultat import *
import re

verbose = 0
print_errors = 0

logger = None

def get_bornes(borne, genome):
    if verbose > 1: print('Analyse genome')
    
    chaine = ''

    for nucl in genome[borne[0] : borne[1]]:
        if nucl not in ('A', 'C', 'G', 'T'):
            logger.write(f'Analysis Error: {nucl} not in A,C,G,T')
            return 0
        chaine += nucl

    return chaine


def get_join(bornes, genome):
    if verbose: print('Analyse join genome')

    chaines = []
    chaine_globale = ''
    
    for borne in bornes:
        chaine = get_bornes(borne, genome)
        if not chaine: return 0
        chaine_globale += chaine
        chaines += [chaine]

    if verbose: print(f'Join: {len(chaines) + 1}')
    return chaines


def get_complement(borne, genome):
    if verbose: print('Analyse complement genome')
    
    complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}

    chaine = ''

    if borne[0] < borne[1]:
        liste = genome[borne[0]:borne[1]]
    else:
        liste = genome[borne[1] : borne[0]]

    for nucl in liste:
        if nucl not in ('A', 'C', 'G', 'T'):
            logger.write(f'Analyse Error: {nucl} not in A,C,G,T')
            return 0
        chaine = complement[nucl] + chaine

    if verbose: print(f'Complement: {len(chaine) + 1}')
    return chaine


def get_complement_join(bornes, genome):
    if verbose: print('Analyse complement join genome')

    chaines = []
    chaine_globale = ''
    
    for borne in bornes:
        chaine = get_complement(borne, genome)
        if not chaine: return 0
        chaine_globale = chaine + chaine_globale
        chaines = [chaine] + chaines

    if verbose: print(f'Complement-Join: {len(chaines) + 1}')
    return chaines


#-------------------------------------------------------------------------------


def transforme_bornes_simple(txt, borne_min, borne_max, sep, txt_join=None, strand_pos=True, intron=False):
    if verbose > 1: print('Parsing single bornes')
    
    tmp = [s for s in txt.split(sep)]
    if len(tmp) != 2:
        logger.write(f'Parsing Error: {sep} ne sépare pas en 2 ({txt})')
        return 0
    try:
        borne_inf = int(tmp[0][1:])
        borne_sup = int(tmp[1][:-1])
    except:
        logger.write(f'Parsing Error: {tmp[0]} ou {tmp[1]} non entier ({txt})')
        return 0

    if strand_pos:
        if borne_min <= borne_inf and borne_sup <= borne_max:
            if verbose > 1:
                print('borne_inf', borne_inf, ' borne_sup ', borne_sup)
            return (borne_inf, borne_sup)
        else:
            logger.write(f'Parsing Error: Bornes non ordonnées ({borne_min} <= {borne_inf} < {borne_sup} <= {borne_max}) ({txt_join if txt_join else txt})')
            return 0
    else:
        if borne_min >= borne_inf or borne_sup >= borne_max:
            if verbose > 1:
                print('borne_inf', borne_inf, ' borne_sup ', borne_sup)
            return (borne_inf, borne_sup)
        else:
            logger.write(f'Parsing Error : Bornes non ordonnées ({borne_min} >= {borne_inf} or {borne_sup} >= {borne_max}) ({txt_join if txt_join else txt})')
            return 0



def transforme_bornes_multiple(txt, borne_max):
    if verbose: print('Parsing multiple bornes')
    strand_pos = True
    if '-' in txt:
        strand_pos = False

    bornes = []
    borne_courante = 0

    for borne in txt.split(', '):
        translation_table = str.maketrans('', '', '](+)[-')
        borne = '(' + borne.translate(translation_table) + ')'
        if not strand_pos: res = transforme_bornes_simple(borne, borne_max, borne_courante, ':', txt, strand_pos)
        else: res = transforme_bornes_simple(borne, borne_courante, borne_max, ':', txt, strand_pos)
        if not res: return 0
        
        bornes += [res]
        borne_courante = res[1]

    return bornes



def transforme_borne_intron(txt, borne_max):
    if verbose: print('Parsing bornes intron')
    strand_pos = False
    bornes = []
    borne_courante = 0
    if '+' in txt: strand_pos = True
    for borne in txt.split(':')[1:-1]:
        translation_table = str.maketrans('', '', '](+)[-')
        borne = '(' + borne.translate(translation_table) + ')'
        if not strand_pos: res = transforme_bornes_simple(borne, borne_max, borne_courante, ', ', txt, strand_pos)
        else: res = transforme_bornes_simple(borne, borne_courante, borne_max, ', ', txt, strand_pos, True)
        if not res: return 0

        bornes += [res]
        borne_courante = res[1]

    return bornes
    

#-------------------------------------------------------------------------------


def enleve_entete(txt, entete, fin):
    if verbose: print(txt)

    tmp = txt.split(entete)
    
    if len(tmp) != 2:
        logger.write(f'Parsing Error: Entête ({entete}) non conforme ({txt})')
        return 0
    tmp = tmp[1].split(fin)
    if len(tmp) != 2:
        logger.write(f'Parsing Error: Fin ({fin}) non conforme ({txt})')
        return 0
    elif len(tmp[1]) > 0:
        logger.write(f'Parsing Error: Fin ({fin}) non conforme ({txt})')
        return 0
    
    return tmp[0]


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------


def analyse_bornes(txt, genome, intron, path, region, nc, log):
    global logger
    logger = log
    if verbose > 1: print('Analyse')
    nb_intron = 0
    bornes_intron = []
    borne_max = len(genome)
    bornes = []
    complement = False


    if '+' in txt and '-' in txt:
        logger.write(f'Parsing Error: Incohérence dans les strands (+) et (-) ({txt})')
        return 0
    if '-' in txt:
        complement = True


    if txt[:4] == 'join' and not complement:            
        txt = enleve_entete(txt, 'join{', '}')
        if not txt:
            return 0
        if intron:
            bornes_intron = transforme_borne_intron(txt, borne_max)
            bornes = transforme_bornes_multiple(txt, borne_max)
            if bornes and bornes_intron:
                nb_intron = len(bornes_intron)  
                seq = get_join(bornes, genome)
                seq_intron = get_join(bornes_intron, genome)
                if not seq or not seq_intron : return 0
                create_result(path, region, bornes, seq, nc, 'join', nb_intron, bornes_intron, log, seq_intron)
            else:
                return 0
        else:
            bornes = transforme_bornes_multiple(txt, borne_max)
            if bornes:
                seq = get_join(bornes, genome)
                if not seq: return 0
                create_result(path, region, bornes, seq, nc, 'join', 0, bornes_intron, log)
            else:
                return 0
        
    elif txt[:4] == 'join' and complement:
        txt = enleve_entete(txt, 'join{', '}')
        if intron:
            #bornes_intron = transforme_borne_intron(txt, borne_max)
            bornes = transforme_bornes_multiple(txt, borne_max)
            bornes = [(a, b) for a, b in reversed(bornes)]

            bornes_intron = [(bornes[i][1], bornes[i+1][0]) for i in range(len(bornes) - 1)]

            if bornes and bornes_intron:
                nb_intron = len(bornes_intron)
                seq = get_complement_join(bornes, genome)
                seq_intron = get_complement_join(bornes_intron, genome)
                if not seq or not seq_intron: return 0
                create_result(path, region, bornes, seq, nc, 'complement join', nb_intron, bornes_intron, log, seq_intron)
            else:
                return 0
        else:
            bornes = transforme_bornes_multiple(txt, borne_max)
            if bornes:
                seq = get_complement_join(bornes, genome)
                if not seq: return 0
                create_result(path, region, bornes, seq, nc, 'complement join', 0, bornes_intron, log)
            else:
                return 0
            
    elif complement:
        translation_table = str.maketrans('', '', '](+)[-')
        borne = '(' + txt.translate(translation_table) + ')'
        borne = transforme_bornes_simple(borne, 0, borne_max, ':')
        if borne:
            seq = get_complement(borne, genome)
            if not seq: return 0
            create_result(path, region, borne, seq, nc, 'complement', nb_intron, bornes_intron, log)
        else:
            return 0
            
    else:
        translation_table = str.maketrans('', '', '](+)[-')
        borne = '(' + txt.translate(translation_table) + ')'
        borne = transforme_bornes_simple(borne, 0, borne_max, ':')
        if borne:
            seq = get_bornes(borne, genome)
            if not seq: return 0
            create_result(path, region, borne, seq, nc, None, nb_intron, bornes_intron, log)
        else:
            return 0



