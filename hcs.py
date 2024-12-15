import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hand Cricket")

# Colors and font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
font = pygame.font.Font(None, 50)

# Initialize sound mixer
pygame.mixer.init()

# Load sounds
try:
    SOUND_TOSS = pygame.mixer.Sound(r"C:\Users\icon\Downloads\coin-flip-88793.wav")
    SOUND_BAT = pygame.mixer.Sound(r"C:\Users\icon\Downloads\cricket_bat_sound.wav")
    SOUND_OUT = pygame.mixer.Sound(r"C:\Users\icon\Downloads\failure-1-89170.wav")
    SOUND_WIN = pygame.mixer.Sound(r"C:\Users\icon\Downloads\victorymale-version-230553.wav")
    SOUND_LOSE = pygame.mixer.Sound(r"C:\Users\icon\Downloads\crowd-shouting-hey-hey-hey-272059.wav")
except pygame.error as e:
    print(f"Error loading sounds: {e}")
    sys.exit()

def draw_text(text, color, y, center=True):
    """Helper function to draw text on the screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, y) if center else None)
    screen.blit(text_surface, text_rect if center else (50, y))

def show_message(message, sub_message=""):
    """Displays a message and waits for a moment."""
    screen.fill(WHITE)
    draw_text(message, BLACK, HEIGHT // 2)
    if sub_message:
        draw_text(sub_message, BLACK, HEIGHT // 2 + 50)
    pygame.display.flip()
    pygame.time.wait(2000)

def toss():
    """Handles the toss logic."""
    screen.fill(WHITE)
    draw_text("Toss: Press H for Heads or T for Tails", BLUE, HEIGHT // 3)
    pygame.display.flip()

    user_choice = None
    while user_choice is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    user_choice = "Heads"
                elif event.key == pygame.K_t:
                    user_choice = "Tails"

    toss_result = random.choice(["Heads", "Tails"])
    SOUND_TOSS.play()
    winner = "You" if user_choice == toss_result else "Computer"

    screen.fill(WHITE)
    draw_text(f"Toss result: {toss_result}", BLACK, HEIGHT // 3)
    draw_text(f"{winner} won the toss!", GREEN, HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(2000)

    if winner == "You":
        screen.fill(WHITE)
        draw_text("Press B to Bat or O to Bowl", BLUE, HEIGHT // 2)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        return "bat"
                    elif event.key == pygame.K_o:
                        return "bowl"
    else:
        decision = random.choice(["bat", "bowl"])
        show_message("Computer chooses to " + decision + " first!")
        return decision

def play_innings(player, target=None):
    """Plays an innings."""
    score = 0
    while True:
        # Display score and prompt
        screen.fill(WHITE)
        draw_text(f"{player}'s Turn", BLACK, HEIGHT // 4)
        draw_text(f"Score: {score}", BLACK, HEIGHT // 3)
        draw_text("Press a number key (1-6)", BLUE, HEIGHT // 2)
        pygame.display.flip()

        user_input = None
        while user_input is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_6:
                        user_input = event.key - pygame.K_0

        comp_input = random.randint(1, 6)

        # Show computer's choice
        screen.fill(WHITE)
        draw_text(f"Computer chose: {comp_input}", BLACK, HEIGHT // 2)
        pygame.display.flip()
        pygame.time.wait(1000)

        if user_input == comp_input:
            SOUND_OUT.play()
            show_message(f"{player} is OUT!", f"Final Score: {score}")
            break

        SOUND_BAT.play()
        score += user_input if player == "You" else comp_input

        if target and score > target:
            show_message(f"{player} has achieved the target!", f"Final Score: {score}")
            break

    return score

def hand_cricket():
    """Main game function."""
    show_message("Welcome to Hand Cricket!", "Press any key to start.")
    pygame.event.clear()

    while True:
        # Toss
        user_first = toss() == "bat"

        # First innings
        if user_first:
            show_message("You are batting first!")
            user_score = play_innings("You")
            show_message(f"Your total score: {user_score}")
            show_message("Computer is batting now!")
            computer_score = play_innings("Computer", target=user_score)
        else:
            show_message("Computer is batting first!")
            computer_score = play_innings("Computer")
            show_message(f"Computer's total score: {computer_score}")
            show_message("You are batting now!")
            user_score = play_innings("You", target=computer_score)

        # Determine winner
        if user_score > computer_score:
            SOUND_WIN.play()
            show_message("Congratulations! You win!")
        elif user_score < computer_score:
            SOUND_LOSE.play()
            show_message("You lose! Better luck next time!")
        else:
            show_message("It's a tie!")

        # Replay prompt
        screen.fill(WHITE)
        draw_text("Press R to Replay or Q to Quit", BLUE, HEIGHT // 2)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return hand_cricket()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

# Run the game
hand_cricket()
