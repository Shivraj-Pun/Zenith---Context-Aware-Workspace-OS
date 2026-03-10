import os
import threading
import sqlite3
import customtkinter as ctk
from zenith.core.listener import ZenithObserver
from zenith.ai.classifier import ContextClassifier
from zenith.automation.executor import AutomationEngine
from sqlalchemy.orm import sessionmaker
from zenith.db.models import get_engine, WindowLog

# --- App Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ZenithApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("Zenith OS")
        self.geometry("400x500")
        self.resizable(False, False)
        
        # Modules
        self.db_path = "zenith.db"
        self.observer = ZenithObserver(db_path=self.db_path, poll_interval=2.0)
        self.classifier = ContextClassifier(db_path=self.db_path)
        self.automation = AutomationEngine()
        
        # SQLAlchemy Session
        engine = get_engine(self.db_path)
        self.Session = sessionmaker(bind=engine)
        
        self.current_context = "Scanning..."
        
        self._build_ui()
        
        # Start background listener
        self.observer.start()
        
        # Start UI loop
        self.after(2000, self._update_loop)

    def _build_ui(self):
        # Title
        self.title_label = ctk.CTkLabel(self, text="Zenith Workspace OS", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(30, 10))
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(self, text="AI Context Awareness Active", text_color="gray")
        self.subtitle_label.pack(pady=(0, 20))
        
        # Context Display Concept (iOS inspired large card)
        self.context_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#2B2B2B", width=300, height=150)
        self.context_frame.pack(pady=20, padx=20, fill="both")
        self.context_frame.pack_propagate(False)
        
        self.mode_title = ctk.CTkLabel(self.context_frame, text="Current Context", font=ctk.CTkFont(size=14))
        self.mode_title.pack(pady=(20, 5))
        
        self.mode_value = ctk.CTkLabel(self.context_frame, text=self.current_context, font=ctk.CTkFont(size=32, weight="bold"), text_color="#00A8FF")
        self.mode_value.pack(pady=(5, 20))
        
        # Current active window title display
        self.window_info = ctk.CTkLabel(self, text="Active: waiting...", font=ctk.CTkFont(size=12), text_color="gray", wraplength=350)
        self.window_info.pack(pady=10)
        
        # Manual Force Buttons
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.pack(pady=10)
        
        self.btn_code = ctk.CTkButton(self.buttons_frame, text="Force Coding", command=lambda: self._force_mode("Coding"), width=120)
        self.btn_code.pack(side="left", padx=10)
        
        self.btn_fun = ctk.CTkButton(self.buttons_frame, text="Force Entertain", command=lambda: self._force_mode("Entertainment"), width=120)
        self.btn_fun.pack(side="left", padx=10)

    def _force_mode(self, mode):
        self.current_context = mode
        self.mode_value.configure(text=mode)
        self.automation.execute_context_profile(mode)

    def _update_loop(self):
        session = self.Session()
        try:
            # Get latest window log
            latest_log = session.query(WindowLog).order_by(WindowLog.timestamp.desc()).first()
            if latest_log:
                win_title = latest_log.window_title
                # Truncate for UI
                display_title = (win_title[:45] + '...') if len(win_title) > 45 else win_title
                self.window_info.configure(text=f"Active: {display_title}")
                
                # Predict new context
                predicted = self.classifier.predict(win_title)
                
                if predicted != self.current_context:
                    self.current_context = predicted
                    self.mode_value.configure(text=predicted)
                    # Automatically trigger environment changes based on context change
                    self.automation.execute_context_profile(predicted)
        except Exception as e:
            print(f"UI Update error: {e}")
        finally:
            session.close()
            
        # Schedule next update
        self.after(2000, self._update_loop)

    def destroy(self):
        self.observer.stop()
        super().destroy()

if __name__ == "__main__":
    app = ZenithApp()
    app.mainloop()
