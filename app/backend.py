import platform
import os
import subprocess
import shutil
import re
import tempfile
import threading
from PySide6.QtCore import QObject, Signal, QThread

class WhisperProcess(QThread):
    # Signals for updating UI
    log_signal = Signal(str)
    finished_signal = Signal(bool, str) # success, message
    
    def __init__(self, cmd, config, input_file, output_dir, parent=None):
        super().__init__(parent)
        self.cmd = cmd
        self.config = config
        self.input_file = input_file
        self.output_dir = output_dir
        self.process = None
        self._is_stopped = False
        
    def stop(self):
        self._is_stopped = True
        if self.process:
            self.process.terminate()
            
    def run(self):
        try:
            env = os.environ.copy()
            if platform.system() == "Darwin":
                env["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
                
            kwargs = {
                'stdout': subprocess.PIPE, 
                'stderr': subprocess.STDOUT, 
                'universal_newlines': True, 
                'bufsize': 1, 
                'env': env
            }
            if platform.system() == "Windows": 
                kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
                
            self.process = subprocess.Popen(self.cmd, **kwargs)
            
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    self.log_signal.emit(line)
            
            self.process.stdout.close()
            return_code = self.process.wait()
            
            if self._is_stopped:
                self.finished_signal.emit(False, "Process stopped by user.")
                return

            if return_code == 0:
                input_basename = os.path.splitext(os.path.basename(self.input_file))[0]
                
                # Gap filling
                if self.config.get("gap_filling", False):
                    srt_file = os.path.join(self.output_dir, input_basename + ".srt")
                    if os.path.exists(srt_file):
                        count = post_process_gaps(srt_file, self.config.get("gap_threshold", 2.0))
                        self.log_signal.emit(f"\n>>> GAP FILLING: {count} gaps closed.\n")
                
                # Renaming
                custom_name = self.config.get("custom_filename", "").strip()
                if custom_name:
                    safe_custom_name = os.path.basename(custom_name.replace('\\', '/'))
                    rename_output_files(self.output_dir, input_basename, safe_custom_name, self.log_signal)
                    
                self.finished_signal.emit(True, "Transcription completed successfully!")
            else:
                self.finished_signal.emit(False, "Process ended with an error.")
                
        except Exception as e:
            if not self._is_stopped:
                self.finished_signal.emit(False, f"Error: {str(e)}")

def time_to_seconds(time_str):
    time_str = time_str.replace(',', '.')
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

def post_process_gaps(filepath, threshold):
    try:
        target_dir = os.path.dirname(filepath)
        temp_fd, temp_path = tempfile.mkstemp(suffix=".srt", dir=target_dir, text=True)
        updated_count = 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            blocks = f.read().split('\n\n')
        
        parsed_blocks = []
        pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2}[,.]\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2}[,.]\d{3})\n(.*)', re.DOTALL)
        
        for block in blocks:
            block = block.strip()
            if not block: continue
            m = pattern.match(block)
            if m:
                parsed_blocks.append({
                    'idx': int(m.group(1)), 
                    'start_str': m.group(2), 
                    'end_str': m.group(3), 
                    'start': time_to_seconds(m.group(2)), 
                    'end': time_to_seconds(m.group(3)), 
                    'text': m.group(4).strip()
                })

        for i in range(len(parsed_blocks) - 1):
            current_block = parsed_blocks[i]
            next_block = parsed_blocks[i+1]
            gap = next_block['start'] - current_block['end']
            if 0.001 < gap < threshold:
                current_block['end'] = next_block['start']
                current_block['end_str'] = next_block['start_str']
                updated_count += 1
        
        with os.fdopen(temp_fd, 'w', encoding='utf-8') as out_f:
            for b in parsed_blocks:
                out_f.write(f"{b['idx']}\n{b['start_str']} --> {b['end_str']}\n{b['text']}\n\n")

        os.replace(temp_path, filepath)
        return updated_count
    except Exception as e:
        print(f"Gap filling error: {e}")
        return 0

