import tkinter as tk #مكتبة انشاء الواجهات الرسومية في بايثون
import random #هذه المكتبة تتيح اختيار أرقام عشوائيةواختيار عناصر بشكل عشوائي
import time # هذه المكتبة تتيح تأخير تنفيذ الكود أو حتى الحصول على الوقت الحالي
import os # هذه المكتبة تتعامل مع نظام التشغيل مباشرة مثل انشاء مجلد
# او قراءة محتوياته أو حذفه كما تتعامل مع الملفات والمسارات



#........... إعدادات عامة للعبة
COLOR_NAMES = ["red", "blue", "green", "yellow", "black", "white",
               "orange", "purple", "pink", "gray", "brown", "cyan"] # قائمة ألوان بطاقات اللعب
TEXT_COLORS = ["blue", "green", "red", "purple"]# ألوان الكلمات أسفل البطاقات
MAX_TIME = 10   #الزمن المتاح لكل مستوى
HIGHSCORE_FILE = "highscore.txt" # الملف الذي يحتفظ به بأعلى عدد نقاط تحصل عليها

#_______________________________________________

#هذا الكلاس الأساسي في اللعبة
# والذي يحتوي على جميع مكوناتها بطريقة منظمة وقابلة للصيانة
class ColorGame:

    def __init__(self, root): # هذه الدالة الأولية و هي مسؤولة عن تهيئة الواجهات وإعداد المتغيرات
        self.root = root #حفظه النافذة الرئيسية لتستخدم لاحقاً في بقية الدوال
        self.root.title("لعبة مطابقة الألوان") # هذا عنوان اللعبة
        self.root.attributes('-fullscreen', True) # هذه خاصية اللعب بوضع ملئ الشاشة
        self.level = 1 # تحديد أول مستوى في اللعبة
        self.score = 0 # عند أول مستوى في البداية تكون لابد أن تبدأ اللعبة ب 0 نقطة
        self.start_time = None #سيتم استخدامه فيما بعد لحساب وقت بداية كل مستوى
        self.remaining_time = MAX_TIME # الوقت المسموح به في كل مستوى
        self.cards_frame = None # هذا الاطار يحتوى على بطاقات الألوان
        self.high_score = self.load_high_score() #لتحميل أعلى نتيجة مسجلة

        #اعدادات الواجهة الرسومية
        self.top_frame = tk.Frame(root, pady=10) # انشاء الاطار العلوي الذي يحتوي على المؤقت و رقم المستوى
        self.top_frame.pack(side="top", pady=10) # تحديد موقع الاطار العلوي
        self.middle_frame = tk.Frame(root) # انشاء الاطار الاوسط الذي يحتوي على بطاقات اللعب
        self.middle_frame.pack(expand=True) # هذا الاطار قابل للتوسيع لأن عدد بطاقات الألوان تزداد مع كل مستوى
        self.bottom_frame = tk.Frame(root) # انشاء الاطار السفلي الخاص بأزرار إعادة اللعبة والخروج منها
        self.bottom_frame.pack(pady=20) # تحديد الاطار السفلي

        #مكونات الاطار العلوي وخواص كل مكون
        self.status_label = tk.Label(self.top_frame, text="اضغط على ابدأ لبداية اللعبة", font=("Arial", 18))
        self.status_label.pack(side="left", padx=20)
        self.timer_label = tk.Label(self.top_frame, text="", font=("Arial", 16), fg="darkred")
        self.timer_label.pack(side="left", padx=20)
        self.timer_id = None
        self.points_label = tk.Label(self.top_frame, text="النقاط الآن: 0", font=("Arial", 16), fg="darkgreen")
        self.points_label.pack(side="left", padx=20)
        self.total_score_label = tk.Label(self.top_frame, text="المجموع الكلي: 0", font=("Arial", 16), fg="blue")
        self.total_score_label.pack(side="left", padx=20)
        self.high_score_label = tk.Label(self.top_frame, text=f"أعلى نتيجة: {self.high_score}", font=("Arial", 16), fg="darkblue")
        self.high_score_label.pack(side="left", padx=20)


        # ️ قمت هنا بفصل واجهة اللعب عن واجهة النتائج حتى لا تتأثر واجهة النتائج بتوسع الاطار
        # الأوسط مما قد يتسبب بإزاحة مكوناته و حتى خروجها عن الواجهة
        self.game_frame = tk.Frame(self.middle_frame)
        self.result_frame = tk.Frame(self.middle_frame)
        self.start_button = tk.Button(self.bottom_frame, text="   ابدأ اللعبة   ", command=self.start_game, bg="green", font=("Arial", 30))
        self.start_button.pack(pady=300)
        self.exit_button = tk.Button(self.bottom_frame, text="خروج من اللعبة", command=self.root.quit, font=("Arial", 14), bg="red", fg="white")
        self.exit_button.pack(pady=5)


        # تحميل أعلى نتيجة لتخزينها في ملف highscore.txt
    def load_high_score(self):
        if os.path.exists(HIGHSCORE_FILE):  # مسار ملف تخزين أعلى عدد نقاط
            try:
                with open(HIGHSCORE_FILE, "r") as f:
                    return int(f.read().strip())
            except:
                return 0
        return 0

