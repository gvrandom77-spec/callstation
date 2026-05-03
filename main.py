# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import socket

from jnius import autoclass
from android.broadcast import BroadcastReceiver

class CallStationApp(App):
    def build(self):
        self.icon = 'icon.png'
        self.monitoring_active = False

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        instruction_text = (
            "Enter the computer's IPv4 address.\n"
            "You can find the address using the ipconfig command."
        )
        self.label = Label(
            text=instruction_text, 
            font_size='16sp', 
            halign='center',
            size_hint_y=0.2
        )
        layout.addWidget(self.label)

        self.ip_input = TextInput(
            text='172.56.21.89',
            font_size='20sp',
            multiline=False,
            halign='center',
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            size_hint_y=0.2
        )
        layout.addWidget(self.ip_input)

        self.toggle_btn = Button(
            text='START MONITORING',
            font_size='18sp',
            background_normal='',
            background_color=(0.9, 0.1, 0.1, 1),
            size_hint_y=0.3
        )
        self.toggle_btn.bind(on_press=self.toggle_monitoring)
        layout.addWidget(self.toggle_btn)

        self.hide_btn = Button(
            text='HIDE APPLICATION',
            font_size='18sp',
            background_color=(0.2, 0.2, 0.2, 1),
            size_hint_y=0.3
        )
        self.hide_btn.bind(on_press=self.hide_app)
        layout.addWidget(self.hide_btn)

        self.br = BroadcastReceiver(self.on_call_event, actions=['android.intent.action.PHONE_STATE'])

        return layout

    def toggle_monitoring(self, instance):
        if not self.monitoring_active:
            try:
                self.br.start()
                self.monitoring_active = True
                self.toggle_btn.text = 'STOP MONITORING'
                self.toggle_btn.background_color = (0.1, 0.8, 0.1, 1)
            except Exception as e:
                self.label.text = f"Error starting monitor: {e}"
        else:
            try:
                self.br.stop()
                self.monitoring_active = False
                self.toggle_btn.text = 'START MONITORING'
                self.toggle_btn.background_color = (0.9, 0.1, 0.1, 1)
            except Exception as e:
                self.label.text = f"Error stopping monitor: {e}"

    def hide_app(self, instance):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            activity.moveTaskToBack(True)
        except Exception as e:
            print(f"Failed to hide app: {e}")

    def on_call_event(self, context, intent):
        state = intent.getStringExtra('state')
        number = intent.getStringExtra('incoming_number') or "Unknown"

        if state == 'RINGING':
            self.send_signal(f"InCall:{number}")
        elif state == 'OFFHOOK':
            self.send_signal("Call:Offhook")
        elif state == 'IDLE':
            self.send_signal("Call:Idle")

    def send_signal(self, message):
        ip = self.ip_input.text.strip()
        port = 5555
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, port))
            s.sendall(message.encode('utf-8'))
            s.close()
        except Exception as e:
            print(f"Socket error: {e}")

    def on_stop(self):
        if self.monitoring_active:
            self.br.stop()

if __name__ == '__main__':
    CallStationApp().run()