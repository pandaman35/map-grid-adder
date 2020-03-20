# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 08:47:55 2020

@author: peter
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog


WINDOW_SIZE_INIT = 200
GRID_COLOR_INIT = 150
GRID_SIZE_INIT = 100
GRID_THICKNESS_INIT = 1


class GUI:
    def __init__(self, master):
        # image
        img = np.zeros((WINDOW_SIZE_INIT,WINDOW_SIZE_INIT,3),np.uint8)
        r,g,b = cv2.split(img)
        self.image = cv2.merge([b,g,r])
        self.gridded_image = self.image.copy()
        self.flag_picture_loaded = 0
        self.path = 0
        
        # color sliders
        self.old_R = GRID_COLOR_INIT
        self.old_G = GRID_COLOR_INIT
        self.old_B = GRID_COLOR_INIT
        
        # other stuffos
        self.mouse_x = 0
        self.mouse_y = 0
        self.kill_loop = False
        
        self.initGUI(master)
        self.initWindows()
        
        
    def initGUI(self, master):
        self.master = master
        
        # Set window size
        self.master.geometry('500x200')
        
        self.frame_top = tk.Frame(self.master)
        self.frame_top.pack(fill=tk.BOTH, expand=1)

        self.frame_file = tk.Frame(self.frame_top)
        self.frame_file.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.frame_grid_size = tk.Frame(self.frame_top)
        self.frame_grid_size.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.frame_grid_color = tk.Frame(self.frame_top)
        self.frame_grid_color.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.frame_quit = tk.Frame(self.master)
        self.frame_quit.pack(fill=tk.BOTH, expand=1)
        
        
        ########################### FILE FRAME ################################
        self.btn_load_image = tk.Button(self.frame_file, text='Load image', command=self.selectImage)
        self.btn_load_image.pack(expand=1)
        
        self.btn_save = tk.Button(self.frame_file, text='Save image', command=self.saveImage)
        self.btn_save.pack(expand=1)

        
        ########################### GRID SIZE FRAME ###########################
        self.label_grid_size = tk.Label(self.frame_grid_size, text='Grid size')
        self.label_grid_size.pack(expand=1)
        
        self.sldr_grid_size = tk.Scale(self.frame_grid_size, from_=10, to=500, orient='horizontal', digits=1, resolution=1)
        self.sldr_grid_size.set(GRID_SIZE_INIT)
        self.sldr_grid_size.pack(fill=tk.BOTH, expand=1)
        
        self.label_grid_thickness = tk.Label(self.frame_grid_size, text='Grid thiccness')
        self.label_grid_thickness.pack(expand=1)
        
        self.sldr_grid_thickness = tk.Scale(self.frame_grid_size, from_=1, to=10, orient='horizontal', digits=1, resolution=1)
        self.sldr_grid_thickness.set(GRID_THICKNESS_INIT)
        self.sldr_grid_thickness.pack(fill=tk.BOTH, expand=1)
        
        
        ########################### GRID COLOR FRAME ##########################
        self.label_grid_color = tk.Label(self.frame_grid_color, text='Grid color [RGB]')
        self.label_grid_color.pack(expand=1)
        
        self.sldr_grid_R = tk.Scale(self.frame_grid_color, from_=0, to=255, orient='horizontal', digits=1, resolution=1)
        self.sldr_grid_R.set(GRID_COLOR_INIT)
        self.sldr_grid_R.pack(fill=tk.BOTH, expand=1)
        self.sldr_grid_G = tk.Scale(self.frame_grid_color, from_=0, to=255, orient='horizontal', digits=1, resolution=1)
        self.sldr_grid_G.set(GRID_COLOR_INIT)
        self.sldr_grid_G.pack(fill=tk.BOTH, expand=1)
        self.sldr_grid_B = tk.Scale(self.frame_grid_color, from_=0, to=255, orient='horizontal', digits=1, resolution=1)
        self.sldr_grid_B.set(GRID_COLOR_INIT)
        self.sldr_grid_B.pack(fill=tk.BOTH, expand=1)
        
        self.var_aspect = tk.IntVar()
        self.check_aspect = tk.Checkbutton(self.frame_grid_color, text='Keep color aspect ratio', variable=self.var_aspect)
        self.check_aspect.pack(expand=1)
        self.var_aspect.set(1)
        
        
        ########################### QUIT BUTTON ###############################
        # Quit button
        self.btn_quit = tk.Button(self.frame_quit, text='Quit program', command=self.killAll)
        self.btn_quit.pack(expand=1)
    
    def initWindows(self):
        self.window_name = 'Gridded image'
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        self.resizeWindow()
    
    def selectImage(self):        
        # open a file chooser dialog and allow the user to select an input image
        self.path = filedialog.askopenfilename()
        if len(self.path) > 0:
            self.image = cv2.imread(self.path,cv2.IMREAD_COLOR)
            self.flag_picture_loaded = 1
            self.resizeWindow()
        else:
            print('No image chosen.')
    
    def saveImage(self):        
        if self.flag_picture_loaded:
            # just removing file extension, assuming only .jpg .png .jpeg
            if self.path[:-5] == '.jpeg':
                pathname = self.path[:-5]
            else:
                pathname = self.path[:-4]
            
            # Saving the numpy array
            grid_size = self.sldr_grid_size.get()
            filename = pathname + '_grid{:d}'.format(grid_size) + '.png'
            cv2.imwrite(filename, self.gridded_image)
        else:
            print('No picture has been chosen yet.')
    
    def resizeWindow(self):
        cv2.resizeWindow(self.window_name, self.image.shape[1], self.image.shape[0])
        
    def aspectRatio(self):        
        if self.var_aspect.get():
            diff_R = self.sldr_grid_R.get() - self.old_R
            diff_G = self.sldr_grid_G.get() - self.old_G
            diff_B = self.sldr_grid_B.get() - self.old_B
            
            if diff_R != 0:
                self.sldr_grid_G.set(self.sldr_grid_G.get() + diff_R)
                self.sldr_grid_B.set(self.sldr_grid_B.get() + diff_R)
            elif diff_G != 0:
                self.sldr_grid_R.set(self.sldr_grid_R.get() + diff_G)
                self.sldr_grid_B.set(self.sldr_grid_B.get() + diff_G)
            elif diff_B != 0:
                self.sldr_grid_R.set(self.sldr_grid_R.get() + diff_B)
                self.sldr_grid_G.set(self.sldr_grid_G.get() + diff_B)
        
        self.old_R = self.sldr_grid_R.get()
        self.old_G = self.sldr_grid_G.get()
        self.old_B = self.sldr_grid_B.get()
    
    def killAll(self):        
        self.master.destroy()
        cv2.destroyAllWindows()
        self.kill_loop = True
    
    def hotKeys(self, key):
        if (key & 0xFF) == 27:
            self.killAll()


def drawGrid(image, size, thickness, color):
    h_lines = np.arange(0,image.shape[0], size)
    v_lines = np.arange(0,image.shape[1], size)
    for line in h_lines:
        cv2.line(image,(0,line),(image.shape[1],line),color,thickness)
    for line in v_lines:
        cv2.line(image,(line,0),(line,image.shape[0]),color,thickness)


if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)
    
    while True:
        gui.gridded_image = gui.image.copy()
        gui.aspectRatio()
        drawGrid(gui.gridded_image, gui.sldr_grid_size.get(), gui.sldr_grid_thickness.get(), (gui.sldr_grid_B.get(), gui.sldr_grid_G.get(), gui.sldr_grid_R.get()))
        cv2.imshow(gui.window_name, gui.gridded_image)
        
        gui.master.update()
        
        key_press = cv2.waitKey(50)
        gui.hotKeys(key_press)
        
        if gui.kill_loop:
            break

