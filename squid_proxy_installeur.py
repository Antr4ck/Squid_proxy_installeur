###########################################################################################
#
# TITRE          : Script d'installation du proxy squid
# DESCRIPTION    :
# Le script d'installation du proxy squid vous permet de faire une installation complète
# de squid, il permet l'ajout d'un mot de passe d'accés, le changement du mot de passe
# ainsi que sa suppression.
# il permet aussi de désinstaller le proxy squid.
#
# AUTEUR         : David Chamaillard
# DATE           : 03/01/2022
#
###########################################################################################

########################## MODULES ########################################################

import subprocess,os # Permet de générer des processus d'interaction avec le systéme
import platform # Permet d'accéder au information du systéme pour la compatibilité

########################## FONCTIONS ################################################################

# Fonction qui installe le proxy Squid
def squidinstall():
    # Verifie la version de squid (avec prise en charge ssl) avec le systéme d'exploitation
    if platform.platform().find("Debian-10"):
        squid = "squid"
    else:
        squid = "squid3"
    # Fait les mises à jours et installe le proxy squid
    subprocess.call(["sudo", "apt-get", "update"])
    subprocess.call(["sudo", "apt-get", "install", "squid"])
    # La gestion subprocess aprés avoir fait l'installation envoi
    # les dossiers dans le chemin ci-dessous
    path = "/etc/{}/squid.conf".format(squid)
    # Puis il ouvre le fichier et lis le contenu
    file = open(path).read()
    # Le fichier d'origine (directive de conf) autorise le gestionnaire local
    s1 = file.replace("http_access allow localhost manager", "#http_access allow localhost manager")
    # le fichier d'origine est remplacé par
    s2 = s1.replace("http_access deny manager", "#http_access deny manager")
    # le fichier d'origine est remplacé par
    s3 = s2.replace("http_access allow localhost\n", "http_access allow all\n")
    #
    file_port = file.split("\nhttp_port ")[1].split("\n")[0]
    # écrit le port par défaut et l'écrit
    print("Default Port: ", file_port)
    # demande le port à changer et l'écrit
    port = input("Change to: ")
    # Remplace le port d'origine par le port changé ci-dessus avec les directives s3
    c_port = s3.replace("\nhttp_port " + file_port + "\n", "\nhttp_port " + port + "\n")
    # ouvre le fichier d'installation et copie le port choisi ci-dessus
    open("/etc/{}/squid.conf".format(squid), "w").write(c_port)
    # passe en sudo, vérifie le service squid et le redémarre
    subprocess.call(["sudo", "service", squid, "restart"])
    # si tous se passe bien
    print("Le proxy squid est installé")

# Fonction qui permet l'ajout d'un utilisateur ainsi que d'un mot de passe

def ajoutpass():
# Verifie la version de squid avec le systéme d'exploitation
    if platform.platform().find("Debian-10"):
        squid = "squid"
    else:
        squid = "squid3"
    # Passe en sudo, fait un apt-get, installe, apache2-utils (utilitaire pour authentification de base)
    subprocess.call(["sudo", "apt-get", "install", "apache2-utils"])
    # passe en sudo, crée un fichier dans le chemin ci-dessous
    subprocess.call(["sudo", "touch", "/etc/{}/squid_passwd".format(squid)])
    # passe en sudo, change les droits du fichier
    subprocess.call(["sudo", "chown", "proxy", "/etc/{}/squid_passwd".format(squid)])
    # demande la création d'un utilisateur
    user = input("Username: ")
    # passe en sudo, copie cette utilisateur créé et crypte le mot de passe
    subprocess.call(["sudo", "htpasswd", "/etc/{}/squid_passwd".format(squid), user])
    # puis il envoit les fichiers vers ce chemin
    path = "/etc/squid/squid.conf"
    # il ouvre les fichiers les lit
    file = open(path).read()
    # puis il remplace le fichier ci-dessous, avec les acls d'autorisation d'accés et crée une sauvegarde
    # du fichier remplacé
    sq = file.replace("http_access allow all\n",
                    "auth_param basic program /usr/lib/squid/basic_ncsa_auth /etc/squid/squid_passwd\n"
                    "acl ncsa_users proxy_auth REQUIRED\n"
                    "http_access allow ncsa_users\n")
    # il ouvre le chemin et copie les acls ci-dessus dans squid
    open("/etc/squid/squid.conf", "w").write(sq)
    # passe en sudo, vérifie le service et redémarre squid
    subprocess.call(["sudo", "service", squid, "restart"])
    # si pas de probléme
    print("Succés")

