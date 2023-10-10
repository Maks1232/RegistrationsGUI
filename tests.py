import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
szerokosc = 800
wysokosc = 600
ekran = pygame.display.set_mode((szerokosc, wysokosc))
pygame.display.set_caption("Strona startowa quizu")

# Kolory
tlo_kolor = (255, 255, 255)
przycisk_kolor = (150, 150, 150)
przycisk_kolor_aktywny = (100, 100, 100)
tekst_kolor = (255, 255, 255)

# Czcionka
czcionka = pygame.font.Font(None, 40)

# Województwa
wojewodztwa = ["Województwo 1", "Województwo 2", "Województwo 3", "Województwo 4", "Województwo 5"]

# Poziomy trudności
poziomy_trudnosci = ["Łatwy", "Trudny"]


def rysuj_rozwijana_liste(pozycja, opcje, wybrane_opcje, rozwinieta):

    pygame.draw.rect(ekran, przycisk_kolor_aktywny, pozycja)
    pygame.draw.rect(ekran, tekst_kolor, pozycja, 2)
    rysuj_tekst(wybrane_opcje, (pozycja.x + 10, pozycja.y + 10))

    if rozwinieta:
        for i, opcja in enumerate(opcje):
            y = pozycja.y + (i + 1) * pozycja.height
            pygame.draw.rect(ekran, przycisk_kolor, (pozycja.x, y, pozycja.width, pozycja.height))
            pygame.draw.rect(ekran, tekst_kolor, (pozycja.x, y, pozycja.width, pozycja.height), 2)
            rysuj_tekst(opcja, (pozycja.x + 10, y + 10))

def rysuj_tekst(tekst, polozenie):
    powierzchnia_tekstu = czcionka.render(tekst, True, tekst_kolor)
    polozenie_tekstu = powierzchnia_tekstu.get_rect(topleft=polozenie)
    ekran.blit(powierzchnia_tekstu, polozenie_tekstu)

wybrane_wojewodztwo = "Wybierz województwo"
wybrane_poziom = "Wybierz poziom"
wojewodztwo_rozwinieta = False
poziom_rozwiniety = False

running = True
while running:
    ekran.fill(tlo_kolor)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if wojewodztwa_przycisk.collidepoint(event.pos):
                wojewodztwo_rozwinieta = not wojewodztwo_rozwinieta
                poziom_rozwiniety = False
            elif poziomy_przycisk.collidepoint(event.pos):
                poziom_rozwiniety = not poziom_rozwiniety
                wojewodztwo_rozwinieta = False
            elif wojewodztwo_rozwinieta:
                for i, opcja in enumerate(wojewodztwa):
                    y = wojewodztwa_przycisk.y + (i + 1) * wojewodztwa_przycisk.height
                    opcja_prostokat = pygame.Rect(wojewodztwa_przycisk.x, y, wojewodztwa_przycisk.width, wojewodztwa_przycisk.height)
                    if opcja_prostokat.collidepoint(event.pos):
                        wybrane_wojewodztwo = opcja
                        wojewodztwo_rozwinieta = False
            elif poziom_rozwiniety:
                for i, opcja in enumerate(poziomy_trudnosci):
                    y = poziomy_przycisk.y + (i + 1) * poziomy_przycisk.height
                    opcja_prostokat = pygame.Rect(poziomy_przycisk.x, y, poziomy_przycisk.width, poziomy_przycisk.height)
                    if opcja_prostokat.collidepoint(event.pos):
                        wybrane_poziom = opcja
                        poziom_rozwiniety = False

    wojewodztwa_przycisk = pygame.Rect(100, 200, 200, 40)
    rysuj_rozwijana_liste(wojewodztwa_przycisk, wojewodztwa, wybrane_wojewodztwo, wojewodztwo_rozwinieta)

    poziomy_przycisk = pygame.Rect(500, 200, 200, 40)
    rysuj_rozwijana_liste(poziomy_przycisk, poziomy_trudnosci, wybrane_poziom, poziom_rozwiniety)

    pygame.display.flip()

print("Wybrane województwo:", wybrane_wojewodztwo)
print("Wybrany poziom trudności:", wybrane_poziom)
