import random
import outils


def _jouer_juste_prix_partie(minimum, maximum, max_essais):
    nombre_secret = random.randint(minimum, maximum)
    nombre_essais = 0
    score_partie = 0

    print("Bienvenue dans le Juste Prix !")
    print("Devinez le nombre secret entre {} et {}.".format(minimum, maximum))

    while nombre_essais < max_essais:
        reponse = outils.saisir_entier("Votre proposition : ", minimum, maximum)
        nombre_essais += 1

        if reponse < nombre_secret:
            print("C'est plus !")
        elif reponse > nombre_secret:
            print("C'est moins !")
        else:
            score_partie = nombre_essais
            print(f"Bravo ! Vous avez trouvé le nombre secret en {nombre_essais} essai(s).")
            break

    if nombre_essais >= max_essais and reponse != nombre_secret:
        print(f"Dommage ! Le nombre secret était {nombre_secret}.")
        score_partie = nombre_essais

    print(f"Score final du juste prix : {score_partie}")
    return score_partie


def jouer_juste_prix():
    """Lance une partie du Juste Prix avec des paramètres fixes."""
    return outils.jouer_session(_jouer_juste_prix_partie, 1, 100, 8)


if __name__ == "__main__":
    jouer_juste_prix()