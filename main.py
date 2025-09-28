import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Blackjack")

# Load images (background, card back, etc.)
background = pygame.image.load(os.path.join("images", "background.png"))
background = pygame.transform.scale(background, (screen_width, screen_height))

card_back = pygame.image.load(os.path.join("images", "back.png"))
card_back = pygame.transform.scale(card_back, (100, 150))  # Adjust size of card back

# Load sound (card sound)
card_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "card-sound.wav"))

# Load card images (example for hearts)
def load_card_image(rank, suit):
    # Special case for Ace
    if rank == 1:
        rank = "ace"
    elif rank == 11:
        rank = "jack"
    elif rank == 12:
        rank = "queen"
    elif rank == 13:
        rank = "king"

    card_image = pygame.image.load(os.path.join("images", suit, f"{rank}-{suit}.png"))
    return pygame.transform.scale(card_image, (100, 150))  # Adjust card size


# Game variables
game_num = 0
player_win = 0
dealer_win = 0
game_ties = 0
player_hand = 0
dealer_hand = 0
current_game_in_progress = False  # Flag to track if the game is in progress
player_cards = []  # List to keep track of the player's cards
dealer_cards = []

def print_game_stats():
    total_games = player_win + dealer_win + game_ties
    print(f"Number of Player wins: {player_win}")
    print(f"Number of Dealer wins: {dealer_win}")
    print(f"Number of tie games: {game_ties}")
    print(f"Total # of games played is: {total_games}")
    if total_games > 0:
        percent_of_player_wins = (player_win / total_games) * 100
        print(f"Percentage of Player wins: {percent_of_player_wins:.1f}%")
    print()

def draw_text(text, position, font_size=24):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, (255, 255, 255))  # White text
    screen.blit(text_surface, position)

def calculate_hand_value(cards):
    """ Calculate the total value of the hand (Ace = 1 or 11, face cards = 10). """
    value = 0
    ace_count = 0
    for card in cards:
        card_rank = card[0]  # The first value in card is rank
        if card_rank == 1:
            value += 11  # Ace starts as 11
            ace_count += 1
        elif card_rank > 10:
            value += 10  # Face cards (Jack, Queen, King) are worth 10
        else:
            value += card_rank  # Cards 2-10 are worth their face value

    # Adjust for Aces (Ace = 11 or Ace = 1)
    while value > 21 and ace_count > 0:
        value -= 10  # Convert Ace from 11 to 1
        ace_count -= 1

    return value


