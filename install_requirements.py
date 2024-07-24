import subprocess
import platform
import sys


def install_requirements():
    system = platform.system()

    if system == 'Darwin':
        print("Detected OS: MacOS")
    elif system == 'Linux':
        print("Detected OS: Linux")
    elif system == 'Windows':
        print("Detected OS: Windows")
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)

    try:
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install','-r', 'requirements.txt','-Uq'])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during installation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    install_requirements()
