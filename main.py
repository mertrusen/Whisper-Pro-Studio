import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import subprocess
import threading
import sys
import platform
import os
import json
import re
import shutil

# --- DETAYLI YARDIM METİNLERİ (BILINGUAL) ---
HELP_TEXTS = {
    "tr": {
        "model": "MODEL BOYUTU (Yapay Zeka Kapasitesi):\n\n"
                 "• large-v3: En yüksek doğruluk. Profesyonel işler için önerilir. (Yavaştır)\n"
                 "• medium: Hız ve kalite dengesi. Youtube videoları için idealdir.\n"
                 "• base/small: Çok hızlıdır ama hata yapabilir. Taslak çıkarmak için kullanılır.\n"
                 "• tiny: Anlık ve basit işler içindir.",
        "language": "KAYNAK DİL:\n\n"
                 "Video veya ses dosyasındaki konuşma dili nedir?\n"
                 "• auto: Yapay zeka dili kendisi tahmin eder (Genelde başarılıdır).\n"
                 "• tr/en/de...: Dili elle seçmek hata payını azaltır.",
        "task": "GÖREV TÜRÜ:\n\n"
                 "• transcribe: Sesi olduğu gibi metne döker. (Örn: Türkçe konuşmayı Türkçe yazar)\n"
                 "• translate: Sesi İngilizceye çevirerek yazar. (Örn: Türkçe konuşmayı İngilizce altyazı yapar)",
        "device": "DONANIM (Hızlandırıcı):\n\n"
                 "• mps: Apple Silicon (M1/M2/M3/M4) için GPU hızlandırma. Mac'te en hızlısı budur.\n"
                 "• cuda: Windows'ta NVIDIA ekran kartları için. (Çok hızlıdır)\n"
                 "• cpu: İşlemci. Ekran kartı yoksa bu seçilir. Yavaştır ama her bilgisayarda çalışır.\n\n"
                 "⚠️ MAC İPUCU: Eğer 'mps' modunda hata alırsanız veya program kapanırsa lütfen 'cpu' seçeneğini kullanın. İşlem biraz daha uzun sürer ama kesinlikle hata vermez.",
        "output_format": "ÇIKTI FORMATI:\n\n"
                 "• srt: Standart altyazı dosyası. (Youtube, VLC, Premiere Pro uyumlu)\n"
                 "• vtt: Web uyumlu altyazı formatı.\n"
                 "• txt: Sadece konuşmaların olduğu düz metin dosyası.\n"
                 "• all: Tüm formatları aynı anda oluşturur.",
        "custom_filename": "ÖZEL DOSYA ADI:\n\n"
                 "Oluşacak dosyanın adını buradan belirleyebilirsiniz.\n"
                 "Eğer boş bırakırsanız, videonun orijinal adı kullanılır.\n"
                 "(Örn: 'Tatil_Vlog' yazarsanız çıktı 'Tatil_Vlog.srt' olur)",
        "gap_fill": "SÜREKLİ ALTYAZI (Gap Filling):\n\n"
                 "Konuşmalar arasındaki sessiz boşlukları, bir önceki altyazı süresini uzatarak kapatır.\n"
                 "Bu sayede videoda altyazı sürekli ekranda kalır, yanıp sönme yapmaz.",
        "word_timestamps": "KELİME ZAMANLARI:\n\n"
                 "Aktif edilirse, altyazı dosyasının içine her kelimenin tam olarak hangi saniyede söylendiği bilgisi eklenir.\n"
                 "Karaoke efekti veya çok hassas video kurgusu (Premiere/DaVinci) yapacaksanız açın.",
        "max_line_count": "SATIR SAYISI:\n\n"
                 "Ekranda aynı anda görünecek maksimum satır sayısı.\n"
                 "• Profesyonel standart: 2 Satır.\n"
                 "• TikTok/Reels stili: 1 Satır.\n"
                 "NOT: Bu özellik çalışmak için 'Satır Genişliği' ayarını ZORUNLU kılar.",
        "line_width": "SATIR GENİŞLİĞİ (Karakter):\n\n"
                 "Bir satıra sığacak maksimum harf sayısı.\n"
                 "Standart: 42 Karakter. Daha düşük yaparsanız (örn: 20) altyazı daha dar ve uzun olur (Mobil uyumlu).",
        "max_words_per_line": "MAX KELİME:\n\n"
                 "Bir satıra sığacak maksimum kelime sayısı.\n"
                 "Satır genişliği yerine kelime sayısını baz almak isterseniz bunu kullanın.",
        "initial_prompt": "ÖZEL İPUÇLARI (Prompt):\n\n"
                 "Modelin yanlış anladığı özel isimleri, marka adlarını veya teknik terimleri buraya virgülle ayırarak yazın.\n"
                 "Örn: 'hmert, OpenAI, Python, Kubernetes'. Bu, modelin bu kelimeleri doğru yazmasını sağlar.",
        "temperature": "YARATICILIK (Temperature):\n\n"
                 "• 0.0: En tutarlı ve kesin sonuç (Önerilen).\n"
                 "• 0.5 - 1.0: Daha çeşitli kelimeler kullanır ama hata/uydurma yapma riski artar.",
        "condition": "BAĞLAM (Context):\n\n"
                 "Modelin bir önceki cümleyi hatırlayarak çeviri yapmasını sağlar.\n"
                 "Anlam bütünlüğü için her zaman AÇIK kalması önerilir.",
        "patience": "SABIR (Patience):\n\n"
                 "Modelin sessiz veya anlaşılmaz kısımları çözmek için ne kadar 'sabırlı' olacağı.\n"
                 "Değer artarsa (örn: 2.0) işlem uzar ama doğruluk artabilir.",
        "beam_size": "IŞIN BOYUTU (Beam Size):\n\n"
                 "Modelin bir cümleyi kurarken aynı anda kaç farklı olasılığı değerlendireceği.\n"
                 "• 1: Hızlı (Greedy)\n"
                 "• 5: Yüksek Kalite (Standart)\n"
                 "• 10: Çok Yüksek Kalite (Yavaş)",
        "thresholds": "SESSİZLİK EŞİĞİ (No Speech):\n\n"
                 "Sesin ne kadar düşük olduğunda 'burada konuşma yok' sayılacağı.\n"
                 "Arka plan gürültüsü çok olan kayıtlarda bu ayarı değiştirmek gerekebilir.",
        "fp16": "FP16 (Yarım Hassasiyet):\n\n"
                 "İşlemi 2 kat hızlandırır ve RAM tasarrufu yapar.\n"
                 "M4 Pro gibi modern işlemcilerde her zaman AÇIK olmalıdır. Eski CPU'larda hata verirse kapatın.",
        "length_penalty": "UZUNLUK CEZASI:\n\n"
                 "Modelin kısa veya uzun cümle kurma eğilimini belirler.\n"
                 "• > 1.0: Uzun cümleleri tercih eder.\n"
                 "• < 1.0: Kısa, kesik cümleleri tercih eder.",
        "compression": "SIKIŞTIRMA EŞİĞİ:\n\n"
                 "Tekrarlayan metinleri (örneğin takılan sesler, 'eee, ııı' gibi) algılayıp filtreleme hassasiyeti."
    },
    "en": {
        "model": "MODEL SIZE (AI Capacity):\n\n• large-v3: Highest accuracy (Recommended for Pro use). Slower.\n• medium: Balanced speed/quality.\n• base/small: Fast drafting.\n• tiny: Very fast, lower accuracy.",
        "language": "SOURCE LANGUAGE:\n\nLanguage spoken in the audio.\n• auto: AI detects language automatically.\n• Manual selection reduces errors.",
        "task": "TASK TYPE:\n\n• transcribe: Speech to text in the same language.\n• translate: Speech to English text.",
        "device": "HARDWARE (Accelerator):\n\n• mps: Mac (M1/M2/M3/M4) GPU acceleration. Best for Mac.\n• cuda: Windows NVIDIA GPU. Very fast.\n• cpu: Processor only. Works everywhere but slow.\n\n"
                 "⚠️ MAC TIP: If you encounter errors or crashes in 'mps' mode, please switch to 'cpu'. It will be slower but strictly stable.",
        "output_format": "OUTPUT FORMAT:\n\n• srt: Standard subtitle file.\n• vtt: Web subtitle format.\n• txt: Plain text transcript.\n• all: Generate all formats.",
        "custom_filename": "CUSTOM FILENAME:\n\nSet a specific name for the output file.\nIf left empty, the original video filename is used.",
        "gap_fill": "GAP FILLING:\n\nFills silence gaps between subtitles by extending the duration of the previous subtitle.\nPrevents subtitle flickering.",
        "word_timestamps": "WORD TIMESTAMPS:\n\nSaves precise timing for every single word.\nEssential for karaoke effects or precise video editing.",
        "max_line_count": "MAX LINES:\n\nMaximum number of lines to display on screen at once.\n• Pro Standard: 2 Lines.\n• Social Media: 1 Line.\nNOTE: Requires 'Line Width' to be active.",
        "line_width": "LINE WIDTH (Chars):\n\nMax characters per line before wrapping.\nStandard: 42 chars.",
        "max_words_per_line": "MAX WORDS:\n\nMax words per line. Alternative to character limit.",
        "initial_prompt": "INITIAL PROMPT:\n\nProvide context or custom words (names, brands) to help the AI.\nEx: 'hmert, OpenAI, Python'.",
        "temperature": "CREATIVITY (Temperature):\n\n• 0.0: Most precise and consistent (Recommended).\n• 1.0: More creative but prone to hallucinations.",
        "condition": "CONTEXT:\n\nUses previous sentence context for better translation continuity.",
        "patience": "PATIENCE:\n\nHow long the model waits to decode silent audio segments.",
        "beam_size": "BEAM SIZE:\n\nNumber of alternative paths searched during generation.\n• 5: Standard high quality.",
        "thresholds": "NO SPEECH THRESHOLD:\n\nSilence detection sensitivity level.",
        "fp16": "FP16 (Half Precision):\n\nSpeeds up processing significantly.\nKeep ON for M4 Pro and modern GPUs.",
        "length_penalty": "LENGTH PENALTY:\n\nBiases the model towards shorter (<1.0) or longer (>1.0) sentences.",
        "compression": "COMPRESSION THRESHOLD:\n\nSensitivity for filtering out repetitive text loops."
    }
}

