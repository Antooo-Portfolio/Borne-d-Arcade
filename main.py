from pathlib import Path

import outils

scores = {}
parties_jouees = {}
total_scores = {}
FICHIER_SCORES = Path(__file__).resolve().with_name("scores.txt")
JEUX = {
    1: ("morpion", "jouer_morpion", "morpion"),
    2: ("mastermind", "jouer_mastermind", "mastermind"),
    3: ("pendu", "jouer_pendu", "pendu"),
    4: ("calcul_mental", "jouer_calcul_mental", "calcul mental"),
    5: ("pierre_feuille_ciseaux", "jouer_pierre_feuille_ciseaux", "pierre-feuille-ciseaux"),
    6: ("juste_prix", "jouer_juste_prix", "juste prix"),
}


def afficher_ecran_accueil(joueur):
    """
    Affiche l'écran d'accueil de la borne d'arcade.

    Returns:
        None: Cette fonction affiche l'écran mais ne renvoie aucune valeur.
    """
    ecran = f"""
    ╔═════════════════════════════════════════════╗
    ║                                             ║
    ║        *  B O R N E   A R C A D E  *        ║
    ║                                             ║
    ║  =========================================  ║
    ║                                             ║
    ║    [ 1 ] Jeux                               ║
    ║    [ 2 ] Scores                             ║
    ║    [ 3 ] Statistiques                       ║
    ║    [ 4 ] Changer de joueur                  ║
    ║    [ 5 ] Quitter                            ║
    ║                                             ║
    ║  =========================================  ║
    ║                                             ║
    ║    Joueur : {joueur[:15]:<15}                 ║
    ║                                             ║
    ╚═════════════════════════════════════════════╝
    """
    print(ecran)


def afficher_menu_jeux():
    """Affiche la liste des jeux disponibles dans la borne."""
    ecran = """
    ╔═════════════════════════════════════════════╗
    ║                                             ║
    ║              M E N U   J E U X              ║
    ║                                             ║
    ║  =========================================  ║
    ║                                             ║
    ║    [ 1 ] Morpion                            ║
    ║    [ 2 ] Mastermind                         ║
    ║    [ 3 ] Pendu                              ║
    ║    [ 4 ] Calcul Mental                      ║
    ║    [ 5 ] Pierre Feuille Ciseaux             ║
    ║    [ 6 ] Juste Prix                         ║
    ║    [ 7 ] Retour au menu principal           ║
    ║                                             ║
    ╚═════════════════════════════════════════════╝
    """
    print(ecran)


def enregistrer_score(joueur, jeu, score):
    """Enregistre le meilleur score et les données statistiques d'une partie.

    Args:
        joueur (str): Pseudo du joueur.
        jeu (str): Nom du jeu joué.
        score (int): Score obtenu pendant la partie.

    Returns:
        None: Les tableaux de scores sont modifiés directement.
    """
    if joueur not in scores:
        scores[joueur] = {}
    if joueur not in parties_jouees:
        parties_jouees[joueur] = {}
    if joueur not in total_scores:
        total_scores[joueur] = {}
    score = score if isinstance(score, int) else 0
    if jeu not in scores[joueur]:
        scores[joueur][jeu] = score
    elif jeu == "juste prix":
        if score < scores[joueur][jeu]:
            scores[joueur][jeu] = score
    elif score > scores[joueur][jeu]:
        scores[joueur][jeu] = score

    if jeu not in parties_jouees[joueur]:
        parties_jouees[joueur][jeu] = 0
    parties_jouees[joueur][jeu] += 1
    if jeu not in total_scores[joueur]:
        total_scores[joueur][jeu] = 0
    total_scores[joueur][jeu] += score


def sauvegarder_scores():
    """Sauvegarde les scores et statistiques dans un fichier texte.

    Returns:
        None: Le fichier de scores est remplacé par l'état courant.
    """
    lignes = []
    for joueur in sorted(scores):
        for jeu in sorted(scores[joueur]):
            lignes.append("{};{};{};{};{}\n".format(
                joueur,
                jeu,
                scores[joueur][jeu],
                parties_jouees[joueur][jeu],
                total_scores[joueur][jeu],
            ))
    try:
        FICHIER_SCORES.write_text("".join(lignes), encoding="utf-8")
    except OSError:
        print("Impossible de sauvegarder les scores.")


def charger_scores():
    """Charge les scores depuis le fichier texte s'il existe.

    Returns:
        None: Les dictionnaires globaux sont remplis avec les données valides.
    """
    if not FICHIER_SCORES.exists():
        return
    try:
        lignes = FICHIER_SCORES.read_text(encoding="utf-8").splitlines()
    except OSError:
        return
    for ligne in lignes:
        morceaux = ligne.split(";")
        if len(morceaux) != 5:
            continue
        joueur, jeu, meilleur, parties, total = morceaux
        try:
            meilleur = int(meilleur)
            parties = int(parties)
            total = int(total)
        except ValueError:
            continue
        if not joueur or not jeu or parties < 1:
            continue
        if joueur not in scores:
            scores[joueur] = {}
        if joueur not in parties_jouees:
            parties_jouees[joueur] = {}
        if joueur not in total_scores:
            total_scores[joueur] = {}
        scores[joueur][jeu] = meilleur
        parties_jouees[joueur][jeu] = parties
        total_scores[joueur][jeu] = total


