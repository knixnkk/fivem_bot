from pywinauto.application import Application
import mss

app = Application().connect(title_re=".*MEOW TOWN.*")  
window = app.window(title_re=".*MEOW TOWN.*") 

rect = window.rectangle()

bbox = {
    'top': rect.top,
    'left': rect.left,
    'width': rect.width(),
    'height': rect.height()
}

with mss.mss() as sct:
    screenshot = sct.grab(bbox)

mss.tools.to_png(screenshot.rgb, screenshot.size, output='screenshot.png')

print(f"Captured screenshot of window: {bbox}")