#هنا يتم حفظ أعلى نتيجة
    def save_high_score(self):
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(self.high_score))

#--------------------------------------------------------------

#هذه دالة بدأ اللعبة
    def start_game(self):
        self.level = 1 # عند بدأ اللعبة يجب تعيين المستوى الأول
        self.score = 0 # و يجب تهيئة عدد النقاط الى الصفر
        self.status_label.config(text=f"المستوى {self.level}") # لاظهار المستوى الحالي
        self.total_score_label.config(text=f"المجموع الكلي: {self.score}") # تهيئة عدد النقاط الاجمالي ليبدأ ب 0
        self.start_button.pack_forget() # اخفاء زر بداية اللعبة
        self.result_frame.pack_forget() # اخفاء شاشة النتائج لو كان اللاعب قد اعاد اللعبة من جديد
        self.game_frame.pack() # اظهار واجهة اللعب
        self.next_level() # الانتقال التلقائي لتنفيذ أول مستوى


#-----------------------------------------------------------------------------

        # وهذه دالة تحسب الوقت المتبقي في كل مستوى و يتم تحديثها تلقائياً كل ثانية
    def update_timer(self):
        elapsed = int(time.time() - self.start_time) # حساب عدد الثواني التي مرت منذ بدأ المستوى
        self.remaining_time = MAX_TIME - elapsed # حساب الوقت المتبقي بطرح الوقت المنقضي من أعلى وقت مسموح به

        if self.remaining_time >= 0: # الشرط هو إذا كان الوقت >الصفر نحدث المؤقت كل ثانية أو تنتهي اللعبة
            self.timer_label.config(text=f"الوقت المتبقي: {self.remaining_time} ثانية")
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="انتهى الوقت!")
            self.points_label.config(text="النقاط الآن: 0")
            self.end_game(wrong=True)

