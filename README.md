# Zenith: Context-Aware Workspace OS

Zenith is a lightweight, context-aware desktop workspace optimizer that automatically adapts to what you are doing. It runs silently in the background, analyzing active window titles to infer your current activity (e.g., Coding, Browsing, Entertainment) and applies system-level automations to maximize your productivity.

## Features
- **Real-Time Context Detection**: Uses machine learning (`scikit-learn`) to classify your current active window and deduce the context.
- **Automated Workspaces**: Reacts dynamically to your workflow. E.g., launching IDEs triggers a "Coding" mode, opening a browser triggers "Browsing".
- **Local AI Parsing**: Employs an intelligent, lightweight Naive Bayes model trained locally on window titles for lightning-fast and private inference.
- **Customizable Actions**: Extendable automation engine capable of running system scripts, minimizing distractions, or adjusting volume based on the active mode.
- **Clean UI**: A sleek, dark-themed dashboard built with `customtkinter`.

## Tech Stack
- **Python 3.10+**
- **Machine Learning**: `scikit-learn`, `joblib`
- **Database**: `SQLAlchemy` (SQLite)
- **UI**: `customtkinter`
- **System Monitoring**: `pywin32`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Shivraj-Pun/Nexus-Flow.git
   cd Nexus-Flow
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   ```

3. Install requirements:
   *(Ensure to run `pip install customtkinter scikit-learn sqlalchemy pywin32 joblib` if `requirements.txt` is missing)*

4. Run the application:
   ```bash
   python main.py
   ```

## Usage
Simply launch the application. Zenith works entirely in the background. You can also monitor your active context using the provided `customtkinter` dashboard.
