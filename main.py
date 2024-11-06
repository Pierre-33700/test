import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('personnes.db')
cursor = conn.cursor()

# Création de la table si elle n'existe pas déjà
cursor.execute('''CREATE TABLE IF NOT EXISTS personnes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    age INTEGER NOT NULL)''')
conn.commit()

# Fonction pour ajouter une personne dans la base de données
def ajouter_personne():
    nom = entry_nom.get()
    prenom = entry_prenom.get()
    age = entry_age.get()
    
    if not (nom and prenom and age.isdigit()):
        messagebox.showerror("Erreur", "Veuillez entrer des informations valides")
        return
    
    cursor.execute("INSERT INTO personnes (nom, prenom, age) VALUES (?, ?, ?)", (nom, prenom, int(age)))
    conn.commit()
    messagebox.showinfo("Succès", "Personne ajoutée avec succès")
    entry_nom.delete(0, tk.END)
    entry_prenom.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    afficher_personnes()  # Rafraîchit la liste après ajout

# Fonction pour afficher toutes les personnes dans la base de données
def afficher_personnes():
    # Effacer les anciennes données affichées dans le Treeview
    for row in tree.get_children():
        tree.delete(row)
    
    cursor.execute("SELECT * FROM personnes")
    rows = cursor.fetchall()
    
    # Insérer les données dans le Treeview
    for row in rows:
        tree.insert("", tk.END, values=row)

# Fonction pour supprimer la personne sélectionnée
def supprimer_personne():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner une personne à supprimer")
        return
    
    # Récupérer l'ID de la personne sélectionnée
    item = tree.item(selected_item)
    person_id = item['values'][0]
    
    # Demander confirmation
    reponse = messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette personne ?")
    if reponse:
        cursor.execute("DELETE FROM personnes WHERE id = ?", (person_id,))
        conn.commit()
        afficher_personnes()  # Rafraîchit la liste après suppression
        messagebox.showinfo("Succès", "Personne supprimée avec succès")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Formulaire d'ajout, visualisation et suppression de personnes")

# Création des widgets pour ajouter une personne
label_nom = tk.Label(root, text="Nom")
label_nom.grid(row=0, column=0, padx=10, pady=10)
entry_nom = tk.Entry(root)
entry_nom.grid(row=0, column=1, padx=10, pady=10)

label_prenom = tk.Label(root, text="Prénom")
label_prenom.grid(row=1, column=0, padx=10, pady=10)
entry_prenom = tk.Entry(root)
entry_prenom.grid(row=1, column=1, padx=10, pady=10)

label_age = tk.Label(root, text="Âge")
label_age.grid(row=2, column=0, padx=10, pady=10)
entry_age = tk.Entry(root)
entry_age.grid(row=2, column=1, padx=10, pady=10)

btn_ajouter = tk.Button(root, text="Ajouter", command=ajouter_personne)
btn_ajouter.grid(row=3, column=0, columnspan=2, pady=10)

# Création d'un Treeview pour afficher les données
tree = ttk.Treeview(root, columns=("ID", "Nom", "Prénom", "Âge"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nom", text="Nom")
tree.heading("Prénom", text="Prénom")
tree.heading("Âge", text="Âge")
tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Bouton pour afficher les personnes
btn_afficher = tk.Button(root, text="Afficher les personnes", command=afficher_personnes)
btn_afficher.grid(row=5, column=0, columnspan=2, pady=5)

# Bouton pour supprimer la personne sélectionnée
btn_supprimer = tk.Button(root, text="Supprimer la personne sélectionnée", command=supprimer_personne)
btn_supprimer.grid(row=6, column=0, columnspan=2, pady=10)

# Boucle principale de l'application
root.mainloop()

# Fermeture de la connexion à la base de données
conn.close()