# fonction qui permet le changement du mot de passe d'accés squid

def changementpass():
    # Verifie la version de squid avec le systéme d'exploitation
    if platform.platform().find("Debian-10"):
        squid = "squid"
    else:
        squid = "squid3"
    # affiche l'utilisateur qui veut changer de mot de passe
    user = input("Username: ")
    # passe en sudo, change le mot de passe et le crypte via htpasswd
    subprocess.call(["sudo", "htpasswd", "/etc/{}/squid_passwd".format(squid), user])
    # passe en sudo, vérifie le service et redémarre squid
    subprocess.call(["sudo", "service", squid, "restart"])
    # si pas de probléme
    print("Succés")

# fonction qui permet de supprimer le mot de passe squid

def supppass():
    # Verifie la version de squid avec le systéme d'exploitation
    if platform.platform().find("Debian-10"):
        squid = "squid"
    else:
        squid = "squid3"
    # permet de supprimer un chemin de fichier (os.rmdir pour supprimer le répertoire)
    os.remove("/etc/{}/squid_passwd".format(squid))
    # puis il vérifie le chemin
    path = "/etc/{}/squid.conf".format(squid)
    # il ouvre le fichier et lit le contenu
    file = open(path).read()
    # puis il remplace le fichier ci-dessous, avec les acls d'autorisation d'accés
    sq = file.replace("auth_param basic program /usr/lib/squid/basic_ncsa_auth /etc/squid/squid_passwd\n"
                          "acl ncsa_users proxy_auth REQUIRED\n"
                          "http_access allow ncsa_users\n", "http_access allow all\n")
    # il ouvre le chemin et copie les acls ci-dessus dans squid
    open("/etc/{}/squid.conf".format(squid), "w").write(sq)
    # passe en sudo, vérifie le service et redémarre squid
    subprocess.call(["sudo", "service", squid, "restart"])
    # si pas de probléme
    print("Succés")

# fonction qui permet la désinstallation du proxy

def desinstallsquid():
    # Verifie la version de squid avec le systéme d'exploitation
    if platform.platform().find("Debian-10"):
        squid = "squid"
    else:
        squid = "squid3"
    # demande si on veut supprimer le squid
    del_sq = input("Are you sure? (y/n): ")
    # si la réponse est YES
    if del_sq == "y" or del_sq == "Y":
        # passe en sudo, fait un apt-get et purge les dossier squid et désinstalle
        subprocess.call(["sudo", "apt-get", "purge", "--auto-remove", squid])
        # si pas de probléme affiche succés et pass
        print("Succés")
    else:
        pass


########################## MENU ################################################################

# Menu qui permet

while True:
    squid_select = input("""
    1 - Installation de squid
    2 - Ajout d'un mot de passe
    3 - Changement du mot de passe
    4 - Suppression du mot de passe
    5 - Désinstallation de squid
    6 - Sortie\n""")

    if squid_select == "1":
        squidinstall()
    elif squid_select == "2":
        ajoutpass()
    elif squid_select == "3":
        changementpass()
    elif squid_select == "4":
        supppass()
    elif squid_select == "5":
        desinstallsquid()
    elif squid_select == "6":
        break
    else:
        pass
