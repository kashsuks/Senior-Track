import subprocess
import sys
import os

def check_pip():
    """Check if pip is installed."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
        return True
    except subprocess.CalledProcessError:
        return False

def install_requirements(requirements_file, user_install=False):
    """Install packages from the requirements file."""
    if not os.path.exists(requirements_file):
        print(f"Error: The file {requirements_file} does not exist.")
        return
    
    install_command = [sys.executable, "-m", "pip", "install", "-r", requirements_file]
    
    # Optionally, install for the user if specified
    if user_install:
        install_command.append("--user")

    try:
        print("Installing packages...")
        subprocess.check_call(install_command)
        print("Installation successful!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        sys.exit(1)

def main():
    requirements_file = "requirements.txt"
    
    if not check_pip():
        print("Error: pip is not installed.")
        sys.exit(1)

    # Ask if user wants to install packages globally or just for the user
    user_input = input("Do you want to install the packages for the user only? (y/n): ").strip().lower()

    if user_input == "y":
        user_install = True
    elif user_input == "n":
        user_install = False
    else:
        print("Invalid input. Defaulting to global install.")
        user_install = False
    
    install_requirements(requirements_file, user_install)

if __name__ == "__main__":
    main()