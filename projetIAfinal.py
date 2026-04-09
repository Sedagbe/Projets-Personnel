import random
import heapq
import math

# Demande la taille de la grille à l'utilisateur
def demander_taille():
    while True:
        try:
            lignes = int(input("Entrez le nombre de lignes : "))
            colonnes = int(input("Entrez le nombre de colonnes : "))
            if lignes > 1 and colonnes > 1:
                return lignes, colonnes
            else:
                print("Veuillez entrer des nombres supérieurs à 1.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer des nombres entiers.")

# Choix de la difficulté (nombre d'obstacles)
def choisir_niveau():
    print("\nChoisissez un niveau de difficulté :")
    print("1 - Facile (10% d'obstacles)")
    print("2 - Moyen  (30% d'obstacles)")
    print("3 - Difficile (50% d'obstacles)")
    while True:
        choix = input("Votre choix (1, 2 ou 3) : ")
        if choix in ['1', '2', '3']:
            return int(choix)
        else:
            print("Entrée invalide. Veuillez choisir 1, 2 ou 3.")

# Choix de l'heuristique
def choisir_heuristique():
    print("\nChoisissez une heuristique :")
    print("1 - Manhattan  (|x2 - x1| + |y2 - y1|) :")
    print("2 - Euclidienne (sqrt((x2-x1)^2 +(y2-y1)^2)):")
    while True: 
        choix = input("Votre choix (1 ou 2) : ")
        if choix in ['1', '2']:
            return int(choix)
        else:
            print("Entrée invalide. Veuillez choisir 1 ou 2.")

# Choix du mode de définition du start et goal
def choisir_positions(rows, cols):
    print("\nChoisissez le mode pour les positions de départ et d'arrivée :")
    print("1 - Par défaut")
    print("2 - Aléatoires")
    print("3 - Choix par l'utilisateur")
    while True:
        choix = input("Votre choix (1, 2 ou 3) : ")
        if choix == '1':
            return (0, 0), (rows - 1, cols - 1)
        elif choix == '2':
            while True:
                start = (random.randint(0, rows - 1), random.randint(0, cols - 1))
                goal = (random.randint(0, rows - 1), random.randint(0, cols - 1))
                if start != goal:
                    return start, goal
        elif choix == '3':
            try:
                x1 = int(input("Ligne du Start : "))
                y1 = int(input("Colonne du Start : "))
                x2 = int(input("Ligne du Goal : "))
                y2 = int(input("Colonne du Goal : "))
                if 0 <= x1 < rows and 0 <= y1 < cols and 0 <= x2 < rows and 0 <= y2 < cols and (x1, y1) != (x2, y2):
                    return (x1, y1), (x2, y2)
                else:
                    print("Coordonnées invalides.")
            except ValueError:
                print("Veuillez entrer des entiers valides.")
        else:
            print("Choix invalide. Veuillez saisir 1, 2 ou 3.")

# Génère les obstacles aléatoires
def generer_obstacles(niveau, rows, cols, start, goal):
    ratio = {1: 0.1, 2: 0.3, 3: 0.5}
    nb_cases = rows * cols
    nb_obstacles = int(nb_cases * ratio[niveau])
    obstacles = set()
    while len(obstacles) < nb_obstacles:
        x = random.randint(0, rows - 1)
        y = random.randint(0, cols - 1)
        if (x, y) != start and (x, y) != goal:
            obstacles.add((x, y))
    return obstacles

# Classe représentant une case
class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent

    def get_g(self):
        if self.parent is None:
            return 0
        return self.parent.get_g() + 1

    def get_h(self, goal, mode):
        x1, y1 = self.position
        x2, y2 = goal
        if mode == 1:
            return abs(x1 - x2) + abs(y1 - y2)
        elif mode == 2:
            return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def get_f(self, goal, mode):
        return self.get_g() + self.get_h(goal, mode)

    def __lt__(self, other):
        return self.get_f(global_goal, heuristique_mode) < other.get_f(global_goal, heuristique_mode)

# A* prenant en compte 8 directions
def a_star(grid, start, goal, mode, rows, cols):
    open_list = []
    closed_set = set()
    start_node = Node(start)
    heapq.heappush(open_list, start_node)

    # 8 directions
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

    while open_list:
        current = heapq.heappop(open_list)
        closed_set.add(current.position)

        if current.position == goal:
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        for dx, dy in directions:
            x, y = current.position[0] + dx, current.position[1] + dy

            if 0 <= x < rows and 0 <= y < cols:
                if grid[x][y] == 1 or (x, y) in closed_set:
                    continue

                neighbor = Node((x, y), current)

                if any(n.position == neighbor.position and n.get_f(goal, mode) <= neighbor.get_f(goal, mode) for n in open_list):
                    continue

                heapq.heappush(open_list, neighbor)

    return None

# Affichage de la grille
def afficher_grille(grid, path, rows, cols, start, goal):
    print("\nGrille (S = start, G = goal, # = obstacle, * = chemin) :\n")
    for i in range(rows):
        ligne = ""
        for j in range(cols):
            if (i, j) == start:
                ligne += "S "
            elif (i, j) == goal:
                ligne += "G "
            elif grid[i][j] == 1:
                ligne += "# "
            elif path and (i, j) in path:
                ligne += "* "
            else:
                ligne += ". "
        print(ligne)
    print()

# Programme principal
def main():
    global global_goal, heuristique_mode

    rows, cols = demander_taille()
    niveau = choisir_niveau()
    heuristique_mode = choisir_heuristique()
    start, goal = choisir_positions(rows, cols)
    global_goal = goal

    obstacles = generer_obstacles(niveau, rows, cols, start, goal)
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for x, y in obstacles:
        grid[x][y] = 1

    path = a_star(grid, start, goal, heuristique_mode, rows, cols)
    afficher_grille(grid, path, rows, cols, start, goal)

    if path:
        print("Chemin trouvé ! Longueur :", len(path))
    else:
        print("Aucun chemin trouvé.")

# Lancement
if __name__ == "__main__":
    main()
