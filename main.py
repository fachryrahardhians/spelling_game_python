from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.lang.builder import Builder
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, BooleanProperty
from functools import partial

import random
import string
import json

# builder halaman
Builder.load_file('homepage.kv')
Builder.load_file('levelpage.kv')
Builder.load_file('gamepage.kv')
Builder.load_file('temapage.kv')

#json reader
def read_json_file(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data


#main app runner 
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.transition = FadeTransition()
        sm.add_widget(HomePage())
        sm.add_widget(LevelPage())
        sm.add_widget(GamePage())
        sm.add_widget(TemaPage())
        return sm

class HomePage(Screen):
    pass

class LevelPage(Screen):
    def go_to_tema_page(self,level):
        self.manager.get_screen('tema_page').set_arg(level)
        self.manager.current = 'tema_page'


class GamePage(Screen):
    arg_tema = StringProperty("")
    arg_level = BooleanProperty(False)
    currentSoalPicture = ""
    currentTheme = []
    currentIndexSoal = 0
    currentAnswer = []
    currentRandomOptions = []    

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
        print(self.arg_tema)

        random.shuffle(self.currentTheme)
        self.currentTheme = self.currentTheme[:10]    

        # self.currentSoalName = self.currentTheme[self.currentIndexSoal]['name']
        # self.currentSoalPicture = f"db/images/{self.currentTheme[self.currentIndexSoal]['source']}"
        # self.currentSoalSound = f"db/sound/{self.currentTheme[self.currentIndexSoal]['sound']}"

        # randomed = self.randomize(self.currentSoalName)
        # self.currentAnswer = list(' '*len(self.currentSoalName))
        # self.currentRandomOptions = list(randomed)
        
        # image_soal = self.ids.image_soal
        # image_soal.source = self.currentSoalPicture
        self.setupSoal(0)

        # answer_container = self.ids.answer_container
        # answer_container.clear_widgets()
        # answer_container.cols = len(self.currentAnswer)
        
        # options_container = self.ids.option_container
        # options_container.clear_widgets()    
        # for i in range(1, len(self.currentAnswer) + 1):
        #     box = AnswerBox()
        #     box.label_text = ' '
        #     answer_container.add_widget(box)
        # for x in range(1, len(self.currentRandomOptions)+ 1):
        #     box = RandomAnswer()
        #     box.label_text = self.currentRandomOptions[x-1] 
        #     box.on_press = partial(self.hit_answer,x-1)
        #     options_container.add_widget(box)


    def delete_answer(self):
        yes = 0 

    def check_answer(self):
        print(self.currentAnswer)
        print(list(self.currentSoalName))
        if(self.currentAnswer == list(self.currentSoalName)):
                print("YEAH")     
                self.next_soal()       
        else:
            print("FLASE")


    def setupSoal(self,index):
        self.currentSoalName = self.currentTheme[index]['name']
        self.currentSoalPicture = f"db/images/{self.currentTheme[index]['source']}"
        self.currentSoalSound = f"db/sound/{self.currentTheme[index]['sound']}"

        randomed = self.randomize(self.currentSoalName)
        self.currentAnswer = list(' '*len(self.currentSoalName))
        self.currentRandomOptions = list(randomed)
        
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

    def next_soal(self):
        if(self.currentIndexSoal < 9):
            print("GANTI SOAL")
            self.currentIndexSoal = self.currentIndexSoal + 1
            self.setupSoal(self.currentIndexSoal)
        else:
           print("SELESAI")
           print("Ke halaman point akhir")    
            



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
    # def create_options(self):
        # options_container = self.ids.option_container
        # options_container.clear_widgets()
        # ans = "MOBIL"
        # # Mengacak huruf dalam kalimat
        # kalimat_acak = ''.join(random.sample(ans, len(ans)))
        
        # # Menentukan jumlah huruf tambahan (antara 3 hingga 4)
        # jumlah_tambahan = random.randint(3, 4)
        
        # # Membuat huruf tambahan yang tidak ada di kalimat input
        # huruf_tambahan = ''.join(random.choices(
        #     [c for c in string.ascii_uppercase if c not in ans], 
        #     k=jumlah_tambahan
        # ))
        
        # # Menyisipkan kalimat acak di posisi acak dalam huruf tambahan
        # posisi = random.randint(0, len(huruf_tambahan))  # Posisi sisipan acakan
        # campuran = kalimat_acak + huruf_tambahan
        # # randomed = huruf_tambahan[:posisi] + kalimat_acak + huruf_tambahan[posisi:]
        # randomed = ''.join(random.sample(campuran,len(campuran)))
        # for i in range(1, len(randomed) + 1):
        #     box = RandomAnswer()
        #     box.label_text = randomed[i-1] 
        #     options_container.add_widget(box)   
    
    

class TemaPage(Screen):
    arg_level = BooleanProperty(False)   

    def set_arg(self,level):
        self.arg_level = level
    
    def gotoGamePage(self,tema):
        self.manager.get_screen('game_page').set_arg(tema,self.arg_level)
        self.manager.current = 'game_page'


class AnswerBox(Button):
    label_text = StringProperty('')


class RandomAnswer(Button):
    label_text = StringProperty('');

class OptionLabel(Label):
    pass

if __name__ == '__main__':
    MyApp().run()