# --- DİL SÖZLÜĞÜ (UI) ---
TRANSLATIONS = {
    "tr": {
        "title": "WHISPER PRO STUDIO",
        "tab_gen": "GENEL", "tab_out": "FORMAT & ZAMAN", "tab_ai": "AI & PROMPT",
        "tab_fine": "İNCE AYAR", "tab_tech": "TEKNİK", "tab_pre": "PRESET", "tab_info": "BİLGİ & KÜNYE",
        "lbl_media": "Medya:", "lbl_save": "Kayıt Yeri:", "btn_sel": "Seç",
        "lbl_model": "Model:", "lbl_lang": "Dil (Audio):", "lbl_task": "Görev:", "lbl_dev": "Cihaz:",
        "lbl_fmt": "Format:", "lbl_name": "Özel İsim:", "lbl_gap": "Sürekli Altyazı:",
        "lbl_time": "Zamanlama:", "lbl_line_cnt": "Satır Sayısı:", "lbl_line_wd": "Satır Genişliği:", "lbl_max_w": "Max Kelime:",
        "lbl_prompt": "Kelime İpuçları (Prompt):", "lbl_temp": "Sıcaklık:", "lbl_ctx": "Context:",
        "lbl_pat": "Patience:", "lbl_beam": "Beam Size:", "lbl_nospeech": "No Speech:",
        "lbl_fp16": "FP16 (Hız):", "lbl_lenpen": "Len. Penalty:", "lbl_comp": "Comp. Thresh:",
        "lbl_presets": "Kayıtlı Ayarlar:", "btn_save_pre": "Farklı Kaydet...", "btn_del_pre": "Bu Ayarı Sil",
        "grp_media": " MEDYA KAYNAĞI ", "grp_preview": " Komut Önizleme ", "lbl_status": "İşlem Durumu:",
        "btn_start": "WHISPER'I BAŞLAT",
        "btn_stop": "WHISPER'I DURDUR",
        "info_dev": "GELİŞTİRİCİ:",
        "info_header": "WHISPER PRO STUDIO",
        "info_desc": """Bu yazılım, OpenAI'nin 'Whisper' modeli için geliştirilmiş, çapraz platform (Windows/Mac) destekli profesyonel bir arayüzdür.

DONANIM DESTEĞİ:
• macOS: Apple Silicon (M1-M4) işlemcilerde 'mps' modu ile tam performans.
• Windows: NVIDIA ekran kartı olanlar 'cuda', olmayanlar 'cpu' seçmelidir.
• Linux/Diğer: 'cpu' modu evrenseldir.

KAYIT KONUMLARI:
• Ayarlarınız 'Kullanıcı Klasörünüze' (C:\\Users\\Ad\\ veya /Users/Ad/) kaydedilir.
• Çıktılar varsayılan olarak Masaüstüne kaydedilir.

ÖZELLİKLER:
• SRT/VTT/TXT Çıktı • Kelime Zamanlama • Boşluk Doldurma • Akıllı Prompt"""
    },
    "en": {
        "title": "WHISPER PRO STUDIO",
        "tab_gen": "GENERAL", "tab_out": "FORMAT & TIMING", "tab_ai": "AI & PROMPT",
        "tab_fine": "FINE TUNE", "tab_tech": "TECHNICAL", "tab_pre": "PRESETS", "tab_info": "INFO & CREDITS",
        "lbl_media": "Media:", "lbl_save": "Save Path:", "btn_sel": "Select",
        "lbl_model": "Model:", "lbl_lang": "Language:", "lbl_task": "Task:", "lbl_dev": "Device:",
        "lbl_fmt": "Format:", "lbl_name": "Custom Name:", "lbl_gap": "Gap Filling:",
        "lbl_time": "Word Time:", "lbl_line_cnt": "Max Lines:", "lbl_line_wd": "Line Width:", "lbl_max_w": "Max Words:",
        "lbl_prompt": "Initial Prompt:", "lbl_temp": "Temperature:", "lbl_ctx": "Context:",
        "lbl_pat": "Patience:", "lbl_beam": "Beam Size:", "lbl_nospeech": "No Speech:",
        "lbl_fp16": "FP16 (Fast):", "lbl_lenpen": "Len. Penalty:", "lbl_comp": "Comp. Thresh:",
        "lbl_presets": "Saved Presets:", "btn_save_pre": "Save As...", "btn_del_pre": "Delete Preset",
        "grp_media": " MEDIA SOURCE ", "grp_preview": " Command Preview ", "lbl_status": "Process Status:",
        "btn_start": "START WHISPER",
        "btn_stop": "STOP WHISPER",
        "info_dev": "DEVELOPER:",
        "info_header": "WHISPER PRO STUDIO",
        "info_desc": """This software is a professional, cross-platform (Windows/Mac) GUI for OpenAI's 'Whisper' model.

HARDWARE SUPPORT:
• macOS: Full performance on Apple Silicon (M1-M4) using 'mps' mode.
• Windows: Select 'cuda' for NVIDIA GPUs, otherwise use 'cpu'.
• Linux/Other: 'cpu' mode is universal.

SAVE LOCATIONS:
• Settings are saved to your User Home Directory.
• Outputs default to your Desktop.

FEATURES:
• SRT/VTT/TXT Output • Word Timing • Gap Filling • Smart Prompting"""
    }
}

ALL_LANGUAGES = ["auto - Otomatik", "tr - Türkçe", "en - İngilizce"] + sorted([
    "de - Almanca", "fr - Fransızca", "es - İspanyolca", "it - İtalyanca", "ja - Japonca", 
    "ru - Rusça", "ar - Arapça", "az - Azerbaijani"
])

