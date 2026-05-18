--- wrap textu 
def draw_menu():
    screen.fill((0, 120, 0))

    pygame.draw.rect(screen, (200, 200, 200), players_button)
    pygame.draw.rect(screen, (200, 200, 200), bots_button)

    p_text = "Gra z graczami"
    b_text = "Gra z botami"

    # --- PLAYER BUTTON TEXT ---
    lines = wrap_text(p_text, font, 200)

    y = players_button.y + 20
    for line in lines:
        rendered = font.render(line, True, (0, 0, 0))
        screen.blit(rendered, (players_button.x + 20, y))
        y += 35

    # --- BOTS BUTTON TEXT ---
    lines = wrap_text(b_text, font, 200)

    y = bots_button.y + 20
    for line in lines:
        rendered = font.render(line, True, (0, 0, 0))
        screen.blit(rendered, (bots_button.x + 20, y))
        y += 35

def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)
    return lines
if event.type == pygame.VIDEORESIZE:
        screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)