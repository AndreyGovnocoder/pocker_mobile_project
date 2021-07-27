from kivy.core.audio import SoundLoader
from kivy.factory import Factory
from kivymd.uix.bottomsheet import MDListBottomSheet, MDCustomBottomSheet
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar
import random
import deck

Window.size = (500, 800)

KV = '''
<ResultCustomSheet@BoxLayout>:
    orientation: "vertical"
    size_hint_y: None
    height: "600dp"
    padding: 10
    
    ScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            size_hint: [1, 1]
            Image:
                source: app.resultImage   
                size_hint: [1, 1] 
            MDLabel:
                text: app.result
                size_hint: [1, 1]
            MDLabel:
                text: app.result_2
                halign: 'center'
                size_hint: [1, 1]
            
            MDRectangleFlatButton:
                text: 'Ок'
                on_press: 
                    app.play_sound('click')
                    app.custom_sheet.dismiss()    

<BidCustomSheet@BoxLayout>:
    orientation: "vertical"
    size_hint_y: None
    height: "1700dp"
    padding: 10
    
    MDBoxLayout:
        orientation: 'vertical'
        MDBoxLayout:
            orientation: 'vertical'
            size_hint: [1, 1]
            spacing: 3
            MDBoxLayout:
                orientation: 'horizontal'
                size_hint: [1, None]
                MDGridLayout:
                    cols: 3
                    size_hint: [1, None]
                    MDLabel:
                        text: 'Ваши деньги:'
                        size_hint: [1, 1]
                    MDLabel:
                        id: plr_money
                        size_hint: [1, 1]
                        halign: 'center'
                        text: str(app.players[0].money - app.players[1].bet)
                    MDLabel:
                        size_hint: [.1, 1]
                        halign: 'left'
                        text: '$'
                    MDLabel:
                        text: 'Ставка: '
                    MDLabel:
                        id: bet_lbl
                        halign: 'center'
                        text: '0' 
                    MDLabel:
                        halign: 'left'
                        text: '$'
                
            MDGridLayout:
                cols: 3
                spacing: 3
                size_hint: [1, None]
                MDRectangleFlatButton: 
                    text: '+10'
                    on_press: 
                        app.set_plr_bet(10, plr_money, bet_lbl)
                MDRectangleFlatButton: 
                    text: '+20'
                    on_press: app.set_plr_bet(20, plr_money, bet_lbl)
                MDRectangleFlatButton: 
                    text: '+30'
                    on_press: app.set_plr_bet(30, plr_money, bet_lbl)
                MDRectangleFlatButton: 
                    text: '-10'
                    on_press: app.set_plr_bet(-10, plr_money, bet_lbl)
                MDRectangleFlatButton: 
                    text: '-20'
                    on_press: app.set_plr_bet(-20, plr_money, bet_lbl)
                MDRectangleFlatButton: 
                    text: '-30'
                    on_press: app.set_plr_bet(-30, plr_money, bet_lbl)
                MDRectangleFlatButton: 
                    text: 'ВА-БАНК!!!'
                    size_hint: [None, None]
                    on_press: 
                        app.play_sound('click')
                        app.custom_sheet.dismiss()
                        app.set_plr_bet(int(plr_money.text), plr_money, bet_lbl)
            MDBoxLayout:
                orientation: 'horizontal'
                spacing: 10
                size_hint: [1, 1]
                MDRaisedButton:
                    text: 'Принять'
                    on_press: 
                        app.play_sound('ok')
                        app.custom_sheet.dismiss()
                        app.plr_raised(int(bet_lbl.text))
                MDRectangleFlatButton:
                    text: 'Отмена'
                    on_press: 
                        app.play_sound('cancel')
                        app.custom_sheet.dismiss()    
                
            
            
MDBoxLayout:
    orientation: 'vertical'
    MDToolbar:
        id: toolbar
        title: 'Полу-Покер'
        right_action_items: [['help', lambda x: app.set_screen('scr_help')], ['cogs', lambda x: app.set_screen('scr_settings')]]
        left_action_items: [['home', lambda x: app.set_screen('scr_main')]]
    NavigationLayout:
        ScreenManager:
            id: scrm
            Screen:
                name: 'scr_main'
                FitImage:
                    source: 'imgs/main_scr.jpg'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: 10
                    spacing: 50
                    size_hint: [1, 1] 
                    
                    MDBoxLayout:
                        orientation: 'horizontal'
                        AnchorLayout:
                            anchor_x: 'left'
                            anchor_y: 'bottom'                        
                            MDRaisedButton:
                                text: 'Начать новую игру'
                                on_press: 
                                    app.play_sound('click')
                                    app.start_new_game()
                                
                        AnchorLayout:
                            anchor_x: 'right'
                            anchor_y: 'bottom'
                            MDRaisedButton:
                                id: continue_btn
                                text: 'Продолжить игру'
                                disabled: True
                                on_press: 
                                    app.play_sound('click')
                                    app.set_screen('scr_game')
            MDScreen:
                name: 'scr_game'   
                FitImage:
                    source: 'imgs/bg.jpg'            
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: 20
                    padding: 10 
                    size_hint: [1, 1]
                    MDLabel:
                        id: round_lbl
                        size_hint: [1, 0.01]
                        halign: 'center'
                        theme_text_color: 'Custom'
                        text_color: 1, 1, 1, 1
                    MDBoxLayout:
                        orientation: 'horizontal'
                        MDLabel:
                            text: 'Деньги соперника:'
                            halign: 'left'
                            size_hint: [1,1]
                            theme_text_color: 'Custom'
                            text_color: 1, 1, 1, 1
                        MDLabel:
                            id: comp_money_lbl
                            text: str(app.players[1].money) + ' $'
                            halign: 'left'
                            size_hint: [1,1]
                            theme_text_color: 'Custom'
                            text_color: 1, 1, 1, 1
                            
                        MDGridLayout:
                            id: comp_hand
                            size_hint: [None,1]
                            spacing: 3
                            cols: 2
                            
                    MDLabel:
                        id: comp_info
                        halign: 'center'
                        theme_text_color: 'Custom'
                        text_color: 1, 1, 1, 1    
                    
                    AnchorLayout:
                        spacing: 3
                        anchor_x: 'left'
                        
                        MDBoxLayout:
                            id: table
                            orientation: 'horizontal'
                            spacing: 5
                            adaptive_height: True
                            size_hint: [1,None]
                            
                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint: [1,1]
                        MDLabel: 
                            text: 'Банк:'
                            halign: 'left'
                            size_hint: [None, 1]
                            theme_text_color: 'Custom'
                            text_color: 1, 1, 1, 1
                        MDLabel: 
                            id: bank_lbl
                            size_hint: [None, 1]
                            text: str(app.bank) + ' $'
                            theme_text_color: 'Custom'
                            text_color: 1, 1, 1, 1
                        
                    
                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint: [1,.1]
                        MDLabel: 
                            id: plr_info
                            halign: 'center'
                            theme_text_color: 'Custom'
                            text_color: 1, 1, 1, 1
                    
                    MDBoxLayout:
                        orientation: 'horizontal'
                        MDLabel: 
                            text: 'Ваши деньги:'
                            size_hint: [None, 1]
                            theme_text_color: 'Custom'
                            text_color: 1, 1, 1, 1
                        MDLabel: 
                            id: plr_money_lbl
                            text: str(app.players[0].money) + ' $'
                            theme_text_color: 'Custom'
                            text_color: 1, 1, 1, 1
                         
                    MDBoxLayout:
                        orientation: 'horizontal'
                        MDGridLayout:
                            id: player_hand
                            cols: 2
                        MDBoxLayout:
                            orientation: 'vertical'
                            spacing: 3
                            size_hint: [1, None]
                            MDRaisedButton:
                                id: call_btn
                                text: 'Принять ставку'
                                on_press: 
                                    app.play_sound('click')
                                    app.plr_call()
                            MDRaisedButton:
                                id: raise_btn
                                text: 'Поднять ставку'
                                on_press: 
                                    app.play_sound('click')
                                    app.plr_raise()
                            MDRaisedButton:
                                id: fold_btn
                                text: 'Сбросить карты'
                                on_press: 
                                    app.play_sound('click')
                                    app.plr_fold()   
                    
                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint: [1, 1]
                        spacing: 5
                        AnchorLayout:
                            spacing: 3
                            anchor_x: 'left'    
                            MDRaisedButton:
                                id: next_game_btn
                                text: 'Дальше'
                                disabled: True
                                on_press: 
                                    app.play_sound('click')
                                    app.start_game()
                        AnchorLayout:
                            spacing: 3
                            anchor_x: 'right'  
                            MDRaisedButton:
                                id: next_round_btn
                                text: 'Внести ставку'
                                disabled: True
                                on_press: 
                                    app.play_sound('click')
                                    app.end_round() 

            Screen:
                name: 'scr_settings'
                MDBoxLayout:
                    size_hint: [1, 1]
                    orientation: 'vertical'
                    padding: 10
                    spacing: 10    
                    MDGridLayout:
                        size_hint: [1, None]
                        adaptive_height: True
                        cols: 3
                        MDLabel:
                            text: 'Громкость звука:'
                        MDSlider:
                            min: 0
                            max: 100
                            value: 100
                            step: 1
                            hint: False
                            show_off: False
                            on_value: 
                                app.set_sound_volume(int(self.value))
                                app.play_sound('sound')
                                sound_volume_value.text = str(int(self.value))                                
                        MDLabel:
                            id: sound_volume_value
                            text: '100'
                        MDLabel:
                            text: 'Громкость музыки:'
                        MDSlider:
                            min: 0
                            max: 100
                            value: 40
                            step: 1
                            hint: False
                            show_off: False
                            on_value: 
                                app.set_music_volume(int(self.value))
                                music_volume_value.text = str(int(self.value))                                
                        MDLabel:
                            id: music_volume_value
                            text: '40'                                                        
                        
                    MDGridLayout:
                        adaptive_height: True
                        size_hint: [1,None]
                        padding: 0,0,0,0
                        cols: 3
                        MDLabel:
                            text: 'Рубашки карт:'
                        
                        MDBoxLayout:
                            orientation: 'vertical'
                            adaptive_height: True
                            size_hint: [1,None]
                            Image:
                                source: 'cards/1_shirt.png'
                            MDCheckbox:
                                id: shirt_kind_1
                                group: 'shirt_kind'
                                active: True
                                on_state: 
                                    app.play_sound('set')
                                    app.settings.shirt_kind = 1
                        MDBoxLayout:
                            orientation: 'vertical'
                            adaptive_height: True
                            size_hint: [1, None]
                            Image:
                                source: 'cards/2_shirt.png'
                            MDCheckbox:
                                id: shirt_kind_2
                                group: 'shirt_kind'
                                active: False
                                on_state: 
                                    app.play_sound('set')
                                    app.settings.shirt_kind = 2
                                
                        MDLabel:
                            text: 'Колода карт:'
                            size_hint: [1,None]
                        MDBoxLayout:
                            orientation: 'vertical'
                            adaptive_height: True
                            size_hint: [1,None]
                            Image:
                                source: 'cards/1_h13.png'
                            MDCheckbox:
                                id: deck_kind_1
                                group: 'deck_kind'
                                active: True
                                on_state: 
                                    app.play_sound('set')
                                    app.settings.deck_kind = 1
                        MDBoxLayout:
                            orientation: 'vertical'
                            adaptive_height: True
                            Image:
                                source: 'cards/2_h13.png'
                            MDCheckbox:
                                id: deck_kind_2
                                group: 'deck_kind'
                                active: False
                                on_state: 
                                    app.play_sound('set')
                                    app.settings.deck_kind = 2
                        MDLabel:
                            text: 'Музыка:'
                        
                        MDBoxLayout:
                            orientation: 'vertical'
                            adaptive_height: True
                            size_hint: [1,None]
                            MDLabel:
                                text: 'Мелодия 1'
                                halign: 'center'
                            MDCheckbox:
                                id: music_1
                                group: 'music_kind'
                                active: True
                                on_state: 
                                    app.load_music('src/musics/m1.mp3')
                                    app.play_music()
                        MDBoxLayout:
                            orientation: 'vertical'
                            adaptive_height: True
                            size_hint: [1, None]
                            MDLabel:
                                text: 'Мелодия 2'
                                halign: 'center'
                            MDCheckbox:
                                id: music_2
                                group: 'music_kind'
                                active: False
                                on_state: 
                                    app.load_music('src/musics/m2.mp3')
                                    app.play_music()
                    
                    MDGridLayout:
                        cols: 3
                        MDLabel:
                            text: 'Цветовая схема'                            
                        MDBoxLayout:
                            orientation: 'horizontal'
                            MDSlider:
                                min: 1
                                max: 18
                                value: 1
                                step: 1
                                hint: False
                                show_off: False
                                on_value: app.set_primary_palette(self.value)
                        MDLabel:
                            id: lbl_primary_palette 
                            text: 'Красный'
                    
                        MDLabel:
                            text: 'Насыщенность цвета'
                            
                        MDBoxLayout:
                            orientation: 'horizontal'
                            MDSlider:
                                min: 1
                                max: 13
                                value: 12
                                step: 1
                                hint: False
                                show_off: False
                                on_value: app.set_primary_hue(self.value)
                        MDLabel:
                            id: lbl_primary_hue 
                            text: '800'
                    MDRectangleFlatButton:
                        text: 'Назад'   
                        on_press:   
                            app.play_sound('back_btn')
                            app.to_back_screen()

            Screen:
                name: 'scr_help'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: 10, 10, 10, 50
                    ScrollView:
                        padding: 30
                        MDLabel:
                            id: help_lbl
                            text_size: self.width, None
                            size_hint: 1, None
                            height: self.texture_size[1]
                MDBoxLayout:
                    size_hint: [1, 1]
                    orientation: 'horizontal'
                    padding: 10
                    spacing: 10                
                    MDRectangleFlatButton:
                        text: 'Назад'   
                        on_press: 
                            app.play_sound('back_btn')
                            app.to_back_screen()
                    AnchorLayout:
                        spacing: 3
                        anchor_x: 'right'  
                        anchor_y: 'bottom'
                        MDRaisedButton:
                            text: 'Комбинации'
                            on_press: 
                                app.play_sound('click')
                                app.play_sound('slide')
                                scrm.current = 'scr_combinations'
                            
            Screen:
                name: 'scr_combinations'
                FitImage:
                    source: 'imgs/combs_bg.png'
                MDBoxLayout:
                    size_hint: [1, 1]
                    orientation: 'horizontal'
                    padding: 20, 0, 20, 50
                    Image:
                        adaptive_height: True
                        size_hint: [1, 1]
                        source: 'imgs/combinations.png'
                MDBoxLayout:
                    size_hint: [1, 1]
                    orientation: 'horizontal'
                    padding: 10
                    spacing: 10                
                    MDRectangleFlatButton:
                        text: 'Назад'   
                        on_press: 
                            app.play_sound('back_btn')
                            app.play_sound('slide')
                            scrm.current = 'scr_help'
                    
'''

