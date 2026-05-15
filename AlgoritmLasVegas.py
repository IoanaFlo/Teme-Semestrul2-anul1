import random
import matplotlib.pyplot as plt



def genereaza_date(dimensiune):
    """Creeaza un vector cu elemente distincte si alege o valoare tinta."""
    vector = list(range(100, 100 + dimensiune))
    tinta = random.choice(vector)
    return vector, tinta


def cautare_las_vegas(vector, tinta):
    """Parcurge indicii intr-o ordine aleatoare pana gaseste tinta."""
    indici = list(range(len(vector)))
    random.shuffle(indici)

    pasi = 0
    for idx in indici:
        pasi += 1
        if vector[idx] == tinta:
            return idx, pasi
    return -1, pasi


# 1. Rulari multiple (30 de ori) pentru același input
n_test = 1000
vector_stabil, tinta_stabila = genereaza_date(n_test)
istoric_pasi = []

for _ in range(30):
    _, p = cautare_las_vegas(vector_stabil, tinta_stabila)
    istoric_pasi.append(p)

p_min, p_max, p_med = min(istoric_pasi), max(istoric_pasi), sum(istoric_pasi) / 30
print(f"--- Statistica 30 rulari (N={n_test}) ---")
print(f"Minim pasi: {p_min} | Maxim pasi: {p_max} | Medie pasi: {p_med:.2f}\n")

# 2. Experimente pentru dimensiuni diferite
dimensiuni = [100, 500, 1000, 5000]
medii_dimensiuni = []

print("--- Influenta dimensiunii vectorului ---")
for d in dimensiuni:
    v, t = genereaza_date(d)
    pasi_d = [cautare_las_vegas(v, t)[1] for _ in range(50)]
    medie_d = sum(pasi_d) / len(pasi_d)
    medii_dimensiuni.append(medie_d)
    print(f"Dimensiune: {d:4} | Medie pasi (50 rulari): {medie_d:.2f}")

# 3. Construire rapoarte grafice
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Grafic 1: Fluctuatia pasilor in cele 30 de rulari
ax1.plot(range(1, 31), istoric_pasi, marker='o', color='purple', linestyle='-')
ax1.axhline(y=p_med, color='red', linestyle='--', label=f'Medie ({p_med:.1f})')
ax1.set_title('Variabilitatea pasilor pentru acelasi input')
ax1.set_xlabel('Numar rulare')
ax1.set_ylabel('Pasi efectuati')
ax1.legend()
ax1.grid(True)

# Grafic 2: Cresterea complexitatii cu dimensiunea n
ax2.bar([str(d) for d in dimensiuni], medii_dimensiuni, color='teal', alpha=0.8)
ax2.set_title('Media pasilor in functie de dimensiune')
ax2.set_xlabel('Dimensiune vector (n)')
ax2.set_ylabel('Numar mediu de pasi')
ax2.grid(True, axis='y', linestyle=':')

plt.tight_layout()
plt.savefig('proiect2_las_vegas.png', dpi=300)
plt.show()
