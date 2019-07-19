import tkinter as tk
import random as r
import os, json

global hp_pos

hp_pos = 2

class Dukat:
  #obsahuje informacie o pozicii, hodnote a rychlosti daneho dukatu
  def __init__(self, canvas, velocity, value, filename):
    self.canvas = canvas
    self.dir_path = os.path.dirname(os.path.realpath(__file__)) #absolutna adresa tohto suboru
    self.m_velocity = velocity
    self.m_value = value
    self.m_image = tk.PhotoImage(file = self.dir_path+'/data'+filename)
    self.m_x = r.randint(0+50,1366-50)
    self.m_body = self.canvas.create_image(self.m_x, 0, image = self.m_image, anchor = tk.CENTER, tag = 'dukat')
    self.invis_body = self.canvas.create_rectangle(self.m_x-50, -50, self.m_x+50, 50, fill = '', outline = '', tag = 'dukat')
    self.alive = True
  
  def die(self, loseHP = False):
    global hp_pos
    del self.m_image
    self.canvas.delete(self.m_body)
    self.alive = False
    if loseHP:
      self.canvas.itemconfigure('HP'+str(hp_pos), state = 'hidden')
      hp_pos -= 1

  def position(self):
    return self.canvas.coords(self.m_body)

class Player:
  #obsahuje informacie o hracovi, jeho pozicii a zabezpecuje pohyb
  def __init__(self, canvas, filename):
    self.canvas = canvas
    self.canvas.update()
    self.dir_path = os.path.dirname(os.path.realpath(__file__)) #absolutna adresa tohto suboru
    self.frames = [tk.PhotoImage(file = self.dir_path+filename, format = 'gif -index 0'), tk.PhotoImage(file = self.dir_path+filename, format = 'gif -index 1')]
    self.posX = self.canvas.winfo_width() / 2
    self.posY = self.canvas.winfo_height() - 150
    self.m_body = self.canvas.create_image(self.posX, self.posY, image = self.frames[0], anchor = tk.CENTER)
    self.m_body2 = self.canvas.create_image(self.posX, self.posY, image = self.frames[1], anchor = tk.CENTER, state = 'hidden')
    self.movement = self.canvas.master.bind('<Motion>', self.move)

  def move(self, event):
    self.canvas.coords(self.m_body, event.x, self.posY)
    self.canvas.coords(self.m_body2, event.x, self.posY)

  def position(self):
    return self.canvas.coords(self.m_body)
  
  def bbox(self):
    return self.canvas.bbox(self.m_body)

