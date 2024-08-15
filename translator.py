import tkinter as tk
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr
import threading
import pygame
import os

pygame.mixer.init()

class Traducere:
    def __init__(self, root):
        
        self.root = root
        self.root.title("Traducere")

        self.alege_limba = tk.Label(root, text="Selecteaza limba vorbita:" , height=2, width=50)
        self.alege_limba.pack()

        self.limba_vorbita = tk.StringVar()
        self.limba_vorbita.set("ro-RO")
        self.limba_meniu = tk.OptionMenu(root, self.limba_vorbita, "ro-RO", "en-US" , "es-ES", "fr-FR", "de-DE", "it-IT")  
        self.limba_meniu.pack()

        self.limba_tradusa = tk.Label(root, text="Selecteaza limba traducerii:", height=2, width=50)
        self.limba_tradusa.pack()

        self.limba_tradusa_var = tk.StringVar()
        self.limba_tradusa_var.set("en")
        self.limba_tradusa_meniu = tk.OptionMenu(root, self.limba_tradusa_var, "es", "en", "fr" , "ro", "de", "it") 
        self.limba_tradusa_meniu.pack()

        self.start_button = tk.Button(root, text="Incepe inregistrarea", command=self.incepe_inregistrare, height=2, width=20)
        self.start_button.pack()

        self.text_spus = tk.Label(root, text="Mesajul vorbit:", height=2, width=50)
        self.text_spus.pack()

        self.text_spus_var = tk.StringVar()
        self.text_spus_introdus = tk.Entry(root, textvariable=self.text_spus_var, state=tk.DISABLED)
        self.text_spus_introdus.pack()

        self.text_tradus = tk.Label(root, text="Mesajul tradus:", height=2, width=50)
        self.text_tradus.pack()

        self.text_tradus_var = tk.StringVar()
        self.text_tradus_introdus = tk.Entry(root, textvariable=self.text_tradus_var, state=tk.DISABLED)
        self.text_tradus_introdus.pack()

        self.translator = Translator()
        self.recording = False

    def incepe_inregistrare(self):
        self.recording = True
        self.start_button.config(state=tk.DISABLED)

        def recunoastere_vocala():
            with sr.Microphone() as source:
                print("Vorbeste acum!")
                audio = r.listen(source)
                try:
                    speech_text = r.recognize_google(audio, language=self.limba_vorbita.get())
                    print(speech_text)
                    self.text_spus_var.set(speech_text)
                except sr.UnknownValueError:
                    print("Nu s-a putut intelege mesajul")
                except sr.RequestError:
                    print("Nu s-a putut realiza traducerea din Google")

                translated_text = self.translator.translate(speech_text, dest=self.limba_tradusa_var.get())
                translated_text_str = translated_text.text

                print(translated_text_str)
                self.text_tradus_var.set(translated_text_str)

                voice = gTTS(translated_text_str, lang=self.limba_tradusa_var.get())
                voice.save("voice.mp3")
                
                pygame.mixer.init()

                pygame.mixer.music.load("voice.mp3")
                pygame.mixer.music.play()
                pygame.mixer.music.get_busy()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(5)
                
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            
                filePath = 'voice.mp3'
                os.remove(filePath)


                self.recording = False
                self.start_button.config(state=tk.NORMAL)
                

        threading.Thread(target=recunoastere_vocala).start()


filePath = 'voice.mp3'
if os.path.exists(filePath):
    os.remove(filePath)
r = sr.Recognizer()

root = tk.Tk()
app = Traducere(root)
root.mainloop()