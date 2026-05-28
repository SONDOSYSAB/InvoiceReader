from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.toolbar import MDTopAppBar
from android.utils import start_activity  # مكتبة أندرويد لفتح التطبيقات الأخرى
from android.runnable import run_on_ui_thread
import pdfplumber
import re
import requests  # لإرسال البيانات للسيرفر السحابي
import time

class InvoiceApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=20)
        
        # شريط التطبيق
        toolbar = MDTopAppBar(title="مُرسل الفواتير التلقائي")
        layout.add_widget(toolbar)
        
        # حالة البرنامج
        self.status_label = MDLabel(
            text="الرجاء اختيار طريقة الإرسال ثم معالجة الفواتير",
            halign="center",
            theme_text_color="Secondary"
        )
        layout.add_widget(self.status_label)
        
        # خيارات الإرسال
        options_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="50dp", spacing=20)
        self.free_check = MDCheckbox(group="method", active=True)
        free_label = MDLabel(text="مجاني (عبر واتساب)")
        options_layout.add_widget(self.free_check)
        options_layout.add_widget(free_label)
        
        self.paid_check = MDCheckbox(group="method")
        paid_label = MDLabel(text="تلقائي (سحابي API)")
        options_layout.add_widget(self.paid_check)
        options_layout.add_widget(paid_label)
        layout.add_widget(options_layout)
        
        # زر التشغيل
        process_btn = MDRaisedButton(
            text="بدء قراءة الفواتير والإرسال",
            pos_hint={"center_x": .5},
            on_release=self.start_process
        )
        layout.add_widget(process_btn)
        
        # سجل العمليات
        self.log_label = MDLabel(
            text="السجل: جاهز لبدء العمل...",
            halign="right",
            size_hint_y=None,
            height="200dp"
        )
        layout.add_widget(self.log_label)
        
        return layout

    def start_process(self, instance):
        # اسم ملف الفواتير المجمع الذي يجب أن تضعه في ذاكرة الهاتف لاحقاً
        pdf_path = "invoices.pdf" 
        self.log_label.text = "⏳ جاري فحص ملف الفواتير...\n"
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text()
                    if text:
                        # استخراج الرقم الذي يبدأ بـ 7 ومكون من 9 أرقام
                        phone_match = re.search(r'\b7\d{8}\b', text)
                        if phone_match:
                            phone = phone_match.group(0)
                            # إضافة رمز الدولة تلقائياً (مثال لليمن 967)
                            full_phone = "967" + phone 
                            
                            self.log_label.text += f"📄 فاتورة لعميل برقم: {phone}\n"
                            
                            # اختيار طريقة الإرسال بناءً على اختيارك من الواجهة
                            if self.free_check.active:
                                self.send_via_whatsapp_intent(full_phone, f"مرحباً، مرفق لكم فاتورة المبيعات رقم {page_num}")
                            else:
                                self.send_via_cloud_api(full_phone, f"فاتورة المبيعات رقم {page_num}")
                            
                            # انتظار 5 ثوانٍ لتجنب الحظر بين الرسائل
                            time.sleep(5)
                        else:
                            self.log_label.text += f"⚠️ الصفحة {page_num}: لم يتم العثور على رقم هاتف.\n"
        except FileNotFoundError:
            self.log_label.text = "❌ خطأ: لم يتم العثور على ملف invoices.pdf في ذاكرة التطبيق!"
        except Exception as e:
            self.log_label.text = f"❌ حدث خطأ: {str(e)}"

    # 1. الطريقة المجانية (تفتح الواتساب الرسمي على هاتف الأندرويد)
    def send_via_whatsapp_intent(self, phone, message):
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        
        # إنشاء رابط الأندرويد المخصص لفتح محادثة واتساب مباشرة بالرسالة
        url = f"whatsapp://send?phone={phone}&text={message}"
        intent = Intent(Intent.ACTION_VIEW)
        intent.setData(Uri.parse(url))
        
        # فتح تطبيق واتساب
        currentActivity = PythonActivity.mActivity
        currentActivity.startActivity(intent)

    # 2. الطريقة السحابية التلقائية بالكامل (ترسل في الخلفية عبر سيرفر وسيط)
    def send_via_cloud_api(self, phone, message):
        # هنا تضع بيانات اشتراكك في بوابة الواتساب السحابية لاحقاً (مثال: UltraMsg أو لقطة هاتف)
        api_url = "https://api.ultramsg.com/instanceXXXXX/messages/chat"
        payload = {
            "token": "YOUR_TOKEN_HERE",
            "to": phone,
            "body": message
        }
        try:
            # إرسال الطلب للسيرفر ليدفع الرسالة فوراً للعميل في الخلفية
            requests.post(api_url, data=payload)
            self.log_label.text += f"✅ تم إرسال الرسالة تلقائياً للرقم {phone}\n"
        except:
            self.log_label.text += f"❌ فشل الإرسال السحابي للرقم {phone}\n"

if __name__ == '__main__':
    InvoiceApp().run()