import pygame
import pygame.freetype
import win32api
import win32con
import win32gui
import requests
import shutil
from PIL import Image


white = (255, 255, 255)
black = (0, 0, 0)
current_number = -1
current_image = None
total = 0

# changeable:
images_url = 'https://paste.gg/p/egorkaalexxx/521d4ebf4fac45f7be200c78dff60553/files/23437fa118c54b8eb15ba9ec5af405c3/raw'
opacity = 100
opacity_step = 30
width = 400
width_step = 20
seconds = 30
in_left = True
margin_side = 10
margin_bottom = 150


def resize_to(number, filename):
    global width
    image = Image.open(f'{number}.png')
    sizes = image.size
    mult = width/sizes[0]
    new_image = image.resize((round(sizes[0]*mult), round(sizes[1]*mult)))
    new_image.save(filename)


def open_file(number):
    try:
        resize_to(number, 'current.png')
        return pygame.image.load('current.png')
    except:
        return None


def load_images():
    global total
    response = requests.get(images_url)
    data = response.text
    urls = data.strip().split()

    total = 0
    for (idx, url) in enumerate(urls):
        try:
            response = requests.get(url, stream=True)
            with open(f'{idx}.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

            total += 1
        except:
            continue
    print('now', total, 'images')


def select_image(delta):
    global current_number, current_image, total
    if current_number == -1 and total > 0:
        current_number = 0
        current_image = open_file(0)
    elif 0 <= current_number+delta and current_number+delta < total:
        current_number += delta
        current_image = open_file(current_number)

    if current_image is None:
        current_number = -1


def blit_with_alpha(target, source, location):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)


def run():
    global current_image, current_number, width, width_step, seconds, margin_bottom, margin_side, in_left, opacity, opacity_step
    pygame.init()

    load_images()
    pygame.time.set_timer(pygame.USEREVENT, seconds*1000)

    window_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
    screen = pygame.display.set_mode((window_size[0], window_size[1]), pygame.NOFRAME, pygame.SRCALPHA)

    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*white), 0, win32con.LWA_COLORKEY)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    font = pygame.font.Font("Roboto-Regular.ttf", 12)

    done = 0
    while not done:   
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:   
                done = 1
                break
            if event.type == pygame.USEREVENT:
                load_images()
                select_image(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = 1
                    break
                if event.key in [pygame.K_q, pygame.K_LCTRL]:
                    current_number = -1
                    current_image = None

                if event.key == pygame.K_z:
                    in_left = True
                if event.key == pygame.K_x:
                    in_left = False

                if event.key == pygame.K_c:
                    opacity -= opacity_step
                if event.key == pygame.K_v:
                    opacity += opacity_step

                if event.key == pygame.K_UP:
                    width += width_step
                    select_image(0)
                if event.key == pygame.K_DOWN:
                    width -= width_step
                    select_image(0)

                if event.key == pygame.K_LEFT:
                    select_image(-1)
                if event.key == pygame.K_RIGHT:
                    select_image(+1)

        screen.fill(white)

        text = font.render(f"{str(current_number+1)}/{str(total)}", True, black)
        text_size = text.get_size()
        text_pos = (0, 0)
        if in_left:
            text_pos = (margin_side, window_size[1]-text_size[1]-margin_bottom)
        else:
            text_pos = (window_size[0]-text_size[0]-margin_side, window_size[1]-text_size[1]-margin_bottom)
        blit_with_alpha(screen, text, text_pos)

        if current_image is not None:
            image_size = current_image.get_size()
            image_pos = (0, 0)
            if in_left:
                image_pos = (margin_side, window_size[1]-image_size[1]-text_size[1]-margin_bottom)
            else:
                image_pos = (window_size[0]-image_size[0]-margin_side, window_size[1]-image_size[1]-text_size[1]-margin_bottom)
            blit_with_alpha(screen, current_image, image_pos)
        
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    while True:
        try:
            run()
            break
        except:
            continue
