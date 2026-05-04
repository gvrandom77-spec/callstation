# -*- coding: utf-8 -*-
import os
import socket
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from android.broadcast import BroadcastReceiver

class StationClientApp(App):
    def build(self):
        self.icon = 'icon.png'
        self.config_path = os.path.join(self.user_data_dir, 'ip_config.txt')
        self.server_ip = self.load_ip()
        self.is_running = False

        # Контейнер для центрирования элементов на экране
        main_layout = AnchorLayout(anchor_x='center', anchor_y='center', padding=30)
        
        # Внутренний контейнер с твоими оригинальными отступами
        layout = BoxLayout(orientation='vertical', spacing=15, size_hint=(None, None), width=450, height=550)

        # Инструкция с автопереносом и зеленым словом ipconfig
        instruction = "Enter the computer's [b]IPv4 address[/b].\nYou can find the address using the [color=#006400]ipconfig[/color] command."
        self.lbl_instruction = Label(
            text=instruction, 
            markup=True, 
            halign='center', 
            valign='middle',
            font_size='20sp',
            size_hint_y=None,
            height=100
        )
        self.lbl_instruction.bind(size=lambda s, w: s.setter('text_size')(s, (w[0], None)))
        layout.add_widget(self.lbl_instruction)

        # Твое оригинальное поле ввода IP: высота 80, без halign='center' для нормального стирания
        self.ip_input = TextInput(
            text=self.server_ip, 
            multiline=False, 
            font_size='24sp', 
            size_hint_y=None, 
            height=80,
            padding=[15, 20, 15, 15]
        )
        layout.add_widget(self.ip_input)

        # Твоя оригинальная кнопка START: высота 100
        self.btn_toggle = Button(
            text='START MONITORING', 
            size_hint_y=None, 
            height=100, 
            background_color=get_color_from_hex('#2E7D32'), 
            background_normal=''
        )
        self.btn_toggle.bind(on_press=self.toggle_monitoring)
        layout.add_widget(self.btn_toggle)

        # Твоя оригинальная кнопка HIDE: высота 80
        btn_hide = Button(
            text='HIDE APPLICATION', 
            size_hint_y=None, 
            height=80, 
            background_color=get_color_from_hex('#455A64'), 
            background_normal=''
        )
        btn_hide.bind(on_press=self.hide_app)
        layout.add_widget(btn_hide)

        # Твой оригинальный статус
        self.status = Label(text='Status: Stopped', color=(0.7, 0.7, 0.7, 1), font_size='16sp')
        layout.add_widget(self.status)

        main_layout.add_widget(layout)
        return main_layout

    def load_ip(self):
        # Исправленный синтаксис твоего оригинального метода чтения
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    saved_ip = f.read().strip()
                    if saved_ip:
                        return saved_ip
        except Exception:
            pass
        return '172.56.21.89'

    def toggle_monitoring(self, instance):
        if not self.is_running:
            self.server_ip = self.ip_input.text.strip()
            try:
                with open(self.config_path, 'w') as f:
                    f.write(self.server_ip)
            except Exception:
                pass
            self.is_running = True
            self.btn_toggle.text = 'STOP MONITORING'
            self.btn_toggle.background_color = get_color_from_hex('#C62828')
            self.status.text = f'Monitoring calls (IP: {self.server_ip})'
            self.start_broadcast()
        else:
            self.is_running = False
            self.btn_toggle.text = 'START MONITORING'
            self.btn_toggle.background_color = get_color_from_hex('#2E7D32')
            self.status.text = 'Status: Stopped'
            self.stop_broadcast()

    def hide_app(self, instance):
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        PythonActivity.mActivity.moveTaskToBack(True)

    def start_broadcast(self):
        self.br = BroadcastReceiver(self.on_call_event, actions=['android.intent.action.PHONE_STATE'])
        self.br.start()

    def stop_broadcast(self):
        if hasattr(self, 'br'):
            self.br.stop()

    def on_call_event(self, context, intent):
        if not self.is_running:
            return
        state = intent.getStringExtra('state')
        number = intent.getStringExtra('incoming_number') or 'Unknown number'
        if state == 'RINGING':
            self.send_signal(f'InCall:{number}')

    def send_signal(self, message):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((self.server_ip, 5555))
            s.sendall(message.encode('utf-8'))
            s.close()
        except:
            pass

if __name__ == '__main__':
    StationClientApp().run()
