"""
Key Management Module
Handles encryption key generation, saving, and loading
"""

import os
from pathlib import Path
from cryptography.fernet import Fernet


def generate_key():
    """
    Generate a new Fernet encryption key
    
    Returns:
        bytes: A URL-safe base64-encoded 32-byte key
    """
    # Fernet.generate_key() creates a 32-byte key encoded in base64
    # This is suitable for AES-128 encryption
    return Fernet.generate_key()


def save_key(key, filepath):
    """
    Save encryption key to a file
    
    Args:
        key: The encryption key (bytes)
        filepath: Where to save the key
    
    Returns:
        Path: Path to saved key file
    """
    # Ensure directory exists
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    # Save key with restricted permissions (readable only by owner)
    with open(filepath, 'wb') as key_file:
        key_file.write(key)
    
    # Set file permissions (Unix/Linux/Mac)
    # 0o600 = owner can read/write, no one else has access
    try:
        os.chmod(filepath, 0o600)
    except Exception:
        pass  # Windows doesn't support Unix permissions
    
    return Path(filepath)


def load_key(filepath):
    """
    Load encryption key from file
    
    Args:
        filepath: Path to key file
    
    Returns:
        bytes: The encryption key, or None if error
    """
    try:
        # Check if file exists
        if not Path(filepath).exists():
            print(f"❌ Error: Key file not found: {filepath}")
            return None
        
        # Read and return key
        with open(filepath, 'rb') as key_file:
            key = key_file.read()
            
        # Validate key format
        try:
            Fernet(key)  # This validates the key
            return key
        except Exception:
            print("❌ Error: Invalid key format")
            return None
            
    except PermissionError:
        print(f"❌ Error: Permission denied reading key file: {filepath}")
        return None
    except Exception as e:
        print(f"❌ Error loading key: {e}")
        return None