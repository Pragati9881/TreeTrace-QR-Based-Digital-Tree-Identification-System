import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import sqlite3
import os
import shutil
import qrcode


# =========================
# SETTINGS
# =========================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

DARK_GREEN = "#245C3A"
LIGHT_GREEN = "#F3F7F3"
WHITE = "#FFFFFF"
TEXT = "#26332B"
GRAY = "#6B756E"
BORDER = "#D8E2DA"

IMAGE_FOLDER = os.path.join("static", "images")

# IMPORTANT:
# QR codes are stored inside Flask static folder
QR_FOLDER = os.path.join("static", "qr")

FLASK_URL = "http://10.216.12.213:5000"



# =========================
# YOUTUBE VIDEO LINKS
# =========================

YOUTUBE_LINKS = {
    "Neem": "https://youtu.be/DsoPxPqmCQg?si=NMgupa17FEBeC_n4",
    "Amla": "https://youtu.be/HPLJyKCJWUg?si=K-7HtBijMWZaLQFA",
    "Ashoka": "https://youtu.be/TMv7sre4JWo?si=FYBz_6sxZQxoHlLZ",
}

# Separate folder for YouTube QR codes
YOUTUBE_QR_FOLDER = os.path.join(
    "static",
    "youtube_qr_codes"
)

os.makedirs(YOUTUBE_QR_FOLDER, exist_ok=True)


os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)


# =========================
# DATABASE
# =========================

def get_connection():

    conn = sqlite3.connect("treetrace.db")
    conn.row_factory = sqlite3.Row

    return conn


# =========================
# TREE ID
# =========================

def get_next_tree_id():

    conn = get_connection()

    rows = conn.execute(
        "SELECT tree_id FROM trees"
    ).fetchall()

    conn.close()

    existing_numbers = set()

    for row in rows:

        tree_id = row["tree_id"]

        if tree_id.startswith("T"):

            try:

                number = int(tree_id[1:])

                existing_numbers.add(number)

            except ValueError:

                pass

    # Find first available Tree ID

    new_number = 1

    while new_number in existing_numbers:

        new_number += 1

    return f"T{new_number:03d}"


# =========================
# GENERATE QR
# =========================

def generate_qr(tree_id):

    url = f"{FLASK_URL}/?tree_id={tree_id}"

    qr = qrcode.make(url)

    qr_path = os.path.join(
        QR_FOLDER,
        f"{tree_id}.png"
    )

    qr.save(qr_path)

    return qr_path




# =========================
# GENERATE YOUTUBE QR
# =========================

def generate_youtube_qr(tree_name):

    video_url = YOUTUBE_LINKS.get(tree_name)

    if not video_url:
        messagebox.showwarning(
            "Video Not Found",
            f"No YouTube link added for {tree_name}."
        )
        return None

    qr = qrcode.make(video_url)

    safe_name = (
        tree_name.strip()
        .replace(" ", "_")
    )

    qr_path = os.path.join(
        YOUTUBE_QR_FOLDER,
        f"{safe_name}_YouTube.png"
    )

    qr.save(qr_path)

    return qr_path


# =========================
# LOGIN
# =========================

