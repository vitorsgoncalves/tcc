# -*- coding: UTF-8 -*-

from kivy.config import Config

#para funcionar em sistemas windows com placas de video integradas
#workaround para o bug 3576 do kivy.Remover quando o bug for solucionado
Config.set('graphics', 'multisamples', '0')

#para desabilitar a simulação de multitouch ao clicar com o botão direito
Config.set('input', 'mouse', 'mouse,disable_multitouch')

#desabilitar sair do programa ao pressionar esc
Config.set('kivy', 'exit_on_escape', '0')

#otimizar para desktop
Config.set('kivy', 'desktop', '1')

#importações dos componentes do kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.utils import platform

#importações dos componentes pneumáticos
from componentes import SimplesAcao
from componentes import DuplaAcao
from componentes import SimplesAcaoInvertida
from componentes import RedutorVazao
from componentes import ReguladorDePressao
from componentes import Valvula
from componentes import Fonte
from componentes import Escape
from componentes import ValvulaOu
from componentes import ValvulaE
from componentes import UnidadeCondicionadora
from componentes import Manometro
from componentes import muda_estado
from componentes import is_simulando

class Painel(GridLayout):

    componentes = [
        {'imagem': 'images/cilindro_simples.png', 'comando': SimplesAcao, 'args':None},
        {'imagem': 'images/cilindro_simples_inv.png',
            'comando': SimplesAcaoInvertida, 'args':None},
        {'imagem': 'images/cilindro_dupla.png', 'comando': DuplaAcao, 'args':None},
        {'imagem': 'images/x10640.png', 'comando': RedutorVazao, 'args':None},
        {'imagem': 'images/val.png', 'comando': Valvula, 'args':2},
        {'imagem': 'images/val3.png', 'comando': Valvula, 'args':3},
        {'imagem': 'images/val4.png', 'comando': Valvula, 'args':4},
        {'imagem': 'images/val5.png', 'comando': Valvula, 'args':5},
        {'imagem': 'images/tri.png', 'comando': Fonte, 'args':None},
        {'imagem': 'images/tri2.png', 'comando': Escape, 'args':None},
        {'imagem': 'images/valOU.png', 'comando': ValvulaOu, 'args':None},
        {'imagem': 'images/valEcomp.png', 'comando': ValvulaE, 'args':None},
        {'imagem': 'images/flr.png', 'comando': UnidadeCondicionadora, 'args':None},
        {'imagem': 'images/manometro.png', 'comando': Manometro, 'args':None},
        {'imagem': 'images/X10500.png', 'comando': ReguladorDePressao, 'args':None}
    ]

    def __init__(self, **kwargs):
        super(Painel, self).__init__(**kwargs)

        def adiciona_componente(instance):

            if not is_simulando():
                if instance.args is not None:
                    novo_componente = instance.comando(instance.args)
                else:
                    novo_componente = instance.comando()

                if platform is 'android':
                    novo_componente.center = instance.last_touch.pos
                else:
                    novo_componente.center = Window.mouse_pos
                instance.parent.area.add_widget(novo_componente)
                

        for componente in self.componentes:
            self.add_widget(
                Botao(
                    comando=componente['comando'],
                    args=componente['args'],
                    source=componente['imagem'],
                    on_press=adiciona_componente))


class Botao(ButtonBehavior, Image):

    click = None

    def __init__(self, comando, args, **kwargs):
        super(Botao, self).__init__(**kwargs)
        self.size_hint = (1, None)
        self.size = self.texture_size
        self.comando = comando
        self.args = args


class Gui(BoxLayout):

    def toogle(self):
        muda_estado()

    texto = "Este simulador foi desenvolvido para o meu trabalho"\
            "de conclusão de curso "\
            "em Engenharia de Controle e Automação e está "\
            "disponível sob licença GPL 3 em: \n"
    link = "[b]github.com/vitorsgoncalves/tcc[/b]"

    content = BoxLayout(orientation='vertical')
    content.add_widget(Label(text=texto, markup=True, text_size=(320,100), halign='justify', valign='middle'))
    content.add_widget(Label(text=link, markup=True, text_size=(320,100), halign='center', valign='middle'))

    popup = Popup(title="Copyright© 2017 Vitor da Silva Gonçalves",
                  content=content,
                  size_hint=(None, None),
                  size=(350, 200),
                  auto_dismiss=True
                  )


class SimuladorApp(App):

    def build(self):
        Window.maximize()
        return Gui()

    #para desabilitar o menu ao apertar f1
    def open_settings(*args):
        pass


if __name__ == '__main__':
    SimuladorApp().run()