# Main game loop
in_progress = True  # Set this to True to start the game
while in_progress:
    if not current_game_in_progress:  # Only start a new game when not in progress
        game_num += 1
        print(f"START GAME #{game_num}")

        # Reset player hand for new game
        player_hand = 0
        dealer_hand = 0
        player_cards = []  # Reset player's cards
        dealer_cards = []  # Reset dealer's cards

        # Randomly choose a card for the player
        player_card = random.randint(1, 13)  # Card from 1 to 13
        player_suit = random.choice(['hearts', 'diamonds', 'spades', 'clubs'])

        # Load the player's first card image and play the sound
        player_card_image = load_card_image(player_card, player_suit)
        card_sound.play()

        # Add the card to player's hand
        player_cards.append((player_card, player_suit))  # Save the card rank and suit
        player_hand = calculate_hand_value(player_cards)

        #dealer
        # Randomly choose a card for the dealer
        dealer_card = random.randint(1, 13)
        dealer_suit = random.choice(['hearts', 'diamonds', 'spades', 'clubs'])

        # Add the dealer's first card to the dealer's hand
        dealer_cards.append((dealer_card, dealer_suit))  # Save the card rank and suit

        # Randomly choose a card for the dealer (face-down card)
        dealer_card = random.randint(1, 13)
        dealer_suit = random.choice(['hearts', 'diamonds', 'spades', 'clubs'])

        # Set the game state to in progress
        current_game_in_progress = True

    # Draw the background only once for each game
    screen.blit(background, (0, 0))

    # Draw game options
    draw_text("1. Draw Card", (20, 20))
    draw_text("2. Hold Hand", (20, 50))
    draw_text("3. Print Stats", (20, 80))
    draw_text("4. Exit", (20, 110))

    # Draw player's cards in the middle
    card_spacing = 120  # Adjust the spacing between cards
    start_x = (screen_width - len(player_cards) * card_spacing) // 2  # Calculate the starting X position to center cards
    for idx, card in enumerate(player_cards):
        x_pos = start_x + idx * card_spacing  # Calculate X position for each card
        screen.blit(load_card_image(card[0], card[1]), (x_pos, screen_height - 180))  # Draw the card

    # Draw dealer's cards in the same way as the player's cards (centered and spaced evenly)
    # Draw dealer's cards (all face-down)
    card_spacing = 120  # Adjust the spacing between cards
    start_x = (screen_width - len(
        dealer_cards) * card_spacing) // 2  # Calculate the starting X position to center the cards

    for idx, card in enumerate(dealer_cards):
        x_pos = start_x + idx * card_spacing  # Calculate X position for each card
        screen.blit(card_back, (x_pos, 50))  # Draw every card as face-down

    # Adjust the Y position for the player's hand score text
    draw_text(f"Your hand: {player_hand}", (screen_width - 150, screen_height - 230))

    # Display updated screen
    pygame.display.flip()

    # Wait for user input with no delay (this part was previously delayed)
    choice = None
    while choice not in [1, 2, 3, 4]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_progress = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choice = 1
                elif event.key == pygame.K_2:
                    choice = 2
                elif event.key == pygame.K_3:
                    choice = 3
                elif event.key == pygame.K_4:
                    choice = 4
        pygame.time.wait(50)  # Small delay just to keep the loop responsive

    if choice == 1:  # Draw another card
        card_sound.play()

        # Player draws a card
        player_card = random.randint(1, 13)
        player_suit = random.choice(['hearts', 'diamonds', 'spades', 'clubs'])
        player_card_image = load_card_image(player_card, player_suit)
        player_cards.append((player_card, player_suit))  # Save the card rank and suit
        player_hand = calculate_hand_value(player_cards)

        # Dealer draws a card
        dealer_card = random.randint(1, 13)
        dealer_suit = random.choice(['hearts', 'diamonds', 'spades', 'clubs'])
        dealer_cards.append((dealer_card, dealer_suit))  # Add card to dealer's hand

        # Check if player hits 21 and automatically wins
        if player_hand == 21:
            player_win += 1
            draw_text("You hit 21! You win automatically!", (300, 300))
            pygame.display.flip()
            pygame.time.wait(1000)  # Shortened automatic win delay
            current_game_in_progress = False

        # Check if player exceeds 21 and loses
        elif player_hand > 21:
            dealer_win += 1
            draw_text("You exceeded 21! You lose.", (300, 300))
            pygame.display.flip()
            pygame.time.wait(1000)  # Wait before starting new game
            current_game_in_progress = False

    elif choice == 2:  # Hold hand
        # Dealer's play
        dealer_hand = random.randint(17, 23)  # Dealer draws between 17 and 23
        screen.blit(background, (0, 0))  # Clear screen
        # Redraw dealer's face-up card
        screen.blit(load_card_image(dealer_card, dealer_suit), (screen_width // 2 - 50, 50))  # Dealer's card
        # Redraw player's cards centered
        for idx, card in enumerate(player_cards):
            x_pos = start_x + idx * card_spacing  # Calculate the X position for centered cards
            screen.blit(load_card_image(card[0], card[1]), (x_pos, screen_height - 180))  # Draw player cards

        # Display hands
        draw_text(f"Dealer's hand: {dealer_hand}", (screen_width - 150, 50))
        draw_text(f"Your hand: {player_hand}", (screen_width - 150, screen_height - 180))

        # Determine winner
        if player_hand > 21:
            dealer_win += 1
            draw_text("You exceeded 21! You lose.", (300, 300))
        elif player_hand == 21:
            player_win += 1
            draw_text("You win with Blackjack!", (300, 300))
        elif dealer_hand > 21 or player_hand > dealer_hand:
            player_win += 1
            draw_text("You win!", (300, 300))
        elif player_hand == dealer_hand:
            game_ties += 1
            draw_text("It's a tie!", (300, 300))
        else:
            dealer_win += 1
            draw_text("Dealer wins!", (300, 300))

        player_cards.clear()  # Clear the player's cards for the next game
        dealer_cards.clear()  # Clear the dealer's cards for the next game

        pygame.display.flip()
        pygame.time.wait(1000)  # Wait before starting a new game
        current_game_in_progress = False

    elif choice == 3:  # Print stats
        print_game_stats()

    elif choice == 4:  # Exit
        in_progress = False
        pygame.quit()
