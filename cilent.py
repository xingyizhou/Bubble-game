import Tkinter as tk
from PIL import Image, ImageTk, ImageFilter
import socket
import numpy
import random
import json

class BubbleGame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width=1200, height=800)
        self.master.title('Bubble game')
        self._box_width = 300
        self._box_height = 300
        self._r = 15
        self._user_name = 'test'
        self._image_id = 1
        self._ans = 1
        self._point = 0
        self._total_score = 0
        self._true_image = ImageTk.PhotoImage(Image.open('true_image.png').resize((150, 150)))
        self._false_image = ImageTk.PhotoImage(Image.open('false_image.png').resize((150, 150)))

        self.init_image_files()
        # This allows the size specification to take effect
        self.pack_propagate(0)
 
        # We'll use the flexible pack layout manager
        self.pack()
        
        self._r_label = tk.Label(self, text = 'Radius : {:d}'.format(self._r))
        self._r_label.place(x = 330, y = 250)


        self._img_1 = ImageTk.PhotoImage(Image.open('default.png').resize((self._box_height, self._box_width)))
        self._image_box_1 = tk.Label(self, image = self._img_1)
        self._image_box_1.place(x = 0, y = 0)

 
        self._img_2 = ImageTk.PhotoImage(Image.open('default.png').resize((self._box_height, self._box_width)))
        self._image_box_2 = tk.Label(self, image = self._img_2)
        self._image_box_2.place(x = 900, y = 0)

        self._bubbles = []


        self._img_origin = Image.open('default.png')
        self._img = self.mask_image(self._img_origin)
        self._bubble_img = ImageTk.PhotoImage(self._img)
        self._image_box_bubble = tk.Label(self, image = self._bubble_img)
        self._image_box_bubble.place(x = 350, y = 300)
        self._image_box_bubble.bind("<Button-1>", self.callback)

        self._name_1 = tk.Label(self, text = 'defalut')
        self._name_1.place(x = 50, y = 350)
        #self._name_1.pack(side = tk.LEFT)
        self._button_1 = tk.Button(self, text = 'click me or press 1',command = self.choose_1)
        #self._button_1.pack(side = tk.LEFT)
        self._button_1.place(x = 20, y = 400)

        self._name_2 = tk.Label(self, text = 'defalut')
        self._name_2.pack(side = tk.RIGHT)
        self._name_2.place(x = 1050, y = 350)
        self._button_2 = tk.Button(self, text = 'click me or press 2',command = self.choose_2)
        self._button_2.pack(side = tk.RIGHT)
        self._button_2.place(x = 1020, y = 400)

        self._point_label = tk.Label(self, text = 'Point : {:d}'.format(self._point))
        self._point_label.place(x = 500, y = 250)

        self._user_label = tk.Label(self, text = 'User name : {:s}'.format(self._user_name))
        self._user_label.place(x = 330, y = 150)

        self._score_label = tk.Label(self, text = 'Total score : {:d}'.format(self._total_score))
        self._score_label.place(x = 500, y = 150)

        self._resluts = tk.Label(self, image = self._true_image)
        self._resluts.place(x = 700, y = 150, height = 150, width = 150)

        self.focus_set()
        self.bind("<Key>", self.key)

        

      #  self.mask_image(img)

    def init_image_files(self):
        self._image_path = '/Users/tenstep/Datasets/CUB_200_2011/CUB_200_2011/images/'
        self._image_name = ['default.png']
        images_index_file = open('images.txt', 'r')
        for line in images_index_file:
            s = line.split(' ')
            self._image_name.append(s[1][:-1])
        images_index_file.close()

        self._class_name = ['default']
        class_name_file = open('classes.txt', 'r')
        for line in class_name_file:
            s = line.split(' ')
            s = s[1].split('.')
            self._class_name.append(s[1])
        class_name_file.close()

        self._label = [0]
        label_file = open('image_class_labels.txt', 'r')
        for line in label_file:
            s = line.split(' ')
            self._label.append(int(s[1]))
        label_file.close()

    def key(self, event):
        if event.char == 'w':
            self._r = self._r + 1
        if event.char == 's' and self._r > 0:
            self._r = self._r - 1
        if event.char == '1':
            self.choose_1()
        if event.char == '2':
            self.choose_2()
        self._r_label.configure(text = 'Radius : {:d}'.format(self._r))

    def init_image(self, img_id_1, img_id_2, bubble_id):
        self._point = 300
        self._point_label.configure(text = 'Point : {:d}'.format(self._point))
        self._bubbles = []
        self._image_id = bubble_id

        #print 'img_1 label', self._label[img_id_1], self._class_name[self._label[img_id_1]]
        #print 'img_2 label', self._label[img_id_2], self._class_name[self._label[img_id_2]]
        #print 'bubble label', self._label[bubble_id], self._class_name[self._label[bubble_id]]
        self._name_1.configure(text = self._class_name[self._label[img_id_1]])
        img_path_1 = self._image_path + self._image_name[img_id_1]
        self._img_1 = ImageTk.PhotoImage(Image.open(img_path_1).resize((self._box_height, self._box_width)))
        self._image_box_1.configure(image = self._img_1)

        self._name_2.configure(text = self._class_name[self._label[img_id_2]])
        img_path_2 = self._image_path + self._image_name[img_id_2]
        self._img_2 = ImageTk.PhotoImage(Image.open(img_path_2).resize((self._box_height, self._box_width)))
        self._image_box_2.configure(image = self._img_2)

        bubble_path = self._image_path + self._image_name[bubble_id]
        self._img_origin = Image.open(bubble_path)
        self._img = self.mask_image(self._img_origin)
        self._bubble_img = ImageTk.PhotoImage(self._img)
        self._image_box_bubble.configure(image = self._bubble_img)

    def submit(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        sock.connect(('localhost', 8001))
        n = len(self._bubbles)
        js = {'user_name':self._user_name, 'image_id':self._image_id, 'bubble_num':n}
        for i in range(n):
            x = self._bubbles[i][0]
            y = self._bubbles[i][1]
            r = self._bubbles[i][2]
            js['x{:d}'.format(i)] = x
            js['y{:d}'.format(i)] = y
            js['r{:d}'.format(i)] = r
        #print 'send js', js
        sock.send(json.dumps(js) + 'END')
        buf = sock.recv(1024)
        #print 'buf ', buf
        recv = json.loads(buf)
        self._ans = recv['ans']
        #print 'recv', recv
        sock.close()
        return recv

    def choose_1(self):
        if (self._ans == 1):
            self._resluts.configure(image = self._true_image)
            self._total_score = self._total_score + self._point
            self._score_label.configure(text = 'Total score : {:d}'.format(self._total_score))
        else:
            self._resluts.configure(image = self._false_image) 
        recv = self.submit()
        self.init_image(recv['img_id_1'], recv['img_id_2'], recv['bubble_id'])

    def choose_2(self):
        if (self._ans == 2):
            self._resluts.configure(image = self._true_image)
            self._total_score = self._total_score + self._point
            self._score_label.configure(text = 'Total score = {:d}'.format(self._total_score))
        else:
            self._resluts.configure(image = self._false_image)
        recv = self.submit()
        self.init_image(recv['img_id_1'], recv['img_id_2'], recv['bubble_id'])

    def callback(self, event):
        #print 'generate bubble at ', event.x, event.y
        self._point = self._point - self._r;
        self._point_label.configure(text = 'Point = {:d}'.format(self._point))
        if (self._point < 0):
            self._point = 0
        self._bubbles.append((event.x, event.y, self._r))
        self._img = self.mask_image(self._img_origin)
        self._bubble_img = ImageTk.PhotoImage(self._img)
        self._image_box_bubble.configure(image = self._bubble_img)

    def mask_image(self, img):
        img_origin = img
        img = img_origin.copy()
        pix_origin = img_origin.load()
        pix = img.load()
        width = img.width
        height = img.height
        for w in range(width):
            for h in range(height):
                d = (pix[w, h][0] + pix[w, h][1] + pix[w, h][2]) / 3
                pix[w, h] = (d, d, d)
        img = img.filter(ImageFilter.GaussianBlur(5))
        pix = img.load()
        n = len(self._bubbles)

        for i in range(n):
            w = self._bubbles[i][0]
            h = self._bubbles[i][1]
            r = self._bubbles[i][2]
            
            for dw in range(2 * r):
                for dh in range(2 * r):
                    if ((dw - r) * (dw - r) + (dh - r) * (dh - r) <= r * r and 
                        w + dw - r >= 0 and w + dw - r < width and 
                        h + dh - r >= 0 and h + dh - r < height):
                        pix[w + dw - r, h + dh - r] = pix_origin[w + dw - r, h + dh - r]
            
        self.img = img_origin.copy;
        return img


app = BubbleGame(tk.Tk())
app.mainloop()