class GameData:
  #obsahuje informacie o vsetkom, co sa pocas hry deje
  def __init__(self, canvas, hrac, menu):
    global hp_pos
    hp_pos = 2
    self.canvas = canvas
    self.menu = menu
    self.canvas.update()
    self.pocet_bodov = 0
    self.dukaty = []
    self.hrac = hrac
    self.level = 1
    self.dir_path = os.path.dirname(os.path.realpath(__file__)) #absolutna adresa tohto suboru
    self.win_height = self.canvas.winfo_height()
    self.win_width = self.canvas.winfo_width()
    
    #informacie ktore vidi hrac
    self.level_up_message = self.canvas.create_text(20, 30, text = 'Level ' + str(self.level), font = ('LeviWindows',50), anchor = tk.NW, fill = 'white', tag = 'game_info')
    self.score_text = self.canvas.create_text(20, 80, text = 'Skóre: '+str(self.pocet_bodov), font = ('LeviWindows',50), anchor = tk.NW, fill = 'white', tag = 'game_info')
    self.srdce = tk.PhotoImage(file = self.dir_path+'/data/srdce.png')
    self.health = [self.canvas.create_image(10+60*i, 125, image = self.srdce, anchor = tk.NW, tag = 'HP'+str(i)) for i in range(3)]
    
    #obrazovka pre pauzu
    self.pauza_text = self.canvas.create_text(self.win_width / 2, self.win_height / 2, text = 'PAUZA', font = ('LeviWindows',80), state = 'hidden', fill = 'white', tag = 'pauza')
    self.pauza_text_dole = self.canvas.create_text(self.win_width / 2, self.win_height / 2+50, text = 'Kliknite na POTKANA pre odpauzovanie alebo stlačte ESC pre ukončenie hry', font = ('LeviWindows',50), state = 'hidden', fill = 'white', tag = 'pauza')
    
    #obrazovka pre koniec hry
    self.game_over = self.canvas.create_text(self.win_width / 2, self.win_height * 0.3, text = 'KONIEC HRY', font = ('LeviWindows',125), state = 'hidden', fill = 'white', tag = 'koniec_hry')
    self.main_menu_btn = tk.Button(self.canvas.master, text = 'Hlavné menu', relief = tk.FLAT, command = self.back2menu)
    self.nova_hra_button = tk.Button(self.canvas.master, text = 'Nová hra', relief = tk.FLAT, command = self.new_game)
    self.main_menu_btn_win = self.canvas.create_window(self.win_width * 0.4, self.win_height * 0.55, width = 200, height = 50, anchor = tk.CENTER, window = self.main_menu_btn, state = 'hidden', tag = 'koniec_hry')
    self.nova_hra_btn_win = self.canvas.create_window(self.win_width * 0.6, self.win_height * 0.55, width = 200, height = 50, anchor = tk.CENTER, window = self.nova_hra_button, state = 'hidden', tag = 'koniec_hry')
    self.high_score = self.canvas.create_text(self.win_width * 0.45, self.win_height * 0.65, anchor = tk.CENTER, text = 'Zadajte meno:', font = ('LeviWindows',50), fill = 'white', state = 'hidden', tag = 'koniec_hry')
    self.entry_data = tk.StringVar()
    self.entry_data.trace('w', self.limit_entry)
    self.name_entry = tk.Entry(self.canvas.master, font = ('LeviWindows', 40), textvariable = self.entry_data)
    self.submit = tk.Button(self.canvas.master, text = 'odošli', relief = tk.FLAT, command = self.update_high_scores)
    self.name_entry_win = self.canvas.create_window(self.win_width * 0.6, self.win_height * 0.65, width = 150, height = 50, anchor = tk.CENTER, window = self.name_entry, state = 'hidden', tag = 'koniec_hry')
    self.submit_win = self.canvas.create_window(self.win_width / 2, self.win_height * 0.75, width = 200, height = 50, anchor = tk.CENTER, window = self.submit, state = 'hidden', tag = 'koniec_hry')
    
    #kontrolne id na ukoncenie nekonecnych funkcii
    self.pridaj_dukat_id = None
    self.game_tick_id = None
  
  #prida do hry novy dukat a odstrani tie, ktoré sú mrtve
  def pridaj_dukat(self, novy_dukat = False):
    self.interval_novych_dukatov = int(2500-500*self.level)
    if self.interval_novych_dukatov < 300: self.interval_novych_dukatov = 300 # najvyssia rychlost
    dukat_info = self.ktory_dukat()
    if not novy_dukat:
      novy_dukat = Dukat(self.canvas, self.level, dukat_info[0], dukat_info[1])
    for index, dukat in enumerate(self.dukaty):
      if not dukat.alive:
        self.dukaty[index] = novy_dukat
        self.pridaj_dukat_id = self.canvas.master.after(self.interval_novych_dukatov, lambda: self.pridaj_dukat(Dukat(self.canvas, self.level, dukat_info[0], dukat_info[1])))
        return
    self.dukaty.append(novy_dukat)
    self.pridaj_dukat_id = self.canvas.after(self.interval_novych_dukatov, lambda: self.pridaj_dukat(Dukat(self.canvas, self.level, dukat_info[0], dukat_info[1])))
  
  #vymyslí, ako pridať body podla toho, či niečo prekryva poziciu hraca
  def pridaj_body(self):
    try:
      x1, y1, x2, y2 = self.hrac.bbox()
    except TypeError:
      return False
    overlapping = self.canvas.find_overlapping(x1, y1, x2, y2)
    if len(overlapping) > 2:
      for d in self.dukaty:
        if d.m_body == overlapping[2]:
          if not d.m_value:
            d.die()
            return True
          self.pocet_bodov += d.m_value
          self.canvas.itemconfigure(self.score_text, text = 'Skóre: '+str(self.pocet_bodov))
          if self.pocet_bodov > (self.level**2) * 100: self.level_up()
          d.die(d.m_value < 0)
          return False
        if not d.alive: self.dukaty.remove(d)
    return False
  
  #pohne vsetky padajuce veci a skontroluje, či nie sú mimo obrazovky
  def pohni_dukaty(self):
    self.canvas.move('dukat', 0, self.level)
    overlapping = self.canvas.find_overlapping(0, 768, 1366, 768)
    if overlapping:
      for d in self.dukaty:
        if d.m_body in overlapping:
          d.die(d.m_value > 0)
  
  #hlavny gameloop, používa vyššie definované funkcie a kontroluje počet životov
  def game_tick(self):
    global hp_pos
    flag = self.pridaj_body()
    self.pohni_dukaty()
    if flag and hp_pos != 2:
      hp_pos += 1
      self.canvas.itemconfigure('HP'+str(hp_pos), state = 'normal')
    if hp_pos < 0:
      self.koniec_hry()
      return
    self.game_tick_id = self.canvas.after(16, self.game_tick)
  
  def level_up(self):
    self.level += 1
    self.canvas.itemconfigure(self.level_up_message,text = 'Level ' + str(self.level), state = 'normal')
  
  #vyberie aky dukat sa ma spawnnut
  def ktory_dukat(self):
    global hp_pos
    temp = r.randint(1,100)
    if temp < 40:
      return (10, '/dukat_10.png')
    elif temp < 50:
      return (-50, '/cancer_m.png')
    elif temp < 60:
      return (-100, '/cancer.png')
    elif temp < 80:
      return (25, '/dukat_25.png')
    elif temp < 90 and hp_pos != 2:
      return (0 ,'/srdce.png')
    elif temp < 99:
      return (50, '/dukat_50.png')
    else:
      return (125, '/dukat_beast.png')
  
  #vyvola obrazovku konca hry
  def koniec_hry(self):
    self.freeze()
    self.canvas.tag_raise('koniec_hry')
    self.canvas.itemconfigure('koniec_hry', state = 'normal')
    self.canvas.itemconfigure('game_info', anchor = tk.CENTER)
    self.canvas.coords(self.level_up_message, self.win_width/2, self.win_height * 0.3 + 60)
    self.canvas.coords(self.score_text, self.win_width/2, self.win_height * 0.3 + 110)

  #zastaví gameloop
  def freeze(self):
    try:
      self.canvas.master.unbind('<Motion>', self.hrac.movement)
    except tk.TclError:
      pass
    self.canvas.after_cancel(self.pridaj_dukat_id)
    self.canvas.after_cancel(self.game_tick_id)
    return True
  #znova obnoví gameloop
  def unfreeze(self):
    self.canvas.master.bind('<Motion>', self.hrac.move)
    self.pridaj_dukat()
    self.game_tick()
    return False
  
  def back2menu(self):
    self.menu.paused = True
    self.menu.pause_game()

  def new_game(self):
    self.menu.game(True)
  
  #skontroluje zadané meno a uloží hodnoty do súboru json
  def update_high_scores(self):
    with open(self.dir_path+'/data/vysoke_skore.json') as s:
      data = s.read()
    data_parsed = json.loads(data)
    data_parsed[self.entry_data.get()] = self.pocet_bodov
    dsorted = dict(sorted(data_parsed.items(), key = lambda elem: self.help_sort(elem), reverse = True)[:10])
    data_parsed = json.dumps(dsorted)
    with open(self.dir_path+'/data/vysoke_skore.json', 'w') as w:
      w.write(data_parsed)
    self.submit.config(state = tk.DISABLED)

  #pomocné funkcie
  def help_sort(self, item):
    return item[1]

  def limit_entry(self, *args):
    value = self.name_entry.get()
    if len(value) > 10: self.entry_data.set(value[:10])

if __name__ == '__main__':
  print('Spustite main.py!')