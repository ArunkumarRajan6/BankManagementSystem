import hashlib
import hmac
import secrets


def hash_pin(pin):
    salt = secrets.token_bytes(16)

    key = hashlib.pbkdf2_hmac(
        "sha256",
        pin.encode(),
        salt,
        200000
    )

    return (
        "pbkdf2_sha256$"
        + salt.hex()
        + "$"
        + key.hex()
    )


def verify_pin(pin, stored_hash):
    # New PBKDF2 hash
    if stored_hash.startswith("pbkdf2_sha256$"):
        try:
            _, salt_hex, key_hex = stored_hash.split("$")

            salt = bytes.fromhex(salt_hex)
            stored_key = bytes.fromhex(key_hex)

            new_key = hashlib.pbkdf2_hmac(
                "sha256",
                pin.encode(),
                salt,
                200000
            )

            return hmac.compare_digest(new_key, stored_key)

        except (ValueError, TypeError):
            return False

    # Support old SHA-256 hashes
    old_hash = hashlib.sha256(pin.encode()).hexdigest()

    return hmac.compare_digest(old_hash, stored_hash)