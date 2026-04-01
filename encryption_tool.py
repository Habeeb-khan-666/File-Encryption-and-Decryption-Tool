#!/usr/bin/env python3
"""
File Encryption and Decryption Tool
A beginner-friendly tool for secure file encryption using AES-128 via Fernet
"""

import os
import sys
from pathlib import Path

# Import our modules
from key_manager import generate_key, load_key, save_key
from file_handler import encrypt_file, decrypt_file


def print_banner():
    """Display welcome banner"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║          🔐 FILE ENCRYPTION & DECRYPTION TOOL 🔐         ║
    ║              Secure Your Files with AES-128              ║
    ╚══════════════════════════════════════════════════════════╝
    """)


def get_menu_choice():
    """Display menu and get user choice"""
    print("\n📋 MAIN MENU:")
    print("1. 🔒 Encrypt a file")
    print("2. 🔓 Decrypt a file")
    print("3. 🔑 Generate new encryption key")
    print("4. ❌ Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            return choice
        print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")


def get_file_path(prompt, must_exist=True):
    """
    Get file path from user with validation
    
    Args:
        prompt: Message to show user
        must_exist: Whether file must already exist
    
    Returns:
        Path object or None if invalid
    """
    while True:
        file_path = input(prompt).strip()
        
        # Remove quotes if user added them
        file_path = file_path.strip('"').strip("'")
        
        # Expand home directory (~)
        file_path = os.path.expanduser(file_path)
        
        path = Path(file_path)
        
        # Check if file exists (when required)
        if must_exist and not path.exists():
            print(f"❌ Error: File not found: {path}")
            retry = input("Try again? (y/n): ").lower()
            if retry != 'y':
                return None
            continue
        
        # Check if it's a file (not directory)
        if must_exist and not path.is_file():
            print(f"❌ Error: This is a directory, not a file: {path}")
            retry = input("Try again? (y/n): ").lower()
            if retry != 'y':
                return None
            continue
        
        return path


def get_key_choice():
    """Ask user how they want to handle the encryption key"""
    print("\n🔑 KEY OPTIONS:")
    print("1. Generate a new key")
    print("2. Use existing key file")
    
    while True:
        choice = input("\nEnter choice (1-2): ").strip()
        if choice in ['1', '2']:
            return choice
        print("❌ Invalid choice. Please enter 1 or 2.")


def main():
    """Main program loop"""
    print_banner()
    
    # Create necessary directories
    Path("keys").mkdir(exist_ok=True)
    Path("test_files").mkdir(exist_ok=True)
    
    while True:
        choice = get_menu_choice()
        
        # ========== ENCRYPT FILE ==========
        if choice == '1':
            print("\n" + "="*50)
            print("🔒 FILE ENCRYPTION")
            print("="*50)
            
            # Get file to encrypt
            file_path = get_file_path("\n📁 Enter path to file to encrypt: ")
            if not file_path:
                continue
            
            # Get key
            key_choice = get_key_choice()
            
            if key_choice == '1':
                # Generate new key
                key = generate_key()
                key_path = Path("keys") / f"key_{file_path.stem}.key"
                save_key(key, key_path)
                print(f"✅ New key generated and saved to: {key_path}")
            else:
                # Load existing key
                key_path = get_file_path("\n📁 Enter path to key file: ")
                if not key_path:
                    continue
                key = load_key(key_path)
                if not key:
                    continue
            
            # Encrypt the file
            try:
                encrypted_path = encrypt_file(file_path, key)
                print(f"\n{'='*50}")
                print(f"✅ SUCCESS! File encrypted successfully!")
                print(f"📄 Original: {file_path}")
                print(f"🔒 Encrypted: {encrypted_path}")
                print(f"🔑 Key file: Remember your key file location!")
                print(f"{'='*50}")
            except Exception as e:
                print(f"\n❌ Encryption failed: {e}")
        
        # ========== DECRYPT FILE ==========
        elif choice == '2':
            print("\n" + "="*50)
            print("🔓 FILE DECRYPTION")
            print("="*50)
            
            # Get file to decrypt
            file_path = get_file_path("\n📁 Enter path to encrypted file: ")
            if not file_path:
                continue
            
            # Get key
            key_path = get_file_path("\n📁 Enter path to key file: ")
            if not key_path:
                continue
            
            key = load_key(key_path)
            if not key:
                continue
            
            # Decrypt the file
            try:
                decrypted_path = decrypt_file(file_path, key)
                print(f"\n{'='*50}")
                print(f"✅ SUCCESS! File decrypted successfully!")
                print(f"🔒 Encrypted: {file_path}")
                print(f"📄 Decrypted: {decrypted_path}")
                print(f"{'='*50}")
            except Exception as e:
                print(f"\n❌ Decryption failed: {e}")
                print("\n💡 Common causes:")
                print("   • Wrong key file")
                print("   • File was corrupted")
                print("   • File wasn't encrypted with this tool")
        
        # ========== GENERATE KEY ==========
        elif choice == '3':
            print("\n" + "="*50)
            print("🔑 GENERATE NEW KEY")
            print("="*50)
            
            key = generate_key()
            key_name = input("Enter name for key file (default: mykey): ").strip()
            if not key_name:
                key_name = "mykey"
            
            key_path = Path("keys") / f"{key_name}.key"
            save_key(key, key_path)
            
            print(f"\n✅ Key generated and saved to: {key_path}")
            print("⚠️  IMPORTANT: Keep this key safe! Without it, you cannot decrypt files!")
        
        # ========== EXIT ==========
        elif choice == '4':
            print("\n👋 Goodbye! Stay secure!")
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
        sys.exit(0)