class ModernScrollbar(tk.Canvas):
    def __init__(self, master, command=None, bg="#1e1e1e", thumb_color="#555", hover_color="#888", width=12, **kwargs):
        super().__init__(master, bg=bg, width=width, highlightthickness=0, **kwargs)
        self.command = command; self.thumb_color = thumb_color; self.hover_color = hover_color; self.bg_color = bg
        self.create_rectangle(0, 0, width, 0, fill=self.thumb_color, outline="", tags="thumb")
        self.bind("<Button-1>", self.on_click); self.bind("<B1-Motion>", self.on_drag)
        self.tag_bind("thumb", "<Enter>", lambda e: self.itemconfig("thumb", fill=self.hover_color))
        self.tag_bind("thumb", "<Leave>", lambda e: self.itemconfig("thumb", fill=self.thumb_color))
        
    def set(self, first, last):
        first, last = float(first), float(last)
        if first <= 0.0 and last >= 1.0: self.place_forget(); return
        if not self.winfo_ismapped(): self.place(relx=1.0, rely=0.0, relheight=1.0, anchor="ne")
        h = self.winfo_height(); y0, y1 = int(first * h), int(last * h)
        if y1 - y0 < 10: y1 = y0 + 10
        self.coords("thumb", 2, y0, 10, y1)

    def on_click(self, event): 
        if self.command: self.command("moveto", event.y / self.winfo_height())
    def on_drag(self, event): 
        if self.command: self.command("moveto", event.y / self.winfo_height())

class ModernButton(tk.Label):
    def __init__(self, parent, text, command, bg="#007acc", fg="white", hover_bg="#005f9e", height=1, font=("Segoe UI", 10, "bold"), width=None, **kwargs):
        super().__init__(parent, text=text, bg=bg, fg=fg, font=font, cursor="hand2", height=height, width=width, **kwargs)
        self.command = command; self.bg = bg; self.hover_bg = hover_bg
        self.bind("<Enter>", lambda e: self.configure(bg=self.hover_bg))
        self.bind("<Leave>", lambda e: self.configure(bg=self.bg))
        self.bind("<Button-1>", lambda e: self.command() if self.command else None)
    
    def update_color(self, bg=None, hover_bg=None, text=None):
        if bg:
            self.bg = bg
            self.configure(bg=bg)
        if hover_bg:
            self.hover_bg = hover_bg
        if text:
            self.configure(text=text)

class CustomSpinbox(tk.Frame):
    def __init__(self, parent, from_, to, textvariable, width=5, bg="#333", fg="white", frame_bg="#1e1e1e", **kwargs):
        super().__init__(parent, bg=frame_bg)
        self.textvariable = textvariable; self.from_ = from_; self.to = to
        ModernButton(self, text="-", command=self.dec, width=2, bg="#444", hover_bg="#555", height=1, font=("Consolas", 10, "bold")).pack(side=tk.LEFT, padx=(0, 2))
        tk.Entry(self, textvariable=self.textvariable, width=width, bg=bg, fg=fg, relief="flat", justify="center", insertbackground="white").pack(side=tk.LEFT, ipady=4)
        ModernButton(self, text="+", command=self.inc, width=2, bg="#444", hover_bg="#555", height=1, font=("Consolas", 10, "bold")).pack(side=tk.LEFT, padx=(2, 0))
    def get_step(self): return (1, True) if isinstance(self.from_, int) else (0.1, False)
    def dec(self): 
        try: val = float(self.textvariable.get()); step, is_int = self.get_step(); new_val = round(val - step, 2)
        except: return
        if new_val >= self.from_: self.textvariable.set(int(new_val) if is_int else new_val)
    def inc(self):
        try: val = float(self.textvariable.get()); step, is_int = self.get_step(); new_val = round(val + step, 2)
        except: return
        if new_val <= self.to: self.textvariable.set(int(new_val) if is_int else new_val)

class ResponsiveWhisperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Whisper Pro Studio")
        self.root.geometry("1050x850")
        self.root.minsize(900, 700)
        
        self.colors = {
            "bg": "#1e1e1e", "panel": "#252526", "fg": "#e0e0e0", "accent": "#007acc",
            "input_bg": "#333333", "input_fg": "#ffffff", "border": "#3e3e42",
            "success": "#4ec9b0", "danger": "#f44336"
        }
        self.root.configure(bg=self.colors["bg"])
        self.root.bind("<Button-1>", self.remove_focus)
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)

        if platform.system() == "Windows":
            try: self.root.iconbitmap("app_icon.ico")
            except: pass

        self.root.option_add('*TCombobox*Listbox.background', self.colors["input_bg"])
        self.root.option_add('*TCombobox*Listbox.foreground', self.colors["input_fg"])
        self.root.option_add('*TCombobox*Listbox.selectBackground', self.colors["accent"])
        self.root.option_add('*TCombobox*Listbox.selectForeground', "white")

        self.current_lang = "tr"
        self.ui_elements = {} 
        self.history = []; self.history_index = -1; self.ignore_changes = False
        self.presets = {}
        self.preset_file = os.path.join(os.path.expanduser("~"), "whisper_presets.json")
        self.config_file = os.path.join(os.path.expanduser("~"), "whisper_config.json")
        
        self.process = None; self.is_running = False; self.stopped_by_user = False

        self.setup_styles()
        self.init_variables()
        self.load_presets_from_file()
        self.load_last_session() 
        self.create_responsive_ui()
        self.save_state()

    def remove_focus(self, event):
        if not isinstance(event.widget, (tk.Entry, tk.Text, ttk.Combobox, ModernButton)): self.root.focus_set()
        
    def setup_styles(self):
        style = ttk.Style(); style.theme_use('clam')
        style.configure("TFrame", background=self.colors["bg"])
        style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["fg"], font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground=self.colors["accent"])
        style.configure("TNotebook", background=self.colors["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", background=self.colors["panel"], foreground="#aaaaaa", padding=[15, 5], font=("Segoe UI", 10))
        style.map("TNotebook.Tab", background=[("selected", self.colors["accent"])], foreground=[("selected", "white")])
        style.map('TCombobox', fieldbackground=[('readonly', self.colors["input_bg"])], selectbackground=[('readonly', self.colors["input_bg"])], selectforeground=[('readonly', self.colors["input_fg"])], background=[('readonly', self.colors["input_bg"])], foreground=[('readonly', self.colors["input_fg"])])
        style.configure("TCombobox", fieldbackground=self.colors["input_bg"], background=self.colors["input_bg"], foreground=self.colors["input_fg"], arrowcolor="white", borderwidth=0)
        style.configure("Sash", sashthickness=6, sashrelief="raised", background=self.colors["border"], handlesize=10)

    def init_variables(self):
        self.file_path = tk.StringVar()
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        if not os.path.exists(desktop):
            onedrive_desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
            if os.path.exists(onedrive_desktop): desktop = onedrive_desktop
            else: desktop = os.path.expanduser("~")
        self.output_dir = tk.StringVar(value=desktop)
        self.custom_filename = tk.StringVar(); self.selected_preset = tk.StringVar()
        self.model_size = tk.StringVar(value="large-v3"); self.language = tk.StringVar(value="tr - Türkçe")
        self.task = tk.StringVar(value="transcribe")
        
        system_name = platform.system(); default_device = "cpu"
        if system_name == "Darwin": default_device = "mps"
        elif system_name == "Windows": default_device = "cuda"
        self.device = tk.StringVar(value=default_device)
        
        self.output_format = tk.StringVar(value="srt"); self.word_timestamps = tk.BooleanVar(value=True)
        
        # YENİ: Satır Sayısı artık checkable
        self.use_line_count = tk.BooleanVar(value=True) 
        self.max_line_count = tk.IntVar(value=2)
        
        self.use_max_words = tk.BooleanVar(value=True)
        self.max_words_per_line = tk.IntVar(value=7)
        self.use_line_width = tk.BooleanVar(value=False)
        self.max_line_width = tk.IntVar(value=42)
        
        self.initial_prompt = tk.StringVar()
        self.temperature = tk.DoubleVar(value=0.0); self.no_speech_threshold = tk.DoubleVar(value=0.6)
        self.beam_size = tk.IntVar(value=5); self.fp16 = tk.BooleanVar(value=False)
        self.condition_on_previous_text = tk.BooleanVar(value=True); self.patience = tk.DoubleVar(value=1.0)
        self.length_penalty = tk.DoubleVar(value=1.0); self.compression_ratio_threshold = tk.DoubleVar(value=2.4)
        self.gap_filling = tk.BooleanVar(value=False); self.gap_threshold = tk.DoubleVar(value=2.0)

    def save_last_session(self):
        data = {
            "model": self.model_size.get(), "lang": self.language.get(), "task": self.task.get(),
            "device": self.device.get(), "format": self.output_format.get(),
            "word_ts": self.word_timestamps.get(), "max_line": self.max_line_count.get(),
            "use_lines": self.use_line_count.get(), 
            "fp16": self.fp16.get(), "out_dir": self.output_dir.get()
        }
        try:
            with open(self.config_file, "w", encoding="utf-8") as f: json.dump(data, f)
        except: pass

    def load_last_session(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "model" in data: self.model_size.set(data["model"])
                    if "lang" in data: self.language.set(data["lang"])
                    if "task" in data: self.task.set(data["task"])
                    if "device" in data: self.device.set(data["device"])
                    if "format" in data: self.output_format.set(data["format"])
                    if "word_ts" in data: self.word_timestamps.set(data["word_ts"])
                    if "max_line" in data: self.max_line_count.set(data["max_line"])
                    if "use_lines" in data: self.use_line_count.set(data["use_lines"])
                    if "fp16" in data: self.fp16.set(data["fp16"])
                    if "out_dir" in data and os.path.exists(data["out_dir"]): self.output_dir.set(data["out_dir"])
            except: pass

    # --- ZİNCİRLEME MANTIK FONKSİYONLARI (KİLİTLİ MOD) ---
    def toggle_line_count_check(self):
        # Satır Sayısı açılırsa -> Satır Genişliği de AÇILMAK ZORUNDA
        if self.use_line_count.get():
            self.use_line_width.set(True)
        self.save_state()

    def toggle_line_width_check(self):
        # Genişlik kapatılırsa -> Satır Sayısı da KAPANMAK ZORUNDA
        if not self.use_line_width.get():
            self.use_line_count.set(False)
        self.save_state()

    def toggle_max_words_check(self):
        # Max Kelime bağımsız çalışabilir (Diğerlerini etkilemez, ama Whisper uyarabilir)
        self.save_state()
    # ----------------------------------------------------

    def on_lang_selected(self, event):
        self.update_preview(); self.save_state()

    def load_presets_from_file(self):
        if os.path.exists(self.preset_file):
            try:
                with open(self.preset_file, "r", encoding="utf-8") as f: self.presets = json.load(f)
            except: pass
        else: self.presets = {"Standart (Türkçe)": {"model": "large-v3", "lang": "tr - Türkçe", "format": "srt", "word_ts": True}}

    def save_presets_to_file(self):
        try:
            with open(self.preset_file, "w", encoding="utf-8") as f: json.dump(self.presets, f, ensure_ascii=False, indent=4)
        except Exception as e: messagebox.showerror("Hata", f"Kaydedilemedi: {e}")

    def update_preset_buttons(self, event=None):
        self.apply_preset(event)
        if self.selected_preset.get(): self.ui_elements["btn_del_pre"].pack(side=tk.LEFT, padx=5)
        else: self.ui_elements["btn_del_pre"].pack_forget()

    def apply_preset(self, event):
        name = self.selected_preset.get()
        if name in self.presets:
            data = self.presets[name]; self.ignore_changes = True
            if "model" in data: self.model_size.set(data["model"])
            if "lang" in data: self.language.set(data["lang"])
            if "task" in data: self.task.set(data["task"])
            if "device" in data: self.device.set(data["device"])
            if "format" in data: self.output_format.set(data["format"])
            if "word_ts" in data: self.word_timestamps.set(data["word_ts"])
            if "max_line" in data: self.max_line_count.set(data["max_line"])
            if "max_word" in data: self.max_words_per_line.set(data["max_word"])
            if "line_width" in data: self.max_line_width.set(data["line_width"])
            if "prompt" in data: self.initial_prompt.set(data["prompt"])
            if "temp" in data: self.temperature.set(data["temp"])
            if "no_speech" in data: self.no_speech_threshold.set(data["no_speech"])
            if "beam" in data: self.beam_size.set(data["beam"])
            if "fp16" in data: self.fp16.set(data["fp16"])
            if "condition" in data: self.condition_on_previous_text.set(data["condition"])
            if "patience" in data: self.patience.set(data["patience"])
            if "len_pen" in data: self.length_penalty.set(data["len_pen"])
            if "comp" in data: self.compression_ratio_threshold.set(data["comp"])
            if "gap_filling" in data: self.gap_filling.set(data["gap_filling"])
            if "gap_threshold" in data: self.gap_threshold.set(data["gap_threshold"])
            if "use_words" in data: self.use_max_words.set(data["use_words"])
            if "use_width" in data: self.use_line_width.set(data["use_width"])
            if "use_lines" in data: self.use_line_count.set(data["use_lines"])
            self.ignore_changes = False; self.update_preview(); self.save_state()
            self.log_area.insert(tk.END, f">>> Preset Yüklendi: {name}\n"); self.log_area.see(tk.END)

    def save_current_as_preset(self):
        name = simpledialog.askstring("Preset Kaydet", "Bu ayar paketi için bir isim girin:")
        if name:
            self.presets[name] = {
                "model": self.model_size.get(), "lang": self.language.get(), "task": self.task.get(),
                "device": self.device.get(), "format": self.output_format.get(), "word_ts": self.word_timestamps.get(),
                "max_line": self.max_line_count.get(), "max_word": self.max_words_per_line.get(),
                "line_width": self.max_line_width.get(),
                "prompt": self.initial_prompt.get(), "temp": self.temperature.get(), "no_speech": self.no_speech_threshold.get(),
                "beam": self.beam_size.get(), "fp16": self.fp16.get(), "condition": self.condition_on_previous_text.get(),
                "patience": self.patience.get(), "len_pen": self.length_penalty.get(), "comp": self.compression_ratio_threshold.get(),
                "gap_filling": self.gap_filling.get(), "gap_threshold": self.gap_threshold.get(),
                "use_words": self.use_max_words.get(), "use_width": self.use_line_width.get(),
                "use_lines": self.use_line_count.get()
            }
            self.save_presets_to_file(); self.preset_combo['values'] = list(self.presets.keys()); self.selected_preset.set(name)
            self.update_preset_buttons(); self.log_area.insert(tk.END, f">>> Preset Kaydedildi: {name}\n")

    def delete_preset(self):
        name = self.selected_preset.get()
        if name and name in self.presets:
            if messagebox.askyesno("Sil", f"'{name}' silinsin mi?"):
                del self.presets[name]; self.save_presets_to_file()
                self.preset_combo['values'] = list(self.presets.keys()); self.selected_preset.set("")
                self.update_preset_buttons(); self.log_area.insert(tk.END, f">>> Preset Silindi: {name}\n")

    def save_state(self, *args):
        if self.ignore_changes: return
        current_state = {
            "file": self.file_path.get(), "out_dir": self.output_dir.get(), "custom_name": self.custom_filename.get(),
            "model": self.model_size.get(), "lang": self.language.get(), "task": self.task.get(),
            "device": self.device.get(), "fmt": self.output_format.get(), "word_ts": self.word_timestamps.get(),
            "max_line": self.max_line_count.get(), "max_word": self.max_words_per_line.get(),
            "line_width": self.max_line_width.get(),
            "no_speech": self.no_speech_threshold.get(), "beam": self.beam_size.get(),
            "prompt": self.initial_prompt.get(), "temp": self.temperature.get(),
            "fp16": self.fp16.get(), "condition": self.condition_on_previous_text.get(),
            "patience": self.patience.get(), "len_pen": self.length_penalty.get(), "comp": self.compression_ratio_threshold.get(),
            "gap_filling": self.gap_filling.get(), "gap_threshold": self.gap_threshold.get(),
            "use_words": self.use_max_words.get(), "use_width": self.use_line_width.get()
        }
        if self.history and self.history[self.history_index] == current_state: return
        if self.history_index < len(self.history) - 1: self.history = self.history[:self.history_index + 1]
        self.history.append(current_state); self.history_index += 1
        self.update_undo_redo_buttons(); self.update_preview()
        self.save_last_session()

    def restore_state(self, state):
        self.ignore_changes = True
        for key, var in [("file", self.file_path), ("out_dir", self.output_dir), ("custom_name", self.custom_filename),
                         ("model", self.model_size), ("lang", self.language), ("task", self.task), ("device", self.device),
                         ("fmt", self.output_format), ("word_ts", self.word_timestamps), ("max_line", self.max_line_count),
                         ("max_word", self.max_words_per_line), ("line_width", self.max_line_width), ("no_speech", self.no_speech_threshold), ("beam", self.beam_size),
                         ("prompt", self.initial_prompt), ("temp", self.temperature), ("fp16", self.fp16), 
                         ("condition", self.condition_on_previous_text), ("patience", self.patience),
                         ("len_pen", self.length_penalty), ("comp", self.compression_ratio_threshold),
                         ("gap_filling", self.gap_filling), ("gap_threshold", self.gap_threshold),
                         ("use_words", self.use_max_words), ("use_width", self.use_line_width), ("use_lines", self.use_line_count)]:
            if key in state: var.set(state[key])
        self.ignore_changes = False
        self.update_preview(); self.update_undo_redo_buttons()

    def undo(self):
        if self.history_index > 0: self.history_index -= 1; self.restore_state(self.history[self.history_index])
    def redo(self):
        if self.history_index < len(self.history) - 1: self.history_index += 1; self.restore_state(self.history[self.history_index])
    def update_undo_redo_buttons(self):
        if hasattr(self, 'btn_undo'): self.btn_undo.update_color(bg="#444" if self.history_index > 0 else "#222", text=None)
        if hasattr(self, 'btn_redo'): self.btn_redo.update_color(bg="#444" if self.history_index < len(self.history) - 1 else "#222", text=None)

    def change_ui_language(self, lang):
        self.current_lang = lang
        texts = TRANSLATIONS[lang]
        self.ui_elements["main_title"].config(text=texts["title"])
        self.ui_elements["grp_media"].config(text=texts["grp_media"])
        self.ui_elements["grp_preview"].config(text=texts["grp_preview"])
        self.ui_elements["lbl_status"].config(text=texts["lbl_status"])
        
        current_btn_key = "btn_stop" if self.is_running else "btn_start"
        self.ui_elements["btn_start"].configure(text=texts[current_btn_key])
        
        self.notebook.tab(0, text=texts["tab_gen"]); self.notebook.tab(1, text=texts["tab_out"]); self.notebook.tab(2, text=texts["tab_ai"])
        self.notebook.tab(3, text=texts["tab_fine"]); self.notebook.tab(4, text=texts["tab_tech"]); self.notebook.tab(5, text=texts["tab_pre"])
        self.notebook.tab(6, text=texts["tab_info"])
        self.ui_elements["info_header"].config(text=texts["info_header"])
        self.ui_elements["info_desc"].config(text=texts["info_desc"])
        self.ui_elements["info_dev"].config(text=texts["info_dev"])
        for key, widget in self.ui_elements.items():
            if key in texts and key != "btn_start": 
                if isinstance(widget, (tk.Label, ttk.Label)): widget.config(text=texts[key])
                elif isinstance(widget, ModernButton): widget.configure(text=texts[key])

    def create_responsive_ui(self):
        self.footer_frame = tk.Frame(self.root, bg=self.colors["bg"], pady=10)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.ui_elements["btn_start"] = ModernButton(self.footer_frame, text="WHISPER'I BAŞLAT", command=self.start_whisper_thread, bg=self.colors["accent"], hover_bg="#0062a3", font=("Segoe UI", 12, "bold"))
        self.ui_elements["btn_start"].pack(fill=tk.X, padx=20, ipady=10)
        self.paned_window = tk.PanedWindow(self.root, orient=tk.VERTICAL, bg=self.colors["border"], sashwidth=8, sashrelief="raised", showhandle=True)
        self.paned_window.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.top_pane = tk.Frame(self.paned_window, bg=self.colors["bg"])
        self.paned_window.add(self.top_pane, minsize=300, height=500, stretch="always")
        self.canvas = tk.Canvas(self.top_pane, bg=self.colors["bg"], highlightthickness=0)
        self.scrollbar = ModernScrollbar(self.top_pane, command=self.canvas.yview, bg=self.colors["bg"])
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.scroll_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.build_top_content(self.scroll_frame)
        self.bottom_pane = tk.Frame(self.paned_window, bg=self.colors["bg"])
        self.paned_window.add(self.bottom_pane, minsize=150, stretch="never")
        self.build_bottom_content(self.bottom_pane)
        self.change_ui_language("tr")

    def on_frame_configure(self, event): self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def on_canvas_configure(self, event): self.canvas.itemconfig(self.canvas_window, width=event.width)
    def _on_mousewheel(self, event):
        if platform.system() == 'Darwin': self.canvas.yview_scroll(int(-1*(event.delta)), "units")
        else: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # --- BUTON DURUM GÜNCELLEME ---
    def update_action_button(self, state="stopped"):
        texts = TRANSLATIONS[self.current_lang]
        if state == "running":
            self.ui_elements["btn_start"].update_color(
                text=texts["btn_stop"],
                bg=self.colors["danger"],
                hover_bg="#d32f2f"
            )
        else:
            self.ui_elements["btn_start"].update_color(
                text=texts["btn_start"],
                bg=self.colors["accent"],
                hover_bg="#0062a3"
            )

    def build_top_content(self, parent):
        main_pad = 15; header_frame = ttk.Frame(parent); header_frame.pack(fill=tk.X, padx=main_pad, pady=(10, 5))
        title_frame = tk.Frame(header_frame, bg=self.colors["bg"]); title_frame.pack(side=tk.LEFT)
        self.ui_elements["main_title"] = ttk.Label(title_frame, text="WHISPER PRO STUDIO", style="Header.TLabel"); self.ui_elements["main_title"].pack(anchor="w")
        right_frame = tk.Frame(header_frame, bg=self.colors["bg"]); right_frame.pack(side=tk.RIGHT)
        self.btn_undo = ModernButton(right_frame, text="⟲", command=self.undo, bg="#333", hover_bg="#444", width=3); self.btn_undo.pack(side=tk.LEFT, padx=2)
        self.btn_redo = ModernButton(right_frame, text="⟳", command=self.redo, bg="#333", hover_bg="#444", width=3); self.btn_redo.pack(side=tk.LEFT, padx=2)
        tk.Label(right_frame, text="|", bg=self.colors["bg"], fg="#555").pack(side=tk.LEFT, padx=5)
        ModernButton(right_frame, text="🇹🇷", command=lambda: self.change_ui_language("tr"), bg=self.colors["bg"], fg="white", hover_bg="#333", font=("Segoe UI", 14)).pack(side=tk.LEFT, padx=2)
        ModernButton(right_frame, text="🇬🇧", command=lambda: self.change_ui_language("en"), bg=self.colors["bg"], fg="white", hover_bg="#333", font=("Segoe UI", 14)).pack(side=tk.LEFT, padx=2)

        self.ui_elements["grp_media"] = tk.LabelFrame(parent, text=" MEDYA KAYNAĞI ", bg=self.colors["bg"], fg="#888888", font=("Segoe UI", 8, "bold"), relief="flat", bd=1)
        self.ui_elements["grp_media"].pack(fill=tk.X, padx=main_pad, pady=5); self.ui_elements["grp_media"].columnconfigure(1, weight=1)
        self.ui_elements["lbl_media"] = tk.Label(self.ui_elements["grp_media"], text="Medya:", bg=self.colors["bg"], fg=self.colors["fg"], anchor="w"); self.ui_elements["lbl_media"].grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(self.ui_elements["grp_media"], textvariable=self.file_path, bg=self.colors["input_bg"], fg="white", relief="flat", insertbackground="white").grid(row=0, column=1, padx=5, sticky="ew")
        self.ui_elements["btn_sel1"] = ModernButton(self.ui_elements["grp_media"], text="Seç", command=self.browse_file, bg="#333", hover_bg="#444", width=6); self.ui_elements["btn_sel1"].grid(row=0, column=2, padx=10)
        self.ui_elements["lbl_save"] = tk.Label(self.ui_elements["grp_media"], text="Kayıt Yeri:", bg=self.colors["bg"], fg=self.colors["fg"], anchor="w"); self.ui_elements["lbl_save"].grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(self.ui_elements["grp_media"], textvariable=self.output_dir, bg=self.colors["input_bg"], fg="white", relief="flat", insertbackground="white").grid(row=1, column=1, padx=5, sticky="ew")
        self.ui_elements["btn_sel2"] = ModernButton(self.ui_elements["grp_media"], text="Seç", command=self.browse_dir, bg="#333", hover_bg="#444", width=6); self.ui_elements["btn_sel2"].grid(row=1, column=2, padx=10)

        self.notebook = ttk.Notebook(parent); self.notebook.pack(fill=tk.X, padx=main_pad, pady=5)
        tab_gen = ttk.Frame(self.notebook, padding=10); tab_out = ttk.Frame(self.notebook, padding=10); tab_ai = ttk.Frame(self.notebook, padding=10); tab_fine = ttk.Frame(self.notebook, padding=10); tab_tech = ttk.Frame(self.notebook, padding=10); tab_presets = ttk.Frame(self.notebook, padding=10); tab_info = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab_gen, text="GENEL"); self.notebook.add(tab_out, text="FORMAT"); self.notebook.add(tab_ai, text="AI"); self.notebook.add(tab_fine, text="İNCE AYAR"); self.notebook.add(tab_tech, text="TEKNİK"); self.notebook.add(tab_presets, text="PRESET"); self.notebook.add(tab_info, text="BİLGİ")
        
        self.add_responsive_row(tab_gen, "lbl_model", self.model_size, ["large-v3", "medium", "base", "small", "tiny"], help_key="model")
        lang_frame = ttk.Frame(tab_gen); lang_frame.pack(fill=tk.X, pady=5)
        self.ui_elements["lbl_lang"] = ttk.Label(lang_frame, text="Dil:", width=15); self.ui_elements["lbl_lang"].pack(side=tk.LEFT)
        self.lang_combo = ttk.Combobox(lang_frame, textvariable=self.language, values=ALL_LANGUAGES, state="readonly", width=15); self.lang_combo.pack(side=tk.LEFT); self.lang_combo.bind("<<ComboboxSelected>>", self.on_lang_selected)
        ModernButton(lang_frame, text="?", command=lambda: messagebox.showinfo("Bilgi", HELP_TEXTS[self.current_lang]["language"]), bg=self.colors["bg"], fg=self.colors["accent"], hover_bg=self.colors["panel"], width=3).pack(side=tk.LEFT, padx=5, anchor="center")
        self.add_responsive_row(tab_gen, "lbl_task", self.task, ["transcribe", "translate"], help_key="task")
        self.add_responsive_row(tab_gen, "lbl_dev", self.device, ["mps", "cuda", "cpu"], help_key="device")

        self.add_responsive_row(tab_out, "lbl_fmt", self.output_format, ["srt", "vtt", "txt", "all"], help_key="output_format")
        self.add_responsive_row(tab_out, "lbl_name", self.custom_filename, widget_type="entry", help_key="custom_filename")
        gap_frame = ttk.Frame(tab_out); gap_frame.pack(fill=tk.X, pady=5)
        self.ui_elements["lbl_gap"] = ttk.Label(gap_frame, text="Sürekli Altyazı:", width=15); self.ui_elements["lbl_gap"].pack(side=tk.LEFT)
        tk.Checkbutton(gap_frame, text="", variable=self.gap_filling, command=self.save_state, bg=self.colors["bg"], activebackground=self.colors["bg"]).pack(side=tk.LEFT)
        CustomSpinbox(gap_frame, from_=0.1, to=10.0, textvariable=self.gap_threshold, bg=self.colors["input_bg"], fg="white", frame_bg=self.colors["bg"], width=5).pack(side=tk.LEFT, padx=10)
        ModernButton(gap_frame, text="?", command=lambda: messagebox.showinfo("Bilgi", HELP_TEXTS[self.current_lang]["gap_fill"]), bg=self.colors["bg"], fg=self.colors["accent"], hover_bg=self.colors["panel"], width=3).pack(side=tk.LEFT, padx=10, anchor="center")
        self.add_responsive_row(tab_out, "lbl_time", self.word_timestamps, widget_type="check", help_key="word_timestamps")
        
        # GÜNCELLENEN KISIM: Satır Sayısı artık Checkbox'lı
        self.add_checkable_spin_row(tab_out, "lbl_line_cnt", self.max_line_count, self.use_line_count, 1, 5, help_key="max_line_count", command=self.toggle_line_count_check)
        
        self.add_checkable_spin_row(tab_out, "lbl_line_wd", self.max_line_width, self.use_line_width, 10, 100, help_key="line_width", command=self.toggle_line_width_check)
        self.add_checkable_spin_row(tab_out, "lbl_max_w", self.max_words_per_line, self.use_max_words, 1, 50, help_key="max_words_per_line", command=self.toggle_max_words_check)

        prompt_frame = ttk.Frame(tab_ai); prompt_frame.pack(fill=tk.X, pady=(0, 10))
        self.ui_elements["lbl_prompt"] = ttk.Label(prompt_frame, text="Prompt:", width=25, foreground=self.colors["success"]); self.ui_elements["lbl_prompt"].pack(side=tk.LEFT)
        ModernButton(prompt_frame, text="?", command=lambda: messagebox.showinfo("Bilgi", HELP_TEXTS[self.current_lang]["initial_prompt"]), bg=self.colors["bg"], fg=self.colors["accent"], hover_bg=self.colors["panel"], width=3).pack(side=tk.LEFT, padx=10, anchor="center")
        tk.Entry(prompt_frame, textvariable=self.initial_prompt, bg=self.colors["input_bg"], fg="white", relief="flat", insertbackground="white").pack(fill=tk.X, ipady=5)
        self.add_responsive_row(tab_ai, "lbl_temp", self.temperature, widget_type="entry", help_key="temperature")
        self.add_responsive_row(tab_ai, "lbl_ctx", self.condition_on_previous_text, widget_type="check", help_key="condition")

        self.add_responsive_row(tab_fine, "lbl_pat", self.patience, widget_type="entry", help_key="patience")
        self.add_responsive_row(tab_fine, "lbl_beam", self.beam_size, [1, 10], widget_type="spin", help_key="beam_size")
        self.add_responsive_row(tab_fine, "lbl_nospeech", self.no_speech_threshold, widget_type="entry", help_key="thresholds")

        self.add_responsive_row(tab_tech, "lbl_fp16", self.fp16, widget_type="check", help_key="fp16")
        self.add_responsive_row(tab_tech, "lbl_lenpen", self.length_penalty, widget_type="entry", help_key="length_penalty")
        self.add_responsive_row(tab_tech, "lbl_comp", self.compression_ratio_threshold, widget_type="entry", help_key="compression")

        preset_row = ttk.Frame(tab_presets); preset_row.pack(fill=tk.X, pady=5)
        self.ui_elements["lbl_presets"] = ttk.Label(preset_row, text="Preset:", width=15); self.ui_elements["lbl_presets"].pack(side=tk.LEFT)
        self.preset_combo = ttk.Combobox(preset_row, textvariable=self.selected_preset, values=list(self.presets.keys()), state="readonly", width=25); self.preset_combo.pack(side=tk.LEFT, padx=5); self.preset_combo.bind("<<ComboboxSelected>>", self.update_preset_buttons)
        action_row = ttk.Frame(tab_presets); action_row.pack(fill=tk.X, pady=15)
        self.ui_elements["btn_save_pre"] = ModernButton(action_row, text="Kaydet", command=self.save_current_as_preset, bg=self.colors["accent"], hover_bg="#0062a3", width=15); self.ui_elements["btn_save_pre"].pack(side=tk.LEFT, padx=5)
        self.ui_elements["btn_del_pre"] = ModernButton(action_row, text="Sil", command=self.delete_preset, bg=self.colors["danger"], hover_bg="#d32f2f", width=12)

        # --- DETAYLI BİLGİ TABI ---
        dev_frame = tk.Frame(tab_info, bg=self.colors["bg"]); dev_frame.pack(fill=tk.X, pady=(15, 5))
        self.ui_elements["info_dev"] = tk.Label(dev_frame, text="GELİŞTİRİCİ:", font=("Segoe UI", 10), fg="#888", bg=self.colors["bg"]); self.ui_elements["info_dev"].pack(side=tk.TOP)
        tk.Label(dev_frame, text="mertrusen", font=("Consolas", 16, "bold"), fg=self.colors["success"], bg=self.colors["bg"]).pack(side=tk.TOP)
        
        ttk.Separator(tab_info, orient='horizontal').pack(fill='x', pady=10, padx=50)
        
        self.ui_elements["info_header"] = tk.Label(tab_info, text="WHISPER PRO STUDIO", font=("Segoe UI", 14, "bold"), fg=self.colors["accent"], bg=self.colors["bg"]); self.ui_elements["info_header"].pack(pady=(5, 5))
        self.ui_elements["info_desc"] = tk.Message(tab_info, text="", width=800, bg=self.colors["bg"], fg=self.colors["fg"], font=("Segoe UI", 10), justify="left"); self.ui_elements["info_desc"].pack(pady=5, padx=20, anchor="center")

    def build_bottom_content(self, parent):
        main_pad = 15
        self.ui_elements["grp_preview"] = tk.LabelFrame(parent, text=" Komut Önizleme ", bg=self.colors["bg"], fg="#888888", relief="flat")
        self.ui_elements["grp_preview"].pack(fill=tk.BOTH, expand=True, padx=main_pad, pady=5)
        self.cmd_preview = tk.Text(self.ui_elements["grp_preview"], height=3, bg=self.colors["input_bg"], fg="#00ff00", font=("Consolas", 9), relief="flat", insertbackground="white", wrap="char")
        self.cmd_preview.pack(fill=tk.BOTH, expand=True, ipady=2)
        self.ui_elements["lbl_status"] = tk.Label(parent, text="İşlem Durumu:", bg=self.colors["bg"], fg=self.colors["fg"], anchor="w")
        self.ui_elements["lbl_status"].pack(fill=tk.X, padx=main_pad, pady=(5, 0))
        self.log_area = tk.Text(parent, height=6, bg="black", fg="#00ff00", font=("Consolas", 10), relief="flat")
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=main_pad, pady=5)
        self.setup_tracers(); self.update_preview()

    def add_responsive_row(self, parent, text_key, variable, options=None, help_key=None, widget_type="combo"):
        frame = ttk.Frame(parent); frame.pack(fill=tk.X, pady=5)
        self.ui_elements[text_key] = ttk.Label(frame, text="Lbl:", width=15); self.ui_elements[text_key].pack(side=tk.LEFT)
        if widget_type == "combo": ttk.Combobox(frame, textvariable=variable, values=options, state="readonly", width=15).pack(side=tk.LEFT)
        elif widget_type == "entry": tk.Entry(frame, textvariable=variable, bg=self.colors["input_bg"], fg="white", relief="flat", insertbackground="white", width=17).pack(side=tk.LEFT, ipady=2)
        elif widget_type == "spin": CustomSpinbox(frame, from_=options[0], to=options[1], textvariable=variable, bg=self.colors["input_bg"], fg="white", frame_bg=self.colors["bg"], width=5).pack(side=tk.LEFT)
        elif widget_type == "check": tk.Checkbutton(frame, text="", variable=variable, command=self.save_state, bg=self.colors["bg"], activebackground=self.colors["bg"]).pack(side=tk.LEFT)
        if help_key: ModernButton(frame, text="?", command=lambda: messagebox.showinfo("Bilgi", HELP_TEXTS[self.current_lang][help_key]), bg=self.colors["bg"], fg=self.colors["accent"], hover_bg=self.colors["panel"], width=3).pack(side=tk.LEFT, padx=10, anchor="center")

    def add_checkable_spin_row(self, parent, text_key, variable, check_var, from_, to, help_key=None, command=None):
        frame = ttk.Frame(parent); frame.pack(fill=tk.X, pady=5)
        cmd = command if command else self.save_state
        tk.Checkbutton(frame, variable=check_var, bg=self.colors["bg"], selectcolor=self.colors["input_bg"], activebackground=self.colors["bg"], command=cmd).pack(side=tk.LEFT)
        self.ui_elements[text_key] = ttk.Label(frame, text="Lbl:", width=13); self.ui_elements[text_key].pack(side=tk.LEFT)
        CustomSpinbox(frame, from_=from_, to=to, textvariable=variable, bg=self.colors["input_bg"], fg="white", frame_bg=self.colors["bg"], width=5).pack(side=tk.LEFT)
        if help_key: ModernButton(frame, text="?", command=lambda: messagebox.showinfo("Bilgi", HELP_TEXTS[self.current_lang][help_key]), bg=self.colors["bg"], fg=self.colors["accent"], hover_bg=self.colors["panel"], width=3).pack(side=tk.LEFT, padx=5, anchor="center")

    # ... (Geri kalan fonksiyonlar aynı) ...
    def browse_file(self):
        f = filedialog.askopenfilename(filetypes=[("Medya", "*.mp3 *.wav *.mp4 *.m4a *.flac *.mkv")]); 
        if f: self.file_path.set(f); self.save_state()
    def browse_dir(self):
        d = filedialog.askdirectory(); 
        if d: self.output_dir.set(d); self.save_state()
    def setup_tracers(self):
        for v in [self.file_path, self.output_dir, self.custom_filename, self.model_size, self.language, self.task, self.device, 
                  self.output_format, self.max_line_count, self.max_words_per_line, self.max_line_width, self.no_speech_threshold, self.beam_size, 
                  self.initial_prompt, self.temperature, self.fp16, self.condition_on_previous_text, self.patience, self.length_penalty, 
                  self.compression_ratio_threshold, self.gap_filling, self.gap_threshold, self.use_max_words, self.use_line_width,
                  self.use_line_count]: # Tracers listesine eklendi
            v.trace_add("write", lambda *args: (self.update_preview(), self.save_state()))
    def get_command(self):
        cmd = ["whisper", f'"{self.file_path.get() or "video.mp4"}"']
        # ... (whisper path check)
        whisper_path = shutil.which("whisper")
        if whisper_path: cmd[0] = whisper_path
        if self.model_size.get() != "large-v3": cmd.extend(["--model", self.model_size.get()])
        else:
            if self.model_size.get() != "small": cmd.extend(["--model", self.model_size.get()])
        lang_val = self.language.get(); lang_code = lang_val.split(" - ")[0] if " - " in lang_val else lang_val
        if lang_code != "auto": cmd.extend(["--language", lang_code])
        if self.task.get() != "transcribe": cmd.extend(["--task", self.task.get()])
        cmd.extend(["--output_dir", f'"{self.output_dir.get()}"']); cmd.extend(["--device", self.device.get()])
        if self.output_format.get() != "all": cmd.extend(["--output_format", self.output_format.get()])
        if self.word_timestamps.get(): cmd.extend(["--word_timestamps", "True"])
        
        # --- CONDITIONAL LOGIC UPDATED ---
        if self.use_line_count.get():
             cmd.extend(["--max_line_count", str(self.max_line_count.get())])

        if self.use_line_width.get():
            cmd.extend(["--max_line_width", str(self.max_line_width.get())])
            
        if self.use_max_words.get():
            cmd.extend(["--max_words_per_line", str(self.max_words_per_line.get())])
        # -------------------------------------

        if self.initial_prompt.get().strip(): cmd.extend(["--initial_prompt", f'"{self.initial_prompt.get()}"'])
        if self.temperature.get() != 0.0: cmd.extend(["--temperature", str(self.temperature.get())])
        if self.beam_size.get() != 5: cmd.extend(["--beam_size", str(self.beam_size.get())])
        if self.no_speech_threshold.get() != 0.6: cmd.extend(["--no_speech_threshold", str(self.no_speech_threshold.get())])
        if not self.fp16.get(): cmd.extend(["--fp16", "False"])
        if not self.condition_on_previous_text.get(): cmd.extend(["--condition_on_previous_text", "False"])
        cmd.extend(["--patience", str(self.patience.get())]); cmd.extend(["--length_penalty", str(self.length_penalty.get())])
        if self.compression_ratio_threshold.get() != 2.4: cmd.extend(["--compression_ratio_threshold", str(self.compression_ratio_threshold.get())])
        return cmd
    def update_preview(self):
        cmd_str = " ".join(self.get_command()); extras = []
        if self.gap_filling.get(): extras.append(f"[PYTHON OTOMASYONU: Sürekli Altyazı Aktif (Eşik: {self.gap_threshold.get()}s)]")
        if self.custom_filename.get().strip(): extras.append(f"[PYTHON OTOMASYONU: Dosya Yeniden Adlandırılacak: {self.custom_filename.get()}]")
        full_text = cmd_str; 
        if extras: full_text += "\n\n" + "\n".join(extras)
        self.cmd_preview.delete(1.0, tk.END); self.cmd_preview.insert(tk.END, full_text)
    def start_whisper_thread(self):
        if hasattr(self, 'is_running') and self.is_running:
            self.stop_process()
            return

        if not self.file_path.get(): return messagebox.showerror("Hata", "Dosya seçmediniz!")
        
        if self.device.get() == "mps" and self.word_timestamps.get():
            pass 

        self.is_running = True
        self.update_action_button(state="running")
        
        self.log_area.delete(1.0, tk.END); self.log_area.insert(tk.END, ">>> İşlem Başlatılıyor...\n")
        threading.Thread(target=self.run_process, daemon=True).start()

    def stop_process(self):
        if self.process:
            self.process.terminate() 
            self.process = None
        
        self.is_running = False
        self.stopped_by_user = True
        self.update_action_button(state="stopped")
        self.log_area.insert(tk.END, "\n>>> İşlem kullanıcı tarafından durduruldu.\n")
        self.log_area.see(tk.END)

    def time_to_seconds(self, time_str):
        time_str = time_str.replace(',', '.'); h, m, s = time_str.split(':')
        return int(h) * 3600 + int(m) * 60 + float(s)
    def seconds_to_time(self, seconds):
        h = int(seconds // 3600); m = int((seconds % 3600) // 60); s = seconds % 60
        return f"{h:02}:{m:02}:{s:06.3f}".replace('.', ',')
    def post_process_gaps(self, filepath, threshold):
        try:
            with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
            pattern = re.compile(r'(\d+)\s+(\d{2}:\d{2}:\d{2}[,.]\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2}[,.]\d{3})\s+(.*?)(?=\n\n|\Z)', re.DOTALL)
            matches = list(pattern.finditer(content))
            if not matches: return 0
            parsed_blocks = []
            for m in matches:
                parsed_blocks.append({'idx': int(m.group(1)), 'start_str': m.group(2), 'end_str': m.group(3), 'start': self.time_to_seconds(m.group(2)), 'end': self.time_to_seconds(m.group(3)), 'text': m.group(4).strip()})
            updated_count = 0
            for i in range(len(parsed_blocks) - 1):
                current_block = parsed_blocks[i]; next_block = parsed_blocks[i+1]
                gap = next_block['start'] - current_block['end']
                if 0.001 < gap < threshold:
                    current_block['end'] = next_block['start']; current_block['end_str'] = self.seconds_to_time(current_block['end']); updated_count += 1
            new_content = []
            for b in parsed_blocks:
                start_s = b['start_str'] if 'start_str' in b else self.seconds_to_time(b['start'])
                end_s = b['end_str'] if 'end_str' in b else self.seconds_to_time(b['end'])
                new_content.append(f"{b['idx']}\n{start_s} --> {end_s}\n{b['text']}\n")
            with open(filepath, 'w', encoding='utf-8') as f: f.write('\n'.join(new_content))
            return updated_count
        except: return 0
    def run_process(self):
        cmd = self.get_command(); real_cmd = [x.replace('"', '') for x in cmd]
        input_file = self.file_path.get(); input_basename = os.path.splitext(os.path.basename(input_file))[0]; output_dir = self.output_dir.get()
        try:
            env = os.environ.copy(); env["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
            self.process = subprocess.Popen(real_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1, env=env)
            for line in iter(self.process.stdout.readline, ''):
                if line: 
                    self.root.after(0, lambda l=line: self.log_area.insert(tk.END, l) or self.log_area.see(tk.END))
            self.process.stdout.close()
            return_code = self.process.wait()
            self.process = None 

            if return_code == 0 and not self.stopped_by_user:
                if self.gap_filling.get():
                    srt_file = os.path.join(output_dir, input_basename + ".srt")
                    if os.path.exists(srt_file):
                        count = self.post_process_gaps(srt_file, self.gap_threshold.get())
                        self.root.after(0, lambda c=count: self.log_area.insert(tk.END, f"\n>>> GAP FILLING: {c} boşluk kapatıldı.\n"))
                custom_name = self.custom_filename.get().strip()
                if custom_name: self.rename_output_files(output_dir, input_basename, custom_name)
                self.root.after(0, lambda: messagebox.showinfo("Bitti", "İşlem tamamlandı!"))
            elif self.stopped_by_user: pass
            else: self.root.after(0, lambda: messagebox.showerror("Hata", "İşlem bir hata ile sonlandı. Logları kontrol edin."))
        except Exception as e: 
            if not self.stopped_by_user: self.root.after(0, lambda: messagebox.showerror("Hata", str(e)))
        finally:
            self.is_running = False
            self.stopped_by_user = False
            self.root.after(0, lambda: self.update_action_button(state="stopped"))

    def rename_output_files(self, output_dir, old_name, new_name):
        try:
            renamed_count = 0; extensions = [".srt", ".txt", ".vtt", ".json", ".tsv"]
            for ext in extensions:
                old_file = os.path.join(output_dir, old_name + ext); new_file = os.path.join(output_dir, new_name + ext)
                if os.path.exists(old_file):
                    if os.path.exists(new_file): os.remove(new_file)
                    os.rename(old_file, new_file); renamed_count += 1
                    msg = f"\n>>> DOSYA YENİDEN ADLANDIRILDI: {old_name}{ext} -> {new_name}{ext}\n"
                    self.root.after(0, lambda m=msg: self.log_area.insert(tk.END, m))
            if renamed_count == 0: self.root.after(0, lambda: self.log_area.insert(tk.END, "\n>>> UYARI: Yeniden adlandırılacak dosya bulunamadı.\n"))
        except Exception as e: self.root.after(0, lambda err=str(e): self.log_area.insert(tk.END, f"\n>>> HATA (Yeniden Adlandırma): {err}\n"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ResponsiveWhisperGUI(root)
    root.mainloop()