#-----------------------------------------------------------------------

   # المستوى التالي باللعبة
    def next_level(self): # هذه دالة الانتقال الى المستوى التالي
        if self.timer_id:
            self.root.after_cancel(self.timer_id) # الغاء المؤقت الذي كان يعمل في المستوى السابق
        self.clear_frame()  # حذف كل محتويات المستوى السابق
        self.cards_frame = tk.Frame(self.game_frame)
        self.cards_frame.pack(pady=20)      # انشاء اطار جديد للمستوى الجديد
        num_cards = self.level  # عدد البطاقات = رقم المستوى
        available_colors = COLOR_NAMES[:min(len(COLOR_NAMES), num_cards + 5)]
        # اختيار مجموعة من الالوان المسموحة و كلما تقدم المستوى تختار عدد اكبر من الالوان لزيادة الصعوبة
        correct_index = random.randint(0, num_cards - 1)
        # اختيار رقم عشوائي لبطاقة واحدة صحيحة يجب على اللاعب اختيارها

        used_combinations = set() # مجموعة لتخزين لون الاسم ولون الزر التي استخدمت مسبقا حتى نتجنب التكرار
        if self.level > 20: # من بعد المستوى 20 تقل احجام بطاقات اللعب
            btn_width = max(5, 10 - (self.level - 20) // 2)
            btn_height = max(2, 4 - (self.level - 20) // 5)
            font_size = max(8, 12 - (self.level - 20) // 5)
        else:
            btn_width = 10
            btn_height = 4
            font_size = 12
        max_cols = 6 # الحد الأقصى لعدد الأعمدة
        for i in range(num_cards): #تكرار العملية بعدد البطاقات المطلوبة في هذا المستوى
            if i == correct_index:
                color = label_color = random.choice(available_colors)
                # تكون البطاقة صحيحة عندما يتطابق اسم اللون مع لون البطاقة

            else: # اختيار عشوائي لاسم الزر و اسم اللون مع منع التكرار
                while True:
                    color = random.choice(available_colors)
                    label_color = random.choice(available_colors)
                    if color != label_color and (color, label_color) not in used_combinations:
                        break

            used_combinations.add((color, label_color)) # حفظ تركيبة اللون و الاسم لمنع تكرارها
            card_frame = tk.Frame(self.cards_frame) # إنشاء إطار صغير لكل بطاقة، ووضعه في صفوف وأعمدة تلقائيا
            card_frame.grid(row=i // max_cols, column=i % max_cols, padx=5, pady=5)
            color_box = tk.Button(
                card_frame,
                bg=color,
                width=btn_width,
                height=btn_height,
                command=lambda correct=(i == correct_index): self.check_choice(correct) # فحص ان كان الاختيار صحيح ام لا
            )
            color_box.pack()

            random_text_color = random.choice(TEXT_COLORS) # اختيار لون خط عشوائي لاسم اللون لزيادة صعوبة التركيز
            label = tk.Label(card_frame, text=label_color, font=("Arial", font_size), fg=random_text_color)
            label.pack()

        self.start_time = time.time() # حفظ وقت بداية المستوى لاستخدامه في حساب الوقت المتبقي
        self.remaining_time = MAX_TIME # تعيين المؤقت للحد الأقصى المحدد مسبقًا
        self.update_timer() # بدء تشغيل دالة المؤقت لتبدأ العد التنازلي لهذا المستوى


#-----------------------------------------------
#هذه الدالة المسؤولة عن فحص اختيارات اللاعب
    def check_choice(self, is_correct):
        if self.timer_id: # نوقف المؤقت اذا اختار اللاعب البطاقة
            self.root.after_cancel(self.timer_id)
        if is_correct: # إذا كانت البطاقة صحيحة تحدث الاجراءات التالية
            elapsed = int(time.time() - self.start_time) # تحسب عدد الثواني التي استغرقها اللاعب بالوصول للإجابة
            self.remaining_time = max(0, MAX_TIME - elapsed) # يحسب الوقت المتبقي
            points = self.remaining_time * self.level # تحسب النقاط بضرب عدد الثواني المتبقي برقم المستوى
            self.score += points # تضاف للمجموع الكلي
            self.points_label.config(text=f"النقاط الآن: {points}") # عرض عدد النقاط المكتسبة في هذا المستوى على الشاشة
            self.total_score_label.config(text=f"المجموع الكلي: {self.score}") #تحديث عرض النقاط الكلية
            self.level += 1 # الانتقال للمستوى التالي بزيادة رقم المستوى ب 1
            self.status_label.config(text=f"المستوى {self.level}") # تحديث رقم المستوى في الشريط العلوي
            self.next_level() # لانشاء البطاقات في المستوى الجديد
        else:
            self.end_game(wrong=True) # إذا لم يتحقق المستوى الأعلى تنتهي اللعبة

#--------------------------------------------------------------------


    def end_game(self, wrong=False): # هذه الدالة تنهي اللعب و تعرض النتائج
        self.clear_frame() # بعد ان تنتهي اللعبة ننظف الشاشة من كل عناصر اللعبة لعرض عناصر النتيجة
        if self.timer_id: # إلغاء المؤقت لأنه لم تعد هنالك حاجة إليه
            self.root.after_cancel(self.timer_id)
            # مسح جميع مكونات الشريط العلوي بالكامل
        self.points_label.config(text="")
        self.timer_label.config(text="")
        self.status_label.config(text="")
        self.total_score_label.config(text="")

        # إذا كانت النتيجة الحالية أعلى نتيجة حصلت عليها يتم تخزينها في ملف highscore.txt
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.config(text=f" أعلى نتيجة:  {self.high_score} ")
            self.save_high_score()

        self.game_frame.pack_forget() # اخفاء واجهة اللعب

        self.result_frame.pack()  #عرض واجهة النتائج
        for widget in self.result_frame.winfo_children():
            widget.destroy() # حذف اي نتائج كانت موجودة مسبقاً في واجهة النتائج

            # الجزء الخاص بتصميم مربع النص الذي يعرض النتائج
        shadow = tk.Frame(self.result_frame, bg="#0b2545")
        shadow.pack(pady=30) # اضافة ظل لمربع النص لابرازه ولونه داكن أكثر من خلفية المربع
        result_inner = tk.Frame(
            shadow,
            bg="#131f4c", # لون كحلي لمربع النص
            padx=100, # عرض مربع النص
            pady=40, # طوله
            bd=4,
            relief="raised",
            highlightbackground="#1a2f4f",
            highlightthickness=2
        )
        result_inner.pack(padx=6, pady=6)

        label_text = tk.Label(result_inner, text=": عدد النقاط الحاصل عليها ",font=("Arial", 20), fg="#FFD700", bg="#131f4c")
        label_text.pack()
        score_value = tk.Label(result_inner, text=f"{self.score} ",font=("Arial", 24, "bold"), fg="red", bg="#131f4c")
        score_value.pack()

        # نص صغير باللون الذهبي يشرح كيف تم احتساب عدد النقاط
        explanation_label = tk.Label(
            result_inner,
            text="تحتسب عدد النقاط بضرب عدد الثواني المتبقية بكل مستوى في رقم المستوى",
            font=("Arial", 8),
            fg="#f0e68c",
            bg="#131f4c",
            wraplength=600,
            justify="center"
        )
        explanation_label.pack(pady=(4, 4))

        # نص يبرز عدد المستويات التي تم اجتيازها
        level_label = tk.Label(
            result_inner,
            text=f"عدد المستويات التي اجتزتها : {self.level - 1}",
            font=("Arial", 16),
            fg="#FFD700",
            bg="#131f4c"
        )
        level_label.pack()
        self.start_button.config(
            text="🔄 إعادة اللعب",
            bg="green",
            fg="white",
            font=("Arial", 16),
            relief="raised"
        )
        self.start_button.pack(pady=15)


#----------------------------------------------------------------------
#هذه الدالة تنظف جميع عناصر اللعبة لتعرض النتائج
    def clear_frame(self):
        if self.cards_frame:
            self.cards_frame.destroy()
            self.cards_frame = None

        for widget in self.game_frame.winfo_children():
            widget.destroy()


#--------------------------------------------------------------------

    #  تشغيل اللعبة
if __name__ == "__main__":
    root = tk.Tk()
    game = ColorGame(root)
    root.mainloop()

