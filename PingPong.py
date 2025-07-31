import tkinter as tk
import csv

root = tk.Tk()
root.title("Ping Pong Game")
root.resizable(False, False)
root.geometry("600x400")


class GUIandLogic():
    def __init__(self, main_loop):
        # Initialize the canvas for the game window with specified dimensions and background color
        self.canvas = tk.Canvas(root, width=600, height=400, bg="black")
        self.canvas.pack()
        
        # Create paddle 1 on the left side and paddle 2 on the right side
        self.paddle1 = self.canvas.create_rectangle(10, 150, 20, 250, fill="white")
        self.paddle2 = self.canvas.create_rectangle(580, 150, 590, 250, fill="white")
        
        # Create the ball at the center of the canvas
        self.ball = self.canvas.create_oval(290, 190, 310, 210, fill="red")
        
        # Initialize player scores
        self.player1_score = 0
        self.player2_score = 0
        
        # Initialize ball velocity in x and y directions (pixels per 10ms)
        self.x_velocity = 0.3
        self.y_velocity = 0.3
        
        # Create a text object to display scores at the top center of the canvas
        self.scoredisplay = self.canvas.create_text(
            300, 50, text=f"{self.player1_score} - {self.player2_score}",
            fill="yellow", font=("Helvetica", 24)
        )
        
        # Paddle speed in pixels per move
        self.ps = 20
        
        # Collision flag to manage ball-paddle collision timing
        self.collision_flag = False
        
        # Initialize coordinates for paddle and ball positions
        self.paddle1top = [self.canvas.coords(self.paddle1)[2], self.canvas.coords(self.paddle1)[1]]
        self.paddle1bottom = [self.canvas.coords(self.paddle1)[2], self.canvas.coords(self.paddle1)[3]]
        self.paddle2top = [self.canvas.coords(self.paddle2)[0], self.canvas.coords(self.paddle2)[1]]
        self.paddle2bottom = [self.canvas.coords(self.paddle2)[0], self.canvas.coords(self.paddle2)[3]]
        self.ballMiddleLeft = [
            self.canvas.coords(self.ball)[0],
            self.canvas.coords(self.ball)[3] - ((self.canvas.coords(self.ball)[3] - self.canvas.coords(self.ball)[1])/2)
        ]
        self.ballMiddleRight = [
            self.canvas.coords(self.ball)[2],
            self.canvas.coords(self.ball)[3] - ((self.canvas.coords(self.ball)[3] - self.canvas.coords(self.ball)[1])/2)
        ]
        self.ballTopMiddle = [
            self.canvas.coords(self.ball)[2] - ((self.canvas.coords(self.ball)[2] - self.canvas.coords(self.ball)[0])/2),
            self.canvas.coords(self.ball)[1]
        ]
        self.ballBottomMiddle = [
            self.canvas.coords(self.ball)[2] - ((self.canvas.coords(self.ball)[2] - self.canvas.coords(self.ball)[0])/2),
            self.canvas.coords(self.ball)[3]
        ]
        
        # Start the ball movement logic and collision detection
        self.update_ball_position()
        self.collision()
        
        # Initialize paddle movement flags for both players
        self.p1_up = False
        self.p1_down = False
        self.p2_up = False
        self.p2_down = False
        
        # Start the paddle movement logic
        self.move_paddles()


    # Sets the flag to move Player 1's paddle up when the corresponding key is pressed
    def moveup1(self, event):
        self.p1_up = True

    # Sets the flag to move Player 1's paddle down when the corresponding key is pressed
    def movedown1(self, event):
        self.p1_down = True

    # Sets the flag to move Player 2's paddle up when the corresponding key is pressed
    def moveup2(self, event):
        self.p2_up = True

    # Sets the flag to move Player 2's paddle down when the corresponding key is pressed
    def movedown2(self, event):
        self.p2_down = True

    # Stops moving Player 1's paddle up when the corresponding key is released
    def stop_moveup1(self, event):
        self.p1_up = False

    # Stops moving Player 1's paddle down when the corresponding key is released
    def stop_movedown1(self, event):
        self.p1_down = False

    # Stops moving Player 2's paddle up when the corresponding key is released
    def stop_moveup2(self, event):
        self.p2_up = False

    # Stops moving Player 2's paddle down when the corresponding key is released
    def stop_movedown2(self, event):
        self.p2_down = False

    def move_paddles(self):
        # Check if Player 1's paddle is moving up and within the canvas bounds
        if self.p1_up and self.canvas.coords(self.paddle1)[1] > 0:
            self.canvas.move(self.paddle1, 0, -self.ps)  # Move paddle 1 up by paddle speed

        # Check if Player 1's paddle is moving down and within the canvas bounds
        if self.p1_down and self.canvas.coords(self.paddle1)[3] < 400:
            self.canvas.move(self.paddle1, 0, self.ps)  # Move paddle 1 down by paddle speed

        # Check if Player 2's paddle is moving up and within the canvas bounds
        if self.p2_up and self.canvas.coords(self.paddle2)[1] > 0:
            self.canvas.move(self.paddle2, 0, -self.ps)  # Move paddle 2 up by paddle speed

        # Check if Player 2's paddle is moving down and within the canvas bounds
        if self.p2_down and self.canvas.coords(self.paddle2)[3] < 400:
            self.canvas.move(self.paddle2, 0, self.ps)  # Move paddle 2 down by paddle speed

        # Schedule the method to run again after 20 milliseconds to enable continuous movement
        root.after(20, self.move_paddles)


    # Updates the ball's velocity based on the type of collision.
    # 'w' indicates a collision with the wall, and 'p' indicates a collision with a paddle.
    def update_velocity(self, x):
        if x == "w":  # If the ball hits the wall, reverse the vertical velocity (y)
            self.y_velocity *= -1
        elif x == "p":  # If the ball hits a paddle, reverse the horizontal velocity (x)
            self.x_velocity *= -1

    # Updates the coordinates of the paddles after each movement, 
    # to reflect the current positions of the top and bottom edges of both paddles.
    def update_paddle_points(self):
        # Update paddle 1 coordinates (left paddle)
        self.paddle1top = [self.canvas.coords(self.paddle1)[2], self.canvas.coords(self.paddle1)[1]]
        self.paddle1bottom = [self.canvas.coords(self.paddle1)[2], self.canvas.coords(self.paddle1)[3]]
        
        # Update paddle 2 coordinates (right paddle)
        self.paddle2top = [self.canvas.coords(self.paddle2)[0], self.canvas.coords(self.paddle2)[1]]
        self.paddle2bottom = [self.canvas.coords(self.paddle2)[0], self.canvas.coords(self.paddle2)[3]]
    # Updates the coordinates of the ball's various key points (middle-left, middle-right, top-middle, and bottom-middle).
    # These points are used to determine collisions with paddles and walls.

    def update_ball_points(self):
        # Calculate the middle-left point of the ball (horizontal center, bottom edge)
        self.ballMiddleLeft = [
            self.canvas.coords(self.ball)[0],  # X-coordinate of the left edge of the ball
            self.canvas.coords(self.ball)[3] - ((self.canvas.coords(self.ball)[3] - self.canvas.coords(self.ball)[1]) / 2)  # Vertical center of the ball
        ]
        
        # Calculate the middle-right point of the ball (horizontal center, bottom edge)
        self.ballMiddleRight = [
            self.canvas.coords(self.ball)[2],  # X-coordinate of the right edge of the ball
            self.canvas.coords(self.ball)[3] - ((self.canvas.coords(self.ball)[3] - self.canvas.coords(self.ball)[1]) / 2)  # Vertical center of the ball
        ]
        
        # Calculate the top-middle point of the ball (horizontal center, top edge)
        self.ballTopMiddle = [
            self.canvas.coords(self.ball)[2] - ((self.canvas.coords(self.ball)[2] - self.canvas.coords(self.ball)[0]) / 2),  # Horizontal center of the ball
            self.canvas.coords(self.ball)[1]  # Y-coordinate of the top edge of the ball
        ]
        
        # Calculate the bottom-middle point of the ball (horizontal center, bottom edge)
        self.ballBottomMiddle = [
            self.canvas.coords(self.ball)[2] - ((self.canvas.coords(self.ball)[2] - self.canvas.coords(self.ball)[0]) / 2),  # Horizontal center of the ball
            self.canvas.coords(self.ball)[3]  # Y-coordinate of the bottom edge of the ball
        ]


    # Moves the ball by the current velocity (scaled by 10) and updates the ball's position.
    # This function is called continuously to animate the ball's movement.
    def update_ball_position(self):
        # Move the ball on the canvas based on the current x and y velocity
        self.canvas.move(self.ball, self.x_velocity * 10, self.y_velocity * 10)
        
        # Update the ball's key points after moving
        self.update_ball_points()
        
        # Call this function again after 10ms to create a continuous animation loop
        root.after(10, self.update_ball_position)

    # Resets the collision flag after a brief delay, preventing multiple collisions in quick succession.
    def reset_collision_flag(self):
        # Resets the collision flag after a brief delay.
        self.collision_flag = False

    # Checks if either player has reached the winning score (10 points).
    # If a player has won, it calls the `declare_winner` method.
    def check_winner(self):
        if self.player1_score == 10:
            self.declare_winner("Player 1")  # Declare Player 1 as the winner
        elif self.player2_score == 10:
            self.declare_winner("Player 2")  # Declare Player 2 as the winner

    # Ends the game and displays a winner message. Stops the ball and saves the game data.
    def declare_winner(self, winner):
        self.game_over = True  # Set the game over flag to True
        # Display the winner's message in the center of the canvas
        self.canvas.create_text(300, 200, text=f"{winner} Wins!", fill="yellow", font=("Helvetica", 32))
        self.canvas.delete(self.ball)  # Remove the ball from the canvas (game over)
        
        # Save the final game scores to a file for record keeping
        self.save_game_data()


    # Checks for collisions between the ball and walls or paddles, and updates the ball's velocity accordingly.
    # This method also resets the ball's position if it goes out of bounds, and updates the score.
    def collision(self):
        # Get the current coordinates of the ball and paddles
        ball_coords = self.canvas.coords(self.ball)
        paddle1_coords = self.canvas.coords(self.paddle1)
        paddle2_coords = self.canvas.coords(self.paddle2)

        # Check for collision with the top or bottom wall (boundary of the canvas)
        if ball_coords[1] < 0 or ball_coords[3] > 400:
            self.update_velocity("w")  # Reverse the ball's vertical direction if it hits a wall

        # Check for collision with Paddle 1 (left paddle)
        if not self.collision_flag:  # Ensure that the flag is not set (to prevent multiple collisions)
            if (ball_coords[0] <= paddle1_coords[2]  # Ball's left edge is touching paddle 1
                    and paddle1_coords[1] <= ball_coords[3] <= paddle1_coords[3]):  # Ball is within paddle 1's vertical range
                self.update_velocity("p")  # Reverse the ball's horizontal direction (paddle collision)
                
                # Slightly increase the ball's speed after every paddle hit
                self.x_velocity += (abs(self.x_velocity) / self.x_velocity) * (0.01)
                self.y_velocity += (abs(self.y_velocity) / self.y_velocity) * (0.01)
                
                self.collision_flag = True  # Set the collision flag to prevent multiple detections
                root.after(1000, self.reset_collision_flag)  # Reset the collision flag after 1 second

        # Check for collision with Paddle 2 (right paddle)
        if not self.collision_flag:  # Ensure that the flag is not set (to prevent multiple collisions)
            if (ball_coords[2] >= paddle2_coords[0]  # Ball's right edge is touching paddle 2
                    and paddle2_coords[1] <= ball_coords[3] <= paddle2_coords[3]):  # Ball is within paddle 2's vertical range
                self.update_velocity("p")  # Reverse the ball's horizontal direction (paddle collision)
                
                # Slightly increase the ball's speed after every paddle hit
                self.x_velocity += (abs(self.x_velocity) / self.x_velocity) * (0.01)
                self.y_velocity += (abs(self.y_velocity) / self.y_velocity) * (0.01)
                
                self.collision_flag = True  # Set the collision flag to prevent multiple detections
                root.after(1000, self.reset_collision_flag)  # Reset the collision flag after 1 second

        # Check if the ball has gone out of bounds (left or right side of the screen)
        if ball_coords[0] < 0 or ball_coords[2] > 600:
            if ball_coords[0] < 0:  # Ball went past left side (Player 1 scores)
                self.player2_score += 1
            else:  # Ball went past right side (Player 2 scores)
                self.player1_score += 1
            
            # Update the displayed score after a point is scored
            self.canvas.itemconfig(self.scoredisplay, text=f"{self.player1_score} - {self.player2_score}")
            
            # Check if either player has won the game
            self.check_winner()

            # Reset the ball's position to the center of the canvas
            self.canvas.coords(self.ball, 290, 190, 310, 210)

            # Reset the ball's velocity for the next round
            self.x_velocity, self.y_velocity = 0.3, 0.3

        # Continue checking for collisions every 10ms
        root.after(10, self.collision)


    # Saves the game data (scores) to a CSV file for record keeping.
    # It checks if the file already contains data and appends a new row with the current game results.
    def save_game_data(self):
        # Open the CSV file in read mode to check how many rows (games) are already recorded
        with open(r"D:\coding\VSCode\amrita\lab_eval\3\scores.csv", "r", newline="") as my_file:
            reader = csv.reader(my_file)
            num_rows = sum(1 for row in reader)  # Count the number of rows in the CSV file

        # Open the CSV file in append mode to add the new game data
        with open(r"D:\coding\VSCode\amrita\lab_eval\3\scores.csv", "a", newline="") as file:
            writer = csv.writer(file)
            
            # Set the game count (Game Number), which is equal to the number of previous games
            game_count = num_rows
            
            # If the file is empty (first game), write the header row with column names
            if num_rows == 0:
                writer.writerow(["Game Number", "Player 1 Score", "Player 2 Score"])
                game_count += 1  # Increment game count to start from 1 for the first game
            
            # Write the current game's data (game number, Player 1 score, Player 2 score)
            writer.writerow([game_count, self.player1_score, self.player2_score])


# Initialize the game logic and bind keys for paddle movement (up and down for both players).
run = GUIandLogic(root)

# Key press bindings to move paddles: 'w' and 's' for Player 1, 'Up' and 'Down' for Player 2.
root.bind("w", run.moveup1)      # Move Player 1's paddle up
root.bind("s", run.movedown1)    # Move Player 1's paddle down
root.bind('<Up>', run.moveup2)   # Move Player 2's paddle up
root.bind('<Down>', run.movedown2)  # Move Player 2's paddle down

# Key release bindings to stop paddle movement: when keys are released, stop the corresponding paddle movement.
root.bind("<KeyRelease-w>", run.stop_moveup1)    # Stop Player 1's paddle from moving up
root.bind("<KeyRelease-s>", run.stop_movedown1)  # Stop Player 1's paddle from moving down
root.bind("<KeyRelease-Up>", run.stop_moveup2)   # Stop Player 2's paddle from moving up
root.bind("<KeyRelease-Down>", run.stop_movedown2)  # Stop Player 2's paddle from moving down

# Start the Tkinter event loop to handle user input and update the game interface continuously.
root.mainloop()