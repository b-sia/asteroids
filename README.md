# Asteroids

A modern interpretation of the classic Asteroids arcade game, built with Python and Pygame.
## Setup

### Prerequisites
- Python 3.8 or higher
- Pygame
- NumPy
- OpenSimplex

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/asteroids.git
cd asteroids
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt --no-cache-dir
or
uv pip install -r requirements.txt --no-cache-dir
```

4. Run the game:
```bash
python main.py
```

## Game Rules & Mechanics

### Controls
- **WASD Keys**: Control ship thrust and rotation
- **Space**: Fire weapon
- **ESC**: Exit game

### Gameplay Mechanics
- Player pilots a spaceship in an asteroid field
- Asteroids move with momentum and wrap around screen edges
- Shooting large asteroids splits them into smaller ones
- Smaller asteroids are worth more points
- Game ends if asteroids collide with the player's ship

### Scoring
- Large Asteroid: 20 points
- Medium Asteroid: 50 points
- Small Asteroid: 100 points
