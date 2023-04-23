import tkinter as tk
from tkinter import filedialog
import hashlib
from Crypto.Cipher import AES

class NoteVault:
    def __init__(self, master):
        self.master = master
        master.title("Note Vault")

        # Create text box
        self.text_box = tk.Text(master, height=20, width=50)
        self.text_box.pack()

        # Create seed label and entry box
        self.seed_label = tk.Label(master, text="Enter seed:")
        self.seed_label.pack()
        self.seed_entry = tk.Entry(master)
        self.seed_entry.pack()
        
        self.second_seed_label = tk.Label(master, text="Enter second seed:")
        self.second_seed_label.pack()
        self.second_seed_entry = tk.Entry(master)
        self.second_seed_entry.pack()

        # Create save button
        self.save_button = tk.Button(master, text="Save", command=self.save_note)
        self.save_button.pack()

        # Create load button
        self.load_button = tk.Button(master, text="Load", command=self.load_note)
        self.load_button.pack()

    def save_note(self):
        # Get the text from the text box
        note = self.text_box.get("1.0", "end-1c")

        # Get the first seed from the entry box
        seed = self.seed_entry.get()

        # Get the second seed from the entry box
        second_seed = self.second_seed_entry.get()

        # Encrypt the note
        encrypted_note = self.encrypt_note(note, seed, second_seed)

        # Open file dialog to choose save location
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")

        # Write the encrypted note to the file
        with open(file_path, "wb") as file:
            file.write(encrypted_note)

    def load_note(self):
        # Open file dialog to choose file to load
        file_path = filedialog.askopenfilename(defaultextension=".txt")

        # Read the encrypted note from the file
        with open(file_path, "rb") as file:
            encrypted_note = file.read()

        # Get the first seed from the entry box
        seed = self.seed_entry.get()

        # Get the second seed from the entry box
        second_seed = self.second_seed_entry.get()

        # Decrypt the note and insert it into the text box
        note = self.decrypt_note(encrypted_note, seed, second_seed)
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", note)

    def encrypt_note(self, note, seed, second_seed):
        # Use the hashlib sha256 function to encrypt the note using the first seed
        key = hashlib.sha256(seed.encode('utf-8')).digest()
        iv = b'0000000000000000'
        note = note.encode('utf-8')
        while len(note) % 16 != 0:
            note += b' '
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_note = cipher.encrypt(note)

        # Use the hashlib sha256 function to encrypt the note again using the second seed
        key = hashlib.sha256(second_seed.encode('utf-8')).digest()
        iv = b'0000000000000000'
        while len(encrypted_note) % 16 != 0:
            encrypted_note += b' '
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_note = cipher.encrypt(encrypted_note)

        return encrypted_note

    def decrypt_note(self, encrypted_note, seed, second_seed):
        # Use the hashlib sha256 function to generate two keys using the two seeds
        key1 = hashlib.sha256(seed.encode('utf-8')).digest()
        key2 = hashlib.sha256(second_seed.encode('utf-8')).digest()
        iv = b'0000000000000000'
        
        # First, decrypt the note using the first key
        cipher1 = AES.new(key1, AES.MODE_CBC, iv)
        decrypted_note1 = cipher1.decrypt(encrypted_note)
        
        # Then, decrypt the note again using the second key
        cipher2 = AES.new(key2, AES.MODE_CBC, iv)
        decrypted_note2 = cipher2.decrypt(decrypted_note1)
        
        # Remove any padding and return the decrypted note as a string
        decrypted_note = decrypted_note2.rstrip()
        return decrypted_note.decode('utf-8')

if __name__ == '__main__':
    root = tk.Tk()
    note_vault = NoteVault(root)
    root.mainloop()