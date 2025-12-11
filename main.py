import pygame
import os
from p1_random import P1Random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")

background = pygame.image.load(os.path.join("images", "background.png"))
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

card_back = pygame.image.load(os.path.join("images", "back.png"))
card_back = pygame.transform.scale(card_back, (100, 150))
deck_image = pygame.transform.scale(card_back, (80, 120))

card_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "card-sound.wav"))

rng = P1Random()

CARD_IMAGES = {}
suits = ['hearts', 'diamonds', 'spades', 'clubs']
for suit in suits:
    for rank in range(1, 14):
        rank_name = {1:"ace",11:"jack",12:"queen",13:"king"}.get(rank, str(rank))
        path = os.path.join("images", suit, f"{rank_name}-{suit}.png")
        CARD_IMAGES[(rank, suit)] = pygame.transform.scale(pygame.image.load(path), (100, 150))

player_win = dealer_win = game_ties = 0

def draw_text(text, pos, size=24, color=(255,255,255)):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    screen.blit(surface, pos)

def calculate_hand_value(cards):
    value, aces = 0, 0
    for rank, _ in cards:
        if rank == 1:
            value += 11
            aces += 1
        elif rank > 10:
            value += 10
        else:
            value += rank
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def draw_cards(cards, y_pos, hide_all=False):
    spacing = 120
    start_x = (SCREEN_WIDTH - len(cards)*spacing)//2
    for i, card in enumerate(cards):
        x = start_x + i*spacing
        if hide_all:
            screen.blit(card_back, (x, y_pos))
        else:
            screen.blit(CARD_IMAGES[card], (x, y_pos))

def print_stats():
    total = player_win + dealer_win + game_ties
    print(f"Player wins: {player_win}, Dealer wins: {dealer_win}, Ties: {game_ties}")
    if total > 0:
        print(f"Player win rate: {player_win/total*100:.1f}%\n")

def draw_random_card():
    rank = rng.next_int(13) + 1
    suit = suits[rng.next_int(4)]
    return (rank, suit)

