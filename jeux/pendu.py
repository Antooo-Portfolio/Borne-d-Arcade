import outils
import random
from pathlib import Path

dessins_pendu = [
    "\n".join([
        "       ",
        "       ",
        "       ",
        "       ",
        "       ",
        "========="
    ]),
    "\n".join([
        "      |",
        "      |",
        "      |",
        "      |",
        "      |",
        "========="
    ]),
    "\n".join([
        "  +---+",
        "      |",
        "      |",
        "      |",
        "      |",
        "========="
    ]),
    "\n".join([
        "  +---+",
        "  |   |",
        "      |",
        "      |",
        "      |",
        "========="
    ]),
    "\n".join([
        "  +---+",
        "  |   |",
        "  O   |",
        "      |",
        "      |",
        "========="
    ]),
    "\n".join([
        "  +---+",
        "  |   |",
        "  O   |",
        "  |   |",
        "      |",
        "========="
    ]),
    "\n".join([
        "  +---+",
        "  |   |",
        "  O   |",
        " /|   |",
        "      |",
        "========="
    ]),
    "\n".join([
        "  +---+",
        "  |   |",
        "  O   |",
        " /|\  |",
        "      |",
        "========="
    ]),
    "\n".join([
        "  +---+",
        "  |   |",
        "  O   |",
        " /|\  |",
        " /    |",
        "========="
    ]),
    "\n".join([
        "  +---+",
        "  |   |",
        "  O   |",
        " /|\  |",
        " / \  |",
        "========="
    ])
]

def choisir_mot():
    """Choisit un mot aléatoire dans la liste disponible."""
    chemin_liste = Path(__file__).resolve().parent.parent / "wordlist.txt"
    with chemin_liste.open(encoding="utf-8") as fichier:
        mots = fichier.read().splitlines()
    mots = [mot.strip() for mot in mots if mot.strip()]
    return random.choice(mots or ["ARCADE"]).upper()

def vérification_victoire(masque):
    """
    Vérifie si le joueur a deviné toutes les lettres du mot.

    Args:
        masque (list): Liste représentant l'état actuel du mot masqué.

    Returns:
        bool: True si le joueur a gagné, False sinon.
    """
    victoire = "_" not in masque
    return victoire

def vérification_lettre(mot, masque, lettre, erreurs):
    """
    Permet au joueur de proposer une lettre et met à jour le masque en conséquence.

    Args:
        mot (str): Le mot à deviner.
        masque (list): Liste représentant l'état actuel du mot masqué.
        lettre (str): Lettre proposée par le joueur.
        erreurs (int): Nombre d'erreurs déjà commises.

    Returns:
        int: Nouveau nombre d'erreurs commises.
    """
    if lettre in mot:
        position = 0
        while position < len(mot):
            if mot[position] == lettre:
                masque[position] = lettre
            position += 1
    else:
        erreurs += 1

    return erreurs

def _jouer_pendu_partie():
    """
    Fonction principale pour jouer au jeu du Pendu.

    Returns:
        int: Score obtenu pour cette partie.
    """
    mot = choisir_mot()
    masque = ["_"] * len(mot)
    erreurs = 0
    score_partie = 0
    lettres_proposees = []

    while not vérification_victoire(masque) and erreurs < len(dessins_pendu) - 1:
        outils.clear()
        print(dessins_pendu[erreurs])
        print(" ".join(masque))
        print("Lettres proposées : {}".format(", ".join(lettres_proposees) or "aucune"))
        lettre = outils.saisir_texte("Proposez une lettre : ").upper()
        if len(lettre) == 1 and lettre in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if lettre in lettres_proposees:
                print("Vous avez déjà proposé cette lettre.")
                outils.saisir_texte("Appuyez sur Entrée pour continuer. ")
            else:
                lettres_proposees.append(lettre)
                erreurs = vérification_lettre(mot, masque, lettre, erreurs)
        else:
            print("Erreur : veuillez entrer une seule lettre.")
            outils.saisir_texte("Appuyez sur Entrée pour continuer. ")

    outils.clear()
    print(dessins_pendu[erreurs])
    print(" ".join(masque))

    if vérification_victoire(masque):
        print("Bravo ! Vous avez deviné le mot :", mot)
        score_partie = 10 - erreurs
        if score_partie < 0:
            score_partie = 0
    else:
        print("Vous avez perdu ! Le mot était :", mot)
        score_partie = 0

    print(f"Score final du pendu : {score_partie}")

    return score_partie


def jouer_pendu():
    """Joue une ou plusieurs parties de pendu sans récursion.

    Returns:
        int: Total des scores obtenus pendant la session.
    """
    return outils.jouer_session(_jouer_pendu_partie)

if __name__ == "__main__":
    jouer_pendu()