def login_window():

    login = tk.Tk()

    login.title("TreeTrace - Admin Login")
    login.geometry("900x600")
    login.resizable(False, False)
    login.configure(bg=WHITE)

    # LEFT PANEL

    left_frame = tk.Frame(
        login,
        bg=DARK_GREEN,
        width=450,
        height=600
    )

    left_frame.pack(
        side="left",
        fill="both"
    )

    left_frame.pack_propagate(False)

    tk.Label(
        left_frame,
        text="🌳",
        font=("Arial", 55),
        bg=DARK_GREEN,
        fg=WHITE
    ).pack(pady=(120, 10))

    tk.Label(
        left_frame,
        text="TreeTrace",
        font=("Arial", 32, "bold"),
        bg=DARK_GREEN,
        fg=WHITE
    ).pack()

    tk.Label(
        left_frame,
        text="Digital Tree Identification System",
        font=("Arial", 13),
        bg=DARK_GREEN,
        fg=WHITE
    ).pack(pady=10)

    tk.Label(
        left_frame,
        text="Admin Panel",
        font=("Arial", 12),
        bg=DARK_GREEN,
        fg="#DDE9E1"
    ).pack(pady=20)

    # RIGHT PANEL

    right_frame = tk.Frame(
        login,
        bg=WHITE,
        width=450,
        height=600
    )

    right_frame.pack(
        side="right",
        fill="both"
    )

    right_frame.pack_propagate(False)

    tk.Label(
        right_frame,
        text="Admin Login",
        font=("Arial", 25, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(pady=(100, 35))

    tk.Label(
        right_frame,
        text="Username",
        font=("Arial", 11),
        bg=WHITE,
        fg=TEXT
    ).pack(anchor="w", padx=70)

    username_entry = tk.Entry(
        right_frame,
        font=("Arial", 12),
        bd=1,
        relief="solid"
    )

    username_entry.pack(
        padx=70,
        pady=(5, 20),
        fill="x"
    )

    tk.Label(
        right_frame,
        text="Password",
        font=("Arial", 11),
        bg=WHITE,
        fg=TEXT
    ).pack(anchor="w", padx=70)

    password_frame = tk.Frame(
        right_frame,
        bg=WHITE
    )

    password_frame.pack(
        padx=70,
        pady=(5, 10),
        fill="x"
    )

    password_entry = tk.Entry(
        password_frame,
        font=("Arial", 12),
        show="*",
        bd=1,
        relief="solid"
    )

    password_entry.pack(
        side="left",
        fill="x",
        expand=True
    )

    def show_password():

        if password_entry.cget("show") == "*":

            password_entry.config(show="")
            show_button.config(text="Hide")

        else:

            password_entry.config(show="*")
            show_button.config(text="Show")

    show_button = tk.Button(
        password_frame,
        text="Show",
        command=show_password,
        bg=WHITE,
        fg=DARK_GREEN,
        bd=0,
        cursor="hand2"
    )

    show_button.pack(
        side="right",
        padx=5
    )

    def login_check(event=None):

        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            login.destroy()

            dashboard_window()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

    tk.Button(
        right_frame,
        text="LOGIN",
        command=login_check,
        font=("Arial", 12, "bold"),
        bg=DARK_GREEN,
        fg=WHITE,
        activebackground=DARK_GREEN,
        activeforeground=WHITE,
        bd=0,
        cursor="hand2",
        height=2
    ).pack(
        padx=70,
        pady=25,
        fill="x"
    )

    password_entry.bind(
        "<Return>",
        login_check
    )

    username_entry.focus()

    login.mainloop()


# =========================
# DASHBOARD
# =========================

def dashboard_window():

    dashboard = tk.Tk()

    dashboard.title(
        "TreeTrace - Admin Dashboard"
    )

    dashboard.geometry("750x550")
    dashboard.resizable(False, False)

    dashboard.configure(
        bg=LIGHT_GREEN
    )

    # HEADER

    header = tk.Frame(
        dashboard,
        bg=DARK_GREEN,
        height=110
    )

    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="🌳 TreeTrace",
        font=("Arial", 25, "bold"),
        bg=DARK_GREEN,
        fg=WHITE
    ).pack(
        anchor="w",
        padx=35,
        pady=(18, 0)
    )

    tk.Label(
        header,
        text="Admin Dashboard",
        font=("Arial", 11),
        bg=DARK_GREEN,
        fg="#DDE9E1"
    ).pack(
        anchor="w",
        padx=38
    )

    # WELCOME

    tk.Label(
        dashboard,
        text="Welcome, Admin",
        font=("Arial", 20, "bold"),
        bg=LIGHT_GREEN,
        fg=TEXT
    ).pack(
        pady=(30, 5)
    )

    tk.Label(
        dashboard,
        text="Manage trees, photos and QR codes",
        font=("Arial", 11),
        bg=LIGHT_GREEN,
        fg=GRAY
    ).pack(
        pady=(0, 25)
    )

    # BUTTON FRAME

    button_frame = tk.Frame(
        dashboard,
        bg=LIGHT_GREEN
    )

    button_frame.pack()

    def dashboard_button(text, command):

        return tk.Button(
            button_frame,
            text=text,
            command=command,
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=DARK_GREEN,
            activebackground="#E8F0EA",
            activeforeground=DARK_GREEN,
            relief="solid",
            bd=1,
            cursor="hand2",
            width=24,
            height=2
        )

    dashboard_button(
        "➕  Add Tree",
        lambda: add_tree_window(dashboard)
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=10
    )

    dashboard_button(
        "✏  Edit Tree",
        lambda: edit_tree_window(dashboard)
    ).grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )

    dashboard_button(
        "🗑  Delete Tree",
        lambda: delete_tree_window(dashboard)
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )

    dashboard_button(
        "📋  View All Trees",
        lambda: view_all_trees(dashboard)
    ).grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )

    dashboard_button(
        "▣  QR Management",
        lambda: qr_management_window(dashboard)
    ).grid(
        row=2,
        column=0,
        padx=10,
        pady=10
    )

    dashboard_button(
        "Logout",
        dashboard.destroy
    ).grid(
        row=2,
        column=1,
        padx=10,
        pady=10
    )

    dashboard.mainloop()


