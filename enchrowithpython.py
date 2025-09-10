"""
Encryption/Decryption Tool
Author: Jan Füllhase
"""

__author__ = "Jan Füllhase"
__version__ = "1.0.0"

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.utils import platform

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64
import os

class EncDecApp(App):

    def build(self):
        self.title = "Encryption/Decryption Tool"
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Password
        layout.add_widget(Label(text='Password:'))
        self.password_input = TextInput(multiline=False, password=True)
        layout.add_widget(self.password_input)

        # Salt (optional)
        layout.add_widget(Label(text='Salt (optional):'))
        self.salt_input = TextInput(multiline=False)
        layout.add_widget(self.salt_input)

        # File to process
        layout.add_widget(Label(text='File:'))
        self.file_label = Label(text='No file selected')
        layout.add_widget(self.file_label)

        # Buttons
        btn_layout = BoxLayout(spacing=10)
        select_file_btn = Button(text='Select File')
        select_file_btn.bind(on_press=self.show_file_chooser)
        btn_layout.add_widget(select_file_btn)

        encrypt_btn = Button(text='Encrypt')
        encrypt_btn.bind(on_press=self.encrypt_file)
        btn_layout.add_widget(encrypt_btn)

        decrypt_btn = Button(text='Decrypt')
        decrypt_btn.bind(on_press=self.decrypt_file)
        btn_layout.add_widget(decrypt_btn)

        layout.add_widget(btn_layout)

        self.selected_file = None

        return layout

    def show_file_chooser(self, instance):
        if platform == 'android':
            # File selection on Android is not yet supported as of 1.0.0
            self.show_popup("File Selection", "File selection on Android is not yet supported.")
            return

        content = FileChooserListView(path=os.path.expanduser('~'))
        content.bind(on_submit=self.select_file)
        self.popup = Popup(title="Select a file", content=content,
                           size_hint=(0.9, 0.9))
        self.popup.open()

    def select_file(self, instance, value, touch):
        if value:
            self.selected_file = value[0]
            self.file_label.text = os.path.basename(self.selected_file)
            if hasattr(self, 'popup'):
                self.popup.dismiss()

    def get_key(self, password, salt):
        return PBKDF2(password, salt, dkLen=32) # AES-256

    def encrypt_file(self, instance):
        if not self.selected_file:
            self.show_popup("Error", "Please select a file first.")
            return

        password = self.password_input.text
        if not password:
            self.show_popup("Error", "Please enter a password.")
            return

        salt_str = self.salt_input.text
        salt = base64.b64decode(salt_str) if salt_str else base64.b64decode("3eAToCvaGxCi9e6dWr1G7g==")

        key = self.get_key(password, salt)

        try:
            with open(self.selected_file, 'rb') as f_in:
                data = f_in.read()

            cipher = AES.new(key, AES.MODE_GCM)
            ciphertext, tag = cipher.encrypt_and_digest(data)

            with open(self.selected_file + '.enc', 'wb') as f_out:
                f_out.write(salt)
                f_out.write(cipher.nonce)
                f_out.write(tag)
                f_out.write(ciphertext)
            
            self.show_popup("Success", f"File encrypted to {os.path.basename(self.selected_file)}.enc")

        except Exception as e:
            self.show_popup("Error", f"Encryption failed: {e}")

    def decrypt_file(self, instance):
        if not self.selected_file:
            self.show_popup("Error", "Please select a file first.")
            return

        password = self.password_input.text
        if not password:
            self.show_popup("Error", "Please enter a password.")
            return

        try:
            with open(self.selected_file, 'rb') as f_in:
                salt = f_in.read(16)
                nonce = f_in.read(16)
                tag = f_in.read(16)
                ciphertext = f_in.read()

            key = self.get_key(password, salt)
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            
            decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

            decrypted_filename = self.selected_file[:-4] if self.selected_file.endswith('.enc') else self.selected_file + '.dec'
            with open(decrypted_filename, 'wb') as f_out:
                f_out.write(decrypted_data)

            self.show_popup("Success", f"File decrypted to {os.path.basename(decrypted_filename)}")

        except (ValueError, KeyError) as e:
            self.show_popup("Error", "Decryption failed. Check password or file integrity.")
        except Exception as e:
            self.show_popup("Error", f"Decryption failed: {e}")


    def show_popup(self, title, text):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=text))
        ok_button = Button(text='OK', size_hint_y=None, height=50)
        content.add_widget(ok_button)
        
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        ok_button.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    EncDecApp().run()
