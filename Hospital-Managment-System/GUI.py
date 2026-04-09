import tkinter as tk
from tkinter import ttk, messagebox, Menu
import time
import os

# ------------------------------
# Patient class
# ------------------------------
class Patient:
    def __init__(self, ID, name, age, problem, entry_time):
        self.ID = ID
        self.name = name
        self.age = age
        self.problem = problem
        self.entry_time = entry_time


# ------------------------------
# File paths
# ------------------------------
PATIENT_FILE = "patients.txt"
REMOVED_FILE = "removed_patients.txt"


# ------------------------------
# Helper functions
# ------------------------------
def get_time():
    return time.strftime("[%d-%m-%Y %H:%M:%S]")


def save_all_patients(patients):
    with open(PATIENT_FILE, "w") as f:
        for p in patients:
            f.write(f"{p.ID},{p.name},{p.age},{p.problem},{p.entry_time}\n")


def load_patients():
    patients = []
    if not os.path.exists(PATIENT_FILE):
        open(PATIENT_FILE, "w").close()

    with open(PATIENT_FILE, "r") as f:
        for line in f:
            data = line.strip().split(",")
            if len(data) == 5:
                patients.append(Patient(*data))
    return patients


def log_removed_patient(p):
    removed_time = get_time()
    with open(REMOVED_FILE, "a") as f:
        f.write(f"Removed: ID={p.ID} Name={p.name} Age={p.age} Problem={p.problem} Entry={p.entry_time} Removed={removed_time}\n")


