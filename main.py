#!/usr/bin/env python3
"""
Numberblocks 数字积木 - 大号动态版
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.animation import Animation
import random
import os

Window.size = (400, 750)

# 字体
FONT = 'Roboto'
for f in ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf']:
    if os.path.exists(f):
        try:
            LabelBase.register(name='CN', fn_regular=f)
            FONT = 'CN'
            break
        except:
            pass

# Numberblocks 颜色 (更鲜艳)
COLORS = {
    1: (0.9, 0.15, 0.15, 1),    # 红
    2: (1, 0.55, 0.1, 1),       # 橙
    3: (1, 0.9, 0.1, 1),        # 黄
    4: (0.2, 0.8, 0.3, 1),      # 绿
    5: (0.15, 0.5, 0.9, 1),     # 蓝
    6: (0.6, 0.3, 0.8, 1),      # 紫
    7: (0.95, 0.4, 0.6, 1),     # 粉
    8: (0.9, 0.4, 0.5, 1),      # 玫红
    9: (0.5, 0.5, 0.55, 1),     # 灰
    10: (0.95, 0.95, 0.95, 1),  # 白
}

NAMES_CN = {1:'一', 2:'二', 3:'三', 4:'四', 5:'五', 6:'六', 7:'七', 8:'八', 9:'九', 10:'十'}
NAMES_EN = {1:'One', 2:'Two', 3:'Three', 4:'Four', 5:'Five', 6:'Six', 7:'Seven', 8:'Eight', 9:'Nine', 10:'Ten'}


class CuteBlock(Widget):
    """可爱的Numberblocks积木"""
    
    def __init__(self, number=1, size=(100, 120), **kwargs):
        super().__init__(**kwargs)
        self.number = number
        self.base_size = size
        self.size_hint = (None, None)
        self.size = size
        self.color = COLORS.get(number, (1,1,1,1))
        self.anim_offset = random.random() * 3.14  # 随机动画偏移
        self.bounce_anim = None
        self.bind(pos=self.draw, size=self.draw)
        self.start_animation()
    
    def start_animation(self):
        """开始弹跳动画"""
        def bounce(dt):
            if self.parent:
                import math
                t = Clock.get_time() + self.anim_offset
                offset = math.sin(t * 2) * 5  # 上下弹跳
                self.y = self.y + offset * 0.1
                self.draw()
        Clock.schedule_interval(bounce, 1/30)
    
    def draw(self, *args):
        self.canvas.clear()
        
        bx, by = self.pos
        bw, bh = self.size
        cx = bx + bw / 2
        
        with self.canvas:
            # 阴影
            Color(0, 0, 0, 0.2)
            Ellipse(pos=(bx + 5, by - 5), size=(bw - 10, 15))
            
            # 主体 - 根据数字画不同形状
            Color(*self.color)
            
            if self.number == 1:
                # 1: 圆形
                Ellipse(pos=(bx + 10, by + 10), size=(bw - 20, bh - 30))
            elif self.number == 2:
                # 2: 两个方块横排
                w = (bw - 25) / 2
                RoundedRectangle(pos=(bx + 5, by + 15), size=(w, bh - 35), radius=[12])
                RoundedRectangle(pos=(bx + w + 15, by + 15), size=(w, bh - 35), radius=[12])
            elif self.number == 3:
                # 3: 三个竖排
                h = (bh - 45) / 3
                for i in range(3):
                    RoundedRectangle(pos=(bx + 15, by + 15 + i * (h + 5)), size=(bw - 30, h), radius=[8])
            elif self.number == 4:
                # 4: 2x2
                s = (min(bw, bh) - 40) / 2
                for r in range(2):
                    for c in range(2):
                        RoundedRectangle(pos=(bx + 8 + c * (s + 6), by + 15 + r * (s + 6)), size=(s, s), radius=[10])
            elif self.number == 5:
                # 5: 5个方块十字形
                s = (min(bw, bh) - 50) / 3
                # 中间
                RoundedRectangle(pos=(bx + s + 15, by + s + 15), size=(s, s), radius=[8])
                # 四周
                RoundedRectangle(pos=(bx + s + 15, by + 2*s + 22), size=(s, s), radius=[8])  # 上
                RoundedRectangle(pos=(bx + s + 15, by + 8), size=(s, s), radius=[8])  # 下
                RoundedRectangle(pos=(bx + 8, by + s + 15), size=(s, s), radius=[8])  # 左
                RoundedRectangle(pos=(bx + 2*s + 22, by + s + 15), size=(s, s), radius=[8])  # 右
            else:
                # 6-10: 方块组合
                s = 25
                cols = min(self.number, 4)
                rows = (self.number + cols - 1) // cols
                for r in range(rows):
                    for c in range(cols):
                        idx = r * cols + c
                        if idx < self.number:
                            x = bx + 12 + c * (s + 6)
                            y = by + bh - 40 - r * (s + 6)
                            RoundedRectangle(pos=(x, y), size=(s, s), radius=[6])
            
            # 眼睛 (白色椭圆)
            Color(1, 1, 1, 1)
            eye_size = 22
            eye_y = by + bh * 0.65
            Ellipse(pos=(cx - 30, eye_y), size=(eye_size, eye_size + 4))
            Ellipse(pos=(cx + 10, eye_y), size=(eye_size, eye_size + 4))
            
            # 眼珠 (黑色圆)
            Color(0.1, 0.1, 0.1, 1)
            pupil_size = 12
            Ellipse(pos=(cx - 24, eye_y + 5), size=(pupil_size, pupil_size))
            Ellipse(pos=(cx + 16, eye_y + 5), size=(pupil_size, pupil_size))
            
            # 高光 (白色小圆)
            Color(1, 1, 1, 1)
            hl_size = 5
            Ellipse(pos=(cx - 21, eye_y + 10), size=(hl_size, hl_size))
            Ellipse(pos=(cx + 19, eye_y + 10), size=(hl_size, hl_size))
            
            # 嘴巴 (微笑曲线)
            Color(0.15, 0.1, 0.1, 1)
            mouth_y = by + bh * 0.35
            Line(points=[
                cx - 18, mouth_y + 8,
                cx - 8, mouth_y,
                cx, mouth_y + 3,
                cx + 8, mouth_y,
                cx + 18, mouth_y + 8
            ], width=3)
            
            # 腮红 (粉色椭圆)
            Color(1, 0.6, 0.6, 0.4)
            Ellipse(pos=(cx - 45, eye_y - 8), size=(15, 10))
            Ellipse(pos=(cx + 32, eye_y - 8), size=(15, 10))
            
            # 数字 (在底部)
            Color(1, 1, 1, 0.9)


class Pet:
    def __init__(self):
        self.name = "小积木"
        self.level = 1
        self.exp = 0
        self.food = 5
        self.love = 50
        self.number = 1
    
    def exp_need(self):
        return self.level * 50
    
    def add_exp(self, n):
        self.exp += n
        while self.exp >= self.exp_need():
            self.exp -= self.exp_need()
            self.level += 1
            return True
        return False
    
    def add_love(self, n):
        self.love = min(100, self.love + n)


class GameApp(App):
    title = 'Numberblocks'
    
    def build(self):
        self.pet = Pet()
        self.root = FloatLayout()
        self.root.background_color = (0.15, 0.15, 0.25, 1)
        self.show_home()
        return self.root
    
    def clear(self):
        self.root.clear_widgets()
    
    def show_home(self):
        self.clear()
        
        main = BoxLayout(orientation='vertical', size_hint=(0.95, 0.95),
                        pos_hint={'center_x': 0.5, 'center_y': 0.5}, spacing=5)
        
        # 标题
        title = BoxLayout(size_hint=(1, 0.08))
        title.add_widget(Label(text='Numberblocks', font_name=FONT, font_size='32sp',
                              color=(1, 0.9, 0.3, 1), bold=True))
        main.add_widget(title)
        
        # 宠物显示
        pet_area = BoxLayout(size_hint=(1, 0.38))
        self.pet_block = CuteBlock(self.pet.number, size=(140, 160))
        pet_area.add_widget(self.pet_block)
        main.add_widget(pet_area)
        
        # 名字
        main.add_widget(Label(
            text=f'{NAMES_CN.get(self.pet.number,"")} ({self.pet.number})  Lv.{self.pet.level}',
            font_name=FONT, font_size='20sp', color=(1,1,1,1), size_hint=(1, 0.06)))
        
        # 状态条
        status = GridLayout(cols=2, size_hint=(1, 0.08), spacing=15)
        for label, value, color in [('经验', self.pet.exp/max(self.pet.exp_need(),1), (0.3,0.9,0.3,1)),
                                     ('好感', self.pet.love/100, (1,0.3,0.5,1))]:
            box = BoxLayout(orientation='vertical')
            box.add_widget(Label(text=label, font_name=FONT, font_size='12sp', color=(0.8,0.8,0.8,1), size_hint=(1,0.4)))
            bar = BoxLayout(size_hint=(1,0.6))
            bg = BoxLayout(size_hint=(1,1))
            bg.background_color = (0.2,0.2,0.25,1)
            fill = BoxLayout(size_hint=(value,1))
            fill.background_color = color
            bg.add_widget(fill)
            bar.add_widget(bg)
            box.add_widget(bar)
            status.add_widget(box)
        main.add_widget(status)
        
        # 食物
        main.add_widget(Label(text=f'食物: {self.pet.food}', font_name=FONT, font_size='18sp',
                             color=(1,0.8,0.3,1), size_hint=(1, 0.05)))
        
        # 按钮
        btns = GridLayout(cols=2, size_hint=(1, 0.3), spacing=12)
        for text, color, action in [
            ('认识数字', (0.2,0.5,1,1), self.show_learn),
            ('数积木', (0.3,0.8,0.3,1), self.show_game),
            ('进化变身', (0.9,0.5,0.1,1), self.show_evolve),
            ('数字朋友', (0.8,0.3,0.8,1), self.show_friends)
        ]:
            b = Button(text=text, font_name=FONT, font_size='22sp',
                      background_color=color, background_normal='', color=(1,1,1,1))
            b.bind(on_press=lambda x, a=action: a())
            btns.add_widget(b)
        main.add_widget(btns)
        
        self.root.add_widget(main)
    
    def show_learn(self):
        self.clear()
        main = BoxLayout(orientation='vertical', size_hint=(0.95, 0.95),
                        pos_hint={'center_x': 0.5, 'center_y': 0.5}, spacing=10)
        
        back = Button(text='← 返回', font_name=FONT, font_size='18sp', size_hint=(0.3, 0.06),
                     background_color=(0.5,0.5,0.5,1), background_normal='')
        back.bind(on_press=lambda x: self.show_home())
        main.add_widget(back)
        
        main.add_widget(Label(text='认识数字朋友', font_name=FONT, font_size='24sp',
                             color=(1,1,1,1), size_hint=(1, 0.06)))
        
        self.learn_area = BoxLayout(size_hint=(1, 0.45))
        main.add_widget(self.learn_area)
        
        self.learn_info = Label(text='', font_name=FONT, font_size='24sp',
                               color=(1,1,1,1), size_hint=(1, 0.08))
        main.add_widget(self.learn_info)
        
        grid = GridLayout(cols=5, size_hint=(1, 0.25), spacing=8)
        for i in range(1, 11):
            b = Button(text=str(i), font_name=FONT, font_size='24sp',
                      background_color=COLORS.get(i, (1,1,1,1)), background_normal='')
            b.bind(on_press=lambda x, n=i: self.show_num(n))
            grid.add_widget(b)
        main.add_widget(grid)
        
        self.root.add_widget(main)
        self.show_num(1)
    
    def show_num(self, n):
        self.learn_area.clear_widgets()
        block = CuteBlock(n, size=(180, 200))
        self.learn_area.add_widget(block)
        self.learn_info.text = f'{NAMES_CN.get(n,"")} - {NAMES_EN.get(n,"")}'
    
    def show_game(self):
        self.clear()
        main = BoxLayout(orientation='vertical', size_hint=(0.95, 0.95),
                        pos_hint={'center_x': 0.5, 'center_y': 0.5}, spacing=8)
        
        top = BoxLayout(size_hint=(1, 0.06))
        back = Button(text='←', font_name=FONT, font_size='18sp', size_hint=(0.15, 1),
                     background_color=(0.5,0.5,0.5,1), background_normal='')
        back.bind(on_press=lambda x: self.show_home())
        top.add_widget(back)
        top.add_widget(Label(text='数积木游戏', font_name=FONT, font_size='20sp', color=(1,1,1,1), size_hint=(0.6,1)))
        self.food_lbl = Label(text=f'🍖{self.pet.food}', font_name=FONT, font_size='18sp', color=(1,0.8,0.3,1), size_hint=(0.25,1))
        top.add_widget(self.food_lbl)
        main.add_widget(top)
        
        main.add_widget(Label(text='有几个积木朋友？', font_name=FONT, font_size='22sp',
                             color=(1,1,1,1), size_hint=(1, 0.06)))
        
        self.blocks_area = BoxLayout(size_hint=(1, 0.42))
        main.add_widget(self.blocks_area)
        
        self.opts_area = GridLayout(cols=3, size_hint=(1, 0.28), spacing=12)
        main.add_widget(self.opts_area)
        
        self.score_lbl = Label(text='答对: 0', font_name=FONT, font_size='16sp',
                              color=(1,1,0.5,1), size_hint=(1, 0.06))
        main.add_widget(self.score_lbl)
        
        self.root.add_widget(main)
        self.correct = 0
        self.new_q()
    
    def new_q(self):
        n = random.randint(1, 6)
        self.answer = n
        self.blocks_area.clear_widgets()
        
        # 显示积木
        grid = GridLayout(cols=min(n, 4), spacing=15, size_hint=(None, None))
        grid.width = min(n, 4) * 90 + (min(n, 4)-1) * 15
        grid.height = ((n + 3) // 4) * 100 + ((n + 3) // 4 - 1) * 15
        
        for i in range(n):
            grid.add_widget(CuteBlock(n, size=(80, 90)))
        
        wrapper = BoxLayout(size_hint=(1, 1))
        wrapper.add_widget(grid)
        self.blocks_area.add_widget(wrapper)
        
        # 选项
        self.opts_area.clear_widgets()
        opts = [n]
        while len(opts) < 3:
            o = random.randint(1, 6)
            if o not in opts:
                opts.append(o)
        random.shuffle(opts)
        
        for o in opts:
            b = Button(text=str(o), font_name=FONT, font_size='40sp',
                      background_color=COLORS.get(o, (0.5,0.5,0.5,1)), background_normal='')
            b.bind(on_press=lambda x, a=o: self.check(a))
            self.opts_area.add_widget(b)
    
    def check(self, ans):
        if ans == self.answer:
            self.correct += 1
            self.pet.food += 1
            self.pet.add_exp(10)
            self.score_lbl.text = f'答对: {self.correct}'
            self.food_lbl.text = f'🍖{self.pet.food}'
            
            p = Popup(title='太棒了！', 
                     content=Label(text=f'+1 食物！\n{NAMES_CN.get(self.answer,"")}个！', 
                                  font_name=FONT, font_size='20sp'),
                     size_hint=(0.7, 0.3))
            p.open()
            Clock.schedule_once(lambda dt: p.dismiss(), 0.8)
            Clock.schedule_once(lambda dt: self.new_q(), 1)
        else:
            p = Popup(title='再数数~', 
                     content=Label(text=f'答案是 {self.answer}', font_name=FONT, font_size='18sp'),
                     size_hint=(0.6, 0.3))
            p.open()
            Clock.schedule_once(lambda dt: p.dismiss(), 1)
            Clock.schedule_once(lambda dt: self.new_q(), 1.2)
    
    def show_evolve(self):
        self.clear()
        main = BoxLayout(orientation='vertical', size_hint=(0.95, 0.95),
                        pos_hint={'center_x': 0.5, 'center_y': 0.5}, spacing=10)
        
        back = Button(text='← 返回', font_name=FONT, font_size='18sp', size_hint=(0.3, 0.08),
                     background_color=(0.5,0.5,0.5,1), background_normal='')
        back.bind(on_press=lambda x: self.show_home())
        main.add_widget(back)
        
        main.add_widget(Label(text='选择你的数字！', font_name=FONT, font_size='28sp',
                             color=(1,1,0.8,1), size_hint=(1, 0.08)))
        
        cur = BoxLayout(size_hint=(1, 0.25))
        self.preview_block = CuteBlock(self.pet.number, size=(120, 140))
        cur.add_widget(self.preview_block)
        main.add_widget(cur)
        
        main.add_widget(Label(text=f'当前: {NAMES_CN.get(self.pet.number,"")} (Lv.{self.pet.level}可选1-{self.pet.level+1})',
                             font_name=FONT, font_size='16sp', color=(1,1,1,1), size_hint=(1,0.06)))
        
        grid = GridLayout(cols=5, size_hint=(1, 0.4), spacing=10)
        for i in range(1, 11):
            b = Button(text=str(i), font_name=FONT, font_size='28sp',
                      background_color=COLORS.get(i, (1,1,1,1)), background_normal='')
            b.bind(on_press=lambda x, n=i: self.do_evolve(n))
            grid.add_widget(b)
        main.add_widget(grid)
        
        self.root.add_widget(main)
    
    def do_evolve(self, n):
        if n <= self.pet.level + 1:
            self.pet.number = n
            p = Popup(title='进化成功！', 
                     content=Label(text=f'变成了 {NAMES_CN.get(n,"")}！', font_name=FONT, font_size='22sp'),
                     size_hint=(0.7, 0.3))
            p.open()
            Clock.schedule_once(lambda dt: p.dismiss(), 1.2)
            Clock.schedule_once(lambda dt: self.show_home(), 1.5)
        else:
            p = Popup(title='等级不够', 
                     content=Label(text=f'需要Lv.{n}，当前Lv.{self.pet.level}', font_name=FONT, font_size='16sp'),
                     size_hint=(0.6, 0.3))
            p.open()
            Clock.schedule_once(lambda dt: p.dismiss(), 1)
    
    def show_friends(self):
        self.clear()
        main = BoxLayout(orientation='vertical', size_hint=(0.95, 0.95),
                        pos_hint={'center_x': 0.5, 'center_y': 0.5}, spacing=8)
        
        back = Button(text='← 返回', font_name=FONT, font_size='18sp', size_hint=(0.3, 0.06),
                     background_color=(0.5,0.5,0.5,1), background_normal='')
        back.bind(on_press=lambda x: self.show_home())
        main.add_widget(back)
        
        main.add_widget(Label(text='数字朋友图鉴', font_name=FONT, font_size='28sp',
                             color=(1,0.9,0.3,1), size_hint=(1, 0.06)))
        
        scroll_content = GridLayout(cols=2, size_hint=(1, None), spacing=10)
        scroll_content.bind(minimum_height=scroll_content.setter('height'))
        
        for i in range(1, 11):
            box = BoxLayout(orientation='vertical', size_hint=(1, None), height=130, spacing=3)
            box.add_widget(CuteBlock(i, size=(100, 100)))
            box.add_widget(Label(text=f'{NAMES_CN.get(i,"")} {NAMES_EN.get(i,"")}',
                                font_name=FONT, font_size='14sp', color=(1,1,1,1), 
                                size_hint=(1, 0.3)))
            scroll_content.add_widget(box)
        
        main.add_widget(scroll_content)
        self.root.add_widget(main)


if __name__ == '__main__':
    GameApp().run()
