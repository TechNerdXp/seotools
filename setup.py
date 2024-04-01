import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

if __name__ == "__main__":
    create_directory('data/input')
    create_directory('data/compressed')
    create_directory('data/specs')
    create_directory('data/failed')
