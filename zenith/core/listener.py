import time
import threading
import psutil
import pygetwindow as gw
from ctypes import Structure, windll, c_uint, sizeof, byref
from datetime import datetime
from zenith.db.models import init_db, get_engine, WindowLog
from sqlalchemy.orm import sessionmaker

class LASTINPUTINFO(Structure):
    _fields_ = [("cbSize", c_uint), ("dwTime", c_uint)]

def get_idle_duration():
    """Returns the system idle time in seconds for Windows."""
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    if windll.user32.GetLastInputInfo(byref(lastInputInfo)):
        millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
        return millis / 1000.0
    return 0

class ZenithObserver:
    def __init__(self, db_path='zenith.db', poll_interval=5.0, idle_threshold=300.0):
        self.db_path = db_path
        self.poll_interval = poll_interval
        self.idle_threshold = idle_threshold  # 5 minutes default
        self.running = False
        self._thread = None
        
        init_db(self.db_path)
        engine = get_engine(self.db_path)
        self.Session = sessionmaker(bind=engine)

    def _get_active_process_name(self, window):
        """Attempts to find process name for a window (best effort abstraction)."""
        # A more robust system would map HWND to PID.
        # For simplicity in this observer, we will focus on Window Title primarily.
        return None

    def start(self):
        if self.running: return
        self.running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        print("Zenith Observer Started.")

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join(timeout=2)
        print("Zenith Observer Stopped.")

    def _loop(self):
        session = self.Session()
        while self.running:
            try:
                idle_sec = get_idle_duration()
                if idle_sec >= self.idle_threshold:
                    # User is away
                    log = WindowLog(
                        window_title="[SYSTEM IDLE]",
                        process_name="Idle"
                    )
                else:
                    win = gw.getActiveWindow()
                    if win is not None and win.title.strip() != "":
                        title = win.title
                        log = WindowLog(
                            window_title=title,
                            process_name=None 
                        )
                    else:
                        log = None
                
                if log:
                    session.add(log)
                    session.commit()
            except Exception as e:
                print(f"Observer error: {e}")
                session.rollback()
                
            time.sleep(self.poll_interval)
        session.close()

if __name__ == '__main__':
    obs = ZenithObserver(poll_interval=2.0, idle_threshold=10)
    obs.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
