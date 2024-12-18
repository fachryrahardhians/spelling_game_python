from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.label import Label
from kivy.lang.builder import Builder

# builder halaman
Builder.load_file('homepage.kv')
Builder.load_file('levelpage.kv')
Builder.load_file('gamepage.kv')


#main app runner 
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.transition = FadeTransition()
        sm.add_widget(HomePage())
        sm.add_widget(LevelPage())
        sm.add_widget(GamePage())
        return sm

class HomePage(Screen):
    pass

class LevelPage(Screen):
    pass

class GamePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
        self.num_boxes = 5
        self.create_boxes()

    def create_boxes(self):
        answer_container = self.ids.answer_container
        answer_container.clear_widgets()

        for i in range(1, self.num_boxes + 1):
            box = AnswerBox()
            box.text = str(i)
            answer_container.add_widget(box)

    def create_options(self):
        options_container = self.ids.option_container
        options_container.clear_widgets()
        ans = 'MOBIL'
        for i in range(1, ans.length + 1):
            box = OptionLabel()
            box.text = ans[i]
            options_container.add_widget(box)        

class AnswerBox(BoxLayout):
    pass   

class OptionLabel(Label):
    pass

if __name__ == '__main__':
    MyApp().run()