from django.db import models

import json
import os
import hashlib
from django.conf import settings
from django.core.exceptions import ValidationError

USERS_FILE = os.path.join(settings.BASE_DIR, 'users.json')

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def save(self):
        users = self.load_users()
        if self.username in users:
            raise ValidationError("Ce nom d'utilisateur est déjà pris.")
        users[self.username] = {"password": self.password}
        self.save_users(users)

    @staticmethod
    def load_users():
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        return {}

    @staticmethod
    def save_users(users):
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)

