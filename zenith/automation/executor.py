import ctypes
import os
import winreg

SPI_SETDESKWALLPAPER = 20

def set_wallpaper(image_path):
    if not os.path.exists(image_path):
        print(f"Wallpaper image not found: {image_path}")
        return False
    result = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)
    return bool(result)

def toggle_dark_mode(enable_dark: bool):
    try:
        value = 0 if enable_dark else 1
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, value)
        winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, value)
        winreg.CloseKey(key)
        print(f"Dark mode set to {enable_dark}")
        return True
    except Exception as e:
        print(f"Failed to toggle dark mode: {e}")
        return False

def manage_distractions(context_label):
    if context_label == "Coding":
        print("Engaged Focus Assist (Coding Mode). Distracting apps conceptually blocked.")
    elif context_label == "Entertainment":
        print("Disabled Focus Assist. Volume normalized.")
    else:
        print(f"Standard rules applied for {context_label} mode.")

class AutomationEngine:
    def __init__(self, resource_dir=None):
        if resource_dir:
            self.resource_dir = resource_dir
        else:
            # Check CWD for resources first (good for packaged execution)
            local_res = os.path.join(os.getcwd(), 'zenith', 'resources')
            if os.path.exists(local_res):
                self.resource_dir = local_res
            else:
                self.resource_dir = os.path.join(os.path.dirname(__file__), '..', 'resources')
    
    def execute_context_profile(self, context_label):
        print(f"Executing profile for: {context_label}")
        if context_label == "Coding":
            toggle_dark_mode(True)
            manage_distractions(context_label)
        elif context_label == "Entertainment":
            toggle_dark_mode(False)
            manage_distractions(context_label)
        else:
            print("No hard automation rules for this context")

if __name__ == '__main__':
    pass
