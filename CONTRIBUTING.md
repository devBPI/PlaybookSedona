# Comment contribuer #

## Environnement de développement
### Prérequis
* Python 3 (3.7 de préférence)
* Gestionnaire de paquet `pip`
* Optionnel: Python Virtualenv

### Préparation
Installer les dépendances du projet (dans un virtualenv si applicable) :  
```shell script
$ python -m pip -r dev-requirements.txt
``` 

## Ajouter un nouveau paramètre d'application

1. Vérifier le nom du/des nouveau(x) paramètre(s) dans le fichier `.env.dist` de l'application Catalogue.
   Exemple: 
   ```dotenv
   ##> Component config
   NEW_PARAMETER="parameter value"
   ```
   À partir de ce nouveau paramètre, dériver un nouveau nom de variable Ansible similaire à la nomenclature suivante :  
   ```yaml
   app_config_<lowercase(parameter name)>
   ```
   Exemple pour un paramètre `CATALOGUE_DESIGN_TITLE` :  
   ```yaml
   app_config_catalogue_design_title
   ```

2. Compléter le template `templates/project_vars.yml.j2`:  
   Ajouter une ligne au format suivant :
   ```yaml
   app_config_parameter_name: "{{ app_config_parameter_name }}"
   ```
   > REMARQUE : C'est ce fichier qui servira de liste de référence lors des vérifications automatiques.
   
3. Compléter le playbook `initial_setup.yml`  
   Ajouter un bloc par nouvelle variable à la liste des `vars_prompt`:  
   ```yaml
   - name: "app_config_parameter_name" # Clé du paramètre
     prompt: Text explanation          # Description du paramètre
     default: "my value"               # Valeaur par défaut (si applicable)
     private: no                       # Passer cette valeur à 'yes' si ce paramètre 
                                       # est une valeur « sensible » (ex: clé secrète, mot de passe…)  
   ``` 

4. Compléter le playbook `deploy.yml`:  
   Compléter la liste des vérifications de variables avec celle(s) ajoutée(s) aux étapes précédentes :
   * Repérer le bloc d'instruction nommé «`BPI — Vérification de la configuration`»
   * Ajouter une ligne au format ci-dessous par variable :  
   ```yaml
   - app_config_parameter_name is defined
   ```

5. Compléter les opérations du fichier `tasks/after_update.yml`:  
   * Repérer l'opération nommée « `Fill config values` »
   * Ajouter un bloc au format ci-dessous au contenu de l'attribut `loop`:  
   ```yaml
   - {
      search: "^(PARAMETER_NAME=).+$",
      replace: "\\g<1>{{ app_config_parameter_name }}"
    }
   ```
   
   Par exemple pour le paramètre `CATALOGUE_DESIGN_TITLE` devant recevoir la valeur du paramètre `app_config_catalogue_design_title`:  
   ```yaml
   - {
      search: "^(CATALOGUE_DESIGN_TITLE=).+$",
      replace: "\\g<1>{{ app_config_catalogue_design }}"
    }
   ```
   
6. Lancer les tests :  
   ```shell script
   $ python -m unittest
   ```
   Le résultat devra être sans erreur, comme l'exemple ci-dessous
   
   ```shell script
   python -m unittest                                                                                                                                      venv    12:24:11  
   ...
   ----------------------------------------------------------------------
   Ran 3 tests in 0.031s
   
   OK
   ```
   
7. Compléter le fichier `CHANGELOG` :
   
   - En ajoutant un item à la liste « *Prochaine version* » en tête du fichier, exemple :  
       ```text
       Prochaine version: 
           - Nouveau paramètre 'PARAMETER_NAME' ajouté
           - Correction des règle de remplacement
       ```
   
   - Ou en créant une nouvelle ligne de « *release* » si applicable, complété par le tag git correspondant.  
     Exemple :  
        ```text
        X.Y.Z — 2019/12/01
           - Nouveau paramètre 'PARAMETER_NAME' ajouté
           - Correction des règle de remplacement
        ```