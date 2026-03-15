HELP_TEXTS = {
    "tr": {
        "model": "MODEL BOYUTU (Yapay Zeka Kapasitesi):\n\n"
                 "• turbo: En güncel, en hızlı ve akıllı versiyon (Mac için En İyisi).\n"
                 "• large-v3: En yüksek doğruluk. (⚠️ Mac 'mps' modunda kararsızdır, hata verebilir.)\n"
                 "• medium: Hız ve kalite dengesi.\n"
                 "• base/small: Hızlı taslak çıkarmak içindir.\n"
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
                 "⚠️ NVIDIA CUDA ÇALIŞMIYORSA:\n"
                 "Eğer bilgisayarınızda NVIDIA kart olmasına rağmen CUDA hata veriyorsa, PyTorch kütüphanesinin CUDA sürümünü kurmalısınız. Terminale şu komutu girin:\n"
                 "pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118\n\n"
                 "⚠️ ÖNEMLİ (MAC): Mac cihazlarda 'mps' seçiliyken 'Zamanlama' ve 'FP16' seçenekleri KAPALI olmalıdır, aksi takdirde program hata verir.",
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
                 "Aktif edilirse, her kelimenin tam saniyesi altyazıya eklenir.\n\n"
                 "⚠️ MAC KULLANICILARI: Apple GPU (mps) bu özelliği desteklemez. Kelime zamanlarını kullanmak için 'Cihaz: cpu' ve 'Model: turbo' seçin. Bu sayede hem hızlı hem de zamanlamalı altyazı alabilirsiniz.",
        "max_line_count": "SATIR SAYISI (Max Line Count):\n\n"
                 "Ekranda aynı anda görünecek maksimum satır sayısı.\n"
                 "• Uzun videolar: 2 Satır (Standart).\n"
                 "• Shorts/Reels/TikTok: 1 Satır (Karaoke stili).\n\n"
                 "⚠️ WHISPER KURALI: Bu özelliğin çalışması için 'Zamanlama (Word Timestamps)' ve 'Satır Genişliği (Max Line Width)' özelliklerinin İKİSİNİN DE AÇIK OLMASI ZORUNLUDUR! Aksi takdirde Whisper hata verir.",
        "line_width": "SATIR GENİŞLİĞİ (Max Line Width):\n\n"
                 "Bir satıra sığacak maksimum karakter (harf) sayısı.\n"
                 "• Standart Geniş Ekran: 42 Karakter\n"
                 "• Dikey Video (TikTok/Reels): 20 Karakter veya altı.\n\n"
                 "⚠️ WHISPER KURALI: Bu ayar tek başına çalışabilir, ancak 'Satır Sayısı (Max Line Count)' kullanmak isterseniz bu ayarı da AÇIK tutmak zorundasınız. 'Zamanlama (Word Timestamps)' da AÇIK olmalıdır.",
        "max_words_per_line": "MAKS KELİME (Max Words Per Line):\n\n"
                 "Bir satıra sığacak maksimum KELİME sayısı. Örneğin '1' yaparsanız her kelime ekrana tek tek gelir (Karaoke).\n\n"
                 "⚠️ WHISPER KURALI: Bu ayar 'Satır Genişliği' ile BİRLİKTE KULLANILAMAZ! İkisinden birini seçmelisiniz. (Satır Genişliği harf sayar, bu kelime sayar). 'Zamanlama (Word Timestamps)' AÇIK olmalıdır.",
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
                 "İşlemi hızlandırır ve bellek tasarrufu yapar.\n"
                 "• NVIDIA (CUDA): Her zaman AÇIK olmalıdır.\n"
                 "• APPLE SILICON (MPS): KAPALI OLMALIDIR! Mac cihazlarda FP16 açmak programın 'NaN/inf' hatasıyla çökmesine neden olur.\n"
                 "• CPU: Genelde desteklenmez, kapalı tutun.",
        "length_penalty": "UZUNLUK CEZASI:\n\n"
                 "Modelin kısa veya uzun cümle kurma eğilimini belirler.\n"
                 "• > 1.0: Uzun cümleleri tercih eder.\n"
                 "• < 1.0: Kısa, kesik cümleleri tercih eder.",
        "compression": "SIKIŞTIRMA EŞİĞİ:\n\n"
                 "Tekrarlayan metinleri (örneğin takılan sesler, 'eee, ııı' gibi) algılayıp filtreleme hassasiyeti."
    },
    "en": {
        "model": "MODEL SIZE (AI Capacity):\n\n• turbo: Latest, fastest and smartest version (Default Recommendation).\n• large-v3: Highest accuracy. Slower than turbo.\n• medium: Balanced speed/quality.\n• base/small: Fast drafting.\n• tiny: Very fast, lower accuracy.",
        "language": "SOURCE LANGUAGE:\n\nLanguage spoken in the audio.\n• auto: AI detects language automatically.\n• Manual selection reduces errors.",
        "task": "TASK TYPE:\n\n• transcribe: Speech to text in the same language.\n• translate: Speech to English text.",
        "device": "HARDWARE (Accelerator):\n\n"
                 "• mps: Mac (M1/M2/M3/M4) GPU acceleration. Best for Mac.\n"
                 "• cuda: Windows NVIDIA GPU. Very fast.\n"
                 "• cpu: Processor only. Works everywhere but slow.\n\n"
                 "⚠️ NVIDIA CUDA ISSUES:\n"
                 "If CUDA fails on NVIDIA, you need the CUDA version of PyTorch. Run:\n"
                 "pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118\n\n"
                 "⚠️ IMPORTANT (MAC): When using 'mps', disable 'Word Timestamps' and 'FP16' to avoid crashes.",
        "output_format": "OUTPUT FORMAT:\n\n• srt: Standard subtitle file.\n• vtt: Web subtitle format.\n• txt: Plain text transcript.\n• all: Generate all formats.",
        "custom_filename": "CUSTOM FILENAME:\n\nSet a specific name for the output file.\nIf left empty, the original video filename is used.",
        "gap_fill": "GAP FILLING:\n\nFills silence gaps between subtitles by extending the duration of the previous subtitle.\nPrevents subtitle flickering.",
        "word_timestamps": "WORD TIMESTAMPS:\n\nSaves precise timing for every single word.\nEssential for karaoke effects or precise video editing.",
        "max_line_count": "MAX LINES (Max Line Count):\n\nMaximum number of lines to display on screen at once.\n• Pro Standard: 2 Lines.\n• Social Media: 1 Line.\n\n⚠️ WHISPER RULE: Requires BOTH 'Word Timestamps' and 'Line Width' to be ON.",
        "line_width": "LINE WIDTH (Chars):\n\nMax characters per line before wrapping.\nStandard: 42 chars.\n\n⚠️ WHISPER RULE: Requires 'Word Timestamps' to be ON.",
        "max_words_per_line": "MAX WORDS:\n\nMax words per line. Alternative to character limit.\n\n⚠️ WHISPER RULE: CANNOT be used with 'Line Width'. Requires 'Word Timestamps' to be ON.",
        "initial_prompt": "INITIAL PROMPT:\n\nProvide context or custom words (names, brands) to help the AI.\nEx: 'hmert, OpenAI, Python'.",
        "temperature": "CREATIVITY (Temperature):\n\n• 0.0: Most precise and consistent (Recommended).\n• 1.0: More creative but prone to hallucinations.",
        "condition": "CONTEXT:\n\nUses previous sentence context for better translation continuity.",
        "patience": "PATIENCE:\n\nHow long the model waits to decode silent audio segments.",
        "beam_size": "BEAM SIZE:\n\nNumber of alternative paths searched during generation.\n• 5: Standard high quality.",
        "thresholds": "NO SPEECH THRESHOLD:\n\nSilence detection sensitivity level.",
        "fp16": "FP16 (Half Precision):\n\n"
                 "Speeds up processing and saves memory.\n"
                 "• NVIDIA (CUDA): Should be ON.\n"
                 "• APPLE SILICON (MPS): MUST BE OFF! Enabling FP16 on Mac causes 'NaN/inf' errors and crashes.\n"
                 "• CPU: Usually not supported, keep off.",
        "length_penalty": "LENGTH PENALTY:\n\nBiases the model towards shorter (<1.0) or longer (>1.0) sentences.",
        "compression": "COMPRESSION THRESHOLD:\n\nSensitivity for filtering out repetitive text loops."
    }
}

