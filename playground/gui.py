import pygame
import sys
import os

# Dodaje folder główny projektu do ścieżek Pythona
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import game.game as game

pygame.init()
screen = pygame.display.set_mode((800, 600)) # ekran pygame.RESIZEABLE mozna zmieniac rozmiar okna
font = pygame.font.SysFont("forte", 40) # tczionka pygame.font.get_fonts() by wyswietlic czcionki


clock = pygame.time.Clock() # fps 

players_button = pygame.Rect(400, 200, 250, 250) # X, Y,width, height rysuje prostokat
bots_button = pygame.Rect(100, 200, 250, 250)

def draw_menu():
    screen.fill((0, 120, 0)) # zapelnij ekran rgb

    pygame.draw.rect(screen, (200, 200, 200), players_button) # ekran, kolor, obiekt
    pygame.draw.rect(screen, (200, 200, 200), bots_button)

    p_text = font.render("Gra z graczami", True, (0, 0, 0)) # tekst, antyanalising always true, rgb 
    b_text = font.render("Gra z botami", True, (0, 0, 0))

    screen.blit(p_text, (players_button.x + 20, players_button.y + 20))
    screen.blit(b_text, (bots_button.x + 20, bots_button.y + 20))


game = game.Game()
def handle_click(pos):
    if players_button.collidepoint(pos):
        game.mode = "players"
        game.state = "game"
        print("Wybrano: players")

    elif bots_button.collidepoint(pos): # jezeli pos jest w srodku obiektu to wykonaj # tak sie tworzy przyciski
        game.mode = "bots"
        game.state = "game"
        print("Wybrano: bots")

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(event.pos) # event pos to jest x,y gdzie zostalo klikniete 

        

    if game.state == "menu":
        draw_menu()

    elif game.state == "game":
        screen.fill((0, 80, 0))
        text = font.render(f"Tryb: {game.mode}", True, (255, 255, 255))
        screen.blit(text, (200, 250))

    pygame.display.flip()
    clock.tick(60)