#Importieren der Pygame-Bibliothek
import pygame
import random
import time #Wird zb für die Animation von Pacmans Mund verwendet
#initialisieren von pygame
pygame.init()

# Farben anpassen
farben = {
    "SCHWARZ": (0, 0, 0),
    "WEISS": (255, 255, 255),
    "ROT": (255, 0, 0),
    "PINK": (255, 96, 243),
    "ORANGE": (255, 155, 0),
    "TUERKIS": (0, 236, 255),
    "BLAU": (0, 0, 255),
    "GELB": (255, 255, 0),
    "LILA": (200, 0, 255)
}

# Titel
pygame.display.set_caption("Willkommen zu PacMan von Noé und Felix")

#für Textausgabe
font = pygame.font.Font(None, 32)

# Bildschirm Aktualisierungen einstellen
clock = pygame.time.Clock() #Für die FPS

#Labyrinth
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
block = 30
fenster_breite = len(layout[0]) * block
fenster_hoehe = len(layout) * block
screen = pygame.display.set_mode((fenster_breite, fenster_hoehe))

#PacManeigenschaften:
pacman_bewegung = 3
pacman_durchmesser = block
pacman_richtung = None #Am Anfang pacman-ausrichtung nach rechts weil bild nach rechts schaut
naechste_richtung = pacman_richtung

#Geistereigenschaften:
geist_durchmesser = block

#hintergrundbild laden
background_image = pygame.image.load('images/background.png')

#Pacmanbilder
pacman_offen = pygame.image.load('images/pacman-offen.png')
pacman_geschlossen = pygame.image.load('images/pacman-geschlossen.png')
pacman_offen = pygame.transform.scale(pacman_offen,(pacman_durchmesser, pacman_durchmesser))
pacman_geschlossen = pygame.transform.scale(pacman_geschlossen, (pacman_durchmesser, pacman_durchmesser))

#Geisterbilder
geist_bilder = {
    "r": pygame.image.load('images/geist_rot.png'),
    "o": pygame.image.load('images/geist_orange.png'),
    "p": pygame.image.load('images/geist_pink.png'),
    "t": pygame.image.load('images/geist_tuerkis.png')
}#Schlüssel und Wert

#Skalieren der Geisterbilder auf den gewünschten Durchmesser
geist_bilder = {key: pygame.transform.scale(image, (geist_durchmesser, geist_durchmesser)) for key, image in geist_bilder.items()}

#Spielfeldeigenschaften:
coin_durchmesser = 10
berry_durchmesser = 25

wand_rechtecke = [] #Erstellt Wände, woraus das Labyrinth entsteht
for y, row in enumerate(layout):
    for x, cell in enumerate(row):
        if cell == '1':  #Wandposition im layout
            wand_rechtecke.append(pygame.Rect(x * block, y * block, block, block))

#Suchen der Startposition 'S' im Layout
def finde_startposition(layout):
    for y, row in enumerate(layout):
        for x, cell in enumerate(row):
            if cell == 'S':
                return x * block, y * block
    return None
