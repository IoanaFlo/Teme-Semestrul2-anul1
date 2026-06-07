import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

FISIER_PROGRAMARI = "programari.json"
ORE_DISPONIBILE = [
    "08:00", "08:30", "09:00", "09:30",
    "10:00", "10:30", "11:00", "11:30",
    "12:00", "12:30", "13:00", "13:30",
    "14:00", "14:30", "15:00", "15:30",
    "16:00"
]

SPECIALIZARI = [
    "Cardiologie",
    "Dermatologie",
    "Neurologie",
    "Pediatrie",
    "Stomatologie",
    "Oftalmologie",
    "Ortopedie",
    "Medicină generală"
]


def incarca_programari():
    """Citește programările din fișierul JSON."""
    if not os.path.exists(FISIER_PROGRAMARI):
        return []

    try:
        with open(FISIER_PROGRAMARI, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def salveaza_programari(programari):
    """Salvează programările în fișierul JSON."""
    with open(FISIER_PROGRAMARI, "w", encoding="utf-8") as f:
        json.dump(programari, f, indent=4, ensure_ascii=False)


def valideaza_data(data_text):
    """Verifică dacă data este în formatul YYYY-MM-DD."""
    try:
        datetime.strptime(data_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def verifica_disponibilitate(programari, data, ora, specializare):
    """Verifică dacă există deja o programare la aceeași dată, oră și specializare."""
    for p in programari:
        if p["data"] == data and p["ora"] == ora and p["specializare"] == specializare:
            return False
    return True


def gaseste_ora_libera(programari, data, ora_dorita, specializare):
    """
    Găsește următoarea oră liberă din aceeași zi.
    Dacă ora dorită este ocupată, caută mai departe în lista ORE_DISPONIBILE.
    """
    if ora_dorita not in ORE_DISPONIBILE:
        return None

    index_start = ORE_DISPONIBILE.index(ora_dorita)

    for ora in ORE_DISPONIBILE[index_start:]:
        if verifica_disponibilitate(programari, data, ora, specializare):
            return ora

    return None


class SchedulerMedical:
    def __init__(self, root):
        self.root = root
        self.root.title("Scheduler inteligent pentru programări medicale")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        self.programari = incarca_programari()

        self.creeaza_interfata()
        self.actualizeaza_lista()

    def creeaza_interfata(self):
        titlu = tk.Label(
            self.root,
            text="Scheduler inteligent pentru programări medicale",
            font=("Arial", 18, "bold")
        )
        titlu.pack(pady=10)

        frame_formular = tk.Frame(self.root)
        frame_formular.pack(pady=10)

        tk.Label(frame_formular, text="Nume pacient:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_nume = tk.Entry(frame_formular, width=30)
        self.entry_nume.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_formular, text="Specializare:", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.combo_specializare = ttk.Combobox(frame_formular, values=SPECIALIZARI, width=27, state="readonly")
        self.combo_specializare.grid(row=1, column=1, padx=10, pady=5)
        self.combo_specializare.set(SPECIALIZARI[0])

        tk.Label(frame_formular, text="Data (YYYY-MM-DD):", font=("Arial", 11)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_data = tk.Entry(frame_formular, width=30)
        self.entry_data.grid(row=2, column=1, padx=10, pady=5)
        self.entry_data.insert(0, datetime.now().strftime("%Y-%m-%d"))

        tk.Label(frame_formular, text="Ora dorită:", font=("Arial", 11)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.combo_ora = ttk.Combobox(frame_formular, values=ORE_DISPONIBILE, width=27, state="readonly")
        self.combo_ora.grid(row=3, column=1, padx=10, pady=5)
        self.combo_ora.set("09:00")

        frame_butoane = tk.Frame(self.root)
        frame_butoane.pack(pady=10)

        btn_adauga = tk.Button(
            frame_butoane,
            text="Adaugă programare",
            width=20,
            command=self.adauga_programare
        )
        btn_adauga.grid(row=0, column=0, padx=10)

        btn_sterge = tk.Button(
            frame_butoane,
            text="Șterge programarea selectată",
            width=25,
            command=self.sterge_programare
        )
        btn_sterge.grid(row=0, column=1, padx=10)

        btn_curata = tk.Button(
            frame_butoane,
            text="Curăță câmpurile",
            width=18,
            command=self.curata_campuri
        )
        btn_curata.grid(row=0, column=2, padx=10)

        frame_lista = tk.Frame(self.root)
        frame_lista.pack(pady=10)

        coloane = ("nume", "specializare", "data", "ora")
        self.tabel = ttk.Treeview(frame_lista, columns=coloane, show="headings", height=13)

        self.tabel.heading("nume", text="Nume pacient")
        self.tabel.heading("specializare", text="Specializare")
        self.tabel.heading("data", text="Data")
        self.tabel.heading("ora", text="Ora")

        self.tabel.column("nume", width=220)
        self.tabel.column("specializare", width=180)
        self.tabel.column("data", width=140)
        self.tabel.column("ora", width=100)

        self.tabel.pack(side="left")

        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tabel.yview)
        self.tabel.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def adauga_programare(self):
        nume = self.entry_nume.get().strip()
        specializare = self.combo_specializare.get()
        data = self.entry_data.get().strip()
        ora = self.combo_ora.get()

        if not nume:
            messagebox.showerror("Eroare", "Introduceți numele pacientului.")
            return

        if not valideaza_data(data):
            messagebox.showerror("Eroare", "Data trebuie să fie în formatul YYYY-MM-DD.")
            return

        if ora not in ORE_DISPONIBILE:
            messagebox.showerror("Eroare", "Selectați o oră validă.")
            return

        if verifica_disponibilitate(self.programari, data, ora, specializare):
            ora_finala = ora
        else:
            ora_libera = gaseste_ora_libera(self.programari, data, ora, specializare)

            if ora_libera is None:
                messagebox.showwarning(
                    "Programare imposibilă",
                    "Nu există ore libere în această zi pentru specializarea aleasă."
                )
                return

            raspuns = messagebox.askyesno(
                "Ora este ocupată",
                f"Ora {ora} este ocupată pentru {specializare}.\n"
                f"Doriți programare la următoarea oră liberă: {ora_libera}?"
            )

            if not raspuns:
                return

            ora_finala = ora_libera

        programare = {
            "nume": nume,
            "specializare": specializare,
            "data": data,
            "ora": ora_finala
        }

        self.programari.append(programare)
        self.programari.sort(key=lambda p: (p["data"], p["ora"], p["specializare"]))
        salveaza_programari(self.programari)

        self.actualizeaza_lista()
        self.curata_campuri()

        messagebox.showinfo("Succes", f"Programarea a fost adăugată la ora {ora_finala}.")

    def sterge_programare(self):
        selectie = self.tabel.selection()

        if not selectie:
            messagebox.showwarning("Atenție", "Selectați o programare din tabel.")
            return

        index = int(self.tabel.item(selectie[0], "tags")[0])

        confirmare = messagebox.askyesno(
            "Confirmare",
            "Sigur doriți să ștergeți această programare?"
        )

        if confirmare:
            self.programari.pop(index)
            salveaza_programari(self.programari)
            self.actualizeaza_lista()
            messagebox.showinfo("Succes", "Programarea a fost ștearsă.")

    def actualizeaza_lista(self):
        for rand in self.tabel.get_children():
            self.tabel.delete(rand)

        for index, p in enumerate(self.programari):
            self.tabel.insert(
                "",
                tk.END,
                values=(p["nume"], p["specializare"], p["data"], p["ora"]),
                tags=(str(index),)
            )

    def curata_campuri(self):
        self.entry_nume.delete(0, tk.END)
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.combo_specializare.set(SPECIALIZARI[0])
        self.combo_ora.set("09:00")


def main():
    root = tk.Tk()
    app = SchedulerMedical(root)
    root.mainloop()


if __name__ == "__main__":
    main()
