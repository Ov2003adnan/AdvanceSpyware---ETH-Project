from cryptography.fernet import Fernet
import os

# Path to the directory containing the encrypted files
file_path = "C:/Users/HP/PycharmProjects/ETHProject"
key_file_path = os.path.join(file_path, "encryption_key.key")

# Ensure the encryption key exists
if not os.path.exists(key_file_path):
    print("Encryption key not found. Decryption cannot proceed.")
    exit()

# Load the encryption key
with open(key_file_path, "rb") as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

# Function to decrypt files
def decrypt_file(encrypted_filepath):
    decrypted_filepath = encrypted_filepath.replace(".enc", "")
    try:
        with open(encrypted_filepath, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        with open(decrypted_filepath, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)
        print(f"Decrypted: {encrypted_filepath} -> {decrypted_filepath}")
    except Exception as e:
        print(f"Failed to decrypt {encrypted_filepath}: {e}")

# Decrypt all .enc files in the directory
def decrypt_all_files():
    encrypted_files = [
        f for f in os.listdir(file_path)
        if f.endswith(".enc")
    ]
    if not encrypted_files:
        print("No encrypted files found.")
        return

    for encrypted_file in encrypted_files:
        full_path = os.path.join(file_path, encrypted_file)
        decrypt_file(full_path)

# Execute decryption
if __name__ == "__main__":
    decrypt_all_files()