rounds = ['Пре-флоп', 'Флоп', 'Тёрн', 'Ривер', 'Вскрытие карт']


class Player:
    bluff = False
    bet = 0
    winner = False
    call = False
    raised = False
    all_in = False

    def __init__(self, turn, money, ai, inGame):
        self.money = money
        self.ai = ai
        self.inGame = inGame
        self.turn = turn

    def set_combination(self, combination):
        self.combination = combination

    def get_combination(self):
        if not self.combination is None:
            return self.combination
        else:
            return False

    def set_bet(self, bet):
        self.bet = bet

    def get_bet(self):
        return self.bet

class Settings:
    def __init__(self, sound_volume, deck_kind, shirt_kind):
        self.sound_volume = sound_volume
        self.deck_kind = deck_kind
        self. shirt_kind = shirt_kind


class MyPokerApp(MDApp):
    back = ''
    deck = []
    player_hand = []
    comp_hand = []
    table = []
    players = []
    sounds = []
    turn = 0
    bank = 0
    custom_sheet = None
    deal_delay = 1.2
    comp_delay = 0.7
    opacity = 0.4
    is_game = False
    is_deal_to_table = False
    is_deal_to_players = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        player = Player(0, 1000, False, True)
        self.players.append(player)
        comp = Player(1, 1000, True, True)
        self.players.append(comp)
        self.music = None
        self.sound = None
        self.load_sounds()
        #self.set_music_volume(40)
        self.set_sound_volume(100)
        self.screen = Builder.load_string(KV)

    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Red'
        self.theme_cls.primary_hue = '800'
        self.title = 'Покер "Техасский холдем"'
        self.load_music('src/musics/m1.mp3')
        self.play_music()
        self.screen.ids.call_btn.disabled = True
        self.screen.ids.raise_btn.disabled = True
        self.screen.ids.fold_btn.disabled = True
        self.init_help()
        self.settings = Settings(50, 1, 1)
        return self.screen

    def load_music(self, path):
        try:
            if self.music is not None:
                self.music.stop()
            self.music = SoundLoader.load(path)
            self.music.loop = True
        except:
            Snackbar(text='Ошибка загрузки музыки').show()

    def load_sounds(self):
        self.load_one_sound('src/sounds/deal1.mp3')
        self.load_one_sound('src/sounds/deal2.mp3')
        self.load_one_sound('src/sounds/deal3.mp3')
        self.load_one_sound('src/sounds/showdown.mp3')
        self.load_one_sound('src/sounds/plr_all_in.mp3')
        self.load_one_sound('src/sounds/plr_win.mp3')
        self.load_one_sound('src/sounds/draw.mp3')
        self.load_one_sound('src/sounds/fold.mp3')
        self.load_one_sound('src/sounds/comp_win.mp3')
        self.load_one_sound('src/sounds/bet+.mp3')
        self.load_one_sound('src/sounds/bet-.mp3')
        self.load_one_sound('src/sounds/comp_all_in.mp3')
        self.load_one_sound('src/sounds/raise.mp3')
        self.load_one_sound('src/sounds/call.mp3')
        self.load_one_sound('src/sounds/bet_voice.mp3')
        self.load_one_sound('src/sounds/call_voice.mp3')
        self.load_one_sound('src/sounds/click.mp3')
        self.load_one_sound('src/sounds/start.mp3')
        self.load_one_sound('src/sounds/slide.mp3')
        self.load_one_sound('src/sounds/back.mp3')
        self.load_one_sound('src/sounds/cancel.mp3')
        self.load_one_sound('src/sounds/ok.mp3')
        self.load_one_sound('src/sounds/back_btn.mp3')
        self.load_one_sound('src/sounds/sound.mp3')
        self.load_one_sound('src/sounds/set.mp3')
        self.load_one_sound('src/sounds/set2.mp3')
        self.load_one_sound('src/sounds/plr_win_game.mp3')
        self.load_one_sound('src/sounds/plr_win_game2.mp3')
        self.load_one_sound('src/sounds/comp_win_game.mp3')
        self.load_one_sound('src/sounds/comp_win_game2.mp3')

    def load_one_sound(self, path):
        try:
            sound = SoundLoader.load(path)
            self.sounds.append(sound)
        except:
            Snackbar(text='Ошибка некоторых звуков').show()

    def play_sound(self, sound):
        try:
            if sound == 'deal':
                self.sounds[random.randint(0, 2)].play()
            elif sound == 'showdown':
                self.sounds[3].play()
            elif sound == 'plr_all_in':
                self.sounds[4].play()
            elif sound == 'plr_win':
                self.sounds[5].play()
            elif sound == 'draw':
                self.sounds[6].play()
            elif sound == 'fold':
                self.sounds[7].play()
            elif sound == 'comp_win':
                self.sounds[8].play()
            elif sound == 'bet+':
                self.sounds[9].play()
            elif sound == 'bet-':
                self.sounds[10].play()
            elif sound == 'comp_all_in':
                self.sounds[11].play()
            elif sound == 'raise':
                self.sounds[12].play()
            elif sound == 'call':
                self.sounds[13].play()
            elif sound == 'bet_voice':
                self.sounds[14].play()
            elif sound == 'call_voice':
                self.sounds[15].play()
            elif sound == 'click':
                self.sounds[16].play()
            elif sound == 'start':
                self.sounds[17].play()
            elif sound == 'slide':
                self.sounds[18].play()
            elif sound == 'back':
                self.sounds[19].play()
            elif sound == 'cancel':
                self.sounds[20].play()
            elif sound == 'ok':
                self.sounds[21].play()
            elif sound == 'back_btn':
                self.sounds[22].play()
            elif sound == 'sound':
                self.sounds[23].play()
            elif sound == 'set':
                self.sounds[24].play()
            elif sound == 'set2':
                self.sounds[25].play()
            elif sound == 'plr_win_game':
                self.sounds[random.randint(26, 27)].play()
            elif sound == 'comp_win_game':
                self.sounds[random.randint(28,29)].play()
        except:
            print('error play sound')

    def play_music(self):
        try:
            if self.music is not None:
                self.music.volume = float(self.screen.ids.music_volume_value.text) / 100
                self.music.play()
        except:
            print('error play music')

    def set_sound_volume(self, value):
        try:
            for sound in self.sounds:
                sound.volume = float(value) / 100
        except:
            print('error set sound volume')

    def set_music_volume(self, value):
        try:
            self.music.volume = float(value) / 100
        except:
            print('error set music volume')

    def set_primary_palette(self, value):
        self.play_sound('set2')
        if value == 1:
            self.theme_cls.primary_palette = 'Red'
            self.screen.ids.lbl_primary_palette.text = 'Красный'
        elif value == 2:
            self.theme_cls.primary_palette = 'Pink'
            self.screen.ids.lbl_primary_palette.text = 'Розовый'
        elif value == 3:
            self.theme_cls.primary_palette = 'Purple'
            self.screen.ids.lbl_primary_palette.text = 'Фиолетовый'
        elif value == 4:
            self.theme_cls.primary_palette = 'DeepPurple'
            self.screen.ids.lbl_primary_palette.text = 'Темно-фиолетовый'
        elif value == 5:
            self.theme_cls.primary_palette = 'Indigo'
            self.screen.ids.lbl_primary_palette.text = 'Индиго'
        elif value == 6:
            self.theme_cls.primary_palette = 'Blue'
            self.screen.ids.lbl_primary_palette.text = 'Синий'
        elif value == 7:
            self.theme_cls.primary_palette = 'LightBlue'
            self.screen.ids.lbl_primary_palette.text = 'Светло-синий'
        elif value == 8:
            self.theme_cls.primary_palette = 'Cyan'
            self.screen.ids.lbl_primary_palette.text = 'Голубой'
        elif value == 9:
            self.theme_cls.primary_palette = 'Teal'
            self.screen.ids.lbl_primary_palette.text = 'Бирюзовый'
        elif value == 10:
            self.theme_cls.primary_palette = 'Green'
            self.screen.ids.lbl_primary_palette.text = 'Зеленый'
        elif value == 1:
            self.theme_cls.primary_palette = 'LightGreen'
            self.screen.ids.lbl_primary_palette.text = 'Светло-зеленый'
        elif value == 12:
            self.theme_cls.primary_palette = 'Yellow'
            self.screen.ids.lbl_primary_palette.text = 'Желтый'
        elif value == 13:
            self.theme_cls.primary_palette = 'Amber'
            self.screen.ids.lbl_primary_palette.text = 'Янтарный'
        elif value == 14:
            self.theme_cls.primary_palette = 'Orange'
            self.screen.ids.lbl_primary_palette.text = 'Оранжевый'
        elif value == 15:
            self.theme_cls.primary_palette = 'DeepOrange'
            self.screen.ids.lbl_primary_palette.text = 'Темно-оранжевый'
        elif value == 16:
            self.theme_cls.primary_palette = 'Brown'
            self.screen.ids.lbl_primary_palette.text = 'Коричневый'
        elif value == 17:
            self.theme_cls.primary_palette = 'Gray'
            self.screen.ids.lbl_primary_palette.text = 'Серый'
        elif value == 18:
            self.theme_cls.primary_palette = 'BlueGray'
            self.screen.ids.lbl_primary_palette.text = 'Серо-голубой'

    def set_primary_hue(self, value):
        self.play_sound('set2')
        if value == 1:
            self.theme_cls.primary_hue = '50'
            self.screen.ids.lbl_primary_hue.text = '50'
        elif value == 2:
            self.theme_cls.primary_hue = '100'
            self.screen.ids.lbl_primary_hue.text = '100'
        elif value == 3:
            self.theme_cls.primary_hue = 'A100'
            self.screen.ids.lbl_primary_hue.text = 'A100'
        elif value == 4:
            self.theme_cls.primary_hue = '200'
            self.screen.ids.lbl_primary_hue.text = '200'
        elif value == 5:
            self.theme_cls.primary_hue = 'A200'
            self.screen.ids.lbl_primary_hue.text = 'A200'
        elif value == 6:
            self.theme_cls.primary_hue = '300'
            self.screen.ids.lbl_primary_hue.text = '300'
        elif value == 7:
            self.theme_cls.primary_hue = '400'
            self.screen.ids.lbl_primary_hue.text = '400'
        elif value == 8:
            self.theme_cls.primary_hue = 'A400'
            self.screen.ids.lbl_primary_hue.text = 'A400'
        elif value == 9:
            self.theme_cls.primary_hue = '500'
            self.screen.ids.lbl_primary_hue.text = '500'
        elif value == 10:
            self.theme_cls.primary_hue = '600'
            self.screen.ids.lbl_primary_hue.text = '600'
        elif value == 11:
            self.theme_cls.primary_hue = '700'
            self.screen.ids.lbl_primary_hue.text = '700'
        elif value == 12:
            self.theme_cls.primary_hue = '800'
            self.screen.ids.lbl_primary_hue.text = '800'
        elif value == 13:
            self.theme_cls.primary_hue = '900'
            self.screen.ids.lbl_primary_hue.text = '900'

    def set_screen(self, screen):
        if self.is_game:
            self.screen.ids.continue_btn.disabled = False
        else:
            self.screen.ids.continue_btn.disabled = True
        if not self.screen.ids.scrm.current == 'scr_combinations' \
                and not self.screen.ids.scrm.current == screen:
            self.play_sound('slide')
            self.back = self.screen.ids.scrm.current
        else:
            self.back = 'scr_help'
        self.play_sound('slide')
        self.screen.ids.scrm.current = screen

    def to_back_screen(self):
        if self.back == self.screen.ids.scrm.current:
            self.play_sound('back')
            if self.is_game:
                self.screen.ids.scrm.current = 'scr_game'
            else:
                self.screen.ids.scrm.current = 'scr_main'
            return

        if not self.back == '':
            self.play_sound('back')
            self.screen.ids.scrm.current = self.back

    def start_new_game(self):
        self.play_sound('start')
        self.players.clear()
        self.table.clear()
        self.screen.ids.plr_info.text = ''
        self.screen.ids.comp_info.text = ''
        player = Player(0, 1000, False, True)
        self.players.append(player)
        comp = Player(1, 1000, True, True)
        self.players.append(comp)
        self.bank = 0
        self.update_players_money()
        self.update_bank()
        if self.is_deal_to_table:
            self.is_deal_to_table = False
            Clock.unschedule(self.deal_card_to_table)
        if self.is_deal_to_players:
            self.is_deal_to_players = False
            Clock.unschedule(self.deal_card_to_players)
        self.is_game = True
        self.screen.ids.next_game_btn.text = 'Дальше'
        self.screen.ids.call_btn.disabled = True
        self.screen.ids.raise_btn.disabled = True
        self.screen.ids.fold_btn.disabled = True
        self.set_screen('scr_game')
        self.round = -1
        self.start_game()

    def start_game(self):
        if not self.is_game:
            self.start_new_game()
            return
        self.screen.ids.table.clear_widgets()
        self.screen.ids.table.add_widget(self.get_shirt())
        if self.players[0].money == 0:
            self.play_sound('comp_win_game')
            self.result = 'К сожалению у вас не осталось денег. Вы всё проиграли.'
            self.result_2 = 'GAME OVER'
            self.resultImage = 'imgs/img_lose.png'
            self.custom_sheet = MDCustomBottomSheet(
                radius_from='top',
                screen=Factory.ResultCustomSheet(),
                animation=True)
            self.custom_sheet.open()
            self.clear_cards()
            self.screen.ids.comp_info.text = ''
            self.screen.ids.comp_money_lbl.text = ''
            self.screen.ids.plr_info.text = ''
            self.screen.ids.plr_money_lbl.text = ''
            self.screen.ids.bank_lbl.text = ''
            self.is_game = False
            self.screen.ids.next_game_btn.text = 'Новая игра'
            return
        elif self.players[1].money == 0:
            self.play_sound('plr_win_game')
            self.result = 'У соперника не осталось денег. Соперник проиграл.'
            self.result_2 = 'Поздравляем!'
            self.resultImage = 'imgs/img_win.jpg'
            self.custom_sheet = MDCustomBottomSheet(
                radius_from='top',
                screen=Factory.ResultCustomSheet(),
                animation=True)
            self.custom_sheet.open()
            self.clear_cards()
            self.screen.ids.comp_info.text = ''
            self.screen.ids.comp_money_lbl.text = ''
            self.screen.ids.plr_info.text = ''
            self.screen.ids.plr_money_lbl.text = ''
            self.screen.ids.bank_lbl.text = ''
            self.is_game = False
            self.screen.ids.next_game_btn.text = 'Новая игра'
            return

        self.screen.ids.next_round_btn.text = 'Внести ставку'
        for player in self.players:
            player.all_in = False
        self.clear_cards()
        self.screen.ids.table.add_widget(self.get_shirt())
        self.screen.ids.next_game_btn.disabled = True
        self.screen.ids.round_lbl.text = rounds[self.round]
        self.init_deck()
        self.round = -1
        self.bank = 0
        self.update_bank()
        self.update_players_money()
        self.screen.ids.plr_info.text = ''
        self.screen.ids.comp_info.text = ''
        self.start_round()

    def start_round(self):
        if self.round == -1:
            self.screen.ids.round_lbl.text = 'Раздача карт'
            self.screen.ids.next_round_btn.disabled = False
            return
        else:
            self.screen.ids.round_lbl.text = rounds[self.round]
        self.update_bank()
        self.screen.ids.next_round_btn.disabled = True
        self.screen.ids.comp_info.text = ''
        self.screen.ids.plr_info.text = ''
        for player in self.players:
            player.call = False
            player.raised = False
            player.bet = 0
        if self.round == 0:
            self.deal_cards()
            for player in self.players:
                '''if player.money < 50:
                    bank += player.money
                    player.money = 0
                else:
                    bank += 50
                    player.money -= 50
                self.bank = bank'''
                player.winner = False
                player.bluff = False

            #self.update_players_money()
            #self.update_bank()
        elif self.round == 1:
            self.deal_to_table(3)
        else:
            self.deal_to_table(1)

    def end_round(self):
        if self.round == -1:
            self.round += 1
            self.play_sound('bet_voice')
            self.screen.ids.next_round_btn.text = 'Раздать карты'
            self.screen.ids.next_round_btn.disabled = True
            if self.players[0].money < 50:
                self.bank += self.players[0].money
                self.players[0].money = 0
                self.players[0].all_in = True
            else:
                self.players[0].money -= 50
                self.bank += 50
            self.screen.ids.plr_info.text = 'Вы вносите ставку'
            self.update_bank()
            self.update_players_money()
            Clock.schedule_once(self.comp_place_bet, self.comp_delay)
            #self.start_round()
        elif self.round == 3:
            self.screen.ids.next_round_btn.text = 'Следующий раунд'
            self.showdown()
        else:
            if not self.screen.ids.next_round_btn.text == 'Раздать карты':
                self.round += 1
            self.screen.ids.next_round_btn.text = 'Следующий раунд'
            self.start_round()

    def player_turn(self):
        if not self.players[1].all_in \
                and not self.players[0].all_in \
                and not self.players[0].money == 0 \
                and not self.players[1].money == 0:
            self.screen.ids.raise_btn.disabled = False
        self.screen.ids.call_btn.disabled = False
        self.screen.ids.fold_btn.disabled = False
        self.screen.ids.plr_info.text = 'Ваш ход'



    def get_card_from_deck(self):
        index = random.randint(0, len(self.deck) - 1)
        card = self.deck[index]
        self.deck.pop(index)
        return card

    def plr_call(self):
        self.screen.ids.call_btn.disabled = True
        self.screen.ids.raise_btn.disabled = True
        self.screen.ids.fold_btn.disabled = True
        self.players[0].call = True
        self.screen.ids.plr_info.text = 'Вы принимаете ставку'
        if self.players[1].raised:
            self.play_sound('raise')
            comp_bet = self.players[1].bet
            if comp_bet > self.players[0].money:
                self.bank += self.players[0].money
                self.players[0].money = 0
            else:
                self.players[0].money -= comp_bet
                self.bank += comp_bet

            self.update_players_money()
            self.update_bank()
            self.screen.ids.next_round_btn.disabled = False
            self.screen.ids.plr_info.text = 'Вы принимаете ставку компа'
            if self.players[0].money == 0:
                self.players[0].all_in = True
                self.screen.ids.plr_info.text += ' (Ва-Банк)'
            if self.round == 3:
                self.screen.ids.next_round_btn.text = 'Вскрыть карты'
        else:
            self.play_sound('call_voice')
            Clock.schedule_once(self.comp_action, self.comp_delay)

    def plr_raise(self):
        self.custom_sheet = MDCustomBottomSheet(
            radius_from='top',
            screen=Factory.BidCustomSheet(),
            animation=True)
        self.custom_sheet.open()

    def plr_raised(self, bet):
        if bet == 0:
            return
        self.screen.ids.plr_info.text = f'вы подняли на {bet} $'
        self.players[0].set_bet(bet)
        self.players[0].raised = True
        self.players[0].money = self.players[0].money - bet - self.players[1].bet
        self.bank = self.bank + bet + self.players[1].bet
        self.update_bank()
        self.update_players_money()
        self.screen.ids.call_btn.disabled = True
        self.screen.ids.raise_btn.disabled = True
        self.screen.ids.fold_btn.disabled = True
        Clock.schedule_once(self.comp_action, self.comp_delay)

    def plr_fold(self):
        self.play_sound('fold')
        self.players[1].money += self.bank
        self.screen.ids.plr_info.text = 'Вы сбрасываете карты (Пас)'
        self.screen.ids.next_game_btn.disabled = False
        self.screen.ids.call_btn.disabled = True
        self.screen.ids.raise_btn.disabled = True
        self.screen.ids.fold_btn.disabled = True
        #self.start_new_game()

    def comp_action(self, dt):
        comp_cards = []
        for card in self.table:
            comp_cards.append(card)
        for card in self.comp_hand:
            comp_cards.append(card)
        comp_combination = deck.get_combination(comp_cards)

        if self.players[1].all_in or self.players[0].all_in or self.players[0].money == 0:
            self.comp_call()
        elif self.players[0].call:
            if comp_combination.comb_power >= 3 and random.randint(1, 2) == 1:
                self.comp_raise(comp_combination)
            elif random.randint(1, 3) == 2 and self.players[1].bluff:
                self.comp_raise(comp_combination)
            elif random.randint(1, 5) == 2:
                self.players[1].bluff = True
                self.comp_raise(comp_combination)
            else:
                self.comp_call()
        elif self.players[0].raised:
            if self.players[0].all_in:
                if comp_combination.comb_power >= 5 or self.players[1].bluff:
                    self.comp_call()
                elif random.randint(1, 6) == 3:
                    self.comp_call()
                else:
                    self.comp_fold()
            elif self.players[0].bet > 100:
                if self.round == 0:
                    if comp_combination.comb_power < 2 and random.randint(1, 5) == 2:
                        self.players[1].bluff = True
                    if comp_combination.comb_power == 2 or self.players[1].bluff:
                        self.comp_raise(comp_combination)
                    elif random.randint(1, 2) == 2:
                        self.comp_call()
                    else:
                        self.comp_fold()
                else:
                    if self.players[1].bluff:
                        if random.randint(1, 2) == 2:
                            self.comp_raise(comp_combination)
                        else:
                            self.comp_call()
                    else:
                        if comp_combination.comb_power >= 4:
                            self.comp_call()
                        elif comp_combination.comb_power >= 5:
                            self.comp_raise(comp_combination)
                        elif random.randint(1, 2) == 2:
                            self.comp_call()
                        else:
                            self.comp_fold()
            else:
                if comp_combination.comb_power >= 4 and random.randint(1, 3) == 2:
                    self.comp_raise(comp_combination)
                elif comp_combination.comb_power >= 5:
                    if random.randint(1,3) == 2:
                        self.comp_call()
                    else:
                        self.comp_raise(comp_combination)
                elif comp_combination.comb_power < 4:
                    if random.randint(1, 3) == 2:
                        self.comp_fold()
                    else:
                        self.comp_call()
                else:
                    self.comp_fold()

    def comp_call(self):
        bet = self.players[0].bet
        if bet == 0:
            self.play_sound('call_voice')
            self.players[1].call = True
            self.screen.ids.comp_info.text = 'Комп принимает ставку'
        elif bet > self.players[1].money:
            self.players[1].set_bet(self.players[1].money)
            self.bank += self.players[1].money
            self.players[1].money = 0
            self.players[1].all_in = True
            self.play_sound('comp_all_in')
            self.screen.ids.comp_info.text = 'Комп Ва-банк'
        else:
            self.players[1].set_bet(bet)
            self.players[1].money = self.players[1].money - bet
            self.bank += bet
            if self.players[1].money == 0:
                self.players[1].all_in = True
            self.play_sound('call')
            self.screen.ids.comp_info.text = 'Комп уравнивает ставку'

        self.update_bank()
        self.update_players_money()
        self.screen.ids.next_round_btn.disabled = False
        if self.round == 3:
            self.screen.ids.next_round_btn.text = 'Вскрыть карты'

    def comp_raise(self, comp_combination):
        comp_bet = self.players[0].bet
        if self.players[0].bet > self.players[1].money:
            self.comp_call()
            return
        elif self.players[0].all_in:
            self.comp_call()
            return
        elif self.players[1].money == 0:
            self.comp_call()
            return

        self.players[1].money -= comp_bet
        self.bank += comp_bet

        '''money = int(self.players[1].money / 100)
        if money < 10:
            money *= 10'''

        money = int(self.players[1].money / 10)

        if comp_combination.comb_power >= 7:
            if random.randint(1, 3) == 2:
                raise_on = self.players[1].money - comp_bet
                self.players[1].all_in = True
            else:
                raise_on = random.randint(1, money)
                if not money == 1:
                    raise_on *= 10
        elif self.players[1].bluff:
            if random.randint(1, 4) == 2:
                raise_on = self.players[1].money - comp_bet
                self.players[1].all_in = True
            else:
                raise_on = random.randint(1, money)
                if not money == 1:
                    raise_on *= 10
        else:
            raise_on = random.randint(1, money)
            if not money == 1:
                raise_on *= 10

        self.players[1].set_bet(raise_on)
        self.players[1].raised = True
        self.players[1].money = self.players[1].money - raise_on
        self.bank += raise_on
        self.update_bank()
        self.update_players_money()
        '''self.screen.ids.call_btn.disabled = False
        self.screen.ids.raise_btn.disabled = False
        self.screen.ids.fold_btn.disabled = False'''
        if self.players[1].money == 0:
            self.players[1].all_in = True
        if self.players[0].raised:
            self.play_sound('call')
            self.play_sound('raise')
            self.screen.ids.comp_info.text = f'Комп принимает вашу ставку и повышает ставку на {raise_on}$'
        else:
            if not self.players[1].all_in:
                self.play_sound('raise')
            self.screen.ids.comp_info.text = f'Комп повышает ставку на {raise_on}$'
        if (self.players[1].all_in):
            self.play_sound('comp_all_in')
            self.screen.ids.comp_info.text += ' (Ва-банк)'
        self.player_turn()

    def comp_fold(self):
        self.play_sound('fold')
        self.screen.ids.comp_info.text = 'Комп сбрасывает карты (Пас)'
        self.players[0].money += self.bank
        self.screen.ids.next_game_btn.disabled = False

    def comp_place_bet(self, dt):
        if self.players[1].money < 50:
            self.bank += self.players[0].money
            self.players[1].money = 0
            self.players[1].all_in = True
        else:
            self.players[1].money -= 50
            self.bank += 50
        self.play_sound('call')
        self.update_bank()
        self.update_players_money()
        self.screen.ids.comp_info.text = 'Комп вносит ставку'
        self.screen.ids.next_round_btn.disabled = False
        #self.start_round()

    def showdown(self):
        self.play_sound('showdown')
        self.round += 1
        self.screen.ids.round_lbl.text = rounds[self.round]
        self.screen.ids.comp_hand.clear_widgets()
        for card in self.comp_hand:
            self.screen.ids.comp_hand.add_widget(card.get_image())
        self.screen.ids.next_game_btn.disabled = False
        self.screen.ids.next_round_btn.disabled = True
        player_cards = []
        comp_cards = []
        for card in self.table:
            player_cards.append(card)
            comp_cards.append(card)
        for card in self.player_hand:
            player_cards.append(card)
        for card in self.comp_hand:
            comp_cards.append(card)

        self.players[0].set_combination(deck.get_combination(player_cards))
        self.players[1].set_combination(deck.get_combination(comp_cards))
        comp_comb = self.players[1].get_combination()
        player_comb = self.players[0].get_combination()
        combinations_txt = ''
        self.screen.ids.plr_info.text = f'У вас комбинация: {player_comb.name}\n'
        self.screen.ids.comp_info.text = f'У компа комбинация: {comp_comb.name}'

        if comp_comb.comb_power > player_comb.comb_power:
            winner_text = 'Компьютер победил!'
            self.play_sound('comp_win')
            winner = 1
            winner_comb = comp_comb.hand
        elif comp_comb.comb_power < player_comb.comb_power:
            winner_text = 'Вы победили!'
            self.play_sound('plr_win')
            winner = 0
            winner_comb = player_comb.hand
        else:
            if comp_comb.power > player_comb.power:
                winner = 1
                winner_comb = comp_comb.hand
                winner_text = 'Компьютер победил!'
                self.play_sound('comp_win')
                combinations_txt = 'У компьютера старшая карта комбинации сильнее\n'
            elif comp_comb.power < player_comb.power:
                winner = 0
                winner_comb = player_comb.hand
                winner_text = 'Вы победили!'
                self.play_sound('plr_win')
                combinations_txt = 'У вас старшая карта комбинации сильнее\n'
            else:
                self.player_hand.sort(key=lambda x: x.rank, reverse=True)
                self.comp_hand.sort(key=lambda x: x.rank, reverse=True)
                if self.comp_hand[0].rank > self.player_hand[0].rank:
                    winner = 1
                    winner_comb = comp_comb.hand
                    winner_comb.append(self.comp_hand[0])
                    winner_text = 'Компьютер победил!'
                    self.play_sound('comp_win')
                    combinations_txt = 'Комбинации равны, но у компьютера лучше карты на руке'
                elif self.comp_hand[0].rank < self.player_hand[0].rank:
                    winner = 0
                    winner_comb = player_comb.hand
                    winner_comb.append(self.player_hand[0])
                    winner_text = 'Вы победили!'
                    self.play_sound('plr_win')
                    combinations_txt = 'Комбинации равны, но у вас лучше карты на руке'
                else:
                    winner = -1
                    winner_text = 'Ничья!'
                    self.play_sound('draw')
                    winner_comb = [self.player_hand[0], self.comp_hand[0]]

        self.screen.ids.round_lbl.text = winner_text
        self.screen.ids.plr_info.text += combinations_txt
        if winner == -1:
            for player in self.players:
                player.money += int(self.bank/2)
        else:
            self.players[winner].money += self.bank
        card_widgets = []
        for widget in self.screen.ids.comp_hand.children:
            card_widgets.append(widget)
        for widget in self.screen.ids.player_hand.children:
            card_widgets.append(widget)
        for widget in self.screen.ids.table.children:
            card_widgets.append(widget)

        if len(winner_comb) == 0:
            return

        for widget in card_widgets:
            in_win_comb = False
            for card in winner_comb:
                if widget.source == card.image:
                    in_win_comb = True
            if in_win_comb:
                continue
            widget.opacity = self.opacity

    def set_plr_bet(self, bet, plr_money, bet_lbl):
        print('set plr bet')
        money = int(plr_money.text)
        plr_bet = int(bet_lbl.text)

        money = money - bet
        plr_bet = plr_bet + bet

        if money < 0 or plr_bet < 0:
            return

        if bet < 0:
            self.play_sound('bet-')
        elif bet > 0:
            self.play_sound('bet+')
        plr_money.text = f'{money}'
        bet_lbl.text = f'{plr_bet}'
        if money == 0:
            self.play_sound('plr_all_in')
            self.players[0].all_in = True
            #self.plr_raised(plr_bet)

    def init_deck(self):
        self.deck.clear()
        for card in deck.get_deck(self.settings.deck_kind):
            self.deck.append(card)

    def init_help(self):
        try:
            file = open('src/rules.txt', 'r')
            for line in file:
                #self.screen.ids.rules_lbl.text += line
                self.screen.ids.help_lbl.text += line
            file.close()
        except:
            Snackbar(text='Ошибка чтения файла').show()

    def deal_cards(self):
        for i in range(2):
            self.player_hand.append(self.get_card_from_deck())
            self.comp_hand.append(self.get_card_from_deck())
        self.deal_to_players()

    def deal_to_table(self, quantity):
        self.is_deal_to_table = True
        if quantity == 1:
            self.deal_cards_count = -1
            Clock.schedule_once(self.deal_card_to_table, self.deal_delay)
        elif quantity == 3:
            self.deal_cards_count = 0
            Clock.schedule_interval(self.deal_card_to_table, self.deal_delay)

    def deal_to_players(self):
        self.is_deal_to_players = True
        self.deal_cards_count = 0
        Clock.schedule_interval(self.deal_card_to_players, self.deal_delay)

    def deal_card_to_table(self, dt):
        if self.deal_cards_count < 3:
            self.play_sound('deal')
            card = self.get_card_from_deck()
            self.table.append(card)
            self.screen.ids.table.add_widget(card.get_image())
            self.deal_cards_count += 1
            if self.deal_cards_count == 0:
                self.player_turn()
        else:
            self.is_deal_to_table = False
            Clock.unschedule(self.deal_card_to_table)
            self.player_turn()

    def deal_card_to_players(self, dt):
        if self.deal_cards_count < 4:
            self.play_sound('deal')
            if self.deal_cards_count < 2:
                if self.deal_cards_count % 2 == 0:
                    self.screen.ids.player_hand.add_widget(self.player_hand[0].get_image())
                else:
                    self.screen.ids.comp_hand.add_widget(self.get_shirt())
            else:
                if self.deal_cards_count % 2 == 0:
                    self.screen.ids.player_hand.add_widget(self.player_hand[1].get_image())
                else:
                    self.screen.ids.comp_hand.add_widget(self.get_shirt())
            self.deal_cards_count += 1
        else:
            self.is_deal_to_players = False
            Clock.unschedule(self.deal_card_to_players)
            self.player_turn()

    def update_bank(self):
        self.screen.ids.bank_lbl.text = f'{self.bank} $'

    def update_players_money(self):
        self.screen.ids.plr_money_lbl.text = str(self.players[0].money)
        self.screen.ids.comp_money_lbl.text = str(self.players[1].money)

    def clear_cards(self):
        self.player_hand.clear()
        self.comp_hand.clear()
        self.table.clear()
        self.screen.ids.table.clear_widgets()
        self.screen.ids.player_hand.clear_widgets()
        self.screen.ids.comp_hand.clear_widgets()

    def get_shirt(self):
        return deck.get_shirt(self.settings.shirt_kind)


MyPokerApp().run()