# =========================
# ADD TREE
# =========================

def add_tree_window(parent):

    window = tk.Toplevel(parent)

    window.title(
        "TreeTrace - Add Tree"
    )

    window.geometry("700x750")
    window.resizable(False, False)

    window.configure(
        bg=LIGHT_GREEN
    )

    tk.Label(
        window,
        text="Add New Tree",
        font=("Arial", 24, "bold"),
        bg=LIGHT_GREEN,
        fg=DARK_GREEN
    ).pack(pady=20)

    form = tk.Frame(
        window,
        bg=LIGHT_GREEN
    )

    form.pack(
        fill="both",
        expand=True,
        padx=40
    )

    fields = [
        "Tree Name",
        "Scientific Name",
        "Family",
        "Category",
        "Description",
        "Age",
        "Location",
        "Benefits",
        "Uses",
        "Parts Used",
        "Health Status",
        "Maintenance Status",
        "Planting Date"
    ]

    entries = {}

    for i, field in enumerate(fields):

        tk.Label(
            form,
            text=field,
            bg=LIGHT_GREEN,
            fg=TEXT,
            font=("Arial", 10, "bold")
        ).grid(
            row=i,
            column=0,
            sticky="w",
            pady=5
        )

        entry = tk.Entry(
            form,
            font=("Arial", 10),
            width=48,
            bd=1,
            relief="solid"
        )

        entry.grid(
            row=i,
            column=1,
            pady=5,
            padx=15
        )

        entries[field] = entry

    # PHOTO

    selected_photo = {
        "path": None
    }

    def choose_photo():

        path = filedialog.askopenfilename(
            title="Select Tree Photo",
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png"
                )
            ]
        )

        if path:

            selected_photo["path"] = path

            photo_label.config(
                text=os.path.basename(path)
            )

    tk.Button(
        form,
        text="Choose Photo",
        command=choose_photo,
        bg=WHITE,
        fg=DARK_GREEN,
        cursor="hand2"
    ).grid(
        row=len(fields),
        column=0,
        pady=10
    )

    photo_label = tk.Label(
        form,
        text="No photo selected",
        bg=LIGHT_GREEN,
        fg=GRAY
    )

    photo_label.grid(
        row=len(fields),
        column=1,
        sticky="w"
    )

    def save_tree():

        values = {}

        for field, entry in entries.items():

            values[field] = entry.get().strip()

        if not values["Tree Name"]:

            messagebox.showerror(
                "Error",
                "Tree Name is required."
            )

            return

        if not selected_photo["path"]:

            messagebox.showerror(
                "Error",
                "Please select a tree photo."
            )

            return

        tree_id = get_next_tree_id()

        original_photo = selected_photo["path"]

        extension = os.path.splitext(
            original_photo
        )[1].lower()

        photo_filename = (
            f"{tree_id}{extension}"
        )

        destination_photo = os.path.join(
            IMAGE_FOLDER,
            photo_filename
        )

        try:

            shutil.copy2(
                original_photo,
                destination_photo
            )

            conn = get_connection()

            conn.execute(
                """
                INSERT INTO trees
                (
                    tree_id,
                    name,
                    scientific_name,
                    family,
                    category,
                    description,
                    age,
                    location,
                    benefits,
                    uses,
                    parts_used,
                    health_status,
                    maintenance_status,
                    planting_date,
                    photo
                )
                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    tree_id,
                    values["Tree Name"],
                    values["Scientific Name"],
                    values["Family"],
                    values["Category"],
                    values["Description"],
                    values["Age"] or None,
                    values["Location"],
                    values["Benefits"],
                    values["Uses"],
                    values["Parts Used"],
                    values["Health Status"],
                    values["Maintenance Status"],
                    values["Planting Date"],
                    photo_filename
                )
            )

            conn.commit()
            conn.close()

            generate_qr(tree_id)

            messagebox.showinfo(
                "Success",
                f"Tree added successfully!\n\n"
                f"Tree Name: {values['Tree Name']}\n"
                f"Tree ID: {tree_id}\n"
                f"Photo: {photo_filename}\n"
                f"QR Code: {tree_id}.png"
            )

            window.destroy()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    tk.Button(
        window,
        text="SAVE TREE",
        command=save_tree,
        font=("Arial", 12, "bold"),
        bg=DARK_GREEN,
        fg=WHITE,
        activebackground=DARK_GREEN,
        activeforeground=WHITE,
        bd=0,
        cursor="hand2",
        width=25,
        height=2
    ).pack(pady=20)


# =========================
# EDIT TREE
# =========================

def edit_tree_window(parent):

    window = tk.Toplevel(parent)

    window.title(
        "TreeTrace - Edit Tree"
    )

    window.geometry("750x780")
    window.resizable(False, False)

    window.configure(
        bg=LIGHT_GREEN
    )

    tk.Label(
        window,
        text="Edit Tree",
        font=("Arial", 24, "bold"),
        bg=LIGHT_GREEN,
        fg=DARK_GREEN
    ).pack(
        pady=(20, 5)
    )

    tk.Label(
        window,
        text="Select a tree to edit its information",
        font=("Arial", 11),
        bg=LIGHT_GREEN,
        fg=GRAY
    ).pack(
        pady=(0, 15)
    )

    # TREE SELECTION

    select_frame = tk.Frame(
        window,
        bg=LIGHT_GREEN
    )

    select_frame.pack()

    tk.Label(
        select_frame,
        text="Select Tree:",
        font=("Arial", 10, "bold"),
        bg=LIGHT_GREEN,
        fg=TEXT
    ).pack(
        side="left",
        padx=5
    )

    tree_var = tk.StringVar()

    tree_combo = tk.OptionMenu(
        select_frame,
        tree_var,
        ""
    )

    tree_combo.config(
        width=35,
        bg=WHITE,
        fg=TEXT
    )

    tree_combo.pack(
        side="left",
        padx=5
    )

    # FORM

    form = tk.Frame(
        window,
        bg=LIGHT_GREEN
    )

    form.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=15
    )

    fields = [
        "Tree Name",
        "Scientific Name",
        "Family",
        "Category",
        "Description",
        "Age",
        "Location",
        "Benefits",
        "Uses",
        "Parts Used",
        "Health Status",
        "Maintenance Status",
        "Planting Date"
    ]

    entries = {}

    for i, field in enumerate(fields):

        tk.Label(
            form,
            text=field,
            bg=LIGHT_GREEN,
            fg=TEXT,
            font=("Arial", 10, "bold")
        ).grid(
            row=i,
            column=0,
            sticky="w",
            pady=4
        )

        entry = tk.Entry(
            form,
            font=("Arial", 10),
            width=48,
            bd=1,
            relief="solid"
        )

        entry.grid(
            row=i,
            column=1,
            pady=4,
            padx=15
        )

        entries[field] = entry

    # CURRENT PHOTO

    current_photo_label = tk.Label(
        form,
        text="Current photo: None",
        bg=LIGHT_GREEN,
        fg=GRAY
    )

    current_photo_label.grid(
        row=len(fields),
        column=1,
        sticky="w",
        pady=5
    )

    selected_photo = {
        "path": None
    }

    def choose_photo():

        path = filedialog.askopenfilename(
            title="Select New Tree Photo",
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png"
                )
            ]
        )

        if path:

            selected_photo["path"] = path

            current_photo_label.config(
                text=(
                    f"New photo: "
                    f"{os.path.basename(path)}"
                )
            )

    tk.Button(
        form,
        text="Choose New Photo",
        command=choose_photo,
        bg=WHITE,
        fg=DARK_GREEN,
        cursor="hand2"
    ).grid(
        row=len(fields),
        column=0,
        pady=5
    )

    # LOAD TREES

    tree_records = {}

    def load_trees():

        try:

            conn = get_connection()

            rows = conn.execute(
                """
                SELECT tree_id, name
                FROM trees
                ORDER BY
                    CAST(
                        SUBSTR(tree_id, 2)
                        AS INTEGER
                    )
                """
            ).fetchall()

            conn.close()

            menu = tree_combo["menu"]

            menu.delete(
                0,
                "end"
            )

            tree_records.clear()

            for row in rows:

                display_text = (
                    f"{row['tree_id']} - "
                    f"{row['name']}"
                )

                tree_records[
                    display_text
                ] = row["tree_id"]

                menu.add_command(
                    label=display_text,
                    command=lambda value=display_text:
                    tree_var.set(value)
                )

            if rows:

                tree_var.set(
                    f"{rows[0]['tree_id']} - "
                    f"{rows[0]['name']}"
                )

                load_selected_tree()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    def load_selected_tree():

        selected = tree_var.get()

        if not selected:
            return

        tree_id = tree_records.get(
            selected
        )

        if not tree_id:
            return

        try:

            conn = get_connection()

            tree = conn.execute(
                "SELECT * FROM trees "
                "WHERE tree_id = ?",
                (tree_id,)
            ).fetchone()

            conn.close()

            if not tree:
                return

            entries["Tree Name"].delete(0, tk.END)
            entries["Tree Name"].insert(
                0,
                tree["name"] or ""
            )

            entries["Scientific Name"].delete(
                0,
                tk.END
            )

            entries["Scientific Name"].insert(
                0,
                tree["scientific_name"] or ""
            )

            entries["Family"].delete(
                0,
                tk.END
            )

            entries["Family"].insert(
                0,
                tree["family"] or ""
            )

            entries["Category"].delete(
                0,
                tk.END
            )

            entries["Category"].insert(
                0,
                tree["category"] or ""
            )

            entries["Description"].delete(
                0,
                tk.END
            )

            entries["Description"].insert(
                0,
                tree["description"] or ""
            )

            entries["Age"].delete(
                0,
                tk.END
            )

            entries["Age"].insert(
                0,
                tree["age"] or ""
            )

            entries["Location"].delete(
                0,
                tk.END
            )

            entries["Location"].insert(
                0,
                tree["location"] or ""
            )

            entries["Benefits"].delete(
                0,
                tk.END
            )

            entries["Benefits"].insert(
                0,
                tree["benefits"] or ""
            )

            entries["Uses"].delete(
                0,
                tk.END
            )

            entries["Uses"].insert(
                0,
                tree["uses"] or ""
            )

            entries["Parts Used"].delete(
                0,
                tk.END
            )

            entries["Parts Used"].insert(
                0,
                tree["parts_used"] or ""
            )

            entries["Health Status"].delete(
                0,
                tk.END
            )

            entries["Health Status"].insert(
                0,
                tree["health_status"] or ""
            )

            entries["Maintenance Status"].delete(
                0,
                tk.END
            )

            entries["Maintenance Status"].insert(
                0,
                tree["maintenance_status"] or ""
            )

            entries["Planting Date"].delete(
                0,
                tk.END
            )

            entries["Planting Date"].insert(
                0,
                tree["planting_date"] or ""
            )

            selected_photo["path"] = None

            current_photo_label.config(
                text=(
                    f"Current photo: "
                    f"{tree['photo'] or 'None'}"
                )
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    tree_var.trace_add(
        "write",
        lambda *args:
        load_selected_tree()
    )

    # UPDATE TREE

    def update_tree():

        selected = tree_var.get()

        if not selected:

            messagebox.showwarning(
                "Select Tree",
                "Please select a tree first."
            )

            return

        tree_id = tree_records.get(
            selected
        )

        if not tree_id:

            messagebox.showerror(
                "Error",
                "Tree ID could not be found."
            )

            return

        values = {}

        for field, entry in entries.items():

            values[field] = entry.get().strip()

        if not values["Tree Name"]:

            messagebox.showerror(
                "Error",
                "Tree Name is required."
            )

            return

        try:

            conn = get_connection()

            old_tree = conn.execute(
                "SELECT photo FROM trees "
                "WHERE tree_id = ?",
                (tree_id,)
            ).fetchone()

            old_photo = (
                old_tree["photo"]
                if old_tree
                else None
            )

            new_photo_filename = old_photo

            # NEW PHOTO

            if selected_photo["path"]:

                original_photo = selected_photo["path"]

                extension = os.path.splitext(
                    original_photo
                )[1].lower()

                new_photo_filename = (
                    f"{tree_id}{extension}"
                )

                new_photo_path = os.path.join(
                    IMAGE_FOLDER,
                    new_photo_filename
                )

                if old_photo:

                    old_photo_path = os.path.join(
                        IMAGE_FOLDER,
                        old_photo
                    )

                    if (
                        os.path.exists(
                            old_photo_path
                        )
                        and
                        old_photo_path
                        != new_photo_path
                    ):

                        os.remove(
                            old_photo_path
                        )

                shutil.copy2(
                    original_photo,
                    new_photo_path
                )

            # UPDATE DATABASE

            conn.execute(
                """
                UPDATE trees
                SET
                    name = ?,
                    scientific_name = ?,
                    family = ?,
                    category = ?,
                    description = ?,
                    age = ?,
                    location = ?,
                    benefits = ?,
                    uses = ?,
                    parts_used = ?,
                    health_status = ?,
                    maintenance_status = ?,
                    planting_date = ?,
                    photo = ?
                WHERE tree_id = ?
                """,
                (
                    values["Tree Name"],
                    values["Scientific Name"],
                    values["Family"],
                    values["Category"],
                    values["Description"],
                    values["Age"] or None,
                    values["Location"],
                    values["Benefits"],
                    values["Uses"],
                    values["Parts Used"],
                    values["Health Status"],
                    values["Maintenance Status"],
                    values["Planting Date"],
                    new_photo_filename,
                    tree_id
                )
            )

            conn.commit()
            conn.close()

            # REGENERATE QR

            generate_qr(tree_id)

            messagebox.showinfo(
                "Success",
                f"Tree updated successfully!\n\n"
                f"Tree ID: {tree_id}\n"
                f"Tree Name: "
                f"{values['Tree Name']}\n\n"
                f"Existing QR code has been updated."
            )

            window.destroy()

        except Exception as e:

            messagebox.showerror(
                "Update Error",
                str(e)
            )

    tk.Button(
        window,
        text="UPDATE TREE",
        command=update_tree,
        font=("Arial", 12, "bold"),
        bg=DARK_GREEN,
        fg=WHITE,
        activebackground=DARK_GREEN,
        activeforeground=WHITE,
        bd=0,
        cursor="hand2",
        width=25,
        height=2
    ).pack(
        pady=15
    )

    load_trees()


# =========================
# DELETE TREE
# =========================

def delete_tree_window(parent):

    window = tk.Toplevel(parent)

    window.title(
        "TreeTrace - Delete Tree"
    )

    window.geometry("650x600")
    window.resizable(False, False)

    window.configure(
        bg=LIGHT_GREEN
    )

    tk.Label(
        window,
        text="Delete Tree",
        font=("Arial", 22, "bold"),
        bg=LIGHT_GREEN,
        fg=DARK_GREEN
    ).pack(pady=15)

    tk.Label(
        window,
        text="Select a tree to delete",
        font=("Arial", 11),
        bg=LIGHT_GREEN,
        fg=GRAY
    ).pack(
        pady=(0, 15)
    )

    list_frame = tk.Frame(
        window,
        bg=WHITE,
        bd=1,
        relief="solid"
    )

    list_frame.pack(
        padx=30,
        pady=5,
        fill="both",
        expand=True
    )

    tree_list = tk.Listbox(
        list_frame,
        font=("Arial", 11),
        width=60,
        height=18,
        bd=0
    )

    tree_list.pack(
        side="left",
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    scrollbar = tk.Scrollbar(
        list_frame,
        command=tree_list.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    tree_list.config(
        yscrollcommand=scrollbar.set
    )

    try:

        conn = get_connection()

        rows = conn.execute(
            """
            SELECT tree_id, name
            FROM trees
            ORDER BY
                CAST(
                    SUBSTR(tree_id, 2)
                    AS INTEGER
                )
            """
        ).fetchall()

        conn.close()

        for row in rows:

            tree_list.insert(
                tk.END,
                f"{row['tree_id']} - "
                f"{row['name']}"
            )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

        window.destroy()

        return

    def delete_selected_tree():

        selection = tree_list.curselection()

        if not selection:

            messagebox.showwarning(
                "Select Tree",
                "Please select a tree first."
            )

            return

        item = tree_list.get(
            selection[0]
        )

        tree_id = item.split(
            " - "
        )[0]

        try:

            conn = get_connection()

            tree = conn.execute(
                """
                SELECT name, photo
                FROM trees
                WHERE tree_id = ?
                """,
                (tree_id,)
            ).fetchone()

            if not tree:

                conn.close()

                messagebox.showerror(
                    "Error",
                    "Tree not found."
                )

                return

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete\n\n"
                f"{tree['name']} ({tree_id})?\n\n"
                f"This will delete the tree record, "
                f"QR code and tree photo."
            )

            if not confirm:

                conn.close()

                return

            conn.execute(
                "DELETE FROM trees "
                "WHERE tree_id = ?",
                (tree_id,)
            )

            conn.commit()
            conn.close()

            # DELETE QR

            qr_path = os.path.join(
                QR_FOLDER,
                f"{tree_id}.png"
            )

            if os.path.exists(qr_path):

                os.remove(qr_path)

            # DELETE PHOTO

            photo_filename = tree["photo"]

            if photo_filename:

                photo_path = os.path.join(
                    IMAGE_FOLDER,
                    photo_filename
                )

                if os.path.exists(
                    photo_path
                ):

                    os.remove(
                        photo_path
                    )

            messagebox.showinfo(
                "Delete Successful",
                f"{tree['name']} "
                f"({tree_id}) deleted successfully."
            )

            window.destroy()

        except Exception as e:

            messagebox.showerror(
                "Delete Error",
                str(e)
            )

    tk.Button(
        window,
        text="🗑  DELETE SELECTED TREE",
        command=delete_selected_tree,
        font=("Arial", 12, "bold"),
        bg="#B3261E",
        fg=WHITE,
        activebackground="#8F1D18",
        activeforeground=WHITE,
        bd=0,
        cursor="hand2",
        width=28,
        height=2
    ).pack(
        pady=20
    )


# =========================
# VIEW ALL TREES
# =========================

def view_all_trees(parent):

    window = tk.Toplevel(parent)

    window.title(
        "TreeTrace - All Trees"
    )

    window.geometry("650x600")

    window.configure(
        bg=LIGHT_GREEN
    )

    tk.Label(
        window,
        text="All Trees",
        font=("Arial", 22, "bold"),
        bg=LIGHT_GREEN,
        fg=DARK_GREEN
    ).pack(
        pady=15
    )

    listbox = tk.Listbox(
        window,
        font=("Arial", 11),
        width=65,
        height=25
    )

    listbox.pack(
        padx=20,
        pady=10
    )

    try:

        conn = get_connection()

        rows = conn.execute(
            """
            SELECT tree_id, name, scientific_name
            FROM trees
            ORDER BY
                CAST(
                    SUBSTR(tree_id, 2)
                    AS INTEGER
                )
            """
        ).fetchall()

        conn.close()

        for row in rows:

            listbox.insert(
                tk.END,
                f"{row['tree_id']}  |  "
                f"{row['name']}  |  "
                f"{row['scientific_name']}"
            )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )



# =========================
# QR MANAGEMENT
# =========================

def qr_management_window(parent):

    window = tk.Toplevel(parent)
    window.title("TreeTrace - QR Management")
    window.geometry("900x750")
    window.resizable(False, False)
    window.configure(bg=LIGHT_GREEN)

    tk.Label(
        window,
        text="QR Code Management",
        font=("Arial", 24, "bold"),
        bg=LIGHT_GREEN,
        fg=DARK_GREEN
    ).pack(pady=(15, 5))

    tk.Label(
        window,
        text="Manage Tree Information and Website QR Codes",
        font=("Arial", 10),
        bg=LIGHT_GREEN,
        fg=GRAY
    ).pack(pady=(0, 12))

    main_frame = tk.Frame(window, bg=LIGHT_GREEN)
    main_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=5
    )

    # LEFT SIDE: TREE LIST

    left_frame = tk.Frame(
        main_frame,
        bg=WHITE,
        bd=1,
        relief="solid"
    )
    left_frame.pack(
        side="left",
        fill="y",
        padx=(0, 15)
    )

    tk.Label(
        left_frame,
        text="Available Trees",
        font=("Arial", 13, "bold"),
        bg=WHITE,
        fg=DARK_GREEN
    ).pack(pady=10)

    tree_list = tk.Listbox(
        left_frame,
        font=("Arial", 10),
        width=27,
        height=27,
        bd=0,
        exportselection=False
    )
    tree_list.pack(padx=8, pady=5, fill="y")

    # RIGHT SIDE

    right_frame = tk.Frame(
        main_frame,
        bg=WHITE,
        bd=1,
        relief="solid"
    )
    right_frame.pack(
        side="right",
        fill="both",
        expand=True
    )

    tree_name_label = tk.Label(
        right_frame,
        text="Select a tree",
        font=("Arial", 15, "bold"),
        bg=WHITE,
        fg=DARK_GREEN
    )
    tree_name_label.pack(pady=(12, 5))

    tk.Label(
        right_frame,
        text="Tree Information QR Preview",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(pady=3)

    qr_label = tk.Label(
        right_frame,
        text="Select a tree to view its QR",
        bg=WHITE,
        fg=GRAY
    )
    qr_label.pack(pady=5)

    url_label = tk.Label(
        right_frame,
        text="",
        font=("Arial", 8),
        bg=WHITE,
        fg=GRAY,
        wraplength=400
    )
    url_label.pack(pady=3)

    qr_image_reference = {"image": None}

    # LOAD TREES FROM DATABASE

    try:
        conn = get_connection()

        rows = conn.execute(
            """
            SELECT tree_id, name
            FROM trees
            ORDER BY CAST(SUBSTR(tree_id, 2) AS INTEGER)
            """
        ).fetchall()

        conn.close()

        for row in rows:
            tree_list.insert(
                tk.END,
                f"{row['tree_id']} - {row['name']}"
            )

    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        window.destroy()
        return

    # SHOW TREE INFORMATION QR

    def show_qr(event=None):

        selection = tree_list.curselection()

        if not selection:
            return

        item = tree_list.get(selection[0])
        tree_id = item.split(" - ", 1)[0]
        tree_name = item.split(" - ", 1)[1]

        try:
            qr_path = os.path.join(
                QR_FOLDER,
                f"{tree_id}.png"
            )

            if not os.path.exists(qr_path):
                qr_path = generate_qr(tree_id)

            image = Image.open(qr_path)
            image.thumbnail((190, 190))

            photo = ImageTk.PhotoImage(image)

            qr_label.config(image=photo, text="")
            qr_image_reference["image"] = photo

            tree_name_label.config(text=tree_name)

            url_label.config(
                text=f"Tree Information URL:\n"
                     f"{FLASK_URL}/?tree_id={tree_id}"
            )

        except Exception as e:
            messagebox.showerror("QR Error", str(e))

    tree_list.bind("<<ListboxSelect>>", show_qr)

    # REGENERATE TREE INFORMATION QR

    def regenerate_selected_qr():

        selection = tree_list.curselection()

        if not selection:
            messagebox.showwarning(
                "Select Tree",
                "Please select a tree first."
            )
            return

        item = tree_list.get(selection[0])
        tree_id = item.split(" - ", 1)[0]

        try:
            generate_qr(tree_id)

            messagebox.showinfo(
                "QR Generated",
                f"Tree Information QR generated for {tree_id}."
            )

            show_qr()

        except Exception as e:
            messagebox.showerror("QR Error", str(e))

    tk.Button(
        right_frame,
        text="Regenerate Tree Information QR",
        command=regenerate_selected_qr,
        font=("Arial", 9, "bold"),
        bg=DARK_GREEN,
        fg=WHITE,
        activebackground=DARK_GREEN,
        activeforeground=WHITE,
        bd=0,
        cursor="hand2",
        width=32,
        height=2
    ).pack(pady=(5, 10))

    # PASTE YOUTUBE / WEBSITE LINK

    tk.Label(
        right_frame,
        text="Generate QR from Your Link",
        font=("Arial", 12, "bold"),
        bg=WHITE,
        fg=DARK_GREEN
    ).pack(pady=(5, 3))

    tk.Label(
        right_frame,
        text="Select a tree and paste its YouTube or website URL:",
        font=("Arial", 9),
        bg=WHITE,
        fg=TEXT,
        wraplength=410
    ).pack(pady=3)

    video_url_entry = tk.Entry(
        right_frame,
        font=("Arial", 10),
        width=45,
        bd=1,
        relief="solid"
    )
    video_url_entry.pack(
        padx=12,
        pady=5,
        ipady=5
    )

    # GENERATE QR FROM PASTED LINK

    def generate_qr_from_pasted_link():

        selection = tree_list.curselection()

        if not selection:
            messagebox.showwarning(
                "Select Tree",
                "Please select a tree first."
            )
            return

        pasted_url = video_url_entry.get().strip()

        if not pasted_url:
            messagebox.showwarning(
                "Missing Link",
                "Please paste a YouTube or website link."
            )
            return

        if not pasted_url.startswith(("https://", "http://")):
            messagebox.showwarning(
                "Invalid Link",
                "The link must start with https:// or http://."
            )
            return

        item = tree_list.get(selection[0])
        tree_name = item.split(" - ", 1)[1]

        safe_name = "".join(
            char if char.isalnum() or char in "_-"
            else "_"
            for char in tree_name.strip()
        )

        try:
            os.makedirs(YOUTUBE_QR_FOLDER, exist_ok=True)

            qr_path = os.path.join(
                YOUTUBE_QR_FOLDER,
                f"{safe_name}_YouTube.png"
            )

            qr_image = qrcode.make(pasted_url)
            qr_image.save(qr_path)

            messagebox.showinfo(
                "QR Generated Successfully",
                f"Tree: {tree_name}\n\n"
                f"QR saved at:\n{qr_path}\n\n"
                "Scan this QR code to open your link."
            )

            video_url_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror(
                "QR Generation Error",
                str(e)
            )

    tk.Button(
        right_frame,
        text="Generate YouTube / Website QR",
        command=generate_qr_from_pasted_link,
        font=("Arial", 10, "bold"),
        bg=DARK_GREEN,
        fg=WHITE,
        activebackground=DARK_GREEN,
        activeforeground=WHITE,
        bd=0,
        cursor="hand2",
        width=30,
        height=2
    ).pack(pady=(5, 10))


# =========================
# START APPLICATION
# =========================

if __name__ == "__main__":

    login_window()