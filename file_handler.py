"""
File Handler Module
Handles file encryption and decryption operations
"""

from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken


def encrypt_file(file_path, key):
    """
    Encrypt a file using Fernet (AES-128)
    
    Args:
        file_path: Path to file to encrypt
        key: Encryption key
    
    Returns:
        Path: Path to encrypted file
    
    Raises:
        Various exceptions for file/crypto errors
    """
    file_path = Path(file_path)
    
    # Validate inputs
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not file_path.is_file():
        raise ValueError(f"Not a file: {file_path}")
    
    # Check if already encrypted (simple check)
    if file_path.suffix == '.encrypted':
        raise ValueError("File appears to already be encrypted (.encrypted extension)")
    
    # Initialize Fernet with key
    try:
        fernet = Fernet(key)
    except Exception as e:
        raise ValueError(f"Invalid encryption key: {e}")
    
    # Read file data
    try:
        with open(file_path, 'rb') as file:
            original_data = file.read()
    except PermissionError:
        raise PermissionError(f"Cannot read file (permission denied): {file_path}")
    except Exception as e:
        raise IOError(f"Error reading file: {e}")
    
    # Check if file is empty
    if len(original_data) == 0:
        raise ValueError("Cannot encrypt empty file")
    
    # Encrypt data
    try:
        encrypted_data = fernet.encrypt(original_data)
    except Exception as e:
        raise RuntimeError(f"Encryption failed: {e}")
    
    # Create output filename: original.encrypted
    encrypted_path = file_path.parent / f"{file_path.name}.encrypted"
    
    # Handle filename collision
    counter = 1
    while encrypted_path.exists():
        encrypted_path = file_path.parent / f"{file_path.name}_{counter}.encrypted"
        counter += 1
    
    # Write encrypted data
    try:
        with open(encrypted_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)
    except PermissionError:
        raise PermissionError(f"Cannot write encrypted file (permission denied): {encrypted_path}")
    except Exception as e:
        raise IOError(f"Error writing encrypted file: {e}")
    
    return encrypted_path


def decrypt_file(file_path, key):
    """
    Decrypt a file using Fernet (AES-128)
    
    Args:
        file_path: Path to encrypted file
        key: Encryption key
    
    Returns:
        Path: Path to decrypted file
    
    Raises:
        Various exceptions for file/crypto errors
    """
    file_path = Path(file_path)
    
    # Validate inputs
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not file_path.is_file():
        raise ValueError(f"Not a file: {file_path}")
    
    # Initialize Fernet with key
    try:
        fernet = Fernet(key)
    except Exception as e:
        raise ValueError(f"Invalid encryption key: {e}")
    
    # Read encrypted data
    try:
        with open(file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
    except PermissionError:
        raise PermissionError(f"Cannot read file (permission denied): {file_path}")
    except Exception as e:
        raise IOError(f"Error reading file: {e}")
    
    # Decrypt data
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except InvalidToken:
        raise ValueError("Invalid key or corrupted file. Decryption failed.")
    except Exception as e:
        raise RuntimeError(f"Decryption failed: {e}")
    
    # Determine output filename
    # Remove .encrypted extension if present
    filename = file_path.name
    if filename.endswith('.encrypted'):
        decrypted_name = filename[:-10]  # Remove '.encrypted'
    else:
        decrypted_name = f"decrypted_{filename}"
    
    decrypted_path = file_path.parent / decrypted_name
    
    # Handle filename collision
    counter = 1
    while decrypted_path.exists():
        name = decrypted_path.stem
        suffix = decrypted_path.suffix
        decrypted_path = file_path.parent / f"{name}_{counter}{suffix}"
        counter += 1
    
    # Write decrypted data
    try:
        with open(decrypted_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)
    except PermissionError:
        raise PermissionError(f"Cannot write decrypted file (permission denied): {decrypted_path}")
    except Exception as e:
        raise IOError(f"Error writing decrypted file: {e}")
    
    return decrypted_path