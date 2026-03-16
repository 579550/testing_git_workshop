#!/usr/bin/env python3
"""
A simple Snake game using curses library.
Use arrow keys to control the snake. Eat food (*) to grow.
Press 'q' to quit.
"""

import curses
import random
import time

def main(stdscr):
    # Setup
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100) # Refresh rate (ms)
    
    # Get screen dimensions
    sh, sw = stdscr.getmaxyx()
    
    # Create game window
    win = curses.newwin(sh, sw, 0, 0)
    win.keypad(1)
    win.timeout(100)
    
    # Initialize snake in the middle of screen
    snake_y = sh // 2
    snake_x = sw // 4
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]
    
    # Initial food position
    food = [sh // 2, sw // 2]
    win.addch(food[0], food[1], '*')
    
    # Initial direction (moving right)
    key = curses.KEY_RIGHT
    
    score = 0
    
    while True:
        # Display score
        win.addstr(0, 2, f' Score: {score} ')
        win.addstr(0, sw - 20, ' Press q to quit ')
        
        # Get next key press
        next_key = win.getch()
        
        # Quit on 'q'
        if next_key == ord('q'):
            break
        
        # Update direction (prevent 180-degree turns)
        if next_key != -1:
            if next_key == curses.KEY_UP and key != curses.KEY_DOWN:
                key = next_key
            elif next_key == curses.KEY_DOWN and key != curses.KEY_UP:
                key = next_key
            elif next_key == curses.KEY_LEFT and key != curses.KEY_RIGHT:
                key = next_key
            elif next_key == curses.KEY_RIGHT and key != curses.KEY_LEFT:
                key = next_key
        
        # Calculate new head position
        head = snake[0].copy()
        if key == curses.KEY_UP:
            head[0] -= 1
        elif key == curses.KEY_DOWN:
            head[0] += 1
        elif key == curses.KEY_LEFT:
            head[1] -= 1
        elif key == curses.KEY_RIGHT:
            head[1] += 1
        
        # Check for collisions with walls
        if head[0] <= 0 or head[0] >= sh - 1:
            break
        if head[1] <= 0 or head[1] >= sw - 1:
            break
        
        # Check for collision with self
        if head in snake:
            break
        
        # Insert new head
        snake.insert(0, head)
        
        # Check if snake ate food
        if head == food:
            score += 10
            # Generate new food position
            while True:
                food = [
                    random.randint(2, sh - 2),
                    random.randint(2, sw - 2)
                ]
                if food not in snake:
                    break
            win.addch(food[0], food[1], '*')
        else:
            # Remove tail if no food eaten
            tail = snake.pop()
            win.addch(tail[0], tail[1], ' ')
        
        # Draw snake head
        win.addch(snake[0][0], snake[0][1], '#')
        
        # Draw snake body
        for segment in snake[1:]:
            win.addch(segment[0], segment[1], 'o')
    
    # Game over screen
    win.clear()
    game_over_msg = f"GAME OVER! Final Score: {score}"
    win.addstr(sh // 2, (sw - len(game_over_msg)) // 2, game_over_msg)
    win.addstr(sh // 2 + 2, (sw - 22) // 2, "Press any key to exit")
    win.nodelay(0)
    win.getch()

if __name__ == "__main__":
    print("Starting Snake Game...")
    print("Use arrow keys to move, 'q' to quit")
    print("Eat the food (*) to grow and score points!")
    time.sleep(1)
    curses.wrapper(main)
