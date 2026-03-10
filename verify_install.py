import sys

print(f"Python version: {sys.version}")

try:
    import psutil
    print("psutil imported successfully.")
except ImportError as e:
    print(f"Failed to import psutil: {e}")

try:
    import pygetwindow
    print("pygetwindow imported successfully.")
except ImportError as e:
    print(f"Failed to import pygetwindow: {e}")

try:
    import sklearn
    print("sklearn imported successfully.")
except ImportError as e:
    print(f"Failed to import sklearn: {e}")

try:
    import joblib
    print("joblib imported successfully.")
except ImportError as e:
    print(f"Failed to import joblib: {e}")

try:
    import pywinauto
    print("pywinauto imported successfully.")
except ImportError as e:
    print(f"Failed to import pywinauto: {e}")

try:
    import pynput
    print("pynput imported successfully.")
except ImportError as e:
    print(f"Failed to import pynput: {e}")

try:
    import sqlalchemy
    print("sqlalchemy imported successfully.")
except ImportError as e:
    print(f"Failed to import sqlalchemy: {e}")

try:
    import PyInstaller
    print("PyInstaller imported successfully.")
except ImportError as e:
    print(f"Failed to import PyInstaller: {e}")

try:
    import customtkinter
    print("customtkinter imported successfully.")
except ImportError as e:
    print(f"Failed to import customtkinter: {e}")

try:
    import flet
    print("flet imported successfully.")
except ImportError as e:
    print(f"Failed to import flet: {e}")

print("\nDependency check complete.")