def animate_draw(card, start_pos, end_pos, is_dealer=False):
    steps = 10
    dx = (end_pos[0]-start_pos[0])/steps
    dy = (end_pos[1]-start_pos[1])/steps
    for i in range(steps):
        screen.blit(background,(0,0))
        draw_text("1. Draw Card",(20,20))
        draw_text("2. Hold Hand",(20,50))
        draw_text("3. Print Stats",(20,80))
        draw_text("4. Exit",(20,110))
        draw_cards(player_cards, SCREEN_HEIGHT-180)
        draw_cards(dealer_cards, 50, hide_all=True)
        draw_text(f"Your hand: {calculate_hand_value(player_cards)}",(SCREEN_WIDTH-150, SCREEN_HEIGHT-230))
        screen.blit(deck_image,(SCREEN_WIDTH-100, SCREEN_HEIGHT//2-60))
        if is_dealer:
            screen.blit(card_back, (start_pos[0]+dx*i, start_pos[1]+dy*i))
        else:
            screen.blit(CARD_IMAGES[card], (start_pos[0]+dx*i, start_pos[1]+dy*i))
        pygame.display.flip()
        pygame.time.wait(30)

menu_positions = [(20, 20), (20, 50), (20, 80), (20, 110)]

running = True
current_game = False
player_cards, dealer_cards = [], []

while running:
    mouse_click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_click = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                choice = 1
            elif event.key == pygame.K_2:
                choice = 2
            elif event.key == pygame.K_3:
                choice = 3
            elif event.key == pygame.K_4:
                choice = 4

    if not current_game:
        player_cards = [draw_random_card()]
        dealer_cards = [draw_random_card()]
        current_game = True

    screen.blit(background,(0,0))
    draw_text("1. Draw Card", menu_positions[0])
    draw_text("2. Hold Hand", menu_positions[1])
    draw_text("3. Print Stats", menu_positions[2])
    draw_text("4. Exit", menu_positions[3])
    draw_cards(player_cards, SCREEN_HEIGHT-180)
    draw_cards(dealer_cards, 50, hide_all=True)
    draw_text(f"Your hand: {calculate_hand_value(player_cards)}", (SCREEN_WIDTH-150, SCREEN_HEIGHT-230))
    deck_rect = deck_image.get_rect(topright=(SCREEN_WIDTH-20, SCREEN_HEIGHT//2-60))
    screen.blit(deck_image, deck_rect)
    pygame.display.flip()

    choice = None
    while choice not in [1,2,3,4]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choice = 4
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choice = 1
                elif event.key == pygame.K_2:
                    choice = 2
                elif event.key == pygame.K_3:
                    choice = 3
                elif event.key == pygame.K_4:
                    choice = 4
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if deck_rect.collidepoint(event.pos):
                    choice = 1
        pygame.time.wait(50)

    if choice == 1:
        new_player_card = draw_random_card()
        player_cards.append(new_player_card)
        animate_draw(new_player_card,(SCREEN_WIDTH-100, SCREEN_HEIGHT//2-60),
                     ((SCREEN_WIDTH-120)//2 + (len(player_cards)-1)*120, SCREEN_HEIGHT-180))
        card_sound.play()

        new_dealer_card = draw_random_card()
        dealer_cards.append(new_dealer_card)
        animate_draw(new_dealer_card,(SCREEN_WIDTH-100, SCREEN_HEIGHT//2-60),
                     ((SCREEN_WIDTH-120)//2 + (len(dealer_cards)-1)*120, 50), is_dealer=True)
        card_sound.play()

        player_val = calculate_hand_value(player_cards)
        dealer_val = calculate_hand_value(dealer_cards)

        if player_val > 21:
            dealer_win += 1
            game_over_msg = "Bust! Dealer wins."
            current_game = False
        elif dealer_val > 21:
            player_win += 1
            game_over_msg = "Dealer bust! You win!"
            current_game = False
        elif player_val == 21:
            player_win += 1
            game_over_msg = "Blackjack! You win!"
            current_game = False
        elif dealer_val == 21:
            dealer_win += 1
            game_over_msg = "Dealer hits 21! Dealer wins."
            current_game = False
        else:
            game_over_msg = None

        if game_over_msg:
            screen.blit(background,(0,0))
            draw_cards(player_cards, SCREEN_HEIGHT-180)
            draw_cards(dealer_cards,50)
            draw_text(f"Your hand: {player_val}", (SCREEN_WIDTH-150, SCREEN_HEIGHT-230))
            draw_text(f"Dealer hand: {dealer_val}", (SCREEN_WIDTH-150,50))
            draw_text(game_over_msg, (300,300),36)
            pygame.display.flip()
            pygame.time.wait(3500)

    elif choice == 2:
        player_val = calculate_hand_value(player_cards)
        dealer_val = calculate_hand_value(dealer_cards)
        screen.blit(background,(0,0))
        draw_cards(player_cards, SCREEN_HEIGHT-180)
        draw_cards(dealer_cards,50)
        draw_text(f"Your hand: {player_val}", (SCREEN_WIDTH-150, SCREEN_HEIGHT-230))
        draw_text(f"Dealer hand: {dealer_val}", (SCREEN_WIDTH-150,50))
        if player_val > 21:
            dealer_win += 1
            result = "Bust! Dealer wins."
        elif dealer_val > 21 or player_val > dealer_val:
            player_win += 1
            result = "You win!"
        elif player_val == dealer_val:
            game_ties += 1
            result = "It's a tie!"
        else:
            dealer_win += 1
            result = "Dealer wins!"
        draw_text(result,(300,300),36)
        pygame.display.flip()
        pygame.time.wait(3500)
        current_game = False

    elif choice == 3:
        print_stats()

    elif choice == 4:
        running = False
        pygame.quit()
