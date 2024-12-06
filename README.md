# Pygame Cube Runner Game - IMU Controlled

This is an IMU pointer controlled version of the open source cube game by lioil987.

The file bleak_eval_client receives IMU data over UART including accelerometer, gyroscope, and magnetometer data.

When the player dies, the Bluetooth of the computer sends a command to the UART BLE peripheral to trigger an action - in our device, this is a light that turns red and a haptic feedback.

The speed and frequency of obstacles are adjusted for IMU control, and the gameplay is continuous when an obstacle is encountered.

## Game description by lioil987 as follows:

This Python script (`cube_game.py`) uses the Pygame library to create a simple cube runner game. The player controls a cube character that must navigate through obstacles while collecting points.

![Game Preview](preview/demo.gif)

## Features

- **Infinite Runner:** The game has an endless scrolling environment with randomly generated obstacles.
- **Player Controls:** Use the arrow keys to control the cube character (up, down, left, right).
- **Obstacle Generation:** Obstacles are randomly generated with varying sizes, colors, and speeds.
- **Scoring System:** The player scores points for successfully navigating through obstacles. The game keeps track of the player's score.

## Getting Started

1. **Install Dependencies:**
   - Make sure you have Python installed on your machine.
   - Install the Pygame library and colour using the following commands:
     ```bash
     pip install pygame
     pip install colour
     ```

2. **Run the Game:**
   - Execute the script using the following command:
     ```bash
     python cube_game.py
     ```

3. **Game Controls:**
   - Use the arrow keys to control the cube character:
     - UP: Move Up
     - DOWN: Move Down
     - LEFT: Move Left
     - RIGHT: Move Right

## Game Over and Restart

- The game ends when the cube collides with an obstacle.
- After a game over, you can restart the game by following the on-screen instructions.

## Customize the Game

- You can customize various aspects of the game, such as the number of obstacles, obstacle properties (size, speed, color), and more by modifying the `cube_game.py` script.


## Contributing

If you have suggestions or find issues with the game, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License
