import pygame
import win32api
import win32con
import win32gui
import requests
import io

white = (255, 255, 255)
current_number = -1
current_image = None
images = []

# changeable:
images_url = 'https://pastebin.ai/raw/ppkgdvet9s'
opacity = 150
opacity_step = 30
width = 400
width_step = 20
seconds = 30
in_left = True
margin_side = 10
margin_bottom = 100


def load_images():
    global images
    response = requests.get(images_url)
    data = response.text
    links = data.strip().split()
    
    new_images = []
    for link in links:
        r = requests.get(link)
        new_images.append(pygame.image.load(io.BytesIO(r.content)))
    # if len(images) != len(new_images):
    images = new_images
    print('saved', len(new_images), 'images')


def blit_with_alpha(target, source, location):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)


def scale(image):
    global width
    sizes = image.get_size()
    mult = width/sizes[0]
    return pygame.transform.scale(image, (sizes[0]*mult, sizes[1]*mult))


def update(delta):
    global current_number, current_image, images
    if current_number == -1 and len(images) > 0:
        current_number = 0       
        current_image = scale(images[current_number])
    elif 0 <= current_number+delta and current_number+delta < len(images):
        current_number += delta
        current_image = scale(images[current_number])


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

    done = 0
    while not done:   
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:   
                done = 1
                break
            if event.type == pygame.USEREVENT:
                load_images()
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
                    update(0)
                if event.key == pygame.K_DOWN:
                    width -= width_step
                    update(0)

                if event.key == pygame.K_LEFT:
                    update(-1)
                if event.key == pygame.K_RIGHT:
                    update(+1)

        screen.fill(white)

        if current_image is not None:
            image_size = current_image.get_size()
            positions = (0, 0)
            if in_left:
                positions = (margin_side, window_size[1]-image_size[1]-margin_bottom)
            else:
                positions = (window_size[0]-image_size[0]-margin_side, window_size[1]-image_size[1]-margin_bottom)
            blit_with_alpha(screen, current_image, positions)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    while True:
        try:
            run()
            break
        except:
            continue
