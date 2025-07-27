from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout

LANGUAGES = {
    "en": {
        "title": "playball",
        "stream1": "Watch Stream 1 - PlayBall1",
        "stream2": "Watch Stream 2 - PlayBall2",
        "subscribe": "Subscribe now",
        "settings": "Settings",
        "language": "Language: English",
        "monthly": "Monthly: $30",
        "yearly": "Yearly: $100",
        "free": "Free Trial: 24h",
        "close": "Close"
    },
    "ar": {
        "title": "بلاي بول",
        "stream1": "مشاهدة البث 1 - PlayBall1",
        "stream2": "مشاهدة البث 2 - PlayBall2",
        "subscribe": "اشترك الآن",
        "settings": "الإعدادات",
        "language": "اللغة: العربية",
        "monthly": "شهرياً: 30$",
        "yearly": "سنوياً: 100$",
        "free": "تجربة مجانية: 24 ساعة",
        "close": "Close"
    }
}

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.current_language = "en"
        self.labels = {}
        self.free_trial_used = False
        self.is_subscribed = False  # حالة الاشتراك، افتراضاً غير مشترك

        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # زر الإعدادات داخل AnchorLayout لوضعه يمين أو يسار في الأعلى
        self.settings_button = Button(text='⚙️', size_hint=(None, None), size=(80, 80), font_size=32 * 3)
        self.settings_button.bind(on_release=self.show_settings)
        self.settings_anchor = AnchorLayout(anchor_y='top', size_hint=(1, None), height=80)
        self.settings_anchor.add_widget(self.settings_button)
        self.update_settings_position()

        # محتوى الشاشة
        self.content_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.content_layout.add_widget(Image(source='playball_logo.png', size_hint=(1, 0.4)))

        self.labels['title'] = Label(font_size=42 * 3, bold=True, color=(1, 0, 0, 1))
        self.content_layout.add_widget(self.labels['title'])

        self.labels['stream1'] = Button(font_size=22 * 3, background_color=(1, 0, 0, 1))
        self.labels['stream2'] = Button(font_size=22 * 3, background_color=(1, 0, 0, 1))

        # ربط ضغط البثوث ليظهر الاشتراك فقط إذا غير مشترك
        self.labels['stream1'].bind(on_release=self.handle_stream_press)
        self.labels['stream2'].bind(on_release=self.handle_stream_press)

        self.content_layout.add_widget(self.labels['stream1'])
        self.content_layout.add_widget(self.labels['stream2'])

        self.labels['subscribe'] = Button(font_size=22 * 3, background_color=(0.6, 0.0, 0.8, 1), color=(1, 1, 1, 1))
        self.labels['subscribe'].bind(on_release=self.show_subscription_popup)
        self.content_layout.add_widget(self.labels['subscribe'])

        main_layout.add_widget(self.settings_anchor)
        main_layout.add_widget(self.content_layout)

        self.add_widget(main_layout)
        self.update_texts()

    def update_settings_position(self):
        # تحكم يمين أو يسار حسب اللغة
        self.settings_anchor.anchor_x = 'right' if self.current_language == "en" else 'left'

    def update_texts(self):
        lang = LANGUAGES[self.current_language]
        self.labels['title'].text = lang['title']
        self.labels['stream1'].text = lang['stream1']
        self.labels['stream2'].text = lang['stream2']
        self.labels['subscribe'].text = lang['subscribe']
        self.update_settings_position()

    def show_settings(self, instance):
        lang = LANGUAGES[self.current_language]
        content = BoxLayout(orientation='vertical', spacing=15, padding=10)
        content.add_widget(Label(text=lang['settings'], font_size=24 * 3))

        language_layout = BoxLayout(orientation='horizontal', spacing=10)
        language_label = Label(text=lang['language'], font_size=18 * 3)

        def toggle_language(instance):
            self.current_language = "ar" if self.current_language == "en" else "en"
            language_label.text = LANGUAGES[self.current_language]['language']
            self.update_texts()

        left_button = Button(text='←', size_hint=(0.2, 1), font_size=20 * 3)
        right_button = Button(text='→', size_hint=(0.2, 1), font_size=20 * 3)
        left_button.bind(on_release=toggle_language)
        right_button.bind(on_release=toggle_language)

        language_layout.add_widget(left_button)
        language_layout.add_widget(language_label)
        language_layout.add_widget(right_button)

        content.add_widget(language_layout)

        popup = Popup(title=lang['settings'], content=content, size_hint=(0.9, 0.5))
        popup.open()

    def show_subscription_popup(self, instance):
        lang = LANGUAGES[self.current_language]
        content = BoxLayout(orientation='vertical', spacing=15, padding=20)

        monthly_label = Label(text=lang['monthly'], font_size=20 * 3)
        yearly_label = Label(text=lang['yearly'], font_size=20 * 3)

        content.add_widget(monthly_label)
        content.add_widget(yearly_label)

        if not self.free_trial_used:
            free_button = Button(text=lang['free'], font_size=20 * 3, background_color=(0.8, 1, 0.8, 1))
            content.add_widget(free_button)
            free_button.bind(on_release=self.start_free_trial)

        close_button = Button(text=lang['close'], font_size=18 * 3, size_hint=(1, 0.3))
        content.add_widget(close_button)

        self.subscription_popup = Popup(title=lang['subscribe'], content=content, size_hint=(0.8, 0.5))
        close_button.bind(on_release=self.subscription_popup.dismiss)
        self.subscription_popup.open()

    def start_free_trial(self, instance):
        self.free_trial_used = True
        Clock.schedule_once(self.end_free_trial, 86400)  # 24 ساعة
        if self.subscription_popup:
            self.subscription_popup.dismiss()

    def end_free_trial(self, dt):
        self.free_trial_used = True

    def handle_stream_press(self, instance):
        if not self.is_subscribed:
            self.show_subscription_popup(instance)
        else:
            # هنا ممكن تضيف فتح البث الحقيقي لو حبيت
            pass

class PlayBallApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    PlayBallApp().run()
