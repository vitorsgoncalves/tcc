# -*- coding: UTF-8 -*-

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics import Line
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.properties import BooleanProperty
from kivy.clock import Clock
from kivy.uix.bubble import Bubble
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.label import Label


# variaveis globais
movendo = None
simulando = False

def muda_estado():
    global simulando
    simulando = not simulando


class Linha(Widget):
    """Classe responsável por criar a linha de ar
    """

    pressao = 0
    vazao = 0

    propaga = BooleanProperty(False)

    orientacao1 = 'vertical'
    orientacao2 = 'vertical'

    moving_points = [None, None, None, None]

    def __init__(self, p1, p2, **kwargs):
        super(Linha, self).__init__(**kwargs)

        self.p1 = p1.pos
        self.p2 = p2.pos

        self.connected_lines = []

        with self.canvas:
            Color(0, 0, 0)

            self.linha = Line()


    def apaga_linha(self):

        for linha_conectada in self.connected_lines:
            linha_conectada.disconnect(self)
        self.connected_lines = []

        for componente in self.parent.children:
            if isinstance(componente, Componente):
                for conector in componente.children:
                    if isinstance(conector, Conector):
                        if conector.linha == self:
                            conector.linha = None
                            conector.tamanho = (5, 5)
                            conector.quadrado.size = (5, 5)

        self.parent.remove_widget(self)


    def atualiza_linha(self):
        """redesenha a linha para a nova posição"""

        if not simulando:
            if self.orientacao1 == 'vertical':
                if self.orientacao2 == 'vertical':
                    # vertical-vertical
                    self.linha.points = [self.p1[0], self.p1[1],
                                         self.p1[0], self.p1[1],
                                         self.p1[0], self.p1[1] +
                                         (self.p2[1] - self.p1[1]) / 2,
                                         self.p2[0], self.p1[1] +
                                         (self.p2[1] - self.p1[1]) / 2,
                                         self.p2[0], self.p2[1],
                                         self.p2[0], self.p2[1]]
                else:
                    # vertical-horizontal
                    self.linha.points = [self.p1[0], self.p1[1],
                                         self.p1[0], self.p1[1],
                                         self.p1[0], self.p2[1],
                                         self.p2[0], self.p2[1],
                                         self.p2[0], self.p2[1]]
            else:
                if self.orientacao2 == 'vertical':
                    # horizontal-vertical
                    self.linha.points = [self.p1[0], self.p1[1],
                                         self.p1[0], self.p1[1],
                                         self.p2[0], self.p1[1],
                                         self.p2[0], self.p2[1],
                                         self.p2[0], self.p2[1]]
                else:
                    # horizontal-horizontal
                    self.linha.points = [self.p1[0], self.p1[1],
                                         self.p1[0], self.p1[1],
                                         self.p1[
                                             0] + (self.p2[0] - self.p1[0]) / 2, self.p1[1],
                                         self.p1[
                                             0] + (self.p2[0] - self.p1[0]) / 2, self.p2[1],
                                         self.p2[0], self.p2[1],
                                         self.p2[0], self.p2[1]]

    def connect_to(self, linha):
        """conecta a linha a outra"""
        if linha not in self.connected_lines:
            self.connected_lines.append(linha)

    def disconnect(self, linha):
        """desconecta a linha de outra"""
        if linha in self.connected_lines:
            self.connected_lines.remove(linha)

    def point_over(self, point):
        """verifica se o mouse está sobre a linha e retorna True ou False"""

        for i in range(3, len(self.linha.points)):

            x0 = round(self.linha.points[i - 3])
            y0 = round(self.linha.points[i + -2])
            x1 = round(self.linha.points[i - 1])
            y1 = round(self.linha.points[i])

            tolerance = 5

            px = round(point[0])
            py = round(point[1])

            if x0 == x1:
                if x0 - tolerance <= px <= x0 + tolerance:
                    if y0 < py < y1 or y1 < py < y0:
                        return True
            elif y0 == y1:
                if y0 - tolerance <= py <= y0 + tolerance:
                    if x0 < px < x1 or x1 < px < x0:
                        return True
        return None

    def on_touch_down(self, touch):
        """movimenta a linha ao clicá-la e arrastá-la"""
        if touch.button == 'right':
            if self.point_over(touch.pos):
                self.apaga_linha()
        else:
            global movendo

            for i in range(5, len(self.linha.points) - 2):

                x0 = round(self.linha.points[i - 3])
                y0 = round(self.linha.points[i + -2])
                x1 = round(self.linha.points[i - 1])
                y1 = round(self.linha.points[i])

                tolerance = 5

                px = round(touch.pos[0])
                py = round(touch.pos[1])

                if x0 == x1:
                    if x0 - tolerance <= px <= x0 + tolerance:
                        if y0 < py < y1 or y1 < py < y0:
                            self.moving_points = [i - 3, i - 2, i - 1, i]
                            movendo = self
                elif y0 == y1:
                    if y0 - tolerance <= py <= y0 + tolerance:
                        if x0 < px < x1 or x1 < px < x0:
                            self.moving_points = [i - 3, i - 2, i - 1, i]
                            movendo = self

    def on_touch_move(self, touch):

        if movendo == self:
            if self.linha.points[self.moving_points[0]
                                 ] == self.linha.points[self.moving_points[2]]:
                self.linha.points[self.moving_points[0]] = touch.pos[0]
                self.linha.points[self.moving_points[2]] = touch.pos[0]

            if self.linha.points[self.moving_points[1]
                                 ] == self.linha.points[self.moving_points[3]]:
                self.linha.points[self.moving_points[1]] = touch.pos[1]
                self.linha.points[self.moving_points[3]] = touch.pos[1]

            # para forcar a atualizacao da linha
            self.linha.points = self.linha.points

    def on_touch_up(self, touch):
        global movendo
        if movendo == self:
            movendo = None

    # def on_pressao(self, instance, value):
    def on_propaga(self, instance, value):
        """tranfere seus dados às linhas seguintes"""
        if self.propaga:
            for linha in self.connected_lines:
                linha.pressao = self.pressao
                linha.vazao = self.vazao
                linha.propaga = True
            self.propaga = False


class Conector(ButtonBehavior, Widget):
    """conectores utilizados para conectar componentes a linhas de ar

    são representados graficamente por pequenos quadrados que permitem
    criar uma nova linha ao clicá-lo e arrastá-lo.
    """
    
    linha = None

    def __init__(self, tipo, pos_relativa, orientacao, **kwargs):
        super(Conector, self).__init__(**kwargs)

        self.orientacao = orientacao

        self.pressed = False

        self.tipo = tipo
        self.pos_relativa = pos_relativa
        self.center = (
            self.pos[0] +
            pos_relativa[0],
            self.pos[1] +
            pos_relativa[1])
        # para facilitar a conexao, o tamanho do quadrado e menor que o real
        self.size = (10, 10)
        self.tamanho = (5, 5)

        with self.canvas.after:
            Color(0, 0, 0)
            self.quadrado = Rectangle(size=self.tamanho, pos=self.pos)

        def update_rect(instance, value):
            instance.quadrado.pos = instance.pos
            instance.quadrado.size = instance.tamanho

            if self.linha is not None:
                self.linha.atualiza_linha()

        self.bind(pos=update_rect)

    def on_press(self):
        """cria uma linha o clicar sobre"""

        global movendo
        if not simulando:
            self.linha = Linha(self, self)
            self.linha.orientacao1 = self.orientacao
            self.parent.parent.add_widget(self.linha)
            movendo = self

        self.pressed = True

    def on_touch_move(self, touch):
        """atualiza a posição da linha ao arrastar o mouse"""
        if self.pressed:
            self.linha.p2 = touch.pos
            self.linha.atualiza_linha()

    def on_release(self):
        """conecta a linha ao conector sob o cursor do mouse e para a
        sua a atualização, liberando o mouse para interagir com outros
        componentes. Caso não haja um conector sob o cursor, apaga a linha

        """
        global movendo
        movendo = None

        self.pressed = False

        # verifica se essta sobre outro conector
        sobrecon = False
        for componente in self.parent.parent.children:
            if isinstance(componente, Componente):
                for objeto in componente.children:
                    if isinstance(objeto, Conector):
                        if objeto.collide_point(*self.last_touch.pos):
                            sobrecon = True
                            objeto.linha = self.linha
                            self.linha.p2 = objeto.pos

                            self.linha.orientacao2 = objeto.orientacao
                            self.linha.atualiza_linha()

                            # apaga os quadrados dos conectores
                            self.tamanho = (0, 0)
                            self.quadrado.size = self.tamanho
                            objeto.tamanho = (0, 0)
                            objeto.quadrado.size = self.tamanho

            elif isinstance(componente, Linha):
                if componente.point_over(self.last_touch.pos):
                    sobrecon = True

                    self.linha.p2 = self.last_touch.pos

                    componente.connect_to(self.linha)
                    self.linha.connect_to(componente)

        if not sobrecon:
            if 'clock' in dir(self.linha):
                self.linha.clock.cancel()
            self.parent.parent.remove_widget(self.linha)
            self.linha = None

    def on_linha(self, instance, value):
        """remove sua referência à linha caso esta tenha sido apagada"""

        if self.linha not in self.parent.parent.children:
            self.linha = None


