import outils
import random
import time

opérateurs = ["+", "-", "*", "/"]


def générer_exercice():
    """
    Génère un exercice de calcul mental aléatoire et retourne
    l'expression ainsi que sa bonne réponse.

    Returns:
        tuple: (exercice, réponse_correcte)
    """
    opérateur = random.choice(opérateurs)

    if opérateur == "+":
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        return f"{a} + {b}", a + b

    if opérateur == "-":
        a = random.randint(1, 100)
        b = random.randint(0, a)
        return f"{a} - {b}", a - b

    if opérateur == "*":
        a = random.randint(1, 12)
        b = random.randint(1, 12)
        return f"{a} * {b}", a * b

    b = random.randint(1, 12)
    a = b * random.randint(1, 12)
    return f"{a} / {b}", a / b


def demander_reponse(exercice):
    """Demande une réponse numérique à l'utilisateur."""
    while True:
        try:
            return float(outils.saisir_texte(f"{exercice} = ", "0"))
        except ValueError:
            print("Réponse invalide. Entrez un nombre.")


def _jouer_calcul_mental_partie():
    """
    Lance le jeu de calcul mental.

    Returns:
        int: Score obtenu pour cette partie.
    """
    score = 0

    depart_timer = time.time()
    for i in range(10):
        exercice, réponse_correcte = générer_exercice()
        réponse_utilisateur = demander_reponse(f"Exercice {i + 1}/10 : {exercice}")

        différence = réponse_utilisateur - réponse_correcte
        if différence < 0:
            différence = -différence
        if différence < 1e-9:
            print("Correct !")
            score += 1
        else:
            print(f"Incorrect. La bonne réponse était {réponse_correcte}.")

    outils.clear()
    print(f"Votre score final est : {score}/10")
    temps_total = time.time() - depart_timer
    print(f"Temps total : {round(temps_total, 2)} secondes")

    return score


def jouer_calcul_mental():
    """Joue une ou plusieurs parties de calcul mental sans récursion.

    Returns:
        int: Total des scores obtenus pendant la session.
    """
    return outils.jouer_session(_jouer_calcul_mental_partie)

if __name__ == "__main__":
    jouer_calcul_mental()