#Importieren der Pygame-Bibliothek
import pygame
import random
import time #Wird zb für die Animation von Pacmans Mund verwendet
import csv
#import cProfile

#initialisieren von pygame
pygame.init()

# Titel
pygame.display.set_caption("Willkommen zu PacMan von Noé und Felix")

# Bildschirm Aktualisierungen einstellen
clock = pygame.time.Clock() #Für die FPS

# Labyrinth
layout = [
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1'],
    ['1', ' ', '1', '1', ' ', '1', '1', '1', ' ', '1', ' ', '1', '1', '1', ' ', '1', '1', ' ', '1'],
    ['1', ' ', '1', '1', ' ', '1', '1', '1', ' ', '1', ' ', '1', '1', '1', ' ', '1', '1', ' ', '1'],
    ['1', 'b', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b', '1'],
    ['1', ' ', '1', '1', ' ', '1', ' ', '1', '1', '1', '1', '1', ' ', '1', ' ', '1', '1', ' ', '1'],
    ['1', ' ', ' ', ' ', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', ' ', ' ', '1'],
    ['1', '1', '1', ' ', ' ', '1', ' ', ' ', ' ', 'p', ' ', ' ', ' ', '1', ' ', ' ', '1', '1', '1'],
    ['1', '1', '1', ' ', '1', '1', ' ', '1', '1', '-', '1', '1', ' ', '1', '1', ' ', '1', '1', '1'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', 'r', 'o', 't', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['1', '1', '1', ' ', '1', '1', ' ', '1', '1', '1', '1', '1', ' ', '1', '1', ' ', '1', '1', '1'],
    ['1', '1', '1', ' ', ' ', '1', ' ', ' ', ' ', 'b', ' ', ' ', ' ', '1', ' ', ' ', '1', '1', '1'],
    ['1', ' ', ' ', ' ', ' ', '1', ' ', '1', '1', '1', '1', '1', ' ', '1', ' ', ' ', ' ', ' ', '1'],
    ['1', ' ', '1', '1', ' ', ' ', ' ', ' ', '1', '1', '1', ' ', ' ', ' ', ' ', '1', '1', ' ', '1'],
    ['1', ' ', ' ', '1', ' ', '1', '1', ' ', ' ', ' ', ' ', ' ', '1', '1', ' ', '1', ' ', ' ', '1'],
    ['1', '1', 'b', '1', ' ', ' ', ' ', ' ', '1', '1', '1', ' ', ' ', ' ', ' ', '1', 'b', '1', '1'],
    ['1', '1', ' ', '1', '1', ' ', '1', ' ', '1', '1', '1', ' ', '1', ' ', '1', '1', ' ', '1', '1'],
    ['1', ' ', ' ', ' ', ' ', ' ', '1', ' ', ' ', 'S', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', '1'],
    ['1', ' ', '1', '1', '1', '1', '1', '1', '1', ' ', '1', '1', '1', '1', '1', '1', '1', ' ', '1'],
    ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
]

# Fenster öffnen, Spalten und Zeilen berechnen
#block = 30

#def calculate_window_size(settings):
    #block = settings["block"]
    # Berechnet die Fenstergröße basierend auf der Anzahl der Spalten und Zeilen
    #return block

#fenster_breite = len(layout[0]) * block
#fenster_hoehe = len(layout) * block
#screen = pygame.display.set_mode((fenster_breite, fenster_hoehe))

def load_images(settings):
    # Pacmanbilder
    pacman_offen = pygame.image.load('images/pacman-offen.png')
    pacman_geschlossen = pygame.image.load('images/pacman-geschlossen.png')

    # Skalieren der Pacman-Bilder auf die angegebenen Durchmesser
    pacman_offen = pygame.transform.scale(pacman_offen,
                                          (settings["pacman_durchmesser"], settings["pacman_durchmesser"]))
    pacman_geschlossen = pygame.transform.scale(pacman_geschlossen,
                                                (settings["pacman_durchmesser"], settings["pacman_durchmesser"]))

    # Geisterbilder
    geist_bilder = {
        "r": pygame.image.load('images/geist_rot.png'),
        "o": pygame.image.load('images/geist_orange.png'),
        "p": pygame.image.load('images/geist_pink.png'),
        "t": pygame.image.load('images/geist_tuerkis.png')
    }

    # Skalieren der Geisterbilder auf den angegebenen Durchmesser
    geist_bilder = {key: pygame.transform.scale(image, (settings["geist_durchmesser"], settings["geist_durchmesser"]))
                    for key, image in geist_bilder.items()}

    return pacman_offen, pacman_geschlossen, geist_bilder

# Funktion, um das Farben-Dictionary aus der CSV-Datei zu laden
def load_colors_from_csv(csv_file):
    farben = {}
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            color_name = row[0]
            rgb_values = tuple(map(int, row[1:]))
            farben[color_name] = rgb_values
    return farben
farben = load_colors_from_csv('farben.csv')

#Funktion zum Anzeigen des Startmenüs
def start_menu(screen, fenster_breite, fenster_hoehe):
    menu_font = pygame.font.Font(None, 64)
    option_font = pygame.font.Font(None, 46)

    #Texte
    titel_text = menu_font.render("Willkommen zu Pacman", True, farben["GELB"])
    start_text = option_font.render("Spiel Starten", True, farben["WEISS"])
    highscore_text = option_font.render("Highscore: ", True, farben["WEISS"])
    quit_text = option_font.render("Beenden", True, farben["WEISS"])


    #Hintergrundbild laden und anpassen
    background_image = pygame.image.load("images/background.png")
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

    options = ["start", "quit"]
    current_option = 0

    while True:
        screen.fill(farben["SCHWARZ"])
        screen.blit(titel_text, (fenster_breite // 2 - titel_text.get_width() // 2, fenster_hoehe // 4))
        screen.blit(background_image, (0, 0))

        #Optionen mit Farbänderung
        start_text_color = farben["GELB"] if current_option == 0 else farben["WEISS"]
        quit_text_color = farben["GELB"] if current_option == 1 else farben["WEISS"]
        highscore_text_color = farben["ROT"]
        letzter_highscore = lade_highscore("highscore.csv")  # Letzte Zeile der Datei

        screen.blit(option_font.render("Spiel Starten", True, start_text_color), (fenster_breite // 2 - start_text.get_width() // 2, fenster_hoehe // 2))
        screen.blit(option_font.render(f"Letzter Highscore: {letzter_highscore}", True, highscore_text_color),(fenster_breite // 2.5 - highscore_text.get_width() // 2, fenster_hoehe // 2 + 100))
        screen.blit(option_font.render("Beenden", True, quit_text_color), (fenster_breite // 2 - quit_text.get_width() // 2, fenster_hoehe // 2 + 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    current_option = (current_option + 1) % len(options)
                elif event.key == pygame.K_UP:
                    current_option = (current_option - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[current_option] == "start":
                        return "start"
                    pygame.quit()
                    quit()

        pygame.display.flip()
        clock.tick(60)

# Spielfeld Funktion zum Erstellen des Layouts
def gameboard(layout, block):
    wand_rechtecke = []  # Erstellen von Wänden aus dem Labyrinth
    for y, row in enumerate(layout):
        for x, cell in enumerate(row):
            if cell == '1':  # Wandposition im Layout
                wand_rechtecke.append(pygame.Rect(x * block, y * block, block, block))
    return wand_rechtecke

# Fenster öffnen, Spalten und Zeilen berechnen
def window(layout, block):
    fenster_breite = len(layout[0]) * block
    fenster_hoehe = len(layout) * block
    screen = pygame.display.set_mode((fenster_breite, fenster_hoehe))


    # wand_rechtecke mit dem Rückgabewert von spielfeld initialisieren
    wand_rechtecke = gameboard(layout, block)

    return screen, wand_rechtecke, fenster_breite, fenster_hoehe

#Suchen der Start position 'S' im Layout
def find_startposition(layout, block):
    for y, row in enumerate(layout):
        for x, cell in enumerate(row):
            if cell == 'S':
                #print(f"Startposition gefunden bei ({x}, {y})")
                return x * block, y * block
    #print("Keine Startposition gefunden!")  # Ausgabe, wenn keine 'S' gefunden wird
    return None

# PacMan Startposition setzen
def pacman_startposition(layout, block, pacman_durchmesser):
    pacman_position = find_startposition(layout, block)
    #print(f"Finde Startposition: {pacman_position}")
    #print(f"Pacman Durchmesser: {pacman_durchmesser}")

    #print(f"Startposition von Pacman: {pacman_position}")
    pacman_position = [pacman_position[0] + pacman_durchmesser // 2, pacman_position[1] + pacman_durchmesser // 2]
    #print(f"Berechnete Pacman-Position (Mittelpunkt): {pacman_position}")
    return pacman_position

    #print(f"Endgültige PacMan Startposition: {pacman_position}")

#Funktion um die Buchstaben für die jeweiligen Geister zu finden (r, o, p, t)
def find_ghost_positionen(layout, block):
    geister_positionen = {
        'r': None,
        'o': None,
        'p': None,
        't': None #Buchstaben haben noch keine x und y Koordinate
    }

    for y, row in enumerate(layout):
        for x, cell in enumerate(row):
            if cell in geister_positionen:  # Wenn der Buchstabe 'r', 'o', 'p' oder 't' gefunden wurde
                geister_positionen[cell] = (x * block + block // 2, y * block + block // 2)  # Speichern der Positionen
    return geister_positionen

def animated_pacman(richtung, pacman_durchmesser, pacman_offen, pacman_geschlossen):
    pacman_bild = pacman_offen if time.time() % 0.5 < 0.3 else pacman_geschlossen
    pacman_bild = rotate_pacman(pacman_bild, richtung, pacman_durchmesser)
    return pacman_bild

def rotate_pacman(pacman_bild, richtung, pacman_durchmesser):
    """Rotiert das PacMan-Bild basierend auf der Richtung und sorgt dafür, dass es um den Mittelpunkt rotiert."""

    # Bestimme den Winkel basierend auf der Richtung
    if richtung == 'rechts':
        winkel = 0
    elif richtung == 'oben':
        winkel = -90
    elif richtung == 'links':
        winkel = 180
    elif richtung == 'unten':
        winkel = 90
    else:
        return pacman_bild  # Rückgabe des Originalbildes, falls keine bekannte Richtung

    # Drehe das Bild
    rotated_image = pygame.transform.rotate(pacman_bild, winkel)

    # Berechne den neuen Rect, um den Mittelpunkt beizubehalten
    rotated_rect = rotated_image.get_rect(center=(pacman_durchmesser // 2, pacman_durchmesser // 2))

    return rotated_image

# Funktion, um einen Geist zu zeichnen
def draw_ghost(screen, geist, geist_durchmesser, geist_bilder):

    # Bild des Geistes auf die Position zeichnen
    screen.blit(geist_bilder[geist["farbe"]], (geist["position"][0] - geist_durchmesser // 2, geist["position"][1] - geist_durchmesser // 2)) #durch 2 für die Mitte des Blocks

# Geister initialisieren
def initialize_ghost(geister_positionen, geist_durchmesser):
    # Geister-Initialisierung als lokale Variable
    geister = [
        {"position": geister_positionen['r'], "farbe": 'r', "durchmesser": geist_durchmesser, "timer": 0},
        {"position": geister_positionen['o'], "farbe": 'o', "durchmesser": geist_durchmesser, "timer": 0},
        {"position": geister_positionen['p'], "farbe": 'p', "durchmesser": geist_durchmesser, "timer": 0},
        {"position": geister_positionen['t'], "farbe": 't', "durchmesser": geist_durchmesser, "timer": 0},
    ]
    return geister

#Pacman Bewegung und Kollisionsüberprüfung, deshalb so lange funktion
#(2 verschiedene Funktionen haben nicht funktioniert, dass er sich so smooth bewegt)
def move_pacman(pacman_richtung, pacman_position, pacman_bewegung, wand_rechtecke, pacman_durchmesser, naechste_richtung, block):
    #Kopie der aktuellen Position erstellen
    #print(f"Startposition vooooor Bewegung: {pacman_position}")
    neuer_pacman_pos = pacman_position.copy()
    #print(f"Startposition vvvvvor Bewegung: {pacman_position}")
    #Pacman prüft, ob er die Richtung ändern kann
    if naechste_richtung == 'hoch':
        test_pos = [pacman_position[0], pacman_position[1] - pacman_bewegung]
        if not kollision_check(test_pos, pacman_durchmesser // 2, wand_rechtecke):
            pacman_richtung = naechste_richtung
    elif naechste_richtung == 'runter':
        test_pos = [pacman_position[0], pacman_position[1] + pacman_bewegung]
        if not kollision_check(test_pos, pacman_durchmesser // 2, wand_rechtecke):
            pacman_richtung = naechste_richtung
    elif naechste_richtung == 'rechts':
        test_pos = [pacman_position[0] + pacman_bewegung, pacman_position[1]]
        if not kollision_check(test_pos, pacman_durchmesser // 2, wand_rechtecke):
            pacman_richtung = naechste_richtung
    elif naechste_richtung == 'links':
        test_pos = [pacman_position[0] - pacman_bewegung, pacman_position[1]]
        if not kollision_check(test_pos, pacman_durchmesser // 2, wand_rechtecke):
            pacman_richtung = naechste_richtung

    # Bewegung basierend auf der aktuellen Richtung
    if pacman_richtung == 'rechts':
        neuer_pacman_pos[0] += pacman_bewegung
    elif pacman_richtung == 'links':
        neuer_pacman_pos[0] -= pacman_bewegung
    elif pacman_richtung == 'hoch':
        neuer_pacman_pos[1] -= pacman_bewegung
    elif pacman_richtung == 'runter':
        neuer_pacman_pos[1] += pacman_bewegung

    # Überprüfen, ob die neue Position gültig ist (keine Kollision)
    if not kollision_check(neuer_pacman_pos, pacman_durchmesser // 2, wand_rechtecke):
        pacman_position = neuer_pacman_pos  # Nur bewegen, wenn keine Kollision
    else:
        # Pacman bleibt stehen, wenn er auf eine Wand trifft
        pacman_position = pacman_position
    # Tunnel nutzen
    pacman_position = tunnel_pacman(pacman_position, pacman_richtung, layout, block)

    return pacman_position, pacman_richtung

# Funktion, um einen Geist zu bewegen
def move_geist(geist, block, wand_rechtecke, geist_timer_intervall):
    # Wenn der Timer das Intervall überschreitet, ändern die Geister die Richtung
    if geist["timer"] >= geist_timer_intervall:
        #(Einfachheit: zufällige Wahl der Richtung)
        directions = ['rechts', 'links', 'hoch', 'runter']
        direction = random.choice(directions)
        # Neue Position berechnen
        new_position = list(geist["position"]) #Erstelle eine Liste aus dem Tuple

        if direction == 'rechts':
            new_position[0] += block
        elif direction == 'links':
            new_position[0] -= block
        elif direction == 'hoch':
            new_position[1] -= block
        elif direction == 'runter':
            new_position[1] += block

        #Kollision prüfen und bewegen wenn keine Kollision vorhanden
        if not kollision_check(new_position, geist["durchmesser"] // 2, wand_rechtecke):
            geist["position"] = new_position
        # Setze den Timer zurück
        geist["timer"] = 0
    else:
        # Erhöhe den Timer nur, wenn die Geister nicht bewegt wurden
        geist["timer"] += 1

    # Tunnel nutzen
    geist = tunnel_ghost(geist, layout, block)
    return geist

# Funktion zur Kollisionserkennung der Geister
def kollision_check(position, radius, wand_rechtecke):
    geist_rect = pygame.Rect(position[0] - radius, position[1] - radius, radius * 2, radius * 2)

    for wand in wand_rechtecke:
        if geist_rect.colliderect(wand):
            return True  # Kollision gefunden
    return False  # Keine Kollision

# Funktion zur Kollisionserkennung zwischen PacMan und Geistern
def kollision_check_pacman_ghost(pacman_rect, geister, geist_durchmesser):
    # Überprüfe für jeden Geist, ob eine Kollision mit PacMan vorliegt
    for geist in geister:
        geist_rect = pygame.Rect(geist["position"][0] - geist_durchmesser // 2, geist["position"][1] - geist_durchmesser // 2, geist_durchmesser, geist_durchmesser)
        # Wenn PacMan mit dem Geist kollidiert
        if pacman_rect.colliderect(geist_rect):
            return True  # Kollision gefunden
    return False  # Keine Kollision

# Funktion zur Tunnelnutzung für PacMan
def tunnel_pacman(pacman_position, richtung, layout, block):
    # Tunnelpositionen definieren (links und rechts)
    if pacman_position[0] < 0:  # Wenn PacMan links aus dem Bildschirm geht
        pacman_position[0] = len(layout[0]) * block - block // 2  # Auf die rechte Seite
    elif pacman_position[0] > len(layout[0]) * block:  # Wenn PacMan rechts aus dem Bildschirm geht
        pacman_position[0] = block // 2  # Auf die linke Seite
    return pacman_position

# Funktion zur Tunnelnutzung für Geister
def tunnel_ghost(geist, layout, block):
    # Tunnelpositionen definieren (links und rechts)
    if geist["position"][0] < 0:  # Wenn der Geist links aus dem Bildschirm geht
        geist["position"][0] = len(layout[0]) * block - block // 2  # Auf die rechte Seite
    elif geist["position"][0] > len(layout[0]) * block:  # Wenn der Geist rechts aus dem Bildschirm geht
        geist["position"][0] = block // 2  # Auf die linke Seite
    return geist

#Position der Coins
def coins(screen, block, coin_durchmesser):
    for y, row in enumerate(layout):
        for x, cell in enumerate(row):
            #Überprüfen, ob die Zelle ein Coin ist (' ')
            if cell == ' ':
                # Berechne die Mitte der Zelle für die Coins
                center_x = x * block + block // 2
                center_y = y * block + block // 2
                coin_rect = pygame.Rect(center_x - coin_durchmesser // 2, center_y - coin_durchmesser // 2, coin_durchmesser, coin_durchmesser)
                pygame.draw.ellipse(screen, farben ["GELB"], coin_rect)

#Position der Berry's
def berry(screen, block, berry_durchmesser):
    for y, row in enumerate(layout):
        for x, cell in enumerate(row):
            # Überprüfen, ob die Zelle eine Berry ist ('b')
            if cell == 'b':
                center_x = x * block + block // 2
                center_y = y * block + block // 2
                berry_rect = pygame.Rect(center_x - berry_durchmesser // 2, center_y - berry_durchmesser // 2, berry_durchmesser, berry_durchmesser)
                pygame.draw.ellipse(screen, farben["LILA"], berry_rect)

def collect_coins(pacman_rect, coin_durchmesser, block, score):
    collected_coins = 0
    for y, row in enumerate(layout):
        for x, cell in enumerate(row):
            # Überprüfen, ob die Zelle ein Coin ist (leerer Raum ' ')
            if cell == ' ':
                center_x = x * block + block // 2  # Korrekte Berechnung der Mitte
                center_y = y * block + block // 2
                coin_rect = pygame.Rect(center_x - coin_durchmesser // 2, center_y - coin_durchmesser // 2, coin_durchmesser, coin_durchmesser)
                # Wenn PacMan auf dem Coin ist, diesen "einsammeln"
                if pacman_rect.colliderect(coin_rect):
                    #print(f"PacMan hat Coin auf Position {x}, {y} eingesammelt") - test
                    layout[y][x] = ''  # Setze den Coin auf ' ' (gesammelt)
                    collected_coins += 1
                    score += 10  # Erhöhe den Score um 10 für einen Coin
                    speichere_punkte("highscore.csv", score)
    return score  # Rückgabe des aktualisierten Scores

def collect_berries(pacman_rect, berry_durchmesser, block, score):
    collected_berries = 0
    for y, row in enumerate(layout):
        for x, cell in enumerate(row):
            #Überprüfen, ob das Feld eine Beere ist ('b')
            if cell == 'b':
                center_x = x * block + block // 2  # Korrekte Berechnung der Mitte
                center_y = y * block + block // 2
                berry_rect = pygame.Rect(center_x - berry_durchmesser // 2, center_y - berry_durchmesser // 2, berry_durchmesser, berry_durchmesser)
                # Wenn PacMan auf der Beere ist, diese "einsammeln"
                if pacman_rect.colliderect(berry_rect):
                    layout[y][x] = ''  # Setze die Beere auf ' ' (gesammelt)
                    collected_berries += 1
                    score += 50  # Erhöhe den Score um 50 für eine Beere
                    speichere_punkte("highscore.csv", score)
    return score

def speichere_punkte(dateiname, punkte):
    with open(dateiname, mode='a') as datei:
        datei.write("Punkte\n")
        datei.write(f"{punkte}\n")

def lade_highscore(dateiname):
    with open(dateiname, mode='r') as datei:
        lines = datei.readlines()
        if lines:
            #Lade den letzten Punktestand
            return int(lines[-1].strip())  #Den letzten Wert (Punkte) lesen

# Funktion, um das Spiel zu beenden und den Sieg anzuzeigen
def victory(screen, settings, fenster_breite, fenster_hoehe):
    font = settings["font"]
    victory_text = font.render("Du hast gewonnen!", True, farben["GELB"])
    screen.fill(farben["SCHWARZ"])
    screen.blit(victory_text, (fenster_breite // 2 - victory_text.get_width() // 2, fenster_hoehe // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Zeige die Nachricht 2 Sekunden lang an
    pygame.quit()  # Beende Pygame

# Funktion zum Überprüfen, ob das Spiel gewonnen wurde (alle Coins eingesammelt)
def check_victory():
    for y, row in enumerate(layout):
        for x, cell in enumerate(row):
            if cell == ' ':
                return False  # Es gibt noch Coins, Spiel nicht gewonnen
    return True  # Alle Coins wurden eingesammelt, Spiel gewonnen

def game_over(screen, settings, fenster_breite, fenster_hoehe):
    font = settings["font"]
    game_over_text = font.render("Game Over!", True, farben["ROT"])
    screen.blit(game_over_text, (fenster_breite // 2 - game_over_text.get_width() // 2, fenster_hoehe // 2))

# ----------

def init_game_settings():
    """Initialisiert alle grundlegenden Spieleeinstellungen."""
    settings = {
        "block" : 30,# Spielfeld ist "dynamisch anpassbar wenn Sie zb. block auf 50 ändern, müssen sie die durchmesser -1 rechnen
        "pacman_bewegung": 3,
        "pacman_durchmesser": 30,
        "geist_durchmesser": 30,
        "geist_timer_intervall": 9,
        "coin_durchmesser": 10,
        "berry_durchmesser": 25,
        "score": 0,
        "font" : pygame.font.Font(None, 32)
    }
    return settings

def handle_user_input(naechste_richtung):
    """Verarbeitet Benutzereingaben und gibt die nächste Richtung zurück."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                return 'rechts'
            elif event.key == pygame.K_LEFT:
                return 'links'
            elif event.key == pygame.K_UP:
                return 'hoch'
            elif event.key == pygame.K_DOWN:
                return 'runter'
            elif event.key == pygame.K_ESCAPE:
                return "quit"
    return naechste_richtung

def update_screen(screen, block, fenster_breite, pacman_bild, pacman_position, pacman_durchmesser, geister,
                  geist_durchmesser, score, wand_rechtecke, coin_durchmesser, berry_durchmesser, geist_bilder):
    """Aktualisiert den Bildschirm mit allen notwendigen Grafiken."""
    screen.fill(farben["SCHWARZ"])

    # Labyrinth und Wandrechtecke zeichnen
    for wand in wand_rechtecke:
        pygame.draw.rect(screen, farben["BLAU"], wand)

    # PacMan anzeigen
    screen.blit(pacman_bild, (
        pacman_position[0] - pacman_durchmesser // 2, pacman_position[1] - pacman_durchmesser // 2))

    # Geister anzeigen
    for geist in geister:
        draw_ghost(screen, geist, geist_durchmesser, geist_bilder)

    # Coins und Berries anzeigen
    coins(screen, block, coin_durchmesser)
    berry(screen, block, berry_durchmesser)

    # Punktestand anzeigen
    font = pygame.font.Font(None, 32)
    score_text = font.render(f"Score: {score}", True, farben["WEISS"])
    screen.blit(score_text, (fenster_breite - score_text.get_width() - 20, 5))

    pygame.display.flip()

def main():
    settings = init_game_settings()
    #screen, fenster_breite, fenster_hoehe = calculate_window_size(settings["block"])
    screen, wand_rechtecke, fenster_breite, fenster_hoehe = window(layout, settings["block"])

    pacman_richtung = None
    naechste_richtung = pacman_richtung
    pacman_position = pacman_startposition(layout, settings["block"], settings["pacman_durchmesser"])

    # Geisterpositionen finden
    geister_positionen = find_ghost_positionen(layout, settings["block"])
    geister = initialize_ghost(geister_positionen, settings["block"])

    # Lade alle Bilder
    pacman_offen, pacman_geschlossen, geist_bilder = load_images(settings)

    if start_menu(screen, fenster_breite, fenster_hoehe) == "start":
        spielaktiv = True
        while spielaktiv:
            screen.fill(farben["SCHWARZ"])
            naechste_richtung = handle_user_input(naechste_richtung)
            if naechste_richtung == "quit":
                spielaktiv = False
                print("Spieler hat Quit-Button angeklickt")

            # Spiellogik
            pacman_position, pacman_richtung = move_pacman(pacman_richtung, pacman_position, settings["pacman_bewegung"],wand_rechtecke, settings["pacman_durchmesser"], naechste_richtung, settings["block"])


            pacman_rect = pygame.Rect(pacman_position[0] - settings["pacman_durchmesser"] // 2,
                                      pacman_position[1] - settings["pacman_durchmesser"] // 2,
                                      settings["pacman_durchmesser"], settings["pacman_durchmesser"])

            # Kollision zwischen PacMan und Geistern
            if kollision_check_pacman_ghost(pacman_rect, geister, settings["geist_durchmesser"]):
                game_over(screen, settings, fenster_breite, fenster_hoehe)
                pygame.display.flip()
                pygame.time.wait(2000)  # Warte 5 Sekunden
                spielaktiv = False

            # Geister bewegen
            for geist in geister:
                geist = move_geist(geist, settings["block"], wand_rechtecke, settings["geist_timer_intervall"])

            # Punkte sammeln
            settings["score"] = collect_coins(pacman_rect, settings["coin_durchmesser"], settings["block"], settings["score"])
            settings["score"] = collect_berries(pacman_rect, settings["coin_durchmesser"], settings["block"], settings["score"])

            # Siegbedingungen überprüfen
            if check_victory():
                victory(screen, settings, fenster_breite, fenster_hoehe)
                break  # Spiel beenden, wenn gewonnen

            # PacMan animieren
            pacman_bild = animated_pacman(pacman_richtung, settings["pacman_durchmesser"], pacman_offen, pacman_geschlossen)

            # Bildschirm aktualisieren
            update_screen(screen,settings["block"], fenster_breite, pacman_bild, pacman_position, settings["pacman_durchmesser"],
                          geister, settings["geist_durchmesser"], settings["score"], wand_rechtecke,
                          settings["coin_durchmesser"], settings["berry_durchmesser"], geist_bilder)

            # Frame Rate
            pygame.time.Clock().tick(60)

    pygame.quit()

#cProfile.run('main()')
if __name__ == '__main__':
    main()
