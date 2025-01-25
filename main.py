from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.lang.builder import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.core.audio import SoundLoader
from functools import partial
from kivy.clock import Clock
from kivy.graphics import Rectangle

import random
import string
import json

# builder halaman
Builder.load_file('homepage.kv')
Builder.load_file('levelpage.kv')
Builder.load_file('gamepage.kv')
Builder.load_file('temapage.kv')
Builder.load_file('skor_page.kv')

#json reader
def read_json_file(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data


#main app runner 
class MyApp(App):
    soundbgm = SoundLoader.load('assets/sounds/bgm.mp3')

    def build(self):
        self.playBGM()
        sm = ScreenManager()
        sm.transition = FadeTransition()
        sm.add_widget(HomePage())
        sm.add_widget(LevelPage())
        sm.add_widget(GamePage())
        sm.add_widget(TemaPage())
        sm.add_widget(SkorPage())
        return sm
    

    def playBGM(self):
        if(self.soundbgm):
            self.soundbgm.loop = True
            self.soundbgm.play()

class SkorPage(Screen):
    skor = None

    def set_score(self,arg_score):
        self.skor = arg_score
        angka_skor = self.ids.angka_skor
        angka_skor.text = str(self.skor)
        

class HomePage(Screen):
    pass

class LevelPage(Screen):
    def go_to_tema_page(self,level):
        self.manager.get_screen('tema_page').set_arg(level)
        self.manager.current = 'tema_page'


class GamePage(Screen):
    soal_count = 3
    arg_tema = None 
    arg_level = None
    currentSoalPicture = ""
    currentTheme = []
    currentIndexSoal = 0
    currentAnswer = []
    currentRandomOptions = []    
    totalPoint = 0

    def set_arg(self,tema,level):
        self.arg_level = level
        self.arg_tema = tema
        self.init_game()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)    
        self.currentIndexSoal = 0
        self.currentAnswer = []
        self.currentRandomOptions = []    


    def randomize(self,before):
        # Mengacak huruf dalam kalimat
        kalimat_acak = ''.join(random.sample(before, len(before)))
        # Menentukan jumlah huruf tambahan (antara 3 hingga 4)
        jumlah_tambahan = random.randint(3, 4)
        # Membuat huruf tambahan yang tidak ada di kalimat input
        huruf_tambahan = ''.join(random.choices(
            [c for c in string.ascii_uppercase if c not in before], 
            k=jumlah_tambahan
        ))
        # Menyisipkan kalimat acak di posisi acak dalam huruf tambahan
        campuran = kalimat_acak + huruf_tambahan
        # randomed = huruf_tambahan[:posisi] + kalimat_acak + huruf_tambahan[posisi:]
        randomed = ''.join(random.sample(campuran,len(campuran)))
        return randomed    

    def init_game(self):
        self.db = read_json_file("db.json")
        self.currentTheme = self.db[self.arg_tema]
        self.totalPoint = 0
        self.currentIndexSoal = 0
        random.shuffle(self.currentTheme)
        # SET jumlah soal disini
        self.currentTheme = self.currentTheme[:self.soal_count]    
        print("INISIASI")
        self.setupSoal()

    def go_to_score_page(self,nan):
        print(f"TOTAL POIN : {self.totalPoint}")
        self.manager.get_screen('score_page').set_score(self.totalPoint)
        self.manager.current = 'score_page'   

    def update_score(self):
        score_label = self.ids.score_label
        score_label.text = f"POIN : {self.totalPoint}"    

    def check_answer(self):
        print(self.currentAnswer)
        print(list(self.currentSoalName))
        if(self.currentAnswer == list(self.currentSoalName)):
                self.totalPoint = self.totalPoint + 100
                self.update_score() 
                self.next_soal()       
        else:
            print("FLASE")


    def setupSoal(self):
        index = self.currentIndexSoal
        self.currentSoalName = self.currentTheme[index]['name']
        self.currentSoalPicture = f"db/images/{self.currentTheme[index]['source']}"
        self.currentSoalSound = f"db/sound/{self.currentTheme[index]['sound']}"

        randomed = self.randomize(self.currentSoalName)
        self.currentAnswer = list(' '*len(self.currentSoalName))
        self.currentRandomOptions = list(randomed)
        
        self.update_score()
        if (self.arg_level):
            sound_button = Button(
                size=(150, 150),
                size_hint=(None, None),
                allow_stretch=False,
                keep_ratio=True,
                pos_hint={'x': 0.7, 'y': 0.5},
                background_normal='assets/buttons/nav/sound.png',
                background_down='assets/buttons/nav/sound.png',
                border=[0, 0, 0, 0]
            )
            sound_button.bind(on_press= lambda instance: self.play_sound(self.currentSoalSound))
            self.add_widget(sound_button)

        image_soal = self.ids.image_soal
        image_soal.source = self.currentSoalPicture

        answer_container = self.ids.answer_container
        answer_container.clear_widgets()
        answer_container.cols = len(self.currentAnswer)
        
        options_container = self.ids.option_container
        options_container.clear_widgets()    
        for i in range(1, len(self.currentAnswer) + 1):
            box = AnswerBox()
            box.label_text = ' '
            answer_container.add_widget(box)
        for x in range(1, len(self.currentRandomOptions)+ 1):
            box = RandomAnswer()
            box.label_text = self.currentRandomOptions[x-1] 
            box.on_press = partial(self.hit_answer,x-1)
            options_container.add_widget(box)
        fillerWidgets = [self.ids.fillerA,self.ids.fillerB]

        # for filler in range(0,len(fillerWidgets)):
        #     filler.do_layout()

    def next_soal(self):
        if(self.currentIndexSoal < (self.soal_count-1)):
            print("GANTI SOAL")
            self.currentIndexSoal = self.currentIndexSoal + 1
            self.setupSoal()
        else:
           print("SELESAI")
           self.play_sound('assets/sounds/yay.mp3')
           self.add_widget(WinDecoration())
           Clock.schedule_once(self.go_to_score_page, 2)
            

    def play_sound(self,source):
        sound = SoundLoader.load(source)
        if(sound):
            sound.play()

    def go_to_home(self):
        self.manager.current = 'home_page'

            
    def hit_answer(self,index):
        if((sum(1 for item in self.currentAnswer if item == ' ') != 0)):  
        #    jika masih bisa menjawab
            self.currentAnswer[max((i+1 for i, c in enumerate(self.currentAnswer) if c != ' '),default=0)] = self.currentRandomOptions[index]
            # self.currentAnswer[0] = 'A'
            self.currentRandomOptions.pop(index)
            answer_container = self.ids.answer_container
            answer_container.clear_widgets()
            answer_container.cols = len(self.currentAnswer)
            options_container = self.ids.option_container
            options_container.clear_widgets()    
            for i in range(1, len(self.currentAnswer) + 1):
                box = AnswerBox()
                box.label_text = self.currentAnswer[i-1]
                answer_container.add_widget(box)
            for x in range(1, len(self.currentRandomOptions)+ 1):
                box = RandomAnswer()
                box.label_text = self.currentRandomOptions[x-1] 
                box.on_press = partial(self.hit_answer,x-1)
                options_container.add_widget(box)
            self.check_answer()         
        else:
            print("")  
    
    

class TemaPage(Screen):
    arg_level = BooleanProperty(False)   

    def set_arg(self,level):
        self.arg_level = level
    
    def gotoGamePage(self,tema):
        self.manager.remove_widget(self.manager.get_screen('game_page'))
        self.manager.add_widget(GamePage())
        self.manager.get_screen('game_page').set_arg(tema,self.arg_level)
        self.manager.current = 'game_page'


class AnswerBox(Button):
    label_text = StringProperty('')


class RandomAnswer(Button):
    label_text = StringProperty('');

class WinDecoration(Image):
    pass

class OptionLabel(Label):
    pass

if __name__ == '__main__':
    MyApp().run()