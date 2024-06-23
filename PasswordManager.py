import base64
import os
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import FileHandler


class PasswordManager:

    def __init__(self):
        self.data = None  # Stores data that's supposed to be saved into or read from the json file
        self.master_key = None

    def save_data(self, file_path):  # Stores information into the json file
        file = open(file_path, 'w')
        json.dump(self.data, file, indent=4)

    def load_data(self, file_path):
        file = open(file_path, 'r')
        self.data = json.load(file)

    def set_master_password(self, password):
        salt = os.urandom(32)  # Generate salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )

        self.master_key = kdf.derive(password.encode())
        # Save salt and master key in base64 for JSON compatibility
        self.data['encryption']['salt'] = base64.b64encode(salt).decode('utf-8')
        self.data['encryption']['master_key'] = base64.b64encode(self.master_key).decode('utf-8')
        self.save_data("passwords.json")

    def verify_master_password(self, entered_password):
        self.load_data('passwords.json')
        if not self.master_key:
            return False

        salt = base64.b64decode(self.data['encryption']['salt'])

        # Derive key from entered password and stored salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000
        )
        derived_key = kdf.derive(entered_password.encode())
        master_key = base64.b64decode(self.data['encryption']['master_key'])

        # Compare derived key with stored master key
        if derived_key == master_key:
            self.master_key = master_key
            return True
        else:
            return False

    def encrypt_password(self, password):
        fernet = Fernet(self.master_key)
        encrypted_password = fernet.encrypt(password.encode())
        return encrypted_password

    # Function to decrypt a password using a derived key
    def decrypt_password(self, password):
        fernet = Fernet(self.master_key)
        password = fernet.decrypt(password).decode()
        return password

    def add_new_password(self, title, username, password, file_path="passwords.json"):
        self.load_data(file_path)

        if 'passwords' not in self.data:
            self.data['passwords'] = []

        encrypted_password = self.encrypt_password(password)
        new_password_entry = {'title': title, 'username': username, 'password': encrypted_password.decode()}

        self.data['passwords'].append(new_password_entry)
        self.save_data(file_path)
        return True

    def get_password(self, title, username, file_path="passwords.json"):
        self.load_data(file_path)

        if 'passwords' not in self.data:
            return None

        for entry in self.data['passwords']:
            if entry['title'] == title and entry['username'] == username:
                encrypted_password = entry['password'].encode()
                decrypted_password = self.decrypt_password(encrypted_password)
                return decrypted_password

        return None  # Return None if no matching password is found
