import random
import matplotlib.pyplot as plt

# 1. Definire date de intrare (10 candidati)
CANDIDATI = [
    {"id": "C1", "cost": 10, "scor": 85},
    {"id": "C2", "cost": 15, "scor": 90},
    {"id": "C3", "cost": 20, "scor": 60},
    {"id": "C4", "cost": 8, "scor": 40},
    {"id": "C5", "cost": 30, "scor": 95},
    {"id": "C6", "cost": 12, "scor": 70},
    {"id": "C7", "cost": 25, "scor": 80},
    {"id": "C8", "cost": 5, "scor": 30},
    {"id": "C9", "cost": 18, "scor": 75},
    {"id": "C10", "cost": 22, "scor": 88}
]
BUGET_MAX = 50


def calculeaza_fitness(cromozom):
    """Evalueaza cromozomul. Returneaza 1 daca bugetul e depasit."""
    cost_total = sum(CANDIDATI[i]["cost"] for i in range(len(cromozom)) if cromozom[i] == 1)
    scor_total = sum(CANDIDATI[i]["scor"] for i in range(len(cromozom)) if cromozom[i] == 1)
    if cost_total > BUGET_MAX:
        return 1  # Penalizare dura
    return scor_total


def genereaza_populatie(dimensiune):
    """Creeaza populatia initiala aleatorie."""
    return [[random.randint(0, 1) for _ in range(len(CANDIDATI))] for _ in range(dimensiune)]


def selectie_turneu(populatie, fitness_uri, k=3):
    """Selecteaza cel mai bun individ din k alesi la intamplare."""
    alesi = random.sample(list(zip(populatie, fitness_uri)), k)
    return max(alesi, key=lambda x: x[1])[0]


def crossover(parinte1, parinte2, probabilitate=0.8):
    """Aplica crossover intr-un punct."""
    if random.random() < probabilitate:
        punct = random.randint(1, len(parinte1) - 1)
        return parinte1[:punct] + parinte2[punct:], parinte2[:punct] + parinte1[punct:]
    return parinte1.copy(), parinte2.copy()


def mutatie(cromozom, probabilitate=0.1):
    """Aplica mutatie prin inversare de bit."""
    for i in range(len(cromozom)):
        if random.random() < probabilitate:
            cromozom[i] = 1 - cromozom[i]
    return cromozom


# Parametrii algoritmului genetic
DIM_POPULATIE = 20
GENERATII = 40
PROB_CROSSOVER = 0.85
PROB_MUTATIE = 0.15

populatie = genereaza_populatie(DIM_POPULATIE)
istoric_best_fitness = []

# Bucla de evolutie
for gen in range(GENERATII):
    fitness_uri = [calculeaza_fitness(ind) for ind in populatie]
    istoric_best_fitness.append(max(fitness_uri))

    noua_populatie = []
    while len(noua_populatie) < DIM_POPULATIE:
        p1 = selectie_turneu(populatie, fitness_uri)
        p2 = selectie_turneu(populatie, fitness_uri)

        copil1, copil2 = crossover(p1, p2, PROB_CROSSOVER)
        noua_populatie.append(mutatie(copil1, PROB_MUTATIE))
        if len(noua_populatie) < DIM_POPULATIE:
            noua_populatie.append(mutatie(copil2, PROB_MUTATIE))

    populatie = noua_populatie

# Evaluare generatie finala si afisare rezultat optim
fitness_uri_final = [calculeaza_fitness(ind) for ind in populatie]
cel_mai_bun_idx = fitness_uri_final.index(max(fitness_uri_final))
solutie_optima = populatie[cel_mai_bun_idx]

echipa_finala = [CANDIDATI[i]["id"] for i in range(len(solutie_optima)) if solutie_optima[i] == 1]
cost_final = sum(CANDIDATI[i]["cost"] for i in range(len(solutie_optima)) if solutie_optima[i] == 1)
scor_final = sum(CANDIDATI[i]["scor"] for i in range(len(solutie_optima)) if solutie_optima[i] == 1)

print("--- REZULTAT ALGORITM GENETIC ---")
print(f"Cea mai buna echipa gasita: {echipa_finala}")
print(f"Cost total: {cost_final} (Buget maxim permis: {BUGET_MAX})")
print(f"Scor total de competenta (Fitness): {scor_final}")

# 7. Graficul evolutiei fitness-ului
plt.figure(figsize=(9, 5))
plt.plot(range(GENERATII), istoric_best_fitness, marker='x', color='darkgreen', label='Cel mai bun fitness')
plt.title('Evolutia calitatii solutiilor (Fitness) de-a lungul generatiilor')
plt.xlabel('Generatie')
plt.ylabel('Scor maxim competenta (Fitness)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)

plt.savefig('proiect3_algoritm_genetic.png', dpi=300)
plt.show()
