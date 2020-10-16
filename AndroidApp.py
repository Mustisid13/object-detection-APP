'''
Camera Example
==============

This example demonstrates a simple use of the camera. It shows a window with
a buttoned labelled 'play' to turn the camera on and off. Note that
not finding a camera, perhaps because gstreamer is not installed, will
throw an exception during the kv language processing.

'''

# Uncomment these lines to see all the messages
# from kivy.logger import Logger
# import logging
# Logger.setLevel(logging.TRACE)

import pyttsx3
import requests
import json
import io
from PIL import Image

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time
Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 140)
    engine.say(text)
    engine.runAndWait()


class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        # timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("image.png")
        print("Captured")
        self.main()
    def main(self):
        img = Image.open('image.png', mode='r')
        # roi_img = img.crop(box)

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        content_type = 'image/jpeg'
        headers = {'content-type': content_type}
        response = requests.post('http://127.0.0.1:5000/api/test', data=img_byte_arr, headers=headers)
        res = json.loads(response.text)
        speak("there is a ")
        for txt in set(res['predictions'].values()):
            speak(txt)
        speak("in the image")
        # str = "predictions: "
        # for txt in res['predictions'].values():
        #     str = str+"\n"+txt
        # lbl = self.add_widget(Label(text=str, text_size=(600, None), line_height=1.5))


class TestCamera(App):

    def build(self):
        return CameraClick()


TestCamera().run()