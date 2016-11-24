# -*- coding: UTF-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')


from componentes import *


class Painel(GridLayout):

    componentes = [
        {'imagem': 'images/cilindro_simples.png', 'comando': 'SimplesAcao()'},
        {'imagem': 'images/cilindro_simples_inv.png',
            'comando': 'SimplesAcaoInvertida()'},
        {'imagem': 'images/cilindro_dupla.png', 'comando': 'DuplaAcao()'},
        {'imagem': 'images/x10640.png', 'comando': 'RedutorVazao()'},
        {'imagem': 'images/val.png', 'comando': 'Valvula(2)'},
        {'imagem': 'images/val3.png', 'comando': 'Valvula(3)'},
        {'imagem': 'images/val4.png', 'comando': 'Valvula(4)'},
        {'imagem': 'images/val5.png', 'comando': 'Valvula(5)'},
        {'imagem': 'images/tri.png', 'comando': 'Fonte()'},
        {'imagem': 'images/tri2.png', 'comando': 'Escape()'},
        {'imagem': 'images/valOUpeq.png', 'comando': 'ValvulaOu()'},
        {'imagem': 'images/valEcomp.png', 'comando': 'ValvulaE()'},
        {'imagem': 'images/flr.png', 'comando': 'UnidadeDeCondicionamento()'},
        {'imagem': 'images/manometro.png', 'comando': 'Manometro()'}
    ]

    def __init__(self, **kwargs):
        super(Painel, self).__init__(**kwargs)

        def func(instance):
            if not instance.parent.area.simulando:
                exec('instance.parent.area.add_widget(' + instance.comando + ')')

        for componente in self.componentes:
            self.add_widget(
                Botao(
                    comando=componente['comando'],
                    source=componente['imagem'],
                    on_press=func))


class Botao(ButtonBehavior, Image):

    def __init__(self, comando, **kwargs):
        super(Botao, self).__init__(**kwargs)
        self.size_hint = (1, None)
        self.size = self.texture_size
        self.comando = comando


class Gui(BoxLayout):

    def toogle(self):
        muda_estado()
        #global simulando
        #simulando = not simulando
        #componentes.simulando = not componentes.simulando

    texto = "Este simulador foi desenvolvido para o meu trabalho de conclusão de curso "\
            "e está disponível sob licença GPL 3 em: \n"
    link = "[b]github.com/vitorsgoncalves/tcc[/b]"

    content = BoxLayout(orientation='vertical')
    content.add_widget(Label(text=texto, markup=True, text_size=(320,100), halign='justify', valign='middle'))
    content.add_widget(Label(text=link, markup=True, text_size=(320,100), halign='center', valign='middle'))

    popup = Popup(title="Copyright (C) 2016 Vitor da Silva Gonçalves",
                  content=content,
                  size_hint=(None, None),
                  size=(350, 160),
                  auto_dismiss=True
                  )


class SimuladorApp(App):

    def build(self):
        Window.maximize()
        return Gui()

if __name__ == '__main__':
    SimuladorApp().run()

