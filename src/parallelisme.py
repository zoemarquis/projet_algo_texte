import os
import threading
import time

# fichiers à lire en parallele
# revoir format des données
file1 = "../fichiers_test_parallelisation/sequence_NC_000020.11.txt"
file2 = "../fichiers_test_parallelisation/sequence_NC_000021.9.txt"
file3 = "../fichiers_test_parallelisation/sequence_NC_000022.11.txt"
files = [file1, file2, file3]

#fonction acces parallele
# bloque l'acces a une ressource partagee en parallele
def parallele_add(value, num_thread):
    global shared_variable, var_wait
    result = value * 2
        

    print(f"thread {num_thread} : tentative mutex")      
    #debut partie avec mutex (partie bloquée)
    with mutex:
        print(f"thread {num_thread} : mutex acquis")
        shared_variable += result
        var_wait +=1
        if var_wait % 10 == 0: #test le blocage
            time.sleep(1)
    #fin partie avec mutex
    print(f"thread {num_thread} : mutex libere")


# fonction de lecture des fichiers / traitement (à modifier en fonction des besoins)
def read_file(file_path, num_thread):
    with open(file_path, 'r') as file:
        for num_ligne, ligne in enumerate(file, start=1):

            if num_ligne % 10000 == 0 or num_ligne==1 : #afficher toutes les 10000 lignes pour vérifier
                print(f"num thread {num_thread} - ligne en cours : {num_ligne}: {ligne.strip()}")
                #time.sleep(1)  # Attendre 1 seconde entre chaque ligne

                parallele_add(num_ligne, num_thread)


#mutex pour éviter la modification d'une même zone
# a voir ou on l'utilise
mutex = threading.Lock()

var_wait = 0
shared_variable = 0 #variable de test 


# traitement parrallele
threads = []
for n_thread, file in enumerate(files, start=1):
    thread = threading.Thread(target=read_file, args=(file, n_thread)) #lancer thread et fonction
    threads.append(thread)
    thread.start()

# fin des threads
for thread in threads:
    thread.join()

# variable final
print("variable incrementee mutex :", shared_variable)