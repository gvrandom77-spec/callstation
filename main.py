# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
import socket
import os
from android.broadcast import BroadcastReceiver

class StationClientApp(App):
    def build(self):
        self.config_path = os.path.join(App().user_data_dir, 'ip_config.txt')
        
        # Загружаем сохраненный IP. Теперь метод возвращает только IP.
        self.server_ip = self.load_ip()
        self.is_running = False
        
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        # Инструкция строго в твоем оригинальном формате
        instruction = "Enter the computer's [b]IPv4 address[/b].\nYou can find the address using the [color=#33cc33]ipconfig[/color] command."
        layout.add_widget(Label(text=instruction, markup=True, halign='center', font_size='18sp'))
        
        # Поле ввода IP — твои оригинальные размеры
        self.ip_input = TextInput(text=self.server_ip, multiline=False, font_size='22sp', size_hint_y=None, height=80, halign='center')
        layout.add_widget(self.ip_input)
        
        # Кнопка запуска
        self.btn_toggle = Button(text='START MONITORING', size_hint_y=None, height=100, background_color=get_color_from_hex('#2E7D32'), background_normal='')
        self.btn_toggle.bind(on_press=self.toggle_monitoring)
        layout.add_widget(self.btn_toggle)
        
        # Кнопка скрытия
        btn_hide = Button(text='HIDE APPLICATION', size_hint_y=None, height=80, background_color=get_color_from_hex('#455A64'), background_normal='')
        btn_hide.bind(on_press=self.hide_app)
        layout.add_widget(btn_hide)
        
        # Статус
        self.status = Label(text='Status: Stopped', color=(0.7, 0.7, 0.7, 1))
        layout.add_widget(self.status)
        return layout

    def load_ip(self):
        # Метод читает сохраненный файл и возвращает только IP-адрес.
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    data = f.read().strip().split(',')
                    if data and data[0]:
                        return data[0]
        except Exception:
            pass
        return '172.56.21.89'

    def toggle_monitoring(self, instance):
        if not self.is_running:
            self.server_ip = self.ip_input.text.strip()
            self.is_running = True
            
            # Сохраняем IP и флаг "1" (активен)
            try:
                with open(self.config_path, 'w') as f:
                    f.write(f"{self.server_ip},1")
            except Exception:
                pass
                
            self.btn_toggle.text = 'STOP MONITORING'
            self.btn_toggle.background_color = get_color_from_hex('#C62828')
            self.status.text = f'Monitoring calls (IP: {self.server_ip})'
            self.start_broadcast()
        else:
            self.is_running = False
            self.server_ip = self.ip_input.text.strip()
            
            # Сохраняем IP и флаг "0" (остановлен)
            try:
                with open(self.config_path, 'w') as f:
                    f.write(f"{self.server_ip},0")
            except Exception:
                pass
                
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
        # При звонке СНАЧАЛА проверяем реальный статус из файла
        is_active = False
        saved_ip = self.server_ip
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    data = f.read().strip().split(',')
                    if len(data) > 1 and data[1] == '1':
                        is_active = True
                    if data and data[0]:
                        saved_ip = data[0]
        except Exception:
            pass

        # Если в файле записано, что мониторинг выключен — полная тишина
        if not is_active:
            return

        state = intent.getStringExtra('state')
        number = intent.getStringExtra('incoming_number') or 'Unknown number'
        if state == 'RINGING':
            # Отправляем только на тот IP, который сохранен в файле
            self.send_signal_to_ip(f'InCall:{number}', saved_ip)

    def send_signal_to_ip(self, message, ip_to_send):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip_to_send, 5555))
            s.sendall(message.encode('utf-8'))
            s.close()
        except:
            pass

if __name__ == '__main__':
    StationClientApp().run()
