from pathlib import Path

def create_path(path):
    try:
        path = Path(path)
        return path
    except:
        print("Cannot create Path object")
        return None