def afficher_scores():
    """Affiche le meilleur score de chaque joueur et de chaque jeu."""
    lignes = ["TABLEAU DES SCORES".center(45), "=" * 45]
    if not scores:
        lignes.append("Aucun score enregistré pour le moment.".center(45))
    else:
        lignes.append("{:<15} {:<25} {:>5}".format("Joueur", "Jeu", "Score"))
        lignes.append("-" * 45)
        for joueur, scores_joueur in sorted(scores.items()):
            for jeu, score in sorted(scores_joueur.items()):
                lignes.append("{:<15} {:<25} {:>5}".format(joueur[:15], jeu, score))
    print("\n".join(lignes))
    outils.saisir_texte("\nAppuyez sur Entrée pour revenir. ")


def afficher_statistiques():
    """Affiche le meilleur joueur, le nombre de parties et la moyenne des scores."""
    lignes = ["STATISTIQUES".center(45), "=" * 45]
    jeux_connus = []
    for joueur in scores:
        for jeu in scores[joueur]:
            if jeu not in jeux_connus:
                jeux_connus.append(jeu)
    jeux_connus.sort()
    if not jeux_connus:
        lignes.append("Aucune statistique pour le moment.".center(45))
    else:
        for jeu in jeux_connus:
            joueurs_jeu = []
            for joueur in scores:
                if jeu in scores[joueur]:
                    joueurs_jeu.append((joueur, scores[joueur][jeu]))

            meilleur_joueur, meilleur_score = joueurs_jeu[0]
            parties = 0
            total = 0
            for joueur, score in joueurs_jeu:
                if jeu == "juste prix":
                    if score < meilleur_score:
                        meilleur_joueur = joueur
                        meilleur_score = score
                elif score > meilleur_score:
                    meilleur_joueur = joueur
                    meilleur_score = score
                parties += parties_jouees[joueur][jeu]
                total += total_scores[joueur][jeu]
            moyenne = total / parties if parties else 0
            lignes.append("\n{}".format(jeu.upper()).center(45))
            lignes.append("  Meilleur joueur : {} ({})".format(meilleur_joueur, meilleur_score))
            lignes.append("  Parties jouées  : {}".format(parties))
            lignes.append("  Moyenne des scores : {:.2f}".format(moyenne))
    print("\n".join(lignes))
    outils.saisir_texte("\nAppuyez sur Entrée pour revenir. ")


def afficher_menu_vide(titre):
    """Affiche un écran vide conservé pour compatibilité avec l'ancien menu."""
    ecran = """
    ╔═════════════════════════════════════════════╗
    ║                                             ║
    ║            {titre:^29}    ║
    ║                                             ║
    ║  =========================================  ║
    ║                                             ║
    ║        Aucun élément pour le moment.        ║
    ║                                             ║
    ║  =========================================  ║
    ║                                             ║
    ║       Appuyez sur Entrée pour revenir.      ║
    ║                                             ║
    ╚═════════════════════════════════════════════╝
    """.format(titre=titre.center(29))
    print(ecran)
    outils.saisir_texte("")


def saisir_pseudo():
    """Demande un pseudo non vide au joueur."""
    while True:
        pseudo = outils.saisir_texte("Entrez votre pseudo : ", "Joueur")
        pseudo = pseudo.replace(";", " ").strip()
        if pseudo:
            return pseudo
        print("Le pseudo ne peut pas être vide.")


def lancer_jeu(choix, joueur):
    """Lance le jeu correspondant au choix et renvoie son score."""
    module_name, function_name, _ = JEUX[choix]
    module = __import__(f"jeux.{module_name}", fromlist=[function_name])
    fonction = getattr(module, function_name)
    if choix == 1:
        return fonction(joueur)
    return fonction()


def afficher_ecran_fin():
    """
    Affiche l'écran de fin de la borne d'arcade.

    Returns:
        None: Cette fonction affiche l'écran mais ne renvoie aucune valeur.
    """
    ecran = """
    ╔═════════════════════════════════════════════╗
    ║                                             ║
    ║              À   B I E N T Ô T              ║
    ║                                             ║
    ║  =========================================  ║
    ║                                             ║
    ║                                             ║
    ║             Merci d'avoir joué !            ║
    ║                                             ║
    ║                                             ║
    ║  =========================================  ║
    ║                                             ║
    ║          N'oubliez pas vos jetons...        ║
    ║                                             ║
    ╚═════════════════════════════════════════════╝
    """
    print(ecran)

def lancer_borne():
    """Gère la navigation dans la borne d'arcade."""
    charger_scores()
    joueur = saisir_pseudo()
    quitter = False

    while not quitter:
        outils.clear()
        afficher_ecran_accueil(joueur)
        choix = outils.saisir_entier("Votre choix (1-5) : ", 1, 5)

        if choix == 1:
            outils.clear()
            afficher_menu_jeux()
            jeu = outils.saisir_entier("Choisissez un jeu (1-7) : ", 1, 7)
            if jeu != 7:
                outils.clear()
                score = lancer_jeu(jeu, joueur)
                enregistrer_score(joueur, JEUX[jeu][2], score)
                sauvegarder_scores()
        elif choix == 2:
            outils.clear()
            afficher_scores()
        elif choix == 3:
            outils.clear()
            afficher_statistiques()
        elif choix == 4:
            outils.clear()
            joueur = saisir_pseudo()
        else:
            quitter = True

    outils.clear()
    afficher_ecran_fin()


if __name__ == "__main__":
    lancer_borne()