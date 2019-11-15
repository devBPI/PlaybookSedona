BPI - Catalogue - Déploiement
=============

## Prérequis
### Commun
* Environnement linux (RedHat, Debian et dérivés)
* Python 3 (version 3.7 de préférence) et son gestionnaire de paquet `pip`
* La librairie `lxml` du langage python
  - `sudo pip install -U lxml`
* Utilisateur non-root avec accès `sudo` pour l'exécution des commandes de déploiement et l'exécution des processus PHP du site.  
  Note: les accès `sudo` sont nécessaires pour redémarrer le service `php-fpm` en fin de déploiement.
    
### Pour la machine de déploiement
* Ansible >= 2.8 and requirements
   - `sudo pip install -r requirements.txt`
* Si le serveur cible est une autre machine : accès ssh avec l'utilisateur exécutant l'application Catalogue
### Pour la machine "serveur web"
* Dossier de déploiement présent et accessible en écriture par l'utilisateur cité au point précédent
* Si cette machine n'est pas celle exécutant l'outil Ansible : service SSH activé et utilisable par l'utilisateur exécutant l'application Catalogue


## Préparation
> Ces étapes sont à réaliser une seule fois, sur la machine en charge du déploiement

1. Cloner / dézipper le projet dans le répertoire de travail sur la machine de déploiement (exemple : `/var/data/scripts/deploy`)
1. Installer les requis si nécessaire (voir « [Prérequis - Pour la machine de déploiement](#pour-la-machine-de-dploiement) »)
1. Créer le fichier `inventory.yml` à partir du fichier d'inventaire d'exemple correspondant à la topologie de déploiement :  
  - Pour une configuration où les rôles de serveur web et de machine de déploiement sont portés par la même machine, 
  copier `example-local-inventory.yml.dist` vers `inventory.yml`.
  - Pour une configuration où les rôles de serveur web et de machine de déploiement sont portés par des machines différentes, 
  copier `example-remote-inventory.yml.dist` vers `inventory.yml` et compléter ce dernier avec les informations requises 
  (adresses IP/nom d'ĥôte, nom d'utilisateur).
1. Se placer dans le répertoire de travail (exemple : `/var/data/scripts/deploy`) et lancer la commande d'initialisation ci-dessous
 et renseigner les informations demandées (en partie fournies par Sedona) :  
  `ansible-playbook initial_setup.yml`

## Déploiement
    
### Déploiement d'une nouvelle version
Lancer la commande ci-dessous permet de déployer une version (nouvelle ou ancienne) disponible dans le dépôt d'artefacts.

    ansible-playbook -i inventory.yml deploy.yml
    
Répondre aux questions proposées pour paramétrer le scénario de déploiement avec les valeurs souhaitées.