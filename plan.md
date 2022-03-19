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

Determine position changes from speed - Pretty easy (test for collision after)
Update x axis
Check x collision
Update y axis
Check y collision

Detect collisions - Sam
Check x collision
    For block in blocks on screen
        If the player and block collide in the x axis
            If the player has positive x velocity
                move player right to block left
            else player has negative x velocity
                move player left to block right
            Set x velocity to zero

Check y collision
    For block in blocks on screen
        If the player and block are colliding in the y axis
            If the player has positive y velocity
                move player bottom to block top
            else the player has negative y velocity
                move player top to block bottom
            Set y velocity