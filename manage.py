#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spotynov_api.settings')
import sys

def main():
    """
    Exécute les tâches administratives Django.
    
    Cette fonction initialise les paramètres d'environnement Django et exécute 
    les commandes Django via `execute_from_command_line`. Elle est utilisée pour 
    lancer les migrations, le serveur de développement ou d'autres tâches Django.
    
    **Processus** :
    1. Définit la variable d'environnement `DJANGO_SETTINGS_MODULE`.
    2. Importe `execute_from_command_line` de Django.
    3. Vérifie que Django est installé et accessible.
    4. Exécute la commande passée en argument.
    
    **Erreurs possibles** :
    - `ImportError` si Django n'est pas installé ou si la variable `PYTHONPATH` est mal configurée.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spotynov_api.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
