import tkinter as tk
import hra_classy as hc
import os, json

class MainMenu:
  #zabezpecuje zmeny medzi obrazmi
  def __init__(self, window):
    self.dir_path = os.path.dirname(os.path.realpath(__file__)) #absolutna adresa tohto suboru
    self.root = window
    #obrazky
    self.patkan_img = [tk.PhotoImage(file = self.dir_path+'/data/patkan_LORGE.gif'), tk.PhotoImage(file = self.dir_path+'/data/patkan_LORGE.gif', format = 'gif -index 1')]
    self.endless_bg = tk.PhotoImage(file = self.dir_path+'/data/d.gif')
    self.exit_img = tk.PhotoImage(file = self.dir_path+'/data/exit.png')
    self.back_img = tk.PhotoImage(file = self.dir_path+'/data/back.png')
    self.help_img = tk.PhotoImage(file = self.dir_path+'/data/help.png')
    #všetky potrebné widgety
    self.patkan = tk.Label(self.root, image = self.patkan_img[0])
    self.canvas = tk.Canvas(self.root)
    self.names = tk.Label(self.root, text = None, font = ('LeviWindows', 75), anchor = tk.NW, justify = tk.LEFT)
    self.scores = tk.Label(self.root, text = None, font = ('LeviWindows', 75), anchor = tk.NW, justify = tk.LEFT)
    self.help = tk.Label(self.root, image = self.help_img)
    #tlacitka hlavneho menu
    self.buttons = []
    self.buttons.append(tk.Button(self.root, text = 'Štart', width = 20, font = ('LeviWindows', 80), relief = tk.GROOVE, command = self.game))
    self.buttons.append(tk.Button(self.root, text = 'Ako hrať?', width = 20, font = ('LeviWindows', 80), relief = tk.GROOVE, command = self.how2))
    self.buttons.append(tk.Button(self.root, text = 'Vysoké skóre', width = 20, font = ('LeviWindows', 80), relief = tk.GROOVE, command = self.high_score_screen))
    self.buttons.append(tk.Button(self.root, image = self.exit_img, width = 30, height = 30, relief = tk.FLAT, command = self.root.destroy))
    self.back_btn = tk.Button(self.root, image = self.back_img, width = 30, height = 30, relief = tk.FLAT, command = self.back2menu)
    
    self.root.bind('<Escape>', self.pause_game)

    self.paused = True
    self.pause_id = None
    
    self.place()
    
  def place(self):
    self.patkan.place(relx = 0.5, rely = 0.2, anchor = tk.NE)
    self.buttons[0].place(relx = 0.75, rely = 0.3, anchor = tk.CENTER)
    self.buttons[1].place(relx = 0.75, rely = 0.5, anchor = tk.CENTER)
    self.buttons[2].place(relx = 0.75, rely = 0.7, anchor = tk.CENTER)
    self.buttons[3].place(relx = 0.03, rely = 0.05, anchor = tk.CENTER)
    self.play_gif()
  
  def play_gif(self, index = 3):
    self.patkan.config(image = self.patkan_img[index % 2])
    if index != 0:
      self.root.after(100, lambda: self.play_gif(index-1))
  
  def pause_game(self, event = None):
    if not self.paused:
      self.paused = self.data.freeze()
      self.canvas.tag_raise('pauza')
      self.canvas.itemconfigure(self.data.pauza_text, state = 'normal')
      self.canvas.itemconfigure(self.data.pauza_text_dole, state = 'normal')
      self.pause_id = self.root.bind('<Button-1>', self.resume)
    else:
      try:
        self.root.unbind('<Button-1>', self.pause_id)
      except tk.TclError:
        pass
      self.canvas.delete('all')
      self.canvas.pack_forget()
      self.back2menu()
  
  def resume(self, event):
    pos = self.data.hrac.bbox()
    if (event.x > pos[0] and event.x < pos[2]) and (event.y > pos[1] and event.y < pos[3]):
      try:
        self.root.unbind('<Button-1>', self.pause_id)
      except tk.TclError:
        pass
      self.paused = self.data.unfreeze()
      self.canvas.itemconfigure(self.data.pauza_text, state = 'hidden')
      self.canvas.itemconfigure(self.data.pauza_text_dole, state = 'hidden')
    else:
      print('minmo')

  def game(self, znova = False):
    if znova:
      self.canvas.delete('all')
    else:
      for w in self.buttons:
        w.place_forget()
      self.paused = False
      self.patkan.pack_forget()
    self.canvas.create_image(0,0,image = self.endless_bg, anchor = tk.NW)
    self.canvas.pack(fill = 'both', expand = True)
    self.data = hc.GameData(self.canvas, hc.Player(self.canvas, "/data/patkan.gif"), self)
    self.data.pridaj_dukat()
    self.data.game_tick()
  
  def high_score_screen(self):
    for d in self.buttons:
      d.place_forget()
    self.patkan.place_forget()
    with open(self.dir_path+'/data/vysoke_skore.json') as f:
      data = json.loads(f.read())
    i = 1
    names = ''
    values = ''
    for key, value in data.items():
      names += str(i) + '. ' + key + '\n'
      values += str(value) + '\n'
      i += 1
    self.names.config(text = names)
    self.scores.config(text = values)
    self.names.place(relx = 0.2, rely = 0)
    self.scores.place(relx = 0.7, rely = 0)
    self.back_btn.place(relx = 0.03, rely = 0.05, anchor = tk.CENTER)
  
  def how2(self):
    for d in self.buttons:
      d.place_forget()
    self.patkan.place_forget()
    self.help.place(relx = 0, rely = 0)
    self.back_btn.place(relx = 0.03, rely = 0.05, anchor = tk.CENTER)
  
  def back2menu(self):
    self.back_btn.place_forget()
    self.names.place_forget()
    self.scores.place_forget()
    self.help.place_forget()
    self.place()

if __name__ == '__main__':
  print('Spustite main.py!')