class Componente(Image):
    """classe que representa os comportamentos comuns a todos os componentes"""

    conectores = []

    def ciclo(self, dt): pass

    def apaga_componente(self):
        """remove o componente"""
        
        for conector in self.conectores:
            if conector.linha is not None:
                conector.linha.apaga_linha()

        self.clock.cancel()
        self.parent.remove_widget(self)

    def __init__(self, **kwargs):
        super(Componente, self).__init__(**kwargs)

        # define posição inicial
        self.size = self.texture_size

        # adiciona os conectores
        for conector in self.conectores:
            self.add_widget(conector)

        # atualiza a posicao dos conectores ao mover o componente
        def update_rect(instance, value):

            for conector in self.conectores:
                conector.center = (self.pos[0] + conector.pos_relativa[0],
                                   self.pos[1] + conector.pos_relativa[1])

        self.bind(pos=update_rect, size=update_rect)

        self.clock = Clock.schedule_interval(self.ciclo, 0.05)

    def on_touch_move(self, touch):
        """move o componente ao clicar a arrastar o mouse sobre ele"""

        global movendo
        if not simulando:
            if movendo is None:
                if self.collide_point(*touch.pos):
                    movendo = self

            if movendo == self:
                self.center = touch.pos

            super(Image, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        """libera o mouse para interagir com outros elementos e apaga
        o componente caso este estaja fora da área de desenho
        """

        global movendo
        movendo = None

        if not self.collide_widget(self.parent):
            self.apaga_componente()
        super(Image, self).on_touch_up(touch)


class Cilindro(Componente):
    """classe que representa os comportamentos comuns a todos os cilindros

    desenha e atualiza o a posição do pistaoão assim como também verifica
    se colidiu com um rolete
    """

    source = 'images/g178.png'

    posicao = 0
    #equacao = None
    direcao = None

    def equacao(self, p1, p2): pass

    def ciclo(self, dt):
        """lê as entradas de pressão e atualiza a posição do pistaoão. Em seguida
        verifica se acionou um rolete
        """
        if simulando:
            pressao = []
            vazao = []
            for conector in self.conectores:
                if conector.linha is not None:
                    pressao.append(conector.linha.pressao)
                    vazao.append(conector.linha.vazao)
            delta = self.equacao(pressao,vazao)
            self.posicao += delta

            if delta > 0:
                self.direcao = 'avanco'
            elif delta < 0:
                self.direcao = 'retorno'
            else:
                self.direcao = None

            # saturacao (dependendo do modelo matemático pode ser inutilizado)
            if self.posicao > 70:
                self.posicao = 70
            elif self.posicao < 0:
                self.posicao = 0

            # posiciona o pistao
            self.pistao.center = (
                self.center[0] + self.posicao,
                self.center[1])
            self.ponta.center = (self.pistao.center[0] + self.pistao.size[0] / 2 + 5,
                                 self.pistao.center[1])

            # verifica se acionou um rolete
            self.verifica_colisao()

    def __init__(self, **kwargs):
        super(Cilindro, self).__init__(**kwargs)

        # cria o pistao
        self.pistao = Image(source='images/g188.png', pos=self.pos)
        self.pistao.center = (self.center[0] + self.posicao, self.center[1])
        self.add_widget(self.pistao)

        # cria a ponta do pistaoao para usar nas colisoes com roletes
        self.ponta = Widget(size=(30, 30),
                            center=(self.pistao.center[0] + self.pistao.size[0] / 2,
                                    self.pistao.center[1])
                            )

        self.add_widget(self.ponta)

        def update_rect(instance, value):
            self.pistao.center = (
                self.center[0] + self.posicao,
                self.center[1])
            self.ponta.center = (
                self.pistao.center[0] +
                self.pistao.size[0] /
                2,
                self.pistao.center[1])

        
        self.bind(pos=update_rect, size=update_rect)


    # para verificar se o pistaoao bateu em um rolete
    # suspeito que está usando calculos desnecessarios
    def verifica_colisao(self):
        """verifica se a ponta do pistao colidiu com um objeto do tipo rolete"""
        if simulando:
            for componente in self.parent.children:  # percorre os children da area de desenho
                if isinstance(componente, Valvula):
                    for objeto in componente.children:
                        if isinstance(objeto, Acionador):
                            if objeto.tipo == 'rolete':
                                if self.ponta.collide_widget(objeto.marca):
                                    objeto.intensidade = 3
                                else:
                                    objeto.intensidade = 0
                            elif objeto.tipo == 'gatilho':
                                if self.ponta.collide_widget(objeto.marca):
                                    if (self.direcao == 'avanco' and
                                            objeto.marca.direcao == 'direita'):
                                        # direção do cilindro aciona o gatilho
                                        objeto.intensidade = 3

                                    elif (self.direcao == 'retorno' and
                                          objeto.marca.direcao == 'esquerda'):
                                        # direção do cilindro aciona o gatilho
                                        objeto.intensidade = 3

                                    else:
                                        objeto.intensidade = 0


class SimplesAcaoInvertida(Cilindro):
    """cilindro de ação simples e retorno por mola, atua no retirno"""

    def atualiza_mola(self):
        """atualiza a posição da mola"""
        for i in range(4):
            self.mola_frente[i].points = (self.pos[0] + (self.pistao.pos[0] - self.pos[0]) / 4 * i, self.pos[1],
                                          self.pos[
                                              0] + (self.pistao.pos[0] - self.pos[0]) / 4 * (i + 1),
                                          self.pos[1] + self.texture.height)
        for i in range(3):
            self.mola_tras[i].points = (self.pos[0] + (self.pistao.pos[0] - self.pos[0]) / 4 * (i + 1),
                                        self.pos[1],
                                        self.pos[
                                            0] + (self.pistao.pos[0] - self.pos[0]) / 4 * (i + 1),
                                        self.pos[1] + self.texture.height)

    def __init__(self, **kwargs):
        self.conectores = [
            Conector(
                'entrada', (90, -2), 'vertical', center=self.pos)]
        super(SimplesAcaoInvertida, self).__init__(**kwargs)

        self.pistao.pos[0] += 70
        self.posicao = 70

        # desenha a mola
        self.mola_frente = [None] * 4
        self.mola_tras = [None] * 3
        with self.canvas:
            Color(0, 0, 0)
            for i in range(4):
                self.mola_frente[i] = Line(points=(self.pos[0] + (self.pistao.pos[0] - self.pos[0]) / 4 * i,
                                                   self.pos[1],
                                                   self.pos[
                                                       0] + (self.pistao.pos[0] - self.pos[0]) / 4 * (i + 1),
                                                   self.pos[1] + self.texture.height))
        with self.canvas.after:
            Color(0, 0, 0)
            for i in range(3):
                self.mola_tras[i] = Line(points=(self.pos[0] + (self.pistao.pos[0] - self.pos[0]) / 4 * (i + 1),
                                                 self.pos[1],
                                                 self.pos[
                                                     0] + (self.pistao.pos[0] - self.pos[0]) / 4 * (i + 1),
                                                 self.pos[1] + self.texture.height))

        def update_rect(instance, value):
            self.atualiza_mola()

        self.bind(pos=update_rect, size=update_rect)

    def equacao(self, pressao, vazao):
        """equação característica do cilindro"""
        variacao = 0
        if len(pressao) > 0:
            if pressao[0] > 0:
                variacao = -pressao[0] * vazao[0]
            else:
                variacao = 10  # forca da mola
        self.atualiza_mola()
        return variacao


class SimplesAcao(Cilindro):
    """cilindro de ação simples e retorno por mola, atua no avanço"""

    def atualiza_mola(self):
        """atualiza a posição da mola"""
        espaco = self.width - (self.pistao.pos[0] - self.pos[0])

        for i in range(4):
            self.mola_frente[i].points = (self.pistao.pos[0] + 10 + espaco / 4 * i,
                                          self.pos[1],
                                          self.pistao.pos[0] +
                                          espaco / 4 * (i + 1),
                                          self.pos[1] + self.texture.height)
        for i in range(3):
            self.mola_tras[i].points = (self.pistao.pos[0] + 10 + espaco / 4 * (i + 1),
                                        self.pos[1],
                                        self.pistao.pos[0] +
                                        espaco / 4 * (i + 1),
                                        self.pos[1] + self.texture.height)

    def __init__(self, **kwargs):

        self.conectores = [
            Conector(
                'entrada', (10, -2), 'vertical', center=self.pos)]

        super(SimplesAcao, self).__init__(**kwargs)

        # desenha a mola
        self.mola_frente = [None] * 4
        self.mola_tras = [None] * 3

        with self.canvas:
            Color(0, 0, 0)
            for i in range(4):
                self.mola_frente[i] = Line(points=(self.pos[0] + (10 + self.texture.width / 4 * i),
                                                   self.pos[1],
                                                   self.pos[
                                                       0] + self.texture.width / 4 * (i + 1),
                                                   self.pos[1] + self.texture.height))
        with self.canvas.after:
            Color(0, 0, 0)
            for i in range(3):
                self.mola_tras[i] = Line(points=(self.pos[0] + 10 + self.texture.width / 4 * (i + 1),
                                                 self.pos[1],
                                                 self.pos[
                                                     0] + self.texture.width / 4 * (i + 1),
                                                 self.pos[1] + self.texture.height))

        def update_rect(instance, value):
            self.atualiza_mola()

        self.bind(pos=update_rect, size=update_rect)

    def equacao(self, pressao, vazao):
        """equação característica do cilindro"""
        variacao = 0
        if len(pressao) > 0:
            if pressao[0] > 0:
                variacao = pressao[0] * vazao[0]
            else:
                variacao = -10  # forca da mola
        self.atualiza_mola()
        return variacao


class DuplaAcao(Cilindro):
    """cilindro de ação dupla"""

    def __init__(self, **kwargs):

        self.conectores = [Conector('entrada', (10, -2), 'vertical', center=self.pos),
                           Conector('entrada', (90, -2), 'vertical', center=self.pos)]

        super(DuplaAcao, self).__init__(**kwargs)

    def equacao(self, pressao, vazao):
        """equação característica do cilindro"""
        variacao = 0
        if len(pressao) > 0:
            variacao = (self.conectores[0].linha.pressao * self.conectores[0].linha.vazao) - (self.conectores[1].linha.pressao * self.conectores[1].linha.vazao)
        return variacao


class Acionador(Image):
    """elemento que aciona a válvula direcional"""

    def remove_bubble(self):
        """remove o menu flutuante"""
        if not simulando:
            if self.menu in self.children:
                self.remove_widget(self.menu)
                
    def pressuriza(self, dt):
        """realiza o acionamento por pilotagem"""
        if simulando:
            if self.conector.linha is not None:
                if self.conector.linha.pressao > 0:
                    self.intensidade = 2
                else:
                    self.intensidade = 0

    def troca_bot(self, instance):
        """substitui o tipo de acionamento"""

        if self.posicao == 'esq':
            self.source = self.botoes[instance.via]['imagem']
        else:
            self.source = self.botoes[instance.via]['dir']
        self.tipo = self.botoes[instance.via]['tipo']

        # remove marca de curso, se houver
        if 'marca' in dir(self):
            self.remove_widget(self.marca)

        # remove conector, se houver
        if self.conector is not None:
            self.parent.remove_widget(self.conector)
            self.conector = None
            if 'clock' in dir(self):
                self.clock.cancel()

        if self.tipo == 'mola':
            self.intensidade = 1
        elif self.tipo == 'rolete':
            self.intensidade = 0
        else:
            self.intensidade = 1

        if self.tipo == 'piloto':

            self.conector = Conector('entrada', (0, 5), 'horizontal')
            if self.posicao == 'esq':
                self.conector.pos = (
                    self.pos[0], self.pos[1] + self.height / 2)
            else:
                self.conector.pos = (
                    self.pos[0] + self.width,
                    self.pos[1] + self.height / 2)

            self.parent.add_widget(self.conector)

            self.clock = Clock.schedule_interval(self.pressuriza, 0.05)

        elif self.tipo == 'rolete':

            if self.posicao == 'dir':
                self.marca = CursoRolete(
                    pos=(
                        self.pos[0] +
                        self.width +
                        10,
                        self.center[1]))
            else:
                self.marca = CursoRolete(
                    pos=(self.pos[0] - 10, self.center[1]))
            self.add_widget(self.marca)

        elif self.tipo == 'gatilho':

            if self.posicao == 'dir':
                self.marca = CursoGatilho(
                    pos=(
                        self.pos[0] +
                        self.width +
                        10,
                        self.center[1]))
            else:
                self.marca = CursoGatilho(
                    pos=(self. pos[0] - 10, self.center[1]))
            self.add_widget(self.marca)

        self.remove_widget(self.menu)

    def __init__(self, posicao, **kwargs):
        super(Acionador, self).__init__(**kwargs)

        self.pressed_right = False
        self.pressed_left = False

        self.conector = None

        self.posicao = posicao

        # cria os tipos padroes
        # tipo pode set botao, rolete ou eletrico
        if posicao == 'esq':
            self.tipo = 'botao'
            self.source = 'images/bot1.png'
            self.intensidade = 1
        else:
            self.tipo = 'mola'
            self.source = 'images/mola.png'
            self.intensidade = 1

        self.size = self.texture_size[0] / 2, self.texture_size[1] / 2

        self.botoes = [
            {'imagem': 'images/bot1.png',
             'dir': 'images/botvirado.png',
             'tipo': 'botao'},
            {'imagem': 'images/bot_retentivo.png',
             'dir': 'images/bot_retentivo_inv.png',
             'tipo': 'botao_retentivo'},
            {'imagem': 'images/rolete.png',
             'dir': 'images/roleteb.png',
             'tipo': 'rolete'},
            {'imagem': 'images/mola.png', 'dir': 'images/mola.png', 'tipo': 'mola'},
            {'imagem': 'images/piloto.png',
             'dir': 'images/piloto.png',
             'tipo': 'piloto'},
            {'imagem': 'images/gatilho.png',
             'dir': 'images/gatilhob.png',
             'tipo': 'gatilho'}
        ]

        # cria o menu bolha para trocar o botao
        self.menu = Bubble(
            size=(88, 40 * len(self.botoes)),
            background_color=(0, 0, 0, 0.2),
            row_default_height=40 * len(self.botoes) + 8,
            col_default_width=90,
            show_arrow = False,
            orientation='vertical')

        # posiciona a imagem do botao
        for botao in self.botoes:
            if self.posicao == 'esq':
                bb = BotaoVia(
                    source=botao['imagem'],
                    via=self.botoes.index(botao),
                    on_press=self.troca_bot)
            else:
                bb = BotaoVia(
                    source=botao['dir'],
                    via=self.botoes.index(botao),
                    on_press=self.troca_bot)
            self.menu.add_widget(bb)

        def update_rect(instance, value):
            if self.tipo == 'piloto':
                if self.posicao == 'esq':
                    self.conector.pos = (
                        self.pos[0], self.pos[1] + self.height / 2)
                else:
                    self.conector.pos = (
                        self.pos[0] + self.width,
                        self.pos[1] + self.height / 2)

        self.bind(pos=update_rect, size=update_rect)


    def on_touch_down(self, touch):
        abre_menu = False
        if 'button' in dir(touch):
            if touch.button == 'right':
                abre_menu = True
        elif touch.is_double_tap:
            abre_menu = True

        if abre_menu:
            if not simulando:
                if self.collide_point(*touch.pos):            
                    if self.menu not in self.children:
                        if self.posicao == 'esq':
                            self.menu.center = (self.center[0] - self.width*2, self.center[1])
                            self.menu.arrow_pos = 'right_mid'
                        else:
                            self.menu.center = (self.center[0] + self.width*2, self.center[1])
                            self.menu.arrow_pos = 'right_mid'
                        self.add_widget(self.menu)  

        else:
            if not self.menu.collide_point(*touch.pos):
                self.remove_bubble()

            if self.collide_point(*touch.pos):
                if self.tipo == 'botao':
                    #self.parent.acionado = 1
                    self.intensidade = 2
                elif self.tipo == 'botao_retentivo':
                    if self.intensidade > 0:
                        self.intensidade = 0
                    else:
                        self.intensidade = 2                

        super(Image, self).on_touch_down(touch)


    def on_touch_up(self,touch):
        """desaciona em caso de botoeira"""
        if simulando:
            if self.tipo == 'botao':
                self.intensidade = 0


class ValvulaLogica(Componente):
    """válvulas lógicas"""

    def __init__(self, **kwargs):

        self.conectores = [
            Conector('entrada', (0, 20), 'horizontal', center=self.pos),
            Conector('entrada', (80, 20), 'horizontal', center=self.pos),
            Conector('saida', (40, 40), 'vertical', center=self.pos)
        ]

        super(ValvulaLogica, self).__init__(**kwargs)
        # posicao padrao da bolinha, varia de 0 a 1
        self.pos_obturador = 0

        self.obturador.size = self.obturador.texture_size  # nao sei se ha necessidade
        self.obturador.center = (
            self.pos[0] +
            self.width /
            2 +
            self.width /
            2 *
            self.pos_obturador,
            self.obturador.height /
            2 +
            self.pos[1] +
            self.height /
            2 -
            self.obturador.height /
            2)
        self.add_widget(self.obturador)

        def update_rect(instance, value):
            """atualiza graficamente a posição do centro"""
            self.obturador.center = (
                self.pos[0] +
                self.width /
                2 +
                self.width /
                2 *
                self.pos_obturador -
                self.obturador.width /
                2 *
                self.pos_obturador,
                self.obturador.height /
                2 +
                self.pos[1] +
                self.height /
                2 -
                self.obturador.height /
                2)

        self.bind(pos=update_rect, size=update_rect)

    def ciclo(self, dt):
        """executa a lógica da válvula"""
        if simulando:
            p1 = p2 = p3 = 0
            if self.conectores[0].linha is not None:
                p1 = self.conectores[0].linha.pressao
            if self.conectores[1].linha is not None:
                p2 = self.conectores[1].linha.pressao
            if self.conectores[1].linha is not None:
                self.equacao(p1, p2)

                self.obturador.center = (
                    self.pos[0] +
                    self.width /
                    2 +
                    self.width /
                    2 *
                    self.pos_obturador -
                    self.obturador.width /
                    2 *
                    self.pos_obturador,
                    self.obturador.height /
                    2 +
                    self.pos[1] +
                    self.height /
                    2 -
                    self.obturador.height /
                    2)


class ValvulaE(ValvulaLogica):
    """válvula lógica do tipo e"""

    def __init__(self, **kwargs):

        self.source = 'images/valE.png'
        self.obturador = Image(source='images/bolinhavalE.png')

        super(ValvulaE, self).__init__(**kwargs)

    def equacao(self, p1, p2):
        """define o comportamento lógico da válvula"""

        if p1 == p2:

            self.pos_obturador = 0
            self.conectores[0].linha.connect_to(self.conectores[2].linha)
            self.conectores[2].linha.connect_to(self.conectores[0].linha)
        else:
            self.conectores[0].linha.disconnect(self.conectores[2].linha)
            self.conectores[2].linha.disconnect(self.conectores[0].linha)
            self.conectores[1].linha.disconnect(self.conectores[2].linha)
            self.conectores[2].linha.disconnect(self.conectores[1].linha)
            if p1 > p2:
                self.pos_obturador = 1
            else:
                self.pos_obturador = -1


class ValvulaOu(ValvulaLogica):
    """válvula lógica do tipo ou"""

    def __init__(self, **kwargs):

        self.source = 'images/valOUpeq.png'
        self.obturador = Image(source='images/bolinhavalOU.png')

        super(ValvulaOu, self).__init__(**kwargs)

    def equacao(self, p1, p2):
        """define o comportamento lógico da válvula"""

        if p1 >= p2 > 0:
            self.pos_obturador = 1
            self.conectores[1].linha.disconnect(self.conectores[2].linha)
            self.conectores[2].linha.disconnect(self.conectores[1].linha)
            self.conectores[0].linha.connect_to(self.conectores[2].linha)
            self.conectores[2].linha.connect_to(self.conectores[0].linha)
        elif p2 > p1:
            self.pos_obturador = -1
            self.conectores[0].linha.disconnect(self.conectores[2].linha)
            self.conectores[2].linha.disconnect(self.conectores[0].linha)
            self.conectores[1].linha.connect_to(self.conectores[2].linha)
            self.conectores[2].linha.connect_to(self.conectores[1].linha)
        else:
            # quando as 2 entradas forem iguais, pode conectar em qualquer
            # linha
            self.conectores[0].linha.disconnect(self.conectores[2].linha)
            self.conectores[2].linha.disconnect(self.conectores[0].linha)
            self.conectores[1].linha.disconnect(self.conectores[2].linha)
            self.conectores[2].linha.disconnect(self.conectores[1].linha)


class Valvula(ButtonBehavior, Componente):
    """válvula direcional

    a válvula direcional pode variar quando ao número de vias e seu
    respectivo arranjo, posições e forma de acionamento.
    O número de vias é definido através do parâmetro qt_vias
    O arranjo das vias é definido pelos objetos do qt_vias via instanciados
    no vetor vias
    O número de posições da váçvula corresponde ao tamanho do vetor vias
    A forma de acionamento é dada em função do objeto do qt_vias acionador instanciado
    """

    def add_via(self):
        self.posicoes += 1
        self.size = 40 * self.posicoes, 40

        if self.qt_vias == 2:
            nova_via = DuasVias(0)
        elif self.qt_vias == 3:
            nova_via = TresVias(0)

        nova_via.pos = (self.pos[0] +
                        nova_via.texture_size[1] *
                        len(self.vias), self.pos[1])

        self.vias.append(nova_via)
        self.add_widget(nova_via)

        self.acionador_direita.pos = (self.pos[0] + self.size[0], self.pos[1])

    def remove_via(self):

        self.posicoes -= 1
        self.size = 40 * self.posicoes, 40

        self.remove_widget(self.vias[self.posicoes])  # obs - ja subtraiu 1
        self.vias.remove(self.vias[self.posicoes])

        self.acionador_direita.pos = (self.pos[0] + self.size[0], self.pos[1])

    def ciclo(self, dt):
        if simulando:
            if self.conectores[1].linha is not None:
                self.vias[
                    self.pos_val].vias[
                    self.vias[
                        self.pos_val].tipo]['logica']()

            direita = self.acionador_esquerda.intensidade
            esquerda = self.acionador_direita.intensidade

            if direita > esquerda:
                varpos = 1
            elif esquerda > direita:
                varpos = -1
            else:
                varpos = 0

            if varpos != self.varpos_ant:
                # houve mudanca na posicao da valvula
                # satura a posicao da valvula aos limites
                if len(self.vias) > self.pos_val - varpos >= 0:
                    # prossegue com a logica da posicao nova
                    self.pos[0] += (self.size[0] / self.posicoes) * varpos
                    self.pos_val -= varpos  # clarificar esses sinais
                self.varpos_ant = varpos

    def __init__(self, qt_vias, **kwargs):

        self.qt_vias = qt_vias
        self.posicoes = 2

        # os conectores não estão aparecendo na posição inicial
        if qt_vias == 2:
            self.conectores = [
                Conector('entrada', (60, 0), 'vertical', center=self.pos),
                Conector('saida', (60, 44), 'vertical', center=self.pos)
            ]
        if qt_vias >= 3:
            self.conectores = [
                Conector('entrada', (50, 0), 'vertical', center=self.pos),
                Conector('saida', (50, 44), 'vertical', center=self.pos),
                Conector('entrada', (75, 0), 'vertical', center=self.pos)
            ]
        if qt_vias >= 4:
            self.conectores.append(
                Conector(
                    'entrada', (75, 44), 'vertical', center=self.pos))
        if qt_vias == 5:
            self.conectores.append(
                Conector(
                    'entrada', (63, 0), 'vertical', center=self.pos))

        super(Valvula, self).__init__(**kwargs)
        self.size = 40 * self.posicoes, 40


        # adicionando botao esquerdo
        self.acionador_esquerda = Acionador('esq')
        self.acionador_esquerda.pos = (
            self.pos[0] -
            self.acionador_esquerda.size[0],
            self.pos[1])
        self.add_widget(self.acionador_esquerda)

        # adiciona bot direito
        self.acionador_direita = Acionador('dir')
        self.acionador_direita.pos = (self.pos[0] + self.size[0], self.pos[1])
        self.add_widget(self.acionador_direita)

        # posicao padrao
        self.pos_val = 1

        self.varpos_ant = 0

        if self.qt_vias == 2:
            self.vias = [DuasVias(0), DuasVias(1)]
        elif self.qt_vias == 3:
            self.vias = [TresVias(0), TresVias(1)]
        elif self.qt_vias == 4:
            self.vias = [QuatroVias(0), QuatroVias(1)]
        elif self.qt_vias == 5:
            self.vias = [CincoVias(1), CincoVias(2)]

        for via in self.vias:
            via.pos = (
                self.pos[0] +
                via.texture_size[1] *
                self.vias.index(via),
                self.pos[1])
            self.add_widget(via)

        def update_rect(instance, value):

            for via in self.vias:
                via.pos = (
                    self.pos[0] +
                    via.texture_size[1] *
                    self.vias.index(via),
                    self.pos[1])

            self.acionador_esquerda.pos = (
                self.pos[0] - self.acionador_esquerda.size[0], self.pos[1])
            self.acionador_direita.pos = (
                self.pos[0] + self.size[0], self.pos[1])

        self.bind(pos=update_rect, size=update_rect)


class BotaoVia(ButtonBehavior, Image):

    def __init__(self, via, **kwargs):
        super(BotaoVia, self).__init__(**kwargs)
        self.via = via


class Vias(Image):

    def remove_bubble(self):
        if not simulando:
            if self.menu in self.children:
                self.remove_widget(self.menu)

    def press_via(self, instance):
        self.tipo = instance.via
        self.source = self.vias[self.tipo]['imagem']
        self.remove_bubble()

    def press_add(self, instance):
        self.parent.add_via()
        self.remove_bubble()

    def press_remove(self, instance):
        # precisa remover o bubblemenu primeiro senao nao havera parent na hora
        # de executar
        self.remove_bubble()
        self.parent.remove_via()

    def desconecta_tudo(self):

        # desconecta todas as linhas
        for conector in self.parent.conectores:
            for conector2 in self.parent.conectores:
                conector.linha.disconnect(conector2.linha)
                conector2.linha.vazao = 0

    def __init__(self, tipo, vias, **kwargs):
        super(Vias, self).__init__(**kwargs)

        self.tipo = tipo
        self.vias = vias

        self.source = self.vias[tipo]['imagem']

        # cria o menu de vias flutuante
        self.menu = Bubble(
            background_color=(0, 0, 0, 0.4),
            size=(40 * (len(self.vias) + 2) + 8, 48),
            orientation='horizontal',
            arrow_pos='bottom_mid',
        )
        for via in self.vias:
            bb = BotaoVia(
                source=via['imagem'],
                on_press=self.press_via,
                via=self.vias.index(via))
            self.menu.add_widget(bb)

        # adiciona botao de incluir posicao
        bot_add = Button(text='+', size=(40, 40), on_press=self.press_add)
        self.menu.add_widget(bot_add)

        # adiciona botao de remover posicao
        bot_remove = Button(text='-', size=(40, 40),
                            on_press=self.press_remove)
        self.menu.add_widget(bot_remove)

        # não ha necessidade de atualizar o tamanho pois todas as vias sao do
        # mesmo tamanho
        self.size = self.texture_size

    # exibe ou remove o menu flutuante
    def on_touch_down(self, touch):
        abre_menu = False
        if 'button' in dir(touch):
            if touch.button == 'right':
                abre_menu = True
        elif touch.is_double_tap:
            abre_menu = True

        if abre_menu:
            if not simulando:
                if self.collide_point(*touch.pos):
                    if self.menu not in self.children:
                        self.menu.center = (
                            self.center[0], self.center[1] + self.height + 6)
                        self.add_widget(self.menu)

        else:
            if not self.menu.collide_point(*touch.pos):
                self.remove_bubble()
            
        super(Image, self).on_touch_down(touch)


class DuasVias(Vias):

    def __init__(self, tipo, **kwargs):

        def passa():
            self.desconecta_tudo()
            self.parent.conectores[1].linha.connect_to(
                self.parent.conectores[0].linha)
            self.parent.conectores[0].linha.connect_to(
                self.parent.conectores[1].linha)

        def bloqueia():
            self.desconecta_tudo()

        self.tipo = tipo
        self.vias = [
            {'imagem': 'images/2vias_b.png', 'logica': passa},
            {'imagem': 'images/2vias_a.png', 'logica': bloqueia}
        ]

        super(DuasVias, self).__init__(self.tipo, self.vias, **kwargs)


class TresVias(Vias):

    def __init__(self, tipo, **kwargs):

        def a():
            """
             .
            / \ ___
             |   |
            """

            self.desconecta_tudo()
            self.parent.conectores[1].linha.connect_to(
                self.parent.conectores[0].linha)
            self.parent.conectores[0].linha.connect_to(
                self.parent.conectores[1].linha)

        def b():
            """
               \
            ___ \
             |  __|
            """
            self.desconecta_tudo()

            self.parent.conectores[1].linha.connect_to(
                self.parent.conectores[2].linha)
            self.parent.conectores[2].linha.connect_to(
                self.parent.conectores[1].linha)

        def c():
            """
             |
             |___
             |   |
            """
            # nao precisa desconectar linhas pois ligara todas

            for conector in self.parent.conectores:
                for conector2 in self.parent.conectores:
                    if conector.linha != conector2.linha:  # para nao conectar a si mesmo
                        conector.linha.connect_to(conector2.linha)

        def d():
            """
             |
            ‾‾‾
            ___  ___
             |    |
            """
            self.desconecta_tudo()

        def e():
            """
             |
            ‾‾‾
             _____
             |   |
            """
            self.desconecta_tudo()

            self.parent.conectores[2].linha.connect_to(
                self.parent.conectores[0].linha)
            self.parent.conectores[0].linha.connect_to(
                self.parent.conectores[2].linha)

        self.tipo = tipo
        self.vias = [
            {'imagem': 'images/3vias_a.png', 'logica': a},
            {'imagem': 'images/3vias_b.png', 'logica': b},
            {'imagem': 'images/3vias_c.png', 'logica': c},
            {'imagem': 'images/3vias_d.png', 'logica': d},
            {'imagem': 'images/3vias_e.png', 'logica': e},
        ]

        super(TresVias, self).__init__(self.tipo, self.vias, **kwargs)


class QuatroVias(Vias):

    def __init__(self, tipo, **kwargs):

        def a():
            """
             |   |
            ‾‾‾ ‾‾‾
            ___ ___
             |   |
            """
            self.desconecta_tudo()

        def b():
            """
             |  |
            ‾‾‾ |
              __|
             |  |
            """
            # remove todas as conexoes da linha 1 e conecta as outras entre si
            for conector in self.parent.conectores:
                conector.linha.disconnect(self.parent.conectores[1].linha)
                self.parent.conectores[1].linha.disconnect(conector.linha)
                for conector2 in self.parent.conectores:
                    if conector.linha != conector2.linha and conector.linha != self.parent.conectores[
                            1].linha:
                        conector.linha.connect_to(conector2.linha)

        def c():
            """
             |   |
             |  ‾‾‾
             |___
             |   |
            """
            # remove todas as conexoes da linha 3 e conecta as outras entre si
            for conector in self.parent.conectores:
                conector.linha.disconnect(self.parent.conectores[3].linha)
                self.parent.conectores[3].linha.disconnect(conector.linha)
                for conector2 in self.parent.conectores:
                    if conector.linha != conector2.linha and conector.linha != self.parent.conectores[
                            3].linha:
                        conector.linha.connect_to(conector2.linha)

        def d():
            """
             |   |
             ‾‾‾‾|
            ___  |
             |   |
            """
            # remove todas as conexoes da linha 0 e conecta as outras entre si
            for conector in self.parent.conectores:
                conector.linha.disconnect(self.parent.conectores[0].linha)
                self.parent.conectores[0].linha.disconnect(conector.linha)
                for conector2 in self.parent.conectores:
                    if conector.linha != conector2.linha and conector.linha != self.parent.conectores[
                            0].linha:
                        conector.linha.connect_to(conector2.linha)

        def e():
            """
             |   |
             |‾‾‾
             |  ___
             |   |
            """
            # remove todas as conexoes da linha 2 e conecta as outras entre si
            for conector in self.parent.conectores:
                conector.linha.disconnect(self.parent.conectores[2].linha)
                self.parent.conectores[2].linha.disconnect(conector.linha)
                for conector2 in self.parent.conectores:
                    if conector.linha != conector2.linha and conector.linha != self.parent.conectores[
                            2].linha:
                        conector.linha.connect_to(conector2.linha)

        def f():
            """
             .    |
            / \  \ /
             |    .
            """
            self.desconecta_tudo()

            self.parent.conectores[1].linha.connect_to(
                self.parent.conectores[0].linha)
            self.parent.conectores[0].linha.connect_to(
                self.parent.conectores[1].linha)

            self.parent.conectores[2].linha.connect_to(
                self.parent.conectores[3].linha)
            self.parent.conectores[3].linha.connect_to(
                self.parent.conectores[2].linha)

        def g():
            """ _
               \/|
               /\
              / __|
            """
            self.desconecta_tudo()
            self.parent.conectores[3].linha.connect_to(
                self.parent.conectores[0].linha)
            self.parent.conectores[0].linha.connect_to(
                self.parent.conectores[3].linha)

            self.parent.conectores[2].linha.connect_to(
                self.parent.conectores[1].linha)
            self.parent.conectores[1].linha.connect_to(
                self.parent.conectores[2].linha)

        def h():
            """
             |   |
            ‾‾‾  |
            ___ \ /
             |   .
            """
            self.desconecta_tudo()
            self.parent.conectores[3].linha.connect_to(
                self.parent.conectores[2].linha)
            self.parent.conectores[2].linha.connect_to(
                self.parent.conectores[3].linha)

        def i():
            """
             .     |
            / \   ‾‾‾
             |    ___
             |     |
            """
            self.desconecta_tudo()
            self.parent.conectores[1].linha.connect_to(
                self.parent.conectores[0].linha)
            self.parent.conectores[0].linha.connect_to(
                self.parent.conectores[1].linha)

        def j():
            """
             \   |
              \ ‾‾‾
            ___\
             | _\|
            """
            self.desconecta_tudo()
            self.parent.conectores[1].linha.connect_to(
                self.parent.conectores[2].linha)
            self.parent.conectores[2].linha.connect_to(
                self.parent.conectores[2].linha)

        def k():
            """
             | ‾/|
            ‾‾‾/
              /___
             /  |
            """
            self.desconecta_tudo()
            self.parent.conectores[3].linha.connect_to(
                self.parent.conectores[0].linha)
            self.parent.conectores[0].linha.connect_to(
                self.parent.conectores[3].linha)

        def l():
            """
             |   |
            ‾‾‾ ‾‾‾
             _____
             |   |
            """
            self.desconecta_tudo()
            self.parent.conectores[0].linha.connect_to(
                self.parent.conectores[2].linha)
            self.parent.conectores[2].linha.connect_to(
                self.parent.conectores[0].linha)

        def m():
            """
             |___|
            ___ ___
             |   |
            """
            self.desconecta_tudo()
            self.parent.conectores[3].linha.connect_to(
                self.parent.conectores[1].linha)
            self.parent.conectores[1].linha.connect_to(
                self.parent.conectores[3].linha)

        def n():
            """
             |   |
             ‾‾‾‾‾
             _____
             |   |
            """
            self.desconecta_tudo()

            self.parent.conectores[3].linha.connect_to(
                self.parent.conectores[1].linha)
            self.parent.conectores[1].linha.connect_to(
                self.parent.conectores[3].linha)

            self.parent.conectores[0].linha.connect_to(
                self.parent.conectores[2].linha)
            self.parent.conectores[2].linha.connect_to(
                self.parent.conectores[0].linha)

        def o():
            """
             |    |
             |____|
             |    |
             |    |
            """
            # conecta tudo
            for conector in self.parent.conectores:
                for conector2 in self.parent.conectores:
                    if conector.linha != conector2.linha:  # para nao conectar a si mesmo
                        conector.linha.connect_to(conector2.linha)

        self.tipo = tipo
        self.vias = [
            {'imagem': 'images/4vias_a.png', 'logica': a},
            {'imagem': 'images/4vias_b.png', 'logica': b},
            {'imagem': 'images/4vias_c.png', 'logica': c},
            {'imagem': 'images/4vias_d.png', 'logica': d},
            {'imagem': 'images/4vias_e.png', 'logica': e},
            {'imagem': 'images/4vias_f.png', 'logica': f},
            {'imagem': 'images/4vias_g.png', 'logica': g},
            {'imagem': 'images/4vias_h.png', 'logica': h},
            {'imagem': 'images/4vias_i.png', 'logica': i},
            {'imagem': 'images/4vias_j.png', 'logica': j},
            {'imagem': 'images/4vias_k.png', 'logica': k},
            {'imagem': 'images/4vias_l.png', 'logica': l},
            {'imagem': 'images/4vias_m.png', 'logica': m},
            {'imagem': 'images/4vias_n.png', 'logica': n},
            {'imagem': 'images/4vias_o.png', 'logica': o}
        ]

        super(QuatroVias, self).__init__(self.tipo, self.vias, **kwargs)


class CincoVias(Vias):

    def __init__(self, tipo, **kwargs):

        def a():
            """
             |      |
            ‾‾‾    ‾‾‾
           ___ ___ ___
            |   |   |
            """
            self.desconecta_tudo()

        def b():
            """
              |\‾  .
            ___ \ / \
             |   \ |
            """
            self.desconecta_tudo()

            self.parent.conectores[4].linha.connect_to(
                self.parent.conectores[1].linha)
            self.parent.conectores[1].linha.connect_to(
                self.parent.conectores[4].linha)

            self.parent.conectores[3].linha.connect_to(
                self.parent.conectores[2].linha)
            self.parent.conectores[2].linha.connect_to(
                self.parent.conectores[3].linha)
            return 0

        def c():
            """
             |   ‾/|
            \ /  / ___
             .  /   |
            """
            self.desconecta_tudo()

            self.parent.conectores[0].linha.connect_to(
                self.parent.conectores[1].linha)
            self.parent.conectores[1].linha.connect_to(
                self.parent.conectores[0].linha)

            self.parent.conectores[3].linha.connect_to(
                self.parent.conectores[4].linha)
            self.parent.conectores[4].linha.connect_to(
                self.parent.conectores[3].linha)

        def d():
            """
             |     |
            \ /___\ /
             .  |  .
            """
            self.desconecta_tudo()

            self.parent.conectores[3].linha.connect_to(
                self.parent.conectores[2].linha)
            self.parent.conectores[2].linha.connect_to(
                self.parent.conectores[3].linha)

            self.parent.conectores[0].linha.connect_to(
                self.parent.conectores[1].linha)
            self.parent.conectores[1].linha.connect_to(
                self.parent.conectores[0].linha)

        def e():
            """
             |   |
             ‾‾‾‾‾
             _____
             | | |
            """
            self.desconecta_tudo()

            self.parent.conectores[3].linha.connect_to(
                self.parent.conectores[1].linha)
            self.parent.conectores[1].linha.connect_to(
                self.parent.conectores[3].linha)

            self.parent.conectores[0].linha.connect_to(
                self.parent.conectores[2].linha)
            self.parent.conectores[2].linha.connect_to(
                self.parent.conectores[0].linha)
            self.parent.conectores[4].linha.connect_to(
                self.parent.conectores[2].linha)
            self.parent.conectores[2].linha.connect_to(
                self.parent.conectores[4].linha)
            self.parent.conectores[0].linha.connect_to(
                self.parent.conectores[4].linha)
            self.parent.conectores[4].linha.connect_to(
                self.parent.conectores[0].linha)

        def f():
            """
             |   |
             |   |
             |___|
             | | |
            """
            # conecta tudo
            for conector in self.parent.conectores:
                for conector2 in self.parent.conectores:
                    if conector.linha != conector2.linha:  # para nao conectar a si mesmo
                        conector.linha.connect_to(conector2.linha)

        def g():
            """
            |      |
             ‾‾‾|‾‾‾
            ___ |  ___
             |  |   |
            """
            self.desconecta_tudo()

            self.parent.conectores[1].linha.connect_to(
                self.parent.conectores[3].linha)
            self.parent.conectores[3].linha.connect_to(
                self.parent.conectores[1].linha)
            self.parent.conectores[4].linha.connect_to(
                self.parent.conectores[1].linha)
            self.parent.conectores[1].linha.connect_to(
                self.parent.conectores[4].linha)
            self.parent.conectores[3].linha.connect_to(
                self.parent.conectores[4].linha)
            self.parent.conectores[4].linha.connect_to(
                self.parent.conectores[3].linha)

        self.tipo = tipo
        self.vias = [
            {'imagem': 'images/5vias_a.png', 'logica': a},
            {'imagem': 'images/5vias_b.png', 'logica': b},
            {'imagem': 'images/5vias_c.png', 'logica': c},
            {'imagem': 'images/5vias_d.png', 'logica': d},
            {'imagem': 'images/5vias_e.png', 'logica': e},
            {'imagem': 'images/5vias_f.png', 'logica': f},
            {'imagem': 'images/5vias_g.png', 'logica': g}
        ]

        super(CincoVias, self).__init__(self.tipo, self.vias, **kwargs)


class Fonte(Componente):
    """fonte de ar comprimido"""

    source = 'images/tri.png'
    pressao = 6
    vazao = 1

    def remove_bubble(self):
        """remove o menu flutuante"""
        if not simulando:
            if self.menu in self.children:
                self.remove_widget(self.menu)

    def ciclo(self, dt):
        """ciclo de pressurização da linha conectada
        """
        if simulando:
            if self.conectores[0].linha is not None:
                self.conectores[0].linha.pressao = self.pressao
                self.conectores[0].linha.vazao =1# self.vazao
                self.conectores[0].linha.propaga = True

    def on_enter(instance, value):
        """altera seu valor de pressão ao pressionar enter"""

        try:
            instance.pressao = float(value.text)
        except:
            instance.pressao = 0
        instance.remove_bubble()

    def __init__(self, **kwargs):

        self.conectores = [
            Conector('saida', (13, 22), 'vertical', center=self.pos)
        ]

        super(Fonte, self).__init__(**kwargs)

        # cria o menu flutuante
        self.menu = Bubble(
            size=(100, 35),
            orientation='horizontal',
            arrow_pos='bottom_mid'
        )
        self.menu.add_widget(Label(text='Pressao:'))
        self.valor_pressao = TextInput(multiline=False)
        self.menu.add_widget(self.valor_pressao)

        self.valor_pressao.bind(on_text_validate=self.on_enter)


    def on_touch_down(self, touch):
        """exibe o menu ao clicar com o botão direito"""
        abre_menu = False
        if 'button' in dir(touch):
            if touch.button == 'right':
                abre_menu = True
        elif touch.is_double_tap:
            abre_menu = True

        if abre_menu:
            if not simulando:
                if self.collide_point(*touch.pos):
                    if self.menu not in self.children:
                        self.menu.center = (
                            self.center[0], self.center[1] + self.height)
                        self.add_widget(self.menu)

        else:
            if not self.menu.collide_point(*touch.pos):
                self.remove_bubble()

        super(Image, self).on_touch_down(touch)


class Escape(Componente):
    """escape de ar para a atmosfera"""

    source = 'images/tri2.png'

    def ciclo(self, dt):
        """ciclo de atualização de pressão da linha"""
        if simulando:
            if self.conectores[0].linha is not None:
                self.conectores[0].linha.pressao = 0
                self.conectores[0].linha.vazao = 0
                self.conectores[0].linha.propaga = True

    def __init__(self, **kwargs):

        self.conectores = [
            Conector('saida', (13, 22), 'vertical', center=self.pos)
        ]

        super(Escape, self).__init__(**kwargs)

        
class UnidadeCondicionadora(Componente):
    """unidade condicionadora de ar comprimido
    sua função no software é apenas de ajustar a saída de pressão
    """

    source = 'images/flr.png'
    # fator que multiplica a pressão de entrada. Varia de 0 a 1
    fator = 1

    def remove_bubble(self):
        """apaga o menu flutuante"""
        if not simulando:
            self.fator = self.slider.value / 100
            if self.menu in self.parent.children:
                self.parent.remove_widget(self.menu)

    def ciclo(self, dt):
        """ciclo de atualização da pressão de saída"""
        if simulando:
            if self.conectores[1].linha is not None:
                self.conectores[1].linha.pressao = self.conectores[
                    0].linha.pressao * self.fator

    def __init__(self, **kwargs):

        self.conectores = [
            Conector('entrada', (0, 20), 'horizontal', center=self.pos),
            Conector('saida', (83, 20), 'horizontal', center=self.pos)
        ]

        super(UnidadeCondicionadora, self).__init__(**kwargs)

        # cria o menu de vias flutuante
        self.menu = Bubble(
            size=(100, 35),
            orientation='horizontal',
            arrow_pos='bottom_mid'
        )
        # adiciona um slider para ajustar a pressão de saída
        self.slider = Slider(min=0, max=100, value=100)
        self.menu.add_widget(self.slider)


    def on_touch_down(self, touch):
        """exibe o menu flutuance ao clicar com o botão direito
        remove o menu ao clicar do lado de fora
        """
        abre_menu = False
        if 'button' in dir(touch):
            if touch.button == 'right':
                abre_menu = True
        elif touch.is_double_tap:
            abre_menu = True

        if abre_menu:
            if not simulando:
                if self.collide_point(*touch.pos):
                    if self.menu not in self.children:
                        self.menu.center = (
                            self.center[0], self.center[1] + self.height)
                        self.parent.add_widget(self.menu)
        else:
            if not self.menu.collide_point(*touch.pos):
                self.remove_bubble()

        super(Image, self).on_touch_down(touch)
            

class RedutorVazao(Componente):
    """Válvula redutora de vazão com retenção
    """
    
    # fator que multiplica a vazão de entrada. Varia de 0 a 1
    fator = 1

    def remove_bubble(self):
        """apaga o menu flutuante"""
        if not simulando:
            self.fator = self.slider.value / 100
            if self.menu in self.parent.children:
                self.parent.remove_widget(self.menu)

    def ciclo(self, dt):
        """ciclo de atualização da pressão de saída"""
        if simulando:
            if self.conectores[0].linha is not None and self.conectores[1].linha is not None:
                self.conectores[1].linha.connect_to(
                    self.conectores[0].linha)

                self.conectores[1].linha.pressao = self.conectores[0].linha.pressao
                self.conectores[1].linha.vazao = self.conectores[0].linha.vazao * self.fator
                self.conectores[1].linha.propaga = True

                self.conectores[0].linha.pressao = self.conectores[1].linha.pressao
                self.conectores[0].linha.vazao = self.conectores[1].linha.vazao


    def inverter(self, instance):
        # troca imagem
        if self.source == 'images/x10640.png':
            self.source = 'images/x10640b.png'
        else:
            self.source = 'images/x10640.png'

        # inverte os conectores
        self.conectores[0].pos_relativa, self.conectores[1].pos_relativa = self.conectores[1].pos_relativa, self.conectores[0].pos_relativa

        # desconecta as linhas
        for conector in self.conectores:
            if conector.linha is not None:
                conector.linha.apaga_linha()        


    def __init__(self, **kwargs):

        self.source = 'images/x10640.png'

        self.conectores = [
            Conector('entrada', (20, -1), 'vartical', center=self.pos),
            Conector('saida', (20, 81), 'vertical', center=self.pos)
        ]

        super(RedutorVazao, self).__init__(**kwargs)

        # cria o menu de vias flutuante
        self.menu = Bubble(
            size=(150, 35),
            orientation='horizontal',
            arrow_pos='bottom_mid'
        )
        # adiciona um slider para ajustar a pressão de saída
        self.slider = Slider(min=0, max=100, value=100)
        self.button = Button(text='inverter', on_press=self.inverter)
        self.menu.add_widget(self.slider)
        self.menu.add_widget(self.button)


    def on_touch_down(self, touch):
        """exibe o menu flutuance ao clicar com o botão direito
        remove o menu ao clicar do lado de fora
        """

    def on_touch_down(self, touch):
        abre_menu = False
        if 'button' in dir(touch):
            if touch.button == 'right':
                abre_menu = True
        elif touch.is_double_tap:
            abre_menu = True

        if abre_menu:
            if not simulando:
                if self.collide_point(*touch.pos):
                    if self.menu not in self.children:
                        self.menu.center = (
                            self.center[0], self.center[1] + self.height)
                        self.parent.add_widget(self.menu)
        else:
            if not self.menu.collide_point(*touch.pos):
                self.remove_bubble()
        super(Image, self).on_touch_down(touch)

class Manometro(Componente):
    """indicador de pressão nas linhas
    exibe o valor de pressão na liha em que está conectado
    """

    source = 'images/manometro.png'

    def ciclo(self, dt):
        if simulando:
            if self.conectores[0].linha is not None:
                self.etiqueta.text = str(self.conectores[0].linha.vazao)

    def __init__(self, **kwargs):

        self.conectores = [
            Conector('saida', (20, 0), 'vertical', center=self.pos)
        ]

        super(Manometro, self).__init__(**kwargs)

        self.etiqueta = Label(text='', color=(0, 0, 0))
        self.add_widget(self.etiqueta)

        def update_rect(instance, value):
            """reposiciona o label naa posição do manômetro"""
            self.etiqueta.center = center = (
                self.center[0], self.pos[1] + self.height + 5)

        self.bind(pos=update_rect, size=update_rect)


class CursoRolete(Widget):
    """marcação de curso do cilindro para acionar o rolete"""

    def __init__(self, **kwargs):

        super(CursoRolete, self).__init__(**kwargs)
        self.size = 5, 10

        with self.canvas:
            Color(0, 0, 0)
            self.marca = Rectangle(size=(5, 10), pos=self.pos)

        self.etiqueta = Label(
            text='S0', color=(
                0, 0, 0), center=(
                self.center[0], self.pos[1] + 20))
        self.add_widget(self.etiqueta)

        def update_rect(instance, value):
            """atualiza as posições dos elementos para acompanhar o arrasto com o mouse"""

            self.etiqueta.center = (self.center[0], self.pos[1] + 20)
            self.marca.pos = self.pos

        
        self.bind(pos=update_rect, size=update_rect)

    def on_touch_move(self, touch):
        """move a marcação ao arrastar com o mouse"""

        global movendo
        if self.collide_point(*touch.pos):
            if movendo is None:
                if self.collide_point(*touch.pos):
                    movendo = self
        if movendo == self:
            self.center = touch.pos

    def on_touch_up(self, touch):
        """libera o mouse para interagir com outros componentes"""

        global movendo
        if movendo == self:
            movendo = None


class CursoGatilho(Image):
    """marcação de curso do cilindro para acionar o gatilho"""

    def __init__(self, **kwargs):

        super(CursoGatilho, self).__init__(**kwargs)
        self.size = 10, 10

        self.source = 'images/seta.png'
        self.direcao = 'direita'

        self.etiqueta = Label(
            text='S0', color=(
                0, 0, 0), center=(
                self.center[0], self.pos[1] + 20))
        self.add_widget(self.etiqueta)

        def update_rect(instance, value):
            """atualiza as posições dos elementos para acompanhar o arrasto com o mouse"""

            self.etiqueta.center = (self.center[0], self.pos[1] + 20)

        
        self.bind(pos=update_rect, size=update_rect)

    def on_touch_down(self, touch):
        """move a marcação ao arrastar com o mouse"""
        muda_marca = False
        def on_touch_down(self, touch):
            if 'button' in dir(touch):
                if touch.button == 'right':
                    muda_marca = True
            elif touch.is_double_tap:
                muda_marca = True

            if muda_marca:
                if self.direcao == 'direita':
                    self.source = 'images/setab.png'
                    self.direcao = 'esquerda'
                else:
                    self.source = 'images/seta.png'
                    self.direcao = 'direita'

    def on_touch_move(self, touch):
        """move a marcação ao arrastar com o mouse"""

        global movendo
        if self.collide_point(*touch.pos):
            if movendo is None:
                if self.collide_point(*touch.pos):
                    movendo = self
        if movendo == self:
            self.center = touch.pos

    def on_touch_up(self, touch):
        """libera o mouse para interagir com outros componentes"""

        global movendo
        if movendo == self:
            movendo = None
