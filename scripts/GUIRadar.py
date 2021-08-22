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
        self.master.title("PokeRadar Reader")
        self.type_var = tk.IntVar()
        self.connect_button = tk.Button(self, text="Connect", fg="green", command=self.connect)
        self.connect_button.grid(column=0,row=1)
        self.current_info_display = tk.Text(self,height=5)
        self.current_info_display.grid(column=2, row=2, rowspan=3)
        self.image_display = tk.Label(self)
        self.image_display.grid(column=0, row=2, columnspan=2, rowspan=3)
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
        read_func = self.G6Reader.readRadar

        try:
            pk6 = PK6(read_func())
            error = False
        except Exception as e:
            print(e)
            error = True
        while error:
            try:
                pk6 = PK6(read_func())
                error = False
            except:
                error = True
        
        if not pk6.isValid:
            print("Invalid or Not Present")
            self.last_info = ""
            self.image_display.config(image='')
            self.current_info_display.delete(1.0, tk.END)
        elif str(pk6) != self.last_info:
            info = str(pk6)
            s1 = pb.SpriteResource('pokemon', pk6.species, shiny=pk6.shinyType).img_data
            im = Image.open(io.BytesIO(s1))
            image = ImageTk.PhotoImage(im)
            self.image = image
            self.image_display.config(image=image)
            self.last_info = info
            self.current_info_display.delete(1.0, tk.END)
            self.current_info_display.insert(1.0, info)
        self.after_token = self.after(1000, self.update)

root = tk.Tk()
app = Application(master=root)
app.mainloop()