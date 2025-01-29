import logging
import os
from cryptography.fernet import Fernet
from config import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_key():
    """
    Генерация ключа шифрования.
    """
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
    logger.info("Ключ шифрования сгенерирован и сохранен.")

def load_key():
    """
    Загрузка ключа шифрования.
    """
    return open('secret.key', 'rb').read()

def encrypt_data(data, key):
    """
    Шифрование данных.
    """
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    """
    Расшифровка данных.
    """
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

def secure_api_keys():
    """
    Защита API-ключей и других конфиденциальных данных.
    """
    key = load_key()
    for exchange_name, exchange_config in config['exchanges'].items():
        for account in exchange_config['accounts']:
            api_key = account['api_key']
            secret_key = account['secret_key']
            passphrase = account.get('passphrase', '')

            encrypted_api_key = encrypt_data(api_key, key)
            encrypted_secret_key = encrypt_data(secret_key, key)
            encrypted_passphrase = encrypt_data(passphrase, key)

            account['api_key'] = encrypted_api_key.decode()
            account['secret_key'] = encrypted_secret_key.decode()
            account['passphrase'] = encrypted_passphrase.decode()

    with open('config_encrypted.yaml', 'w') as file:
        yaml.dump(config, file)
    logger.info("API-ключи зашифрованы и сохранены в config_encrypted.yaml.")

def decrypt_config():
    """
    Расшифровка конфигурационного файла.
    """
    key = load_key()
    with open('config_encrypted.yaml', 'r') as file:
        encrypted_config = yaml.safe_load(file)

    for exchange_name, exchange_config in encrypted_config['exchanges'].items():
        for account in exchange_config['accounts']:
            api_key = account['api_key']
            secret_key = account['secret_key']
            passphrase = account.get('passphrase', '')

            decrypted_api_key = decrypt_data(api_key.encode(), key)
            decrypted_secret_key = decrypt_data(secret_key.encode(), key)
            decrypted_passphrase = decrypt_data(passphrase.encode(), key)

            account['api_key'] = decrypted_api_key
            account['secret_key'] = decrypted_secret_key
            account['passphrase'] = decrypted_passphrase

    return encrypted_config

if __name__ == "__main__":
    if not os.path.exists('secret.key'):
        generate_key()
    secure_api_keys()