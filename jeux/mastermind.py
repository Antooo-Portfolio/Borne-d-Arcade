import outils
from random import randint

liste_couleurs = ["R", "V", "B", "C", "J", "M"]  # Rouge, Vert, Bleu, Cyan, Jaune, Magenta
def créer_grille():
    """
    Crée une grille de jeu vide pour mastermind.

    Returns:
        list: Une liste de listes représentant la grille de jeu.
    """
    grille = [[" " for _ in range(4)] for _ in range(10)]
    return grille

def afficher_grille(grille):
    """
    Affiche la grille de jeu dans le terminal.

    Args:
        grille (list): La grille de jeu à afficher.

    Returns:
        None: Cette fonction affiche la grille mais ne renvoie aucune valeur.
    """
    print("+---+---+---+---+")
    for ligne in grille:
        print(f"| " + " | ".join(ligne) + " |")
        print("+---+---+---+---+")

def vérification_combinaison(grille, code_secret):
    """
    Permet à l'utilisateur de saisir une combinaison et vérifie si elle est correcte.

    Args:
        grille (list): La grille de jeu.
        code_secret (list): Le code secret à deviner.

    Returns:
        list: La combinaison proposée par l'utilisateur.
    """
    combinaison_valide = False

    while not combinaison_valide:
        saisie = outils.saisir_texte(
            "Proposez une combinaison de 4 couleurs parmis les couleurs disponibles (R, V, B, C, J, M)"
            "\n(exemple : RVBC) : ",
            ""
        ).upper()
        outils.clear()
        saisie = saisie.replace(" ", "").replace(",", "").replace("-", "")
        combinaison_proposée = list(saisie)
        combinaison_valide = len(combinaison_proposée) == 4
        if combinaison_valide:
            for couleur in combinaison_proposée:
                if couleur not in liste_couleurs:
                    combinaison_valide = False

        if not combinaison_valide:
            print("Combinaison invalide. Utilisez 4 couleurs parmi R, V, B, C, J et M.")

    return combinaison_proposée


def compter_pions(combinaison_proposée, code_secret):
    """Compte les couleurs bien placées et mal placées.

    Args:
        combinaison_proposée (list): Couleurs proposées par le joueur.
        code_secret (list): Couleurs du code secret.

    Returns:
        tuple[int, int]: Nombre de pions bien placés puis mal placés.
    """
    bien_places = 0
    propositions_restantes = []
    code_restant = []
    for position in range(4):
        proposition = combinaison_proposée[position]
        secret = code_secret[position]
        if proposition == secret:
            bien_places += 1
        else:
            propositions_restantes.append(proposition)
            code_restant.append(secret)

    mal_places = 0
    for proposition in propositions_restantes:
        position = 0
        while position < len(code_restant):
            if proposition == code_restant[position]:
                mal_places += 1
                code_restant[position] = ""
                break
            position += 1
    return bien_places, mal_places

def placer_combinaison(grille, combinaison_proposée, code_secret, ligne):
    """
    Place et colore la combinaison proposée dans la grille.

    Une couleur bien placée est affichée en gras avec sa couleur correspondante.
    Une couleur présente dans le code mais mal placée est soulignée.
    Une couleur absente du code est affichée avec la couleur par défaut du terminal.

    Args:
        grille (list): La grille de jeu.
        combinaison_proposée (list): La combinaison proposée par l'utilisateur.
        code_secret (list): Le code secret à comparer avec la combinaison.
        ligne (int): La ligne de la grille où placer la combinaison.

    Returns:
        None: Cette fonction modifie la grille mais ne renvoie aucune valeur.
    """
    couleurs_terminal = {
        "R": "31",  # Rouge
        "V": "32",  # Vert
        "B": "34",  # Bleu
        "C": "36",  # Cyan
        "J": "93",  # Jaune
        "M": "35"   # Magenta
    }
    positions_correctes = [False] * 4
    couleurs_restantes = list(code_secret)

    for i in range(4):
        if combinaison_proposée[i] == code_secret[i]:
            positions_correctes[i] = True
            couleurs_restantes[i] = None

    for i in range(4):
        combinaison = combinaison_proposée[i]
        code_couleur = couleurs_terminal[combinaison]

        if positions_correctes[i]:
            formatage = f"\033[1;{code_couleur}m"
        elif combinaison in couleurs_restantes:
            formatage = f"\033[4;{code_couleur}m"
            couleurs_restantes[couleurs_restantes.index(combinaison)] = None
        else:
            formatage = "\033[0m"

        grille[ligne][i] = f"{formatage}{combinaison}\033[0m"

def _jouer_mastermind_partie():
    """
    Lance une partie de Mastermind et gère son déroulement.

    Returns:
        int: Score obtenu pour cette partie.
    """
    grille = créer_grille()
    code_secret = [liste_couleurs[randint(0, 5)] for _ in range(4)]
    print("Bienvenue dans le jeu Mastermind !")
    print("Vous devez deviner le code secret composé de 4 couleurs.")
    print("Les couleurs disponibles sont : R (Rouge), V (Vert), B (Bleu), C (Cyan), J (Jaune), M (Magenta).")
    print("Une couleur bien placée est affichée en gras, une couleur mal placée est soulignée, et une couleur absente est affichée normalement.")

    partie_gagnee = False
    ligne = 0
    score_partie = 0

    while ligne < 10 and not partie_gagnee:
        afficher_grille(grille)
        combinaison_proposée = vérification_combinaison(grille, code_secret)
        placer_combinaison(grille, combinaison_proposée, code_secret, ligne)
        bien_places, mal_places = compter_pions(combinaison_proposée, code_secret)
        print("Pions bien placés : {}".format(bien_places))
        print("Pions mal placés : {}".format(mal_places))

        if combinaison_proposée == code_secret:
            afficher_grille(grille)
            print("Félicitations ! Vous avez trouvé le code secret !")
            score_partie = 10 - ligne
            if score_partie < 0:
                score_partie = 0
            partie_gagnee = True
        else:
            ligne += 1

    if not partie_gagnee:
        afficher_grille(grille)
        print(f"Désolé, vous n'avez pas trouvé le code secret. Le code était : {' '.join(code_secret)}")
        score_partie = 0

    print(f"Score final du mastermind : {score_partie}")

    return score_partie


def jouer_mastermind():
    """Joue une ou plusieurs parties de Mastermind sans récursion.

    Returns:
        int: Total des scores obtenus pendant la session.
    """
    return outils.jouer_session(_jouer_mastermind_partie)

if __name__ == "__main__":
    jouer_mastermind()