import hashlib
import os

def hash_password(password: str) -> str:
    # Generate a random 16-byte salt as a hexadecimal string.
    salt = os.urandom(16).hex()
    
    # Combine the salt with the password and hash it with SHA-256.
    hashed = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
    
    # Return the salt and hash as 'salt:hash' for database storage.
    return f"{salt}:{hashed}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    if not stored_password:
        return False

    # Support both the legacy plain SHA-256 format and the new salt:hash format.
    if ':' in stored_password:
        try:
            salt, hashed = stored_password.split(':', 1)
            recalculated_hash = hashlib.sha256((salt + provided_password).encode('utf-8')).hexdigest()
            return recalculated_hash == hashed
        except ValueError:
            return False

    # Legacy data from seed.sql stores plain SHA-256 hashes without a salt.
    legacy_hash = hashlib.sha256(provided_password.encode('utf-8')).hexdigest()
    return legacy_hash == stored_password