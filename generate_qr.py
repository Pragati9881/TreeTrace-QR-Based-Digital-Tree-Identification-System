
import qrcode
import os
import sqlite3

# Flask server IP address
ip_address = "10.216.12.213"

# QR code folder inside static
qr_folder = "static/qr_codes"
os.makedirs(qr_folder, exist_ok=True)

# Connect to database
conn = sqlite3.connect("treetrace.db")

# Get all tree IDs
trees = conn.execute(
    "SELECT tree_id FROM trees ORDER BY tree_id"
).fetchall()

conn.close()

# Generate QR code for every tree
for tree in trees:

    tree_id = tree[0]

    # URL that opens the specific tree information
    url = f"http://{ip_address}:5000/?tree_id={tree_id}"

    # Create QR code
    qr = qrcode.make(url)

    # Save QR code inside static/qr_codes
    qr.save(f"{qr_folder}/{tree_id}.png")

    print(f"Created QR: {tree_id}")

print("All QR codes created successfully!")
