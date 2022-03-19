# Plan

## Requirements

### Demo
*   Hard coded arena to demonstrate mechanics
*   Mechanics:
    *   Movement (left arrow/A and right arrow/D)
    *   Jump (up arrow/W/space)
    *   Explosion (C/J)
*   Erik should not go through the ground
*   Erik should not go through walls
*   Erik should not go through the bottom of blocks
*   Gravity exists

## System analysis

### Demo

#### Input
*   Keydown and keyup events

#### Output
*   Where Erik appears on the screen

#### Forumlae
*   Determine if a key is held
*   Determine speed changes from held keys
*   Determine position changes from speed
    *   Detect collisions

## Design

### Demo

Determine if a key is held - Lyle
Determine speed changes from held keys - Lyle

Determine position changes from speed - Pretty easy

Detect collisions - Sam
If they are colliding
    Move back to wall
    Set velocity to zero