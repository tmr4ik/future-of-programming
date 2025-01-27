import numpy as np

# Define colors for each piece (R, G, B)
COLORS = {
    'F': (128, 0, 128),  # Purple
    'I': (0, 0, 255),    # Blue
    'L': (255, 165, 0),  # Orange
    'N': (0, 128, 128),  # Teal
    'P': (255, 192, 203),# Pink
    'T': (255, 255, 0),  # Yellow
    'U': (0, 255, 0),    # Green
    'V': (139, 69, 19),  # Light Brown
    'W': (173, 216, 230),# Light Blue
    'X': (255, 0, 0),    # Red
    'Y': (128, 128, 128),# Gray
    'Z': (165, 42, 42),  # Brown
}

# Define all pentomino shapes using numpy arrays
PENTOMINOES = {
    'F': np.array([
        [0, 1, 1],
        [1, 1, 0],
        [0, 1, 0]
    ]),
    'I': np.array([
        [1],
        [1],
        [1],
        [1],
        [1]
    ]),
    'L': np.array([
        [1, 0],
        [1, 0],
        [1, 0],
        [1, 1]
    ]),
    'N': np.array([
        [1, 0],
        [1, 0],
        [1, 1],
        [0, 1]
    ]),
    'P': np.array([
        [1, 1],
        [1, 1],
        [1, 0]
    ]),
    'T': np.array([
        [1, 1, 1],
        [0, 1, 0],
        [0, 1, 0]
    ]),
    'U': np.array([
        [1, 0, 1],
        [1, 1, 1]
    ]),
    'V': np.array([
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1]
    ]),
    'W': np.array([
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 1]
    ]),
    'X': np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]),
    'Y': np.array([
        [0, 1],
        [1, 1],
        [0, 1],
        [0, 1]
    ]),
    'Z': np.array([
        [1, 1, 0],
        [0, 1, 0],
        [0, 1, 1]
    ])
}

class Piece:
    def __init__(self, name):
        self.name = name
        self.shape = PENTOMINOES[name].copy()
        self.color = COLORS[name]
        self.rotation = 0
        self.x = 0
        self.y = 0
    
    def rotate(self):
        """Rotate the piece 90 degrees clockwise"""
        self.shape = np.rot90(self.shape, -1)
        self.rotation = (self.rotation + 1) % 4
    
    def get_shape(self):
        """Return the current shape of the piece"""
        return self.shape
    
    def get_width(self):
        """Return the width of the piece"""
        return self.shape.shape[1]
    
    def get_height(self):
        """Return the height of the piece"""
        return self.shape.shape[0]
