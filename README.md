# Pentos Game

A Tetris-like game featuring pentominoes - geometric game pieces composed of 5 squares.

## Installation

1. Ensure you have Python 3.8+ installed
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## How to Play

Run the game:
```
python main.py
```

### Controls
- Left/Right Arrow: Move piece horizontally
- Up Arrow: Rotate piece
- Down Arrow: Soft drop (accelerate descent)
- Space: Hard drop (instant placement)

### Scoring
- Single line: 100 points
- Double line: 300 points
- Triple line: 500 points
- Quadruple line: 700 points
- Pentos (5 lines): 800 points
- Back-to-back Pentos: 1200 points
- Soft drop: 1 point per cell dropped
- Hard drop: 2 points per cell dropped