# ------------------------------
# Main Application Class
# ------------------------------
class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏥 Hospital Management System")
        self.root.geometry("800x480")
        self.root.resizable(False, False)
        self.patients = load_patients()
        self.dark_mode = False

        self.style = ttk.Style()
        self.set_theme()

        self.setup_menu()
        self.setup_widgets()
        self.load_patients_to_tree()

    # --------------------------
    # Theme handling
    # --------------------------
    def set_theme(self):
        if self.dark_mode:
            bg_color = "#2e2e2e"
            fg_color = "#eeeeee"
            entry_bg = "#3c3f41"
            self.style.theme_use('clam')
            self.style.configure('.', background=bg_color, foreground=fg_color, fieldbackground=entry_bg)
            self.style.map('Treeview', background=[('selected', '#6a9fb5')])
            self.root.configure(bg=bg_color)
        else:
            bg_color = "#f0f0f0"
            fg_color = "#000000"
            entry_bg = "#ffffff"
            self.style.theme_use('clam')
            self.style.configure('.', background=bg_color, foreground=fg_color, fieldbackground=entry_bg)
            self.style.map('Treeview', background=[('selected', '#3399ff')])
            self.root.configure(bg=bg_color)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.set_theme()

    # --------------------------
    # Menu setup
    # --------------------------
    def setup_menu(self):
        menubar = Menu(self.root)

        # File Menu
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open patient data", command=lambda: os.startfile(PATIENT_FILE))
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # Help Menu
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=lambda: messagebox.showinfo(
            "About", "Hospital Management System\nCreated by Salaar Editor"))
        helpmenu.add_command(label="Contact", command=lambda: messagebox.showinfo(
            "Contact", "Created by Salaar\nContact: 03284081665"))
        menubar.add_cascade(label="Help", menu=helpmenu)

        # Theme Menu
        thememenu = Menu(menubar, tearoff=0)
        thememenu.add_command(label="Toggle Light/Dark Theme", command=self.toggle_theme)
        menubar.add_cascade(label="Theme", menu=thememenu)

        self.root.config(menu=menubar)

    # --------------------------
    # Widgets
    # --------------------------
    def setup_widgets(self):
        input_frame = ttk.LabelFrame(self.root, text="Add Patient")
        input_frame.pack(fill="x", padx=15, pady=10)

        labels = ["Patient ID:", "Name:", "Age:", "Problem:"]
        for i, text in enumerate(labels):
            ttk.Label(input_frame, text=text).grid(row=i, column=0, sticky="w", padx=5, pady=5)

        self.entry_id = ttk.Entry(input_frame, width=20)
        self.entry_id.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.entry_name = ttk.Entry(input_frame, width=35)
        self.entry_name.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.entry_age = ttk.Entry(input_frame, width=20)
        self.entry_age.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        self.entry_problem = ttk.Entry(input_frame, width=35)
        self.entry_problem.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        # Buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=4, column=1, sticky="e", pady=10, padx=5)

        ttk.Button(btn_frame, text="Add Patient", command=self.add_patient).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_inputs).pack(side="left", padx=5)

        # Patient List
        columns = ("ID", "Name", "Age", "Problem", "Entry Time")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings', selectmode="browse")
        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

        for col in columns:
            self.tree.heading(col, text=col)
            if col in ("Problem", "Name"):
                self.tree.column(col, width=150, anchor='center')
            elif col == "Entry Time":
                self.tree.column(col, width=180, anchor='center')
            else:
                self.tree.column(col, width=90, anchor='center')

        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        # Remove button
        ttk.Button(self.root, text="Remove Selected Patient", command=self.remove_patient).pack(pady=(0, 15))

        # Status Bar
        self.status = ttk.Label(self.root, text="Welcome! Ready to manage patients.", relief=tk.SUNKEN, anchor="w")
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Bindings
        self.root.bind('<Return>', lambda event: self.add_patient())
        self.tree.bind("<Double-1>", self.show_patient_details)

    # --------------------------
    # Core functionality
    # --------------------------
    def clear_inputs(self):
        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_age.delete(0, tk.END)
        self.entry_problem.delete(0, tk.END)
        self.status['text'] = "Input fields cleared."

    def add_patient(self):
        ID = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        age = self.entry_age.get().strip()
        problem = self.entry_problem.get().strip()

        errors = []
        if not ID:
            errors.append("Patient ID is required.")
        if not name:
            errors.append("Name is required.")
        if not age or not age.isdigit() or int(age) <= 0:
            errors.append("Valid positive Age is required.")
        if not problem:
            errors.append("Problem description is required.")
        if any(p.ID == ID for p in self.patients):
            errors.append("Patient ID must be unique.")

        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            self.status['text'] = "Error: Invalid input!"
            return

        entry_time = get_time()
        new_patient = Patient(ID, name, age, problem, entry_time)
        self.patients.append(new_patient)
        save_all_patients(self.patients)
        self.tree.insert("", tk.END, values=(ID, name, age, problem, entry_time))

        self.clear_inputs()
        self.status['text'] = f"Patient ID {ID} added successfully."

    def load_patients_to_tree(self):
        for p in self.patients:
            self.tree.insert("", tk.END, values=(p.ID, p.name, p.age, p.problem, p.entry_time))

    def remove_patient(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a patient to remove.")
            return

        confirm = messagebox.askyesno("Confirm Remove", "Are you sure you want to remove the selected patient?")
        if not confirm:
            self.status['text'] = "Patient removal canceled."
            return

        item = selected_item[0]
        values = self.tree.item(item, "values")
        ID = values[0]

        for i, p in enumerate(self.patients):
            if p.ID == ID:
                log_removed_patient(p)
                del self.patients[i]
                break

        save_all_patients(self.patients)
        self.tree.delete(item)
        self.status['text'] = f"Patient ID {ID} removed."

    def show_patient_details(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item = selected_item[0]
        values = self.tree.item(item, "values")

        info = (f"Patient Details:\n\n"
                f"ID: {values[0]}\n"
                f"Name: {values[1]}\n"
                f"Age: {values[2]}\n"
                f"Problem: {values[3]}\n"
                f"Entry Time: {values[4]}\n")

        messagebox.showinfo("Patient Details", info)


# ------------------------------
# Run Application
# ------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalApp(root)
    root.mainloop()
