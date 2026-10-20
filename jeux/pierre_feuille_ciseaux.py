from random import choice
import outils

# P = Pierre, F = Feuille, C = Ciseaux
éléments = ["P", "F", "C"]
regles = {"P": "C", "F": "P", "C": "F"}


def reponse_joueur():
    """Demande la réponse du joueur et valide sa saisie."""
    while True:
        choix = outils.saisir_texte(
            "Choisissez P (Pierre), F (Feuille) ou C (Ciseaux) : "
        ).upper()
        if choix in éléments:
            return choix
        print("Réponse invalide. Entrez P, F ou C.")


def reponse_ordinateur():
    """Retourne un choix aléatoire pour l'ordinateur."""
    return choice(éléments)


def vérification_victoire(joueur, ordinateur):
    """Détermine le gagnant d'un tour.

    Args:
        joueur (str): Choix du joueur.
        ordinateur (str): Choix de l'ordinateur.

    Returns:
        str: Résultat du tour.
    """
    if joueur == ordinateur:
        return "égalité"

    if regles[joueur] == ordinateur:
        return "joueur"

    return "ordinateur"

def _jouer_pierre_feuille_ciseaux_partie():
    """Joue une partie de pierre-feuille-ciseaux."""
    score_joueur = 0
    score_ordinateur = 0
    nombre_tours = 3

    print("\nBienvenue dans Pierre Feuille Ciseaux !")
    print(f"Premier à {nombre_tours} points gagne la partie.\n")

    while score_joueur < nombre_tours and score_ordinateur < nombre_tours:
        choix_joueur = reponse_joueur()
        choix_ordinateur = reponse_ordinateur()

        print(f"L'ordinateur a choisi : {choix_ordinateur}")

        résultat = vérification_victoire(choix_joueur, choix_ordinateur)

        if résultat == "égalité":
            print("Égalité !")
        elif résultat == "joueur":
            score_joueur += 1
            print("Vous gagnez ce tour !")
        else:
            score_ordinateur += 1
            print("L'ordinateur gagne ce tour !")

        print(f"Score : Vous {score_joueur} - {score_ordinateur} Ordinateur\n")

    outils.clear()
    if score_joueur > score_ordinateur:
        print("Félicitations ! Vous avez gagné la partie !")
        score_partie = 1
    elif score_ordinateur > score_joueur:
        print("L'ordinateur remporte la partie. Réessayez !")
        score_partie = 0
    else:
        score_partie = 0

    print(f"Score final du pierre-feuille-ciseaux : {score_partie}")

    return score_partie


def jouer_pierre_feuille_ciseaux():
    """Joue une ou plusieurs parties sans utiliser la récursion.

    Returns:
        int: Total des scores obtenus pendant la session.
    """
    return outils.jouer_session(_jouer_pierre_feuille_ciseaux_partie)


if __name__ == "__main__":
    jouer_pierre_feuille_ciseaux()