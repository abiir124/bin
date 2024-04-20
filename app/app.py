from flask import Flask, render_template, jsonify, request
import random
from typing import List
import numpy as np
import os
import json
import sqlite3
import subprocess
import matplotlib.pyplot as plt
from flask import send_from_directory

app = Flask(__name__)



# Chemin relatif vers le dossier SQLite
db_folder = 'app/SQLite'

# Construire le chemin complet vers le fichier mydb.db
db_path = os.path.join('C:\\Users\\bouha\\OneDrive\\Bureau\\bin-projet-main', db_folder, 'mydb.db')

# Fonction pour ouvrir la base de données
def ouvrir_base_de_donnees():
    try:
        # Établir une connexion à la base de données
        conn = sqlite3.connect(db_path)
        print("Base de données ouverte avec succès !")
        return conn
    except sqlite3.Error as e:
        print(f"Erreur lors de l'ouverture de la base de données : {e}")
        return None
    
    

def best_fit_heuristic(objets, capacite_bin):
    # Tri des objets par ordre décroissant de taille
    objets_tries = sorted(objets, reverse=True)

    if not objets_tries:
        return []

    # Initialisation des bins avec le premier objet
    bins = [[objets_tries[0]]]

    # Placement des objets restants
    for objet in objets_tries[1:]:
        bin_trouve = False

        # Parcours des bins existants pour trouver le meilleur fit
        for bin in bins:
            if sum(bin) + objet <= capacite_bin:
                bin.append(objet)
                bin_trouve = True
                break

        # Création d'un nouveau bin si aucun fit n'est trouvé
        if not bin_trouve:
            bins.append([objet])

    return bins

def initialiser_population(taille_population, objets, capacite_bin):
    population = []

    for _ in range(taille_population):
        individu = best_fit_heuristic(objets, capacite_bin)
        population.append(individu)

    return population


def fitness(individu, capacite_bin):
    nombre_boites_utilisees = len([bac for bac in individu if bac])  # Nombre de bacs non vides
    return 1 / (1 + nombre_boites_utilisees)

def selection_par_roulette(population, fitness_values):
    probabilites = np.array(fitness_values) / sum(fitness_values)
    indice_selectionne = np.random.choice(range(len(population)), p=probabilites)
    return population[indice_selectionne]


def croisement(parent1, parent2):
    if len(parent1) > 1:
        point_crossover = random.randint(1, len(parent1) - 1)
        enfant = parent1[:point_crossover] + [objet for objet in parent2 if objet not in parent1[:point_crossover]]
        return enfant
    else:
        return parent1  # Si la longueur est inférieure à 2, on ne peut pas effectuer le croisement


def mutation(individu, taux_mutation):
    for i in range(len(individu)):
        if random.random() < taux_mutation:
            j = random.randint(0, len(individu) - 1)
            individu[i], individu[j] = individu[j], individu[i]
    return individu


def algorithme_genetique(objets, capacite_bin, taille_population, taux_mutation, nombre_generations):
    population = initialiser_population(taille_population, objets, capacite_bin)

    meilleure_solution = None
    nombre_boites_utilisees = 0

    for generation in range(nombre_generations):
        fitness_values = [fitness(individu, capacite_bin) for individu in population]

        nouvelle_population = []
        for _ in range(taille_population // 2):
            parent1 = selection_par_roulette(population, fitness_values)
            parent2 = selection_par_roulette(population, fitness_values)

            enfant1 = croisement(parent1, parent2)
            enfant2 = croisement(parent2, parent1)

            enfant1 = mutation(enfant1, taux_mutation)
            enfant2 = mutation(enfant2, taux_mutation)

            nouvelle_population.extend([enfant1, enfant2])

        population = nouvelle_population

        if population:
            meilleure_solution = max(population, key=lambda individu: fitness(individu, capacite_bin))
            nombre_boites_utilisees = 1 / fitness(meilleure_solution, capacite_bin) - 1
            # Faites quelque chose avec la meilleure solution et le nombre de boîtes utilisées
        else:
            # Gérez le cas où la population est vide
            print("La population est vide.")

    return meilleure_solution, nombre_boites_utilisees






def initialiser_loups(nombre_loups, dimension, capacite_maximale):
     return np.random.randint(0, capacite_maximale + 1, (nombre_loups, dimension))


def generate_initial_solution(items, bin_capacity):
    solution = [[]]
    for item in items:
        # Sélectionne un bac aléatoire
        selected_bin = random.choice(solution)
        # Vérifie si l'ajout de l'objet respecte la capacité du bac
        if sum(selected_bin) + item <= bin_capacity:
            selected_bin.append(item)
        else:
            # Si la capacité du bac est dépassée, crée un nouveau bac
            solution.append([item])
    return solution

# Fonction pour évaluer une solution en comptant le nombre de bacs utilisés
def evaluate_solution(solution):
    return len(solution)

def Algo_fourmis(items, bin_capacity, num_ants):
    best_solution = None
    best_solution_bins = float('inf')  # Initialisation avec une valeur infinie
    for _ in range(num_ants):
        # Génère une solution initiale
        solution = generate_initial_solution(items, bin_capacity)
        # Évalue la solution
        bins_used = evaluate_solution(solution)
        # Met à jour la meilleure solution trouvée jusqu'à présent
        if bins_used < best_solution_bins:
            best_solution = solution
            best_solution_bins = bins_used

# Affiche la meilleure solution trouvée
#print("Meilleure solution trouvée:")
#for bin_index, bin_items in enumerate(best_solution):
    #print(f"Bac {bin_index + 1}: {bin_items}")

    return best_solution,best_solution_bins


    # Votre route principale
# Votre route principale
@app.route('/')
def home():
    # Ajoutez cette ligne pour exécuter votre script python.py
    subprocess.Popen(["python", "python.py"], cwd=r"C:\\Users\\bouha\\OneDrive\\Bureau\\bin-projet-main\app\SQLite")

    return render_template('accueil.html')

@app.route('/index.html')
def index():
    # Ajoutez ici le code pour préparer les données nécessaires à la page index.html
    return render_template('index.html')
    
# Route pour ouvrir la base de données
@app.route('/ouvrir-base-de-donnees')
def ouvrir_base_route():
    conn = ouvrir_base_de_donnees()  # Appel de la fonction qui ouvre la base de données
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM benchmarks")
            data_benchmarks = cursor.fetchall()

            cursor.execute("SELECT * FROM benchmarks_perso")
            data_benchmarks_perso = cursor.fetchall()

            conn.close()

            # Ajoutez des instructions d'impression pour afficher les données extraites
            print("Données extraites de la base de données (benchmarks) :", data_benchmarks)
            print("Données extraites de la base de données (benchmarks_perso) :", data_benchmarks_perso)
            
            return render_template('afficher_benchmarks.html', benchmarks=data_benchmarks, benchmarks_perso=data_benchmarks_perso)
        except Exception as e:
            return f"Erreur lors de la récupération des données : {e}"
    else:
        return "Erreur lors de l'ouverture de la base de données."
    
    # Route pour lancer l'algorithme

@app.route('/run-algorithm/<algorithme>', methods=['POST'])  # Utiliser POST au lieu de GET
def run_algorithm(algorithme):
    # Récupérer les paramètres depuis la requête
    try:
      data = request.get_json()  # Obtenir les données depuis le corps de la requête
      print(f'Données reçues du client : {data}')

      capacite_bin = int(data.get('capaciteBin', 0))
      dimensions_objets = data.get('dimensionsObjets', [])
      print(f'Données reçues du client : {capacite_bin,dimensions_objets}')
      

      if algorithme == 'genetique':
        # Ajouter les paramètres spécifiques à l'algorithme génétique
        taille_population = int(data.get('parametres', {}).get('taillePopulation', 0))
        nbr_generations = int(data.get('parametres', {}).get('nbrGenerations', 0))
        taux_mutation = float(data.get('parametres', {}).get('tauxMutation', 0.0))


        parametres = {
            'capacite_bin': capacite_bin,
            'dimensions_objets': dimensions_objets,
            'taille_population': taille_population,
            'nbr_generations': nbr_generations,
            'taux_mutation': taux_mutation
                    }

        print(f'Parametres de l algo : {parametres}')
        # Appeler l'algorithme génétique avec les paramètres
        meilleure_solution_genetique, nombre_boites_utilisees_genetique = algorithme_genetique(dimensions_objets, capacite_bin, parametres['taille_population'], parametres['taux_mutation'], parametres['nbr_generations'])
        print("Résultats de l'algorithme :", meilleure_solution_genetique, nombre_boites_utilisees_genetique)
        try:
          return jsonify({"solution": meilleure_solution_genetique, "nombre_boites_utilisees": nombre_boites_utilisees_genetique})
        except Exception as e:
          print("Erreur lors de la conversion en JSON : {e}")
          return jsonify({"erreur": "Erreur lors de la conversion en JSON"}), 500

      elif algorithme == 'Algo_Fourmis':
        # Ajouter les paramètres spécifiques à l'algorithme des loups gris
        nombre_Fourmis = int(data.get('parametres', {}).get('nombre_Fourmis', 0))

        parametres = {
        'capacite_bin': capacite_bin,
        'dimensions_objets': dimensions_objets,
        'nombre_Fourmis': nombre_Fourmis,
                    }

        print(f'Parametres de l algo : {parametres}')
        # Appeler l'algorithme des loups gris avec les paramètres
        meilleure_solution_fourmis, nombre_boites_utilisees_fourmis = Algo_fourmis(dimensions_objets, capacite_bin, parametres['nombre_Fourmis'])
        print("Résultats de l'algorithme :", meilleure_solution_fourmis, nombre_boites_utilisees_fourmis)
        try:
          return jsonify({"solution": meilleure_solution_fourmis, "nombre_boites_utilisees": nombre_boites_utilisees_fourmis})
        except Exception as e:
          print("Erreur lors de la conversion en JSON : {e}")
          return jsonify({"erreur": "Erreur lors de la conversion en JSON"}), 500

      else:
        # Gérer le cas où un algorithme non pris en charge est sélectionné
        return jsonify({"erreur": "Algorithme non pris en charge"}), 400

    except Exception as e:
        print(f'Erreur dans la fonction run_algorithm : {e}')
        return jsonify({"erreur": "Une erreur est survenue lors de l'exécution de l'algorithme"}), 500

@app.route('/generer_graphe')
def generer_graphe():
    objets_range = range(1, 100)
    taille_population = 10
    taux_mutation = 0.1
    nombre_generations = 100
    nombre_fourmis = 5
    bin_capacity=10 
    bins_used_genetic = []
    bins_used_ant_colony = []

    for n_objets in objets_range:
        objets = [random.randint(1, 10) for _ in range(n_objets)]
        _, bins_genetic = algorithme_genetique(objets, bin_capacity, taille_population, taux_mutation, nombre_generations)
        _, bins_ant_colony = Algo_fourmis(objets, bin_capacity, nombre_fourmis)
        bins_used_genetic.append(bins_genetic)
        bins_used_ant_colony.append(bins_ant_colony)

    plt.plot(objets_range, bins_used_genetic, label='Algorithme génétique')
    plt.plot(objets_range, bins_used_ant_colony, label='Algorithme des fourmis', linestyle='--')
    plt.xlabel('Nombre d\'objets')
    plt.ylabel('Nombre de bacs utilisés')
    plt.title('Nombre de bacs utilisés en fonction du nombre d\'objets')
    plt.legend()
    plt.savefig('static/graph.png')  # Sauvegarde du graphe en tant qu'image PNG
    plt.close()
    return 'Graphe généré et sauvegardé avec succès !'

@app.route('/graph_image')
def graph_image():
    return send_from_directory('static', 'graph.png')  # Renvoie l'image sauvegardée@app.route('/enregistrer-donnees', methods=['POST'])
@app.route('/enregistrer-donnees', methods=['POST'])
def enregistrer_donnees():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nombre_objets = request.form['nbr_objets']
        capacite_bins = request.form['capacite-bin']
        taille_objets = request.form['dimensions']

        try:
    
            print("Données à enregistrer :", nombre_objets, capacite_bins, taille_objets)  # Ajout de l'instruction print
            # Établir une connexion à la base de données

            conn = ouvrir_base_de_donnees()  # Appel de la fonction qui ouvre la base de données
            cur = conn.cursor()

            # Insérer les données dans la table benchmarks
            cur.execute("INSERT INTO benchmarks_perso (nombre_objets, capacite_bins, taille_objets) VALUES (?, ?, ?)",
                        (nombre_objets, capacite_bins, taille_objets))

            # Valider la transaction et fermer la connexion
            conn.commit()
            print("Benchmark modifié avec succès !")
            conn.close()
            return jsonify({'message': 'Benchmark modifié avec succès'})
        except Exception as e:
            # En cas d'erreur lors de l'enregistrement des données
            print(f"Erreur lors de l'enregistrement des données : {e}")
            return "Une erreur s'est produite lors de l'enregistrement des données."

    # Gérer le cas où la méthode de requête n'est pas POST
    return "Méthode de requête non autorisée."


@app.route('/modifier-benchmark', methods=['POST'])
def modifier_benchmark():
    # Récupérer les données envoyées par la requête AJAX
    data = request.json

    # Extraire les valeurs nécessaires des données
    id_benchmark = data.get('id')
    nombre_objets = data.get('nombreObjets')
    capacite_bin = data.get('capaciteBin')
    dimensions_objets = data.get('dimensionsObjets')
    
    print("les données récupérés sont:",id_benchmark,nombre_objets,capacite_bin,dimensions_objets)
    conn = ouvrir_base_de_donnees()  # Appel de la fonction qui ouvre la base de données
    cur = conn.cursor()
    if conn: 
     try:
    
        # Requête pour mettre à jour le benchmark avec l'ID spécifié
        cur.execute("UPDATE benchmarks SET nombre_objets = ?, capacite_bins = ?, taille_objets = ? WHERE ID = ?",
                    (nombre_objets, capacite_bin, dimensions_objets, id_benchmark))
        
        # Valider la transaction
        conn.commit()
        print("Benchmark modifié avec succès !")
        conn.close()
        return jsonify({'message': 'Benchmark modifié avec succès'})
     except sqlite3.Error as e:
        print(f"Erreur lors de la modification du benchmark : {e}")
        return jsonify({'message': ' Erreur lors de la modification du Benchmark '})
    else:
        return "Erreur lors de l'ouverture de la base de données."


if __name__ == '__main__':

    app.run(debug=True)

  
  



