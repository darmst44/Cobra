"""
Cobra Slime Elite
Made with PyGame
"""

import pygame, sys, time, random


# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

# Window size
frame_size_x = 720
frame_size_y = 480

# Checks for errors encountered
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Cobra Slime Elite')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

# Changed to list of food positions
food_positions = []
apple_count = 1  # Will be set by home screen

direction = 'RIGHT'
change_to = direction

score = 0


def spawn_food():
    """Spawn a new food item at a random position."""
    return [random.randrange(1, (frame_size_x//10)) * 10, 
            random.randrange(1, (frame_size_y//10)) * 10]


# Game Over
def game_over():
    my_font = pygame.font.SysFont('consolas', 90)
    small_font = pygame.font.SysFont('consolas', 30)
    
    while True:
        game_window.fill(black)
        
        # Game Over text
        game_over_surface = my_font.render('GAME OVER :(', True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
        game_window.blit(game_over_surface, game_over_rect)
        
        # Show final score
        show_score(2, red, 'consolas', 35)
        
        # Menu options
        restart_text = small_font.render('ENTER = Restart', True, white)
        home_text = small_font.render('H = Home Menu', True, white)
        quit_text = small_font.render('ESC = Quit', True, white)
        
        game_window.blit(restart_text, (frame_size_x/2 - restart_text.get_width()/2, 350))
        game_window.blit(home_text, (frame_size_x/2 - home_text.get_width()/2, 390))
        game_window.blit(quit_text, (frame_size_x/2 - quit_text.get_width()/2, 430))
        
        pygame.display.flip()
        
        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 'restart'
                if event.key == pygame.K_h:
                    return 'home'
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    elif choice == 2:
        score_rect.midtop = (frame_size_x/2, frame_size_y/2 - 30)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)


# Home Screen
def home_screen():
    menu_font = pygame.font.SysFont('consolas', 50)
    small_font = pygame.font.SysFont('consolas', 30)

    # Difficulty setup
    difficulties = {
        "Easy": 10,
        "Medium": 25,
        "Hard": 40,
        "Harder": 60,
        "Impossible": 120
    }
    diff_names = list(difficulties.keys())
    diff_index = diff_names.index("Medium")

    # Apple count selection
    apple_count = 1  # 1 to 3

    while True:
        game_window.fill(black)

        # Title
        title_surface = menu_font.render("Cobra Slime Elite", True, green)
        game_window.blit(title_surface, (frame_size_x/2 - title_surface.get_width()/2, 50))

        # Difficulty display
        diff_text = small_font.render(f"Difficulty: {diff_names[diff_index]}", True, white)
        game_window.blit(diff_text, (frame_size_x/2 - diff_text.get_width()/2, 170))

        # Apple Count display
        apple_text = small_font.render(f"Apples on Screen: {apple_count}", True, white)
        game_window.blit(apple_text, (frame_size_x/2 - apple_text.get_width()/2, 220))

        # Instructions
        instructions = [
            "LEFT / RIGHT = Change Difficulty",
            "UP / DOWN = Change Apple Count (1–3)",
            "ENTER = Start Game",
            "ESC = Quit"
        ]
        y = 300
        for line in instructions:
            txt = small_font.render(line, True, blue)
            game_window.blit(txt, (frame_size_x/2 - txt.get_width()/2, y))
            y += 35

        pygame.display.update()

        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # Quit
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Difficulty selection
                if event.key == pygame.K_LEFT:
                    diff_index = (diff_index - 1) % len(diff_names)
                if event.key == pygame.K_RIGHT:
                    diff_index = (diff_index + 1) % len(diff_names)

                # Apple count selection (1–3)
                if event.key == pygame.K_UP:
                    apple_count = min(3, apple_count + 1)
                if event.key == pygame.K_DOWN:
                    apple_count = max(1, apple_count - 1)

                # Start the game
                if event.key == pygame.K_RETURN:
                    return difficulties[diff_names[diff_index]], apple_count


# Main logic
while True:
    difficulty, apple_count = home_screen()

    # Reset game variables
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
    direction = 'RIGHT'
    change_to = direction
    score = 0
    
    # Initialize food positions based on apple_count
    food_positions = [spawn_food() for _ in range(apple_count)]

    # Game loop
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        
        # Check if snake ate any food
        food_eaten = False
        for i, food_pos in enumerate(food_positions):
            if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
                score += 1
                food_eaten = True
                # Respawn this food at a new location
                food_positions[i] = spawn_food()
                break
        
        # Remove tail if no food was eaten
        if not food_eaten:
            snake_body.pop()

        # GFX
        game_window.fill(black)
        for pos in snake_body:
            # Snake body
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Draw all food items
        for food_pos in food_positions:
            pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Game Over conditions
        # Getting out of bounds
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10 or snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
            result = game_over()
            if result == 'restart':
                game_running = False  # Break inner loop to restart
            elif result == 'home':
                game_running = False  # Break to go back to home screen
                break
        
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                result = game_over()
                if result == 'restart':
                    game_running = False  # Break inner loop to restart
                elif result == 'home':
                    game_running = False  # Break to go back to home screen
                    break

        # Display score and update screen
        show_score(1, white, 'consolas', 20)
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(difficulty)