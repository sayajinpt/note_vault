import sys
import hashlib
from Crypto.Cipher import AES
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtWidgets import QMessageBox

class NoteVault(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Note Vault'
        self.left = 100
        self.top = 100
        self.width = 500
        self.height = 500
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create text box
        self.text_box = QTextEdit(self)
        self.text_box.setFixedHeight(250)
        self.text_box.setFixedWidth(450)
        self.text_box.move(25, 50)

        # Create seed label and entry box
        self.seed_label = QLabel('Enter seed:', self)
        self.seed_label.move(25, 325)
        self.seed_entry = QLineEdit(self)
        self.seed_entry.move(25, 350)

        self.second_seed_label = QLabel('Enter second seed:', self)
        self.second_seed_label.move(25, 375)
        self.second_seed_entry = QLineEdit(self)
        self.second_seed_entry.move(25, 400)

        # Create save button
        self.save_button = QPushButton('Save', self)
        self.save_button.move(25, 440)
        self.save_button.clicked.connect(self.save_note)

        # Create load button
        self.load_button = QPushButton('Load', self)
        self.load_button.move(100, 440)
        self.load_button.clicked.connect(self.load_note)

    def save_note(self):
        # Get the text from the text box
        note = self.text_box.toPlainText()

        # Get the first seed from the entry box
        seed = self.seed_entry.text()

        # Get the second seed from the entry box
        second_seed = self.second_seed_entry.text()

        # Encrypt the note
        encrypted_note = self.encrypt_note(note, seed, second_seed)

        # Open file dialog to choose save location
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Note', '', 'Text Files (*.txt)')

        # Write the encrypted note to the file
        with open(file_path, "wb") as file:
            file.write(encrypted_note)

    def load_note(self):
        # Open file dialog to choose file to load
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Note', '', 'Text Files (*.txt)')

        # Read the encrypted note from the file
        with open(file_path, "rb") as file:
            encrypted_note = file.read()

        # Get the first seed from the entry box
        seed = self.seed_entry.text()

        # Get the second seed from the entry box
        second_seed = self.second_seed_entry.text()

        # Decrypt the note and insert it into the text box
        try:
            note = self.decrypt_note(encrypted_note, seed, second_seed)
            self.text_box.setText(note)
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Wrong seed or seeds!")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

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
    app = QApplication(sys.argv)
    ex = NoteVault()
    ex.show()
    sys.exit(app.exec_())