#!/usr/bin/env python3
"""
Installation Helper for Student Data Management Application
Installs required dependencies for PDF and Excel export functionality
"""

import subprocess
import sys

def install_packages():
    """Install required packages for the application."""
    
    packages = {
        'reportlab': 'PDF export functionality',
        'pandas': 'Excel export (recommended method)',
        'openpyxl': 'Excel file handling'
    }
    
    print("=" * 60)
    print("Student Data Management App - Package Installer")
    print("=" * 60)
    print("\nThis will install the following packages:\n")
    
    for package, description in packages.items():
        print(f"  • {package:15} - {description}")
    
    print("\n" + "=" * 60)
    user_input = input("Do you want to install these packages? (y/n): ").strip().lower()
    
    if user_input != 'y':
        print("Installation cancelled.")
        return False
    
    failed = []
    
    for package, description in packages.items():
        print(f"\n📦 Installing {package}...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"   ✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"   ❌ Failed to install {package}")
            failed.append(package)
    
    print("\n" + "=" * 60)
    if not failed:
        print("✅ All packages installed successfully!")
        print("You can now run the application with all export features enabled.")
    else:
        print(f"⚠️  Failed to install: {', '.join(failed)}")
        print("The application will still work, but some features may be limited.")
        print("\nTry manual installation with:")
        for package in failed:
            print(f"  pip install {package}")
    
    print("=" * 60)
    return len(failed) == 0


if __name__ == "__main__":
    try:
        install_packages()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during installation: {e}")
        sys.exit(1)
