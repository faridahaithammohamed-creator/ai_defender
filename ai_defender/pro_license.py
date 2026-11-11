import hashlib

class EnterpriseLicenseManager:
    def __init__(self, secret_salt="AI_DEFENDER_2026_FARIDA"):
        self.secret_salt = secret_salt

    def generate_key(self, client_email):
        raw = f"{client_email}:{self.secret_salt}".encode()
        return "PRO-" + hashlib.sha256(raw).hexdigest()[:24].upper()

    def verify_key(self, client_email, license_key):
        expected = self.generate_key(client_email)
        return license_key == expected
