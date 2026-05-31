# Dodge the Blocks

A progressive difficulty block-dodging game built with Pygame.

## Description

Dodge the Blocks is an endless survival game where you control a white square and must avoid falling blocks. The game features dynamic difficulty, multiple phases, special effects, and a final boss fight.

## Features

- Dynamic difficulty system with 9 block sizes (1x1 to 9x9)
- Day/Night cycle with visual effects (Day, Evening, Night)
- Color-coded blocks based on size
- Bullet hell phase (score 250+)
- Final Boss at score 500
- Device selection (Phone/Tablet/Desktop)
- High score saving

## Block Sizes & Colors

| Size | Color | Unlock Score |
|------|-------|--------------|
| 1x1 | Green | 0 |
| 2x2 | Yellow | 25 |
| 3x3 | Orange | 65 |
| 4x4 | Red | 75 |
| 5x5 | Light Purple | 100 |
| 6x6 | Dark Purple | 125 |
| 7x7 | Blue | 150 |
| 8x8 | Dark Blue | 175 |
| 9x9 | Brown | 200 |

## Game Phases

- **Score 0-25:** Day - Basic blocks
- **Score 25-65:** Evening - Medium blocks
- **Score 65+:** Night - Large blocks appear
- **Score 250+:** Bullet Hell - All blocks become small brown blocks that shoot pink bullets
- **Score 500:** Boss Fight - Giant 8x8 red boss with black veins, shoots 4 bullets per second!
- **Score 501:** YOU WIN!

## Controls

- Mouse movement or touch
- Arrow keys (Left/Right)
- A/D keys
- SPACE to start/restart

## Scoring

Points = Block size (n)
- Dodge a 1x1 block: 1 point
- Dodge a 9x9 block: 9 points

## Installation

1. Install Python 3.x
2. Install Pygame: `pip install pygame`
3. Run: `Block_Dodge.py`

## Author

**Amirmahdi Ghorbani**
https://github.com/AmirmahdiGhorbani2000

---

⭐ If you like this project, please consider giving it a star! Thank you for your support!