# PacMan Startposition setzen
pacman_position = finde_startposition(layout)
pacman_position = [pacman_position[0] + pacman_durchmesser // 2, pacman_position[1] + pacman_durchmesser // 2]

#Pacman Bewegung und Kollisionsüberprüfung, deshalb so lange funktion (2 verschiedene Funktionen haben nicht funktioniert, dass er sich so smooth bewegt)
def bewege_pacman(pacman_richtung, pacman_pos, pacman_bewegung, wand_rechtecke, pacman_durchmesser, naechste_richtung):
    #Kopie der aktuellen Position erstellen
    neuer_pacman_pos = pacman_pos.copy()
    #Pacman prüft, ob er die Richtung ändern kann
    if naechste_richtung == 'hoch':
        test_pos = [pacman_pos[0], pacman_pos[1] - pacman_bewegung]
        if not kollision_check(test_pos, pacman_durchmesser // 2, wand_rechtecke):
            pacman_richtung = naechste_richtung
    elif naechste_richtung == 'runter':
        test_pos = [pacman_pos[0], pacman_pos[1] + pacman_bewegung]
        if not kollision_check(test_pos, pacman_durchmesser // 2, wand_rechtecke):
            pacman_richtung = naechste_richtung
    elif naechste_richtung == 'rechts':
        test_pos = [pacman_pos[0] + pacman_bewegung, pacman_pos[1]]
        if not kollision_check(test_pos, pacman_durchmesser // 2, wand_rechtecke):
            pacman_richtung = naechste_richtung
    elif naechste_richtung == 'links':
        test_pos = [pacman_pos[0] - pacman_bewegung, pacman_pos[1]]
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
        pacman_pos = neuer_pacman_pos  # Nur bewegen, wenn keine Kollision
    else:
        # Pacman bleibt stehen, wenn er auf eine Wand trifft
        pacman_pos = pacman_pos
    # Tunnel nutzen
    pacman_pos = tunnel_pacman(pacman_pos, pacman_richtung, layout, block)
    return pacman_pos, pacman_richtung

#Funktion um die Buchstaben für die jeweiligen Geister zu finden (r, o, p, t)
def finde_geister_positionen(layout):
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

#Geisterpositionen finden
geister_positionen = finde_geister_positionen(layout)

#Geister initialisieren
geister = [
    {"position": geister_positionen['r'], "farbe": 'r', "durchmesser": geist_durchmesser, "timer": 0},
    {"position": geister_positionen['o'], "farbe": 'o', "durchmesser": geist_durchmesser, "timer": 0},
    {"position": geister_positionen['p'], "farbe": 'p', "durchmesser": geist_durchmesser, "timer": 0},
    {"position": geister_positionen['t'], "farbe": 't', "durchmesser": geist_durchmesser, "timer": 0},
]
geist_timer = 0  # Timer für Geisterbewegung
geist_timer_intervall = 12  #Intervall für Richtungsänderung der Geister (z. B. alle 9 Frames/s) umso höher desto langsamer

# Funktion, um die Geisterbilder einzufügen
def draw_ghost(screen, geist):
    # Bild des Geistes auf die Position zeichnen
    screen.blit(geist_bilder[geist["farbe"]], (geist["position"][0] - geist_durchmesser // 2, geist["position"][1] - geist_durchmesser // 2)) #durch 2 für die Mitte des Blocks

# Funktion, um einen Geist zu bewegen
def bewege_geist(geist, block, wand_rechtecke, geist_timer_intervall):
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

# Funktion zur Kollisionserkennung
def kollision_check(position, radius, wand_rechtecke):
    geist_rect = pygame.Rect(position[0] - radius, position[1] - radius, radius * 2, radius * 2)

    for wand in wand_rechtecke:
        if geist_rect.colliderect(wand):
            return True  # Kollision gefunden
    return False  # Keine Kollision

# Funktion zur Kollisionserkennung zwischen PacMan und Geistern
def kollision_check_pacman_geister(pacman_rect, geister, geist_durchmesser):
    # Überprüfe für jeden Geist, ob eine Kollision mit PacMan vorliegt
    for geist in geister:
        geist_rect = pygame.Rect(geist["position"][0] - geist_durchmesser // 2, geist["position"][1] - geist_durchmesser // 2, geist_durchmesser, geist_durchmesser)
        # Wenn PacMan mit dem Geist kollidiert
        if pacman_rect.colliderect(geist_rect):
            return True  # Kollision gefunden
    return False  # Keine Kollision

def pacman_animiert(richtung):
    pacman_bild = pacman_offen if time.time() % 0.5 < 0.3 else pacman_geschlossen
    '''pacman_bild = rotate_pacman(pacman_bild, richtung)'''
    return pacman_bild

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
                    speichere_punkte("highscore.csv", score)  # Speichern nach jedem Coin
    return score  # Rückgabe des aktualisierten Scores

def collect_berrys(pacman_rect, berry_durchmesser, block, score):
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
                    speichere_punkte("highscore.csv", score)# Speichern nach jeder Beere
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

# Funktion zur Tunnelnutzung für PacMan
def tunnel_pacman(pacman_pos, richtung, layout, block):
    # Tunnelpositionen definieren (links und rechts)
    if pacman_pos[0] < 0:  # Wenn PacMan links aus dem Bildschirm geht
        pacman_pos[0] = len(layout[0]) * block - block // 2  # Auf die rechte Seite
    elif pacman_pos[0] > len(layout[0]) * block:  # Wenn PacMan rechts aus dem Bildschirm geht
        pacman_pos[0] = block // 2  # Auf die linke Seite
    return pacman_pos

# Funktion zur Tunnelnutzung für Geister
def tunnel_ghost(geist, layout, block):
    # Tunnelpositionen definieren (links und rechts)
    if geist["position"][0] < 0:  # Wenn der Geist links aus dem Bildschirm geht
        geist["position"][0] = len(layout[0]) * block - block // 2  # Auf die rechte Seite
    elif geist["position"][0] > len(layout[0]) * block:  # Wenn der Geist rechts aus dem Bildschirm geht
        geist["position"][0] = block // 2  # Auf die linke Seite
    return geist

#Funktion zum Anzeigen des Startmenüs
def start_menu():
    menu_font = pygame.font.Font(None, 64)
    option_font = pygame.font.Font(None, 46)
    #Texte
    titel_text = menu_font.render("Willkommen zu Pacman", True, farben["GELB"])
    start_text = option_font.render("Spiel Starten", True, farben["WEISS"])
    quit_text = option_font.render("Beenden", True, farben["WEISS"])
    highscore_text = option_font.render("Highscore: ", True, farben["WEISS"])
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
        letzter_highscore = lade_highscore("highscore.csv") #Letzte Zeile der Datei
        screen.blit(option_font.render("Spiel Starten", True, start_text_color), (fenster_breite // 2 - start_text.get_width() // 2, fenster_hoehe // 2))
        screen.blit(option_font.render("Beenden", True, quit_text_color), (fenster_breite // 2 - quit_text.get_width() // 2, fenster_hoehe // 2 + 50))
        screen.blit(option_font.render(f"Letzter Highscore: {letzter_highscore}", True, highscore_text_color), (fenster_breite // 2.5 - highscore_text.get_width() // 2, fenster_hoehe // 2 + 100))
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

def game_over():
    game_over_text = font.render("Game Over!", True, farben["ROT"])
    screen.blit(game_over_text, (fenster_breite // 2 - game_over_text.get_width() // 2, fenster_hoehe // 2))
# Funktion zum Überprüfen, ob das Spiel gewonnen wurde (alle Coins eingesammelt)
def check_victory():
    for y, row in enumerate(layout):
        for x, cell in enumerate(row):
            if cell == ' ':
                return False  # Es gibt noch Coins, Spiel nicht gewonnen
    return True  # Alle Coins wurden eingesammelt, Spiel gewonnen

# Funktion, um das Spiel zu beenden und den Sieg anzuzeigen
def victory(screen, font):
    victory_text = font.render("Du hast gewonnen!", True, farben["GELB"])
    screen.fill(farben["SCHWARZ"])
    screen.blit(victory_text, (fenster_breite // 2 - victory_text.get_width() // 2, fenster_hoehe // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Zeige die Nachricht 2 Sekunden lang an
    pygame.quit()  # Beende Pygame
# ----------
# Schleife Hauptprogramm
spielaktiv = True
score = 0
if start_menu() == "start":
    while spielaktiv:
        #Überprüfen, ob Nutzer eine Aktion durchgeführt hat
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                spielaktiv = False
                print("Spieler hat Quit-Button angeklickt")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    naechste_richtung = 'rechts'
                elif event.key == pygame.K_LEFT:
                    naechste_richtung = 'links'
                elif event.key == pygame.K_UP:
                    naechste_richtung = 'hoch'
                elif event.key == pygame.K_DOWN:
                    naechste_richtung = 'runter'
                elif event.key == pygame.K_ESCAPE:
                    spielaktiv = False
                    print("Spiel wurde beendet")

        # Spiellogik
        pacman_position, pacman_richtung = bewege_pacman(pacman_richtung, pacman_position, pacman_bewegung, wand_rechtecke, pacman_durchmesser, naechste_richtung)
        pacman_rect = pygame.Rect(pacman_position[0] - pacman_durchmesser // 2, pacman_position[1] - pacman_durchmesser // 2, pacman_durchmesser, pacman_durchmesser)

        # Kollisionserkennung zwischen PacMan und Geistern
        if kollision_check_pacman_geister(pacman_rect, geister, geist_durchmesser):
            # Game Over wenn PacMan mit einem Geist kollidiert
            game_over()
            pygame.display.flip()
            pygame.time.wait(5000)  # Warte für 5 Sekunden, damit der Spieler das Game Over sieht
            spielaktiv = False  # Setze das Spiel auf inaktiv (Game Over)

        #Geister bewegen und zeichnen
        for geist in geister:
            geist = bewege_geist(geist, block, wand_rechtecke, geist_timer_intervall)  # Geister bewegen

        #Coins sammeln
        score = collect_coins(pacman_rect, coin_durchmesser, block, score)

        # Berries sammeln
        score = collect_berrys(pacman_rect, coin_durchmesser, block, score)

        # Funktion check-vicotry prüfen
        if check_victory():
            victory(screen, font)
            break  # Spiel beenden, wenn gewonnen

        #Spielfeld löschen (ist notwendig um Überlagerung von Grafiken zu vermeiden)
        screen.fill(farben["SCHWARZ"])

        #Labyrinth bauen
        for wand in wand_rechtecke:
            pygame.draw.rect(screen, farben["BLAU"], wand)

        #Pacman anzeigen
        pacman_bild = pacman_animiert(pacman_richtung)
        screen.blit(pacman_bild, (pacman_position[0] - pacman_durchmesser // 2, pacman_position[1] - pacman_durchmesser // 2))
        #Geister anzeigen
        for geist in geister:
            draw_ghost(screen, geist)

        #Coins anzeigen
        coins(screen, block, coin_durchmesser)

        #Berrys anzeigen
        berry(screen, block, berry_durchmesser)

        #Anzeigen des Punktestands oben rechts
        score_text = font.render(f"Score: {score}", True, farben["WEISS"])
        screen.blit(score_text, (fenster_breite - score_text.get_width() - 20, 5))

        # Fenster aktualisieren
        pygame.display.flip()

        # Refresh-Zeiten festlegen
        clock.tick(60)

pygame.quit()