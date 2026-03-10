import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Application(Base):
    """Stores distinct applications observed."""
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    
class Context(Base):
    """User-defined or ML-predicted contexts (e.g., 'Coding', 'Research')."""
    __tablename__ = 'contexts'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

class WindowLog(Base):
    """Logs the active window over time."""
    __tablename__ = 'window_logs'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    window_title = Column(String(500), nullable=True)
    process_name = Column(String(255), nullable=True)
    context_id = Column(Integer, ForeignKey('contexts.id'), nullable=True)

class Dataset(Base):
    """Training data for ML model."""
    __tablename__ = 'dataset'
    id = Column(Integer, primary_key=True)
    window_title = Column(String(500), nullable=False)
    context_label = Column(String(100), nullable=False)

def get_engine(db_path='zenith.db'):
    return create_engine(f'sqlite:///{db_path}', connect_args={'check_same_thread': False})

def init_db(db_path='zenith.db'):
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    
    # Pre-populate some base contexts as examples
    session = Session()
    default_contexts = ['Coding', 'Research', 'Entertainment', 'Idle']
    for ctx in default_contexts:
        if not session.query(Context).filter_by(name=ctx).first():
            session.add(Context(name=ctx))
    session.commit()
    session.close()

if __name__ == '__main__':
    init_db()
    print("Database Initialized.")