TRANSLATIONS = {
    "tr": {
        "title": "WHISPER PRO STUDIO",
        "tab_gen": "Genel Ayarlar", 
        "tab_out": "Format & Zamanlama", 
        "tab_ai": "AI & Prompt",
        "tab_fine": "İnce Ayar", 
        "tab_tech": "Teknik Performans",
        "lbl_media": "Medya Dosyası:", 
        "lbl_save": "Çıktı Klasörü:", 
        "btn_sel": "Seç",
        "lbl_model": "Model Boyutu:", "lbl_lang": "Kaynak Dil:", "lbl_task": "Görev Türü:", "lbl_dev": "Donanım / Cihaz:",
        "lbl_fmt": "Çıktı Formatı:", "lbl_name": "Özel Dosya Adı:", "lbl_gap": "Sürekli Altyazı (Gap Fill):",
        "lbl_gap_thresh": "Kapanma Eşiği (Sn):",
        "lbl_time": "Kelime Zamanlaması (Word TS):", 
        "lbl_line_cnt": "Satır Sayısı Sınırı:", 
        "lbl_line_wd": "Satır Genişliği (Karakter):", 
        "lbl_max_w": "Satır Başına Kelime Limiti:",
        "lbl_prompt": "Yapay Zeka Prompt (Özel İsimler vb.):", "lbl_temp": "Sıcaklık (Temperature):", "lbl_ctx": "Önceki Metin Bağlamını Koru:",
        "lbl_pat": "Patience (Sabır):", "lbl_beam": "Beam Size (Arama Genişliği):", "lbl_nospeech": "Sessizlik Eşiği:",
        "lbl_fp16": "FP16 Hızlandırma:", "lbl_lenpen": "Length Penalty (Uzunluk Cezası):", "lbl_comp": "Tekrar Filtreleme (Compression):",
        "btn_save_pre": "Mevcut Ayarları Profile Kaydet", "btn_del_pre": "Seçili Profili Sil",
        "btn_start": "WHISPER'I BAŞLAT",
        "btn_stop": "İŞLEMİ DURDUR",
        "lbl_preview": "KOMUT ÖNİZLEMESİ",
        "lbl_log": "İŞLEM DURUMU VE LOGLAR",
        "btn_load_pre": "Seçili Profili Yükle",
        "info_dev": "GELİŞTİRİCİ:",
        "info_header": "WHISPER PRO STUDIO",
        "info_desc": """Bu yazılım, OpenAI'nin 'Whisper' modeli için geliştirilmiş, çapraz platform destekli profesyonel bir arayüzdür.
Karmaşık komut satırı işlemlerini otomatikleştirerek video içerik üreticileri için hızlı, kararlı ve hatasız bir altyazı ortamı sunmayı hedefler.

WHISPER CLI OLANAKLARI (Güncel - Mart 2026):
• Modeller: turbo (Varsayılan, en hızlısı), large-v3, medium, base, small, tiny.
• Çıktı Formatları: .srt, .vtt, .txt, .tsv, .json.
• Hızlandırıcılar: CUDA (NVIDIA Kartlar), MPS (Apple M serisi), CPU (Standart İşlemci).
• Temel Komutlar ve Kullanımları:
  --language: Yapay zekayı belirli bir dilde zorlamayı sağlar. Hata payını düşürür.
  --task: transcribe (metne dökme) veya translate (İngilizceye çevirme) işlemi.
  --word_timestamps: Karaoke stili veya çok detaylı kurgu işleri için kelime bazlı zamanlama açar.
  --max_line_count & --max_line_width: Altyazı satırlarının ne kadar geniş ve kaç satır olacağını kısıtlar.
  --max_words_per_line: Yukarıdaki ayar yerine ekranda tek seferde kaç kelime gözükeceğini zorlar.
  --initial_prompt: Yapay zekaya özel isimleri ve marka adlarını öğretmek için ipuçları verir.
  --condition_on_previous_text: Kesik kesik konuşmalarda anlam bütünlüğünü korumaya çalışır.
  --fp16: Matematiksel işlemleri yarım hassasiyete düşürerek devasa bir hız kazanımı sağlar.
  --temperature: Yaratıcılık düzeyi (0.0 standarttır, değiştirilmesi önerilmez).
  --beam_size: İhtimal hesaplama genişliği (Genelde 5 standarttır).
  --no_speech_threshold: Sessiz kısımların atlanma eşiğini (0.6) belirler.

PySide6 altyapısı ile maksimum sistem performansı sağlayacak şekilde kodlanmıştır."""
    },
    "en": {
        "title": "WHISPER PRO STUDIO",
        "tab_gen": "General Settings", 
        "tab_out": "Format & Timing", 
        "tab_ai": "AI & Prompt",
        "tab_fine": "Fine Tuning", 
        "tab_tech": "Technical Performance",
        "lbl_media": "Media File:", 
        "lbl_save": "Output Folder:", 
        "btn_sel": "Browse",
        "lbl_model": "Model Size:", "lbl_lang": "Source Language:", "lbl_task": "Task Type:", "lbl_dev": "Hardware Device:",
        "lbl_fmt": "Output Format:", "lbl_name": "Custom Filename:", "lbl_gap": "Continuous Subtitles (Gap Fill):",
        "lbl_gap_thresh": "Gap Threshold (Sec):",
        "lbl_time": "Word Timestamps:", 
        "lbl_line_cnt": "Max Line Count Limit:", 
        "lbl_line_wd": "Max Line Width (Chars):", 
        "lbl_max_w": "Max Words Per Line Limit:",
        "lbl_prompt": "AI Prompt (Custom names, etc):", "lbl_temp": "Temperature:", "lbl_ctx": "Condition on Previous Text:",
        "lbl_pat": "Patience:", "lbl_beam": "Beam Size:", "lbl_nospeech": "No Speech Threshold:",
        "lbl_fp16": "FP16 Acceleration:", "lbl_lenpen": "Length Penalty:", "lbl_comp": "Compression Threshold:",
        "btn_save_pre": "Save Current Settings to Profile", "btn_del_pre": "Delete Selected Profile",
        "btn_start": "START WHISPER",
        "btn_stop": "STOP PROCESS",
        "lbl_preview": "COMMAND PREVIEW",
        "lbl_log": "PROCESS STATUS & LOGS",
        "btn_load_pre": "Load Selected Profile",
        "info_dev": "DEVELOPER:",
        "info_header": "WHISPER PRO STUDIO",
        "info_desc": """This software is a professional, cross-platform GUI for OpenAI's 'Whisper' model.
It optimizes and automates complex command-line arguments to streamline subtitle creation and transcription tasks.

WHISPER CLI CAPABILITIES (March 2026):
• Models: turbo (default, fastest), large-v3, medium, base, small, tiny.
• Outputs: .srt, .vtt, .txt, .tsv, .json.
• Accelerators: CUDA (NVIDIA), MPS (Apple Silicon), CPU.
• Core Arguments:
  --language: Force a specific language.
  --task: transcribe or translate (to English).
  --word_timestamps: Essential for precise karaoke-style alignment.
  --max_line_count & --max_line_width: Native subtitle splitting rules.
  --max_words_per_line: Karaoke specific short line breaking.
  --initial_prompt: Give context or spellings for unknown terms.
  --condition_on_previous_text: Helps maintain contextual coherence across segments.
  --fp16: Forces half-precision math. Faster, but might fail on old CPUs.
  --temperature: 0.0 (Greedy) is standard.
  --beam_size: 5 is optimal.
  --no_speech_threshold: Adjusts silence filtering (0.6 default).

Built with PySide6 for maximum native OS integration and performance."""
    }
}
