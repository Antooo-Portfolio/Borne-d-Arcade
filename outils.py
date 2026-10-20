import subprocess
import os

def clear():
    """
    Efface l'écran du terminal.

    Returns:
        None: Cette fonction efface l'écran mais ne renvoie aucune valeur.
    """
    commande = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run(commande, shell=True)

def saisir_entier(prompt, min_val, max_val):
    """
    Demande à l'utilisateur de saisir un entier compris entre deux limites.

    Args:
        prompt (str): Message affiché pour demander la saisie.
        min_val (int): Valeur minimale autorisée.
        max_val (int): Valeur maximale autorisée.

    Returns:
        int: Entier saisi par l'utilisateur et compris entre les deux limites.
    """
    while True:
        try:
            valeur = int(input(prompt))
            if min_val <= valeur <= max_val:
                return valeur
            else:
                print(f"Veuillez entrer un nombre entre {min_val} et {max_val}.")
        except (ValueError, EOFError, KeyboardInterrupt):
            print("Entrée invalide. Veuillez entrer un nombre entier.")


def saisir_oui_non(prompt):
    """Demande une réponse oui/non et la retourne sous forme booléenne.

    Args:
        prompt (str): Message affiché pour demander la confirmation.

    Returns:
        bool: True pour une réponse affirmative, sinon False.
    """
    while True:
        try:
            reponse = input(f"{prompt} (O/N) : ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return False
        if reponse in ("o", "oui"):
            return True
        if reponse in ("n", "non"):
            return False
        print("Réponse invalide. Entrez O pour oui ou N pour non.")


def saisir_texte(prompt, valeur_par_defaut=""):
    """Demande un texte et retourne une valeur sûre en cas d'interruption.

    Args:
        prompt (str): Message affiché avant la saisie.
        valeur_par_defaut (str): Valeur retournée si la saisie est interrompue.

    Returns:
        str: Texte saisi, sans espaces inutiles aux extrémités.
    """
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return valeur_par_defaut


def jouer_session(fonction_partie, *arguments):
    """Relance une partie jusqu'au refus du joueur et additionne les scores."""
    score_total = 0
    while True:
        score_total += fonction_partie(*arguments)
        rejouer = saisir_oui_non("Voulez-vous relancer une partie ?")
        clear()
        if not rejouer:
            return score_total