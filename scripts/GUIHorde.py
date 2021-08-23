import io
import signal
import sys
import tkinter as tk
import pokebase as pb

# Go to root of PyNTRReader
sys.path.append('../')

from ntrreader import G6Reader
from PIL import Image, ImageTk
from structure import PK6
from ip import IP_ADDR

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.last_info = ""
        signal.signal(signal.SIGINT, self.signal_handler)

    def create_widgets(self):
        self.master.title("Horde Reader")
        self.type_var = tk.IntVar()
        self.connect_button = tk.Button(self, text="Connect", fg="green", command=self.connect)
        self.connect_button.grid(column=0,row=1)
        self.image_displays = []
        self.info_displays = []
        self.images = [0]*5
        for i in range(5):
            image_display = tk.Label(self)
            image_display.grid(column=2+i*2, row=2, columnspan=2, rowspan=3)
            self.image_displays.append(image_display)
            info_display = tk.Text(self,height=5)
            info_display.grid(column=2, row=8+i*3, columnspan=10, rowspan=3)
            self.info_displays.append(info_display)
        self.quit = tk.Button(self, text="Disconnect", fg="red", command=self.disconnect)
        self.quit.grid(column=1,row=1)

    def connect(self):
        print("Connecting to: ", IP_ADDR)
        self.G6Reader = G6Reader(IP_ADDR)
        self.update()

    def disconnect(self):
        print("Disconnecting")
        self.after_cancel(self.after_token)
        self.G6Reader.close(False)
        self.G6Reader = None
    
    def signal_handler(self, signal, frame):
        self.disconnect()
        sys.exit(0)
    
    def update(self):
        try:
            pk6s = self.G6Reader.readHorde()
            error = False
        except Exception as e:
            print(e)
            error = True
        while error:
            try:
                pk6s = self.G6Reader.readHorde()
                error = False
            except:
                error = True
        
        i = 0
        full_info = ""
        for pk6_data in pk6s:
            pk6 = PK6(pk6_data)
            self.info_displays[i].delete(1.0, tk.END)
            if not pk6.isValid:
                self.image_displays[i].config(image='')
            if pk6.isValid:
                info = str(pk6)
                s1 = pb.SpriteResource('pokemon', pk6.species, shiny=pk6.shinyType).img_data
                im = Image.open(io.BytesIO(s1)).convert('RGBA')
                image = ImageTk.PhotoImage(im)
                self.images[i] = image
                self.image_displays[i].config(image=image)
                self.last_info = info
                self.info_displays[i].insert(1.0, info)
            full_info += str(pk6) + '\n'
            i += 1
        self.last_info = full_info
        self.after_token = self.after(1000, self.update)

root = tk.Tk()
app = Application(master=root)
app.mainloop()