# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: '/content/.buildozer/android/app/main.py'
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2026-01-15 16:39:36 UTC (1768495176)

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
        self.server_ip = self.load_ip()
        self.is_running = False
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        instruction = 'Введите [b]IPv4-адрес[/b] компьютера.\nЕго можно узнать через команду [color=#006400]ipconfig[/color]'
        layout.add_widget(Label(text=instruction, markup=True, halign='center', font_size='18sp'))
        self.ip_input = TextInput(text=self.server_ip, multiline=False, font_size='22sp', size_hint_y=None, height=80, halign='center')
        layout.add_widget(self.ip_input)
        self.btn_toggle = Button(text='ЗАПУСТИТЬ МОНИТОРИНГ', size_hint_y=None, height=100, background_color=get_color_from_hex('#2E7D32'), background_normal='')
        self.btn_toggle.bind(on_press=self.toggle_monitoring)
        layout.add_widget(self.btn_toggle)
        btn_hide = Button(text='СКРЫТЬ ПРИЛОЖЕНИЕ', size_hint_y=None, height=80, background_color=get_color_from_hex('#455A64'), background_normal='')
        btn_hide.bind(on_press=self.hide_app)
        layout.add_widget(btn_hide)
        self.status = Label(text='Статус: Остановлено', color=(0.7, 0.7, 0.7, 1))
        layout.add_widget(self.status)
        return layout
    def load_ip(self):
        # МЕНЯЕМ: Полностью убираем поврежденный декомпилятором мусор.
        # Делаем чистый возврат твоего американского IP, если файла еще нет.
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
            with open(self.config_path, 'w') as f:
                f.write(self.server_ip)
            self.is_running = True
            self.btn_toggle.text = 'ОСТАНОВИТЬ'
            self.btn_toggle.background_color = get_color_from_hex('#C62828')
            self.status.text = f'Слежу за звонками (IP: {self.server_ip})'
            self.start_broadcast()
        else:
            self.is_running = False
            self.btn_toggle.text = 'ЗАПУСТИТЬ МОНИТОРИНГ'
            self.btn_toggle.background_color = get_color_from_hex('#2E7D32')
            self.status.text = 'Статус: Остановлено'
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
            return None
        else:
            state = intent.getStringExtra('state')
            number = intent.getStringExtra('incoming_number') or 'Скрытый номер'
            if state == 'RINGING':
                self.send_signal(f'Входящий: {number}')
    def send_signal(self, message):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((self.server_ip, 5555))
            s.sendall(message.encode('utf-8'))
            s.close()
        except:
            return None
if __name__ == '__main__':
    StationClientApp().run()