def rename_output_files(output_dir, old_name, new_name, log_signal=None):
    try:
        renamed_count = 0
        extensions = [".srt", ".txt", ".vtt", ".json", ".tsv"]
        for ext in extensions:
            old_file = os.path.join(output_dir, old_name + ext)
            new_file = os.path.join(output_dir, new_name + ext)
            if os.path.exists(old_file):
                if os.path.exists(new_file): 
                    os.remove(new_file)
                os.rename(old_file, new_file)
                renamed_count += 1
                if log_signal:
                    log_signal.emit(f"\n>>> RENAMED: {old_name}{ext} -> {new_name}{ext}\n")
        if renamed_count == 0 and log_signal:
            log_signal.emit("\n>>> WARNING: No files found to rename.\n")
    except Exception as e:
        if log_signal:
            log_signal.emit(f"\n>>> ERROR (Renaming): {str(e)}\n")

def build_whisper_command(config):
    cmd = []
    whisper_path = shutil.which("whisper")
    if whisper_path: 
        cmd.append(whisper_path)
    else: 
        cmd.append("whisper")
        
    cmd.append(config.get("file", "video.mp4"))
    
    model = config.get("model", "turbo")
    # Whisper'ın yeni default modeli turbo, eskiden large-v3 idi. Gereksiz argümanı eklememek için kontrol ediyoruz.
    if model != "turbo": 
        cmd.extend(["--model", model])
        
    lang_val = config.get("lang", "auto")
    lang_code = lang_val.split(" - ")[0] if " - " in lang_val else lang_val
    if lang_code != "auto": 
        cmd.extend(["--language", lang_code])
        
    task = config.get("task", "transcribe")
    if task != "transcribe": 
        cmd.extend(["--task", task])
        
    cmd.extend(["--output_dir", config.get("out_dir", "")])
    cmd.extend(["--device", config.get("device", "cpu")])
    
    fmt = config.get("fmt", "srt")
    if fmt != "all": 
        cmd.extend(["--output_format", fmt])
        
    if config.get("device", "cpu") == "mps":
        # Force Word Timestamps False on MPS to prevent TypeError: Cannot convert a MPS Tensor to float64
        cmd.extend(["--word_timestamps", "False"])
    elif config.get("word_ts", True): 
        cmd.extend(["--word_timestamps", "True"])
    
    if config.get("use_lines", True):
        cmd.extend(["--max_line_count", str(config.get("max_line", 2))])
    if config.get("use_width", False):
        cmd.extend(["--max_line_width", str(config.get("line_width", 42))])
    if config.get("use_words", False):
        cmd.extend(["--max_words_per_line", str(config.get("max_word", 7))])
        
    prompt = config.get("prompt", "").strip()
    if prompt: 
        cmd.extend(["--initial_prompt", prompt])
        
    temp = config.get("temp", 0.0)
    if temp != 0.0: 
        cmd.extend(["--temperature", str(temp)])
        
    beam = config.get("beam", 5)
    if beam != 5: 
        cmd.extend(["--beam_size", str(beam)])
        
    no_speech = config.get("no_speech", 0.6)
    if no_speech != 0.6: 
        cmd.extend(["--no_speech_threshold", str(no_speech)])
        
    if config.get("device", "cpu") == "mps":
        # Force FP16 False on MPS to prevent NaN/crashes as per user feedback
        cmd.extend(["--fp16", "False"])
    elif not config.get("fp16", False): 
        cmd.extend(["--fp16", "False"])
        
    if not config.get("condition", True): 
        cmd.extend(["--condition_on_previous_text", "False"])
        
    cmd.extend(["--patience", str(config.get("patience", 1.0))])
    cmd.extend(["--length_penalty", str(config.get("len_pen", 1.0))])
    
    comp = config.get("comp", 2.4)
    if comp != 2.4: 
        cmd.extend(["--compression_ratio_threshold", str(comp)])
        
    return cmd