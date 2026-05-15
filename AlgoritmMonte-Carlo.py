import random
import matplotlib.pyplot as plt

# O singură rundă a jocului
def arunca_zaruri():
    """Simuleaza o singura runda: returneaza True daca suma este 7 sau 11."""
    zar1 = random.randint(1, 6)
    zar2 = random.randint(1, 6)
    return (zar1 + zar2) in (7, 11)

def simuleaza_monte_carlo(N):
    """Ruleaza experimentul de N ori si returneaza probabilitatea estimata."""
    castiguri = sum(1 for _ in range(N) if arunca_zaruri())
    return castiguri / N

# 1. Experimente pentru valori diferite ale lui N
valori_N = [100, 1000, 10000, 100000]
print("--- Estimari unice pentru N diferit ---")
for n in valori_N:
    p_estimat = simuleaza_monte_carlo(n)
    print(f"N = {n:7} | Probabilitate estimata: {p_estimat:.5f}")

# 2. Experimente repetate pentru a demonstra scaderea variatiei
print("\n--- Rulari repetate (Stabilitate) ---")
for n in [100, 10000]:
    rulari = [simuleaza_monte_carlo(n) for _ in range(5)]
    print(f"N = {n:5} | 5 rulari succesive: " + ", ".join(f"{r:.4f}" for r in rulari))

# 3. Generare date pentru raportul grafic
istoric_N = list(range(100, 5001, 100))
rulare_1 = [simuleaza_monte_carlo(n) for n in istoric_N]
rulare_2 = [simuleaza_monte_carlo(n) for n in istoric_N]

# Construire grafic
plt.figure(figsize=(10, 5))
plt.plot(istoric_N, rulare_1, label='Rularea 1', color='blue', alpha=0.7)
plt.plot(istoric_N, rulare_2, label='Rularea 2', color='orange', alpha=0.7)
plt.axhline(y=8/36, color='red', linestyle='--', label='Valoarea teoretica (0.2222)')

plt.title('Convergenta simularii Monte Carlo in functie de N')
plt.xlabel('Numar de simulari (N)')
plt.ylabel('Probabilitate estimata')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)

# Salvare grafic
plt.savefig('proiect1_monte_carlo.png', dpi=300)
plt.show()
