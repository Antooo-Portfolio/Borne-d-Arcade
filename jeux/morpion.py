import random

import outils
def créer_grille():
    """
    Crée une grille de morpion vide avec les positions disponibles.

    Returns:
        dict[tuple[str, int], str]: Plateau indexé par colonne et ligne.
    """
    
    return {(colonne, ligne): " " for colonne in "abc" for ligne in range(1, 4)}

def afficher_grille(grille):
    """
    Affiche la grille du morpion dans le terminal.

    Args:
        grille (dict[tuple[str, int], str]): Plateau du morpion à afficher.

    Returns:
        None: Cette fonction affiche la grille mais ne renvoie aucune valeur.
    """
    
    numero_case = 1
    print("  +---+---+---+")
    for ligne in range(1, 4):
        cases = []
        for colonne in "abc":
            symbole = grille[colonne, ligne]
            if symbole == "X":
                cases.append("\033[31mX\033[0m")
            elif symbole == "O":
                cases.append("\033[34mO\033[0m")
            else:
                cases.append(str(numero_case))
            numero_case += 1
        print("{} | {} | {} | {} |".format(ligne, cases[0], cases[1], cases[2]))
        print("  +---+---+---+")

def vérification_victoire(grille, symbole_joueur):
    """
    Vérifie si un joueur possède une ligne, une colonne ou une diagonale complète.

    Args:
        grille (list[list[str]]): Grille de morpion à vérifier.
        symbole_joueur (str): Symbole du joueur à rechercher, `X` ou `O`.

    Returns:
        bool: `True` si le joueur a gagné, sinon `False`.
    """
    
    lignes_gagnantes = [
        [(colonne, ligne) for colonne in "abc"]
        for ligne in range(1, 4)
    ]
    colonnes_gagnantes = [
        [(colonne, ligne) for ligne in range(1, 4)]
        for colonne in "abc"
    ]
    diagonales_gagnantes = [
        [("a", 1), ("b", 2), ("c", 3)],
        [("c", 1), ("b", 2), ("a", 3)],
    ]
    combinaisons = lignes_gagnantes + colonnes_gagnantes + diagonales_gagnantes
    for combinaison in combinaisons:
        victoire = True
        for position in combinaison:
            if grille[position] != symbole_joueur:
                victoire = False
                break
        if victoire:
            return True
    return False


def choisir_coup_ordinateur(grille):
    """Choisit un coup aléatoire, gagnant ou bloquant.

    Args:
        grille (dict[tuple[str, int], str]): Plateau actuel.

    Returns:
        tuple[str, int]: Coordonnée choisie par l'ordinateur.
    """
    cases_libres = [position for position, valeur in grille.items() if valeur == " "]
    for symbole in ("O", "X"):
        for position in cases_libres:
            grille[position] = symbole
            victoire = vérification_victoire(grille, symbole)
            grille[position] = " "
            if victoire:
                return position
    return random.choice(cases_libres)

def vérficiation_position(grille):
    """
    Demande une position et vérifie que la case choisie est disponible.

    Args:
        grille (dict[tuple[str, int], str]): Plateau dans lequel jouer.

    Returns:
        tuple[str, int]: Coordonnée disponible choisie.
    """
    
    afficher_grille(grille)
    while True:
        saisie = outils.saisir_texte("Choisissez une case (1-9) : ").strip()
        if len(saisie) == 1 and saisie in "123456789":
            numero_case = int(saisie) - 1
            position = "abc"[numero_case % 3], numero_case // 3 + 1
            if grille[position] == " ":
                return position
            print("Cette case est déjà occupée.")
        else:
            print("Position invalide. Choisissez un chiffre de 1 à 9.")

def vérification_match_nul(grille):
    """
    Vérifie si toutes les cases de la grille sont occupées.

    Args:
        grille (list[list[str]]): Grille de morpion à vérifier.

    Returns:
        bool: `True` si la grille est pleine, sinon `False`.
    """
    
    for case in grille.values():
        if case not in ["X", "O"]:
            return False
    return True

def _jouer_morpion_partie(joueur1_name="Joueur 1"):
    """
    Lance une partie de morpion et gère son déroulement.

    Returns:
        int: Score obtenu pour cette partie (1 victoire, 0 nul ou défaite).
    """
    print("Bienvenue dans le jeu du Morpion !")
    print("Vous devez aligner trois symboles identiques pour gagner.")
    print("Les symboles disponibles sont : X et O.")
    print("Choisissez une case numérotée de 1 à 9. Un alignement peut être horizontal, vertical ou diagonal.")

    game_mode = outils.saisir_entier(
        "Jouer contre un autre joueur (1) ou contre l'ordinateur (2) ? ",
        1,
        2,
    )

    grille = créer_grille()
    joueur2_name = "Joueur 2" if game_mode == 1 else "Ordinateur"
    symbole_joueur1 = "X"
    symbole_joueur2 = "O"
    partie_en_cours = True
    tour_joueur = 1
    score_partie = 0

    while partie_en_cours:
        if tour_joueur == 1:
            nom_actuel = joueur1_name
            symbole_actuel = symbole_joueur1
        else:
            nom_actuel = joueur2_name
            symbole_actuel = symbole_joueur2
        outils.clear()
        print(f"C'est au tour de {nom_actuel} ({symbole_actuel})")
        if game_mode == 2 and tour_joueur == 2:
            position = choisir_coup_ordinateur(grille)
            numero_case = (position[1] - 1) * 3 + "abc".index(position[0]) + 1
            print("L'ordinateur joue dans la case {}.".format(numero_case))
        else:
            position = vérficiation_position(grille)

        grille[position] = symbole_actuel
        outils.clear()
        afficher_grille(grille)

        if vérification_victoire(grille, symbole_actuel):
            print(f"{nom_actuel} a gagné !")
            score_partie = 1 if tour_joueur == 1 else 0
            partie_en_cours = False
        elif vérification_match_nul(grille):
            print("Le match est nul !")
            partie_en_cours = False
        else:
            tour_joueur = 2 if tour_joueur == 1 else 1

    print(f"Score final du morpion : {score_partie}")

    return score_partie


def jouer_morpion(joueur1_name="Joueur 1"):
    """Joue une ou plusieurs parties de morpion sans récursion.

    Args:
        joueur1_name (str): Pseudo du joueur principal.

    Returns:
        int: Total des scores obtenus pendant la session.
    """
    return outils.jouer_session(_jouer_morpion_partie, joueur1_name)

if __name__ == "__main__":
    jouer_morpion()