import requests
import os
import pygame
import tempfile
from datetime import datetime, timedelta
import schedule
from PIL import Image, ImageFilter, ImageGrab
import ctypes
import json

def download_audio(url, filename):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded audio to {filename}")
    else:
        print(f"Failed to download audio. Status code: {response.status_code}")

def get_prayer_times(url):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        data = response.json()
        prayer_times = data['items'][0]
        return {
            'Fajr': datetime.strptime(prayer_times['fajr'], '%I:%M %p').time(),
            'Dhuhr': datetime.strptime(prayer_times['dhuhr'], '%I:%M %p').time(),
            'Asr': datetime.strptime(prayer_times['asr'], '%I:%M %p').time(),
            'Maghrib': datetime.strptime(prayer_times['maghrib'], '%I:%M %p').time(),
            'Isha': datetime.strptime(prayer_times['isha'], '%I:%M %p').time()
        }
    else:
        print(f"Failed to get prayer times. Status code: {response.status_code}")
        return None

def play_adhan():
    pygame.mixer.init()
    pygame.mixer.music.load(tmp_filename)
    pygame.mixer.music.play()
    show_reminder("L'heure de la prière !")
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()  
    pygame.mixer.quit()

def show_reminder(text):
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.NOFRAME | pygame.FULLSCREEN)
    pygame.display.set_caption("Prayer Reminder")

    hwnd = pygame.display.get_wm_info()['window']
    ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0004)
    pygame.event.set_grab(True)

    screen_image = ImageGrab.grab()
    screen_image = screen_image.filter(ImageFilter.GaussianBlur(radius=15))
    screen_image.save("blurred_screen.jpg")

    bg_image = pygame.image.load("blurred_screen.jpg")
    bg_image = pygame.transform.scale(bg_image, (screen.get_width(), screen.get_height()))
    
    font = pygame.font.Font(None, 74)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
    running = True
    start_time = datetime.now()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                pygame.mixer.music.stop()  
        
        screen.blit(bg_image, (0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        
        if (datetime.now() - start_time).seconds > 30:
            running = False
            pygame.mixer.music.stop() 
    
    pygame.event.set_grab(False) 
    pygame.display.quit()  

def schedule_prayers(prayer_times):
    for prayer, prayer_time in prayer_times.items():
        schedule_time = prayer_time.strftime('%H:%M')
        schedule.every().day.at(schedule_time).do(play_adhan)
        print(f"Scheduled {prayer} prayer at {schedule_time}")

city = 'Ans'
country = 'Belgium'
url = 'https://muslimsalat.com/ans.json'
prayer_times = get_prayer_times(url)

if prayer_times:
    for prayer, time in prayer_times.items():
        print(f"{prayer}: {time.strftime('%H:%M')}")

    audio_url = 'https://media.sd.ma/assabile/adhan_3435370/0bf83c80b583.mp3'

    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
        tmp_filename = tmp_file.name
        download_audio(audio_url, tmp_filename)

    schedule_prayers(prayer_times)

    try:
        while True:
            schedule.run_pending()

            next_run = schedule.idle_seconds()
            if next_run is None:
                break
            elif next_run > 0:
                next_run = min(next_run, 60) 
                now = datetime.now()
                future = now + timedelta(seconds=next_run)
                while datetime.now() < future:
                    pass
    finally:
        os.remove(tmp_filename)
else:
    print("Failed to retrieve prayer times.")