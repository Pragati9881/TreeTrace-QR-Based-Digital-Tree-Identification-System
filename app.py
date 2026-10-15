
from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)


# ================================
# DATABASE CONNECTION
# ================================

def get_tree(tree_id):

    conn = sqlite3.connect("treetrace.db")
    conn.row_factory = sqlite3.Row

    try:
        tree = conn.execute(
            "SELECT * FROM trees WHERE tree_id = ?",
            (tree_id,)
        ).fetchone()

        return tree

    finally:
        conn.close()


# ================================
# HOME / TREE INFORMATION
# ================================

@app.route("/")
def home():

    tree_id = request.args.get("tree_id")

    if tree_id:

        tree = get_tree(tree_id)

        if tree:
            return render_template(
                "index.html",
                tree=tree
            )

    return render_template(
        "index.html",
        tree=None
    )


# ================================
# EXPLORE TREES
# ================================

@app.route("/explore")
def explore():

    conn = sqlite3.connect("treetrace.db")
    conn.row_factory = sqlite3.Row

    try:
        trees = conn.execute(
            "SELECT * FROM trees ORDER BY tree_id"
        ).fetchall()

    finally:
        conn.close()

    return render_template(
        "explore.html",
        trees=trees
    )


# ================================
# YOUTUBE QR PAGE
# ================================

@app.route("/qr/<tree_id>")
def show_qr(tree_id):

    tree = get_tree(tree_id)

    if not tree:
        return "Tree not found", 404

    tree_name = tree["name"]

    safe_name = "".join(
        char if char.isalnum() or char in "_-"
        else "_"
        for char in tree_name.strip()
    )

    qr_filename = f"{safe_name}_YouTube.png"

    youtube_qr_path = os.path.join(
        app.static_folder,
        "youtube_qr_codes",
        qr_filename
    )

    qr_exists = os.path.isfile(youtube_qr_path)

    return render_template(
        "qr.html",
        tree=tree,
        qr_exists=qr_exists,
        qr_filename=qr_filename
    )


# ================================
# RUN FLASK
# ================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
