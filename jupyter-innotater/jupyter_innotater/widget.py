from .example import DrawingPad
from ipywidgets import HBox, VBox, Button, Text
from IPython import display
import numpy as np


class CustomBox(HBox):
    def __init__(self):
        drawing_pad = DrawingPad()
        button = Button(description="Clear", tooltip="Click me")
        save_button = Button(description="Save", tooltip="Click me")
        login_button = Button(description="Login", tooltip="Click me")
        text_area = Text(value='', placeholder='Type your name', description='Name:', disabled=False)
        button.on_click(lambda b : self.clean())
        save_button.on_click(lambda b : self.set_saved())
        login_button.on_click(lambda b : self.check())
        buttons = VBox([text_area, button, save_button, login_button])
        self.drawing_pad = drawing_pad
        self.text_area = text_area
        self.__saved = {}
        super().__init__([drawing_pad, buttons])

    def clean(self):
        self.drawing_pad.clear()
        self.text_area.value=""

    def is_empty(self):
        return len(self.drawing_pad.data[0])==0

    def set_saved(self):
        name = self.text_area.value
        self.__saved[name] = self.drawing_pad.data
        self.clean()
        print('Your signature was saved, ' + str(name))
    
    def get_saved(self):
        return self.__saved
    
    def renormalize(self,t):
        t = (t-t[0])/(t[-1]-t[0])
        return t

    def value(self,t, list_x, list_y, list_t):
        idx = (np.abs(list_t-t)).argmin()
        return np.array([list_x[idx], list_y[idx]])

    def value_der(self,t, list_x, list_y, list_t):
        idx = (np.abs(list_t-t)).argmin()
        return np.array([(list_x[idx]-list_x[idx-1])/(list_t[idx]-list_t[idx-1]), 
                        (list_y[idx]-list_y[idx-1])/(list_t[idx]-list_t[idx-1])])

    def distance(self,x, y):
        return np.linalg.norm(x-y)

    def distance_total(self,list_x, list_y, list_t, list_x_prime, list_y_prime, list_t_prime):
        grid_time = np.linspace(0, 1, 100)
        value_tot = sum([self.distance(self.value(t, list_x, list_y, list_t), self.value(t, list_x_prime, list_y_prime, list_t_prime)) for t in grid_time])
        value_der = sum([self.distance(self.value_der(t, list_x, list_y, list_t), self.value_der(t, list_x_prime, list_y_prime, list_t_prime)) for t in grid_time])
        # print(value_der)
        return value_tot + value_der / 15

    def normalize_all(self,x,y,t):
        x = np.array(x)
        y = np.array(y)
        t = np.array(t)
        list_t_norm = self.renormalize(t)
        list_x_norm = (x - np.mean(x))/(np.std(x))
        list_y_norm = (y - np.mean(y))/(np.std(y))
        return (list_x_norm, list_y_norm, list_t_norm)

    def check(self):
        if self.is_empty():
            print("Pas de dessin")
            return
        x,y,t = self.normalize_all(self.drawing_pad.data[0], self.drawing_pad.data[1], self.drawing_pad.data[2])
        grid_time = np.linspace(0, 1, 100)

        distance_min = 10000
        name_min = ""
        t_min = 0

        for (name, list_of_coord) in self.__saved.items():
            x_saved, y_saved, t_saved = self.normalize_all(list_of_coord[0], list_of_coord[1], list_of_coord[2])
            print('Trying to match with ' + str(name) + "'s signature...")
            distance = self.distance_total(x, y, t, x_saved, y_saved, t_saved) + np.abs(len(t)-len(t_saved))/2
            # print('distance: ' + str(distance))
            distance_norm = distance / np.sqrt(len(t_saved))
            print('distance_norm: ' + str(distance_norm))
            if distance_norm < distance_min:
                distance_min = distance_norm
                name_min = name
        if distance_min < 15:
            print('Welcome ' + str(name_min))
        else:
            print('Signature does not match')
