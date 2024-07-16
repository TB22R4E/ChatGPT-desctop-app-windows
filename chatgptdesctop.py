import customtkinter
from tkinter import *
import tkinter
from openai import OpenAI
from PIL import Image, ImageTk
import pyautogui
import time
import base64
import re
import requests
from bs4 import BeautifulSoup
from tkinter.font import Font
import openai
from pathlib import Path
from playsound import playsound
from tkinterdnd2 import TkinterDnD, DND_ALL
import pywinstyles
from hPyT import *
from pypdf import PdfReader
import os
from pathlib import Path
import threading
import pandas as pd
from docx import Document
import random
import anthropic

anthropic_client = anthropic.Anthropic(api_key="your-api-key")

openai = OpenAI(api_key="your-api-key")
openai.api_key="your-api-key"
voicemode = False
model_llm = 'gpt4'
genAi = True
dodaniepliku = False
dodanielinku = False
webs = False

customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk(fg_color='#202020')
app.geometry("610x770")
app.title('LLM TBSoftwareAI Desctop App')
app.iconbitmap('tb.ico')
maximize_minimize_button.hide(app)

attimg = customtkinter.CTkImage(Image.open("att.png"))
vii = customtkinter.CTkImage(Image.open("vii.png"), size=(100, 67))
vii2 = customtkinter.CTkImage(Image.open("viih.png"), size=(100, 67))
mici = customtkinter.CTkImage(Image.open("mici.png"), size=(100, 67))
mici2 = customtkinter.CTkImage(Image.open("micih.png"), size=(100, 67))
logo = customtkinter.CTkImage(Image.open("log.png"), size=(100, 67))
logo2 = customtkinter.CTkImage(Image.open("logh.png"), size=(100, 67))
logo21 = customtkinter.CTkImage(Image.open("logh2.png"), size=(100, 67))
logo22 = customtkinter.CTkImage(Image.open("logh3.png"), size=(100, 67))
logo23 = customtkinter.CTkImage(Image.open("logh4.png"), size=(100, 67))
logo24 = customtkinter.CTkImage(Image.open("logh5.png"), size=(100, 67))
logo25 = customtkinter.CTkImage(Image.open("logh6.png"), size=(100, 67))

logo3 = customtkinter.CTkImage(Image.open("bsai.png"), size=(172, 50))
histconv = []

my_font = customtkinter.CTkFont(family="Segoe UI", size=14)
my_font2 = customtkinter.CTkFont(family="Segoe UI", size=12, weight='bold')
my_font3 = customtkinter.CTkFont(family="Segoe UI", size=12)
line_space = my_font.metrics("linespace")

def openaitts(event=None):
    butmi.configure(image=mici2)
    def ttsmake():
        speech_file_path = Path(__file__).parent / "speech.mp3"
        response = openai.audio.speech.create(
            model="tts-1",
            voice="shimmer",
            speed=1,
            input=app.clipboard_get()
            )
        response.stream_to_file(speech_file_path)
        playsound(speech_file_path)
    
       

    
    threading.Thread(target=ttsmake).start()
    butmi.configure(image=mici)

def zmienlink(event=None):
    global dodanielinku
    dodanielinku = True

def stopgen(event=None):
    def changegen():
        global genAi
        genAi = False
    threading.Thread(target=changegen).start()
    

def radiobutton_event():
    global model_llm
    global histconv
    wybrany = radio_var.get()
    if wybrany == 1:
        model_llm = 'gpt4'
        if len(histconv) > 0:
            newHist = []
            for i in histconv:
                if i['role'] == 'user':
                    print(type(i['content']))
                    if isinstance(i['content'], list):
                        print('lista joł')
                        i = {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Udostępniam Ci widok mojego pulpitu komputera i zaraz powiem Ci co chce żebyć zrobił."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{i['content'][0]['source']['data']}"
                                            },
                            }
                        ]
                    }
                        print(i['content'][0])
                newHist.append(i)
            histconv = newHist
            
    elif wybrany == 2:
        model_llm = 'claude'
        if len(histconv) > 0:
            newHist = []
            for i in histconv:
                if i['role'] == 'user':
                    print(type(i['content']))
                    if isinstance(i['content'], list):
                        print('lista joł')
                        urlbase = i['content'][1]['image_url']['url']
                        i = {
                        "role": "user",
                        "content": [
                            
                            {
                                "type": "image",
                                "source": {
                                    "type": 'base64',
                                    "media_type": "image/jpeg",
                                    "data": urlbase.replace('''data:image/jpeg;base64,''', '')
                                            },
                            }
                        ]
                    }
                        print(i['content'][0])
                newHist.append(i)
            histconv = newHist

def google_search(query):
        global webs
        webs = True
        endpoint = "https://www.googleapis.com/customsearch/v1"
        params = {
            'q': query,
            'key': 'your-api-key',
            'cx': 'your-cx-key',
            'num': 5
        }
        response = requests.get(endpoint, params=params)
        return response.json()

def add_message_to_chat(text, is_user=True):
    
    inpp.delete(0, 'end')
    label = customtkinter.CTkLabel(master=ramcia, text=text, fg_color='#303030', wraplength=540, anchor='w', justify='left', corner_radius=25, font=my_font, pady=10)
    
    label.pack(pady=10, padx=30, anchor='e')
    ramcia._parent_canvas.yview_moveto(1.0)
    app.update()

def process_file_content(file_path, content):
    histconv.append({
        "role": "user",
        "content": f'Wklejam Ci treść dokumentu, którym chcę żebyśmy się zajęli:\n\n<dokument>\n\n---------------------------------\n\n{content}</dokument>'
    })
    add_message_to_chat('📃 ' + file_path, is_user=True)
    ramcia._parent_canvas.yview_moveto(1.0)
    app.update()
    global dodaniepliku
    dodaniepliku = True
    send_gpt()

def drop_func(file):
    file_path = file[0]
    file_name = os.path.basename(file_path).lower()

    try:
        if re.match(r'^[a-z0-9\:\s!@#$%^&*=._{}()\-]+\.pdf$', file_name):
            reader = PdfReader(file_path)
            dokument = [page.extract_text() for page in reader.pages]
            combined_text = '\n\n---------------------------------\n\n'.join(dokument)
            process_file_content(file_path, combined_text)

        elif re.match(r'^[a-z0-9\:\s!@#$%^&*=._{}()\-]+\.xlsx?$', file_name):
            plikex = pd.read_excel(file_path)
            combined_text = '\n'.join(plikex.apply(lambda row: ' '.join(row.astype(str)), axis=1))
            process_file_content(file_path, combined_text)

        elif re.match(r'^[a-z0-9\:\s!@#$%^&*=._{}()\-]+\.csv$', file_name):
            plikex = pd.read_csv(file_path)
            combined_text = '\n'.join(plikex.apply(lambda row: ' '.join(row.astype(str)), axis=1))
            process_file_content(file_path, combined_text)

        elif re.match(r'^[a-z0-9\:\s!@#$%^&*=._{}()\-]+\.docx?$', file_name):
            doc = Document(file_path)
            combined_text = '\n'.join([para.text for para in doc.paragraphs])
            process_file_content(file_path, combined_text)

        elif re.match(r'^[a-z0-9\:\s!@#$%^&*=._{}()\-]+\.txt$', file_name):
            with open(file_path, 'r', encoding='utf-8') as tekstowy:
                combined_text = tekstowy.read()
            process_file_content(file_path, combined_text)

        else:
            print(f"Unsupported file format: {file_name}")

    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

def histconvch(event=None):
    global histconv
    histconvn = histconv[:(len(histconv) - 1)]
    histconv = histconvn

def send_gpt(event=None):
    olok = inpp.get()
    print(olok)
    addusermes = True
    visionprogresbar = None
    webpat = r'^web\: '
    linkpat = r'^link\: '
    linkhttps = r'^https\:\/'
    linkgl = re.match(linkhttps, olok)
    
    if linkgl != None:
        
        print('link')
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "sec-ch-ua": """"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109" """,
            "sec-ch-ua-platform": "Windows",
            "sec-ch-ua-mobile": "?0",
            "referer": "https://google.com",
            "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        # soup = BeautifulSoup()
        
        
        
        # print(linki)

        
        r = requests.get(olok, headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()
        soup = soup.get_text()
        soup = soup.strip()
        teks = soup.replace("\n\n", " ").replace("\n", " ").replace("  ", " ")
        # dek = re.sub(" +", " ", teks)
        dek2 = teks.replace("  ", " ")
        
        
        
        
        histconv.append({"role": "user", 
                         "content": 'Wklejam Ci informacje ze strony www:' + '\n\n' + '<informacje>' + '\n\n' + dek2 + '\n\n' + '</informacje>\n\nBazując na tych wiadomościach zrób streszczenie i przedstaw najistotniejsze rzeczy.'})


    if re.match(linkpat, olok):
        zmienlink()

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "sec-ch-ua": """"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109" """,
            "sec-ch-ua-platform": "Windows",
            "sec-ch-ua-mobile": "?0",
            "referer": "https://google.com",
            "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        

        
        r = requests.get(olok.split('link: ')[1].split(' | ')[0], headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()
        soup = soup.get_text()
        soup = soup.strip()
        teks = soup.strip()
        # dek = re.sub(" +", " ", teks)
        dek2 = teks.replace("  ", " ")
        
        
        
        
        histconv.append({"role": "user", 
                         "content": 'Wklejam Ci informacje ze strony www:' + '\n\n' + '<informacje>' + '\n\n' + '\n\n' + '</informacje>\n\nBazując na tych wiadomościach wykonaj polecenie:\n\n' + olok.split(' | ')[1]})

    
    if re.match(webpat, olok):
        
        add_message_to_chat(olok, is_user=True)
        ai_label = customtkinter.CTkLabel(master=ramcia, text='Szukam informacji na temat: ' + olok.split(': ')[1] + '..', wraplength=500, anchor='w', justify='left', corner_radius=25, font=my_font2, text_color='#00ffff')
        ai_label.pack(pady=10, padx=10, anchor='w')
        addusermes = False
        linki = []
        results = google_search(olok.split('web: ')[1])
        for item in results.get('items', []):
            linki.append(item['link'])

        tekostr = ""

        for lin in linki:
            if len(lin) > 40:
                lin = lin[:40]
                tekostr += '🌐 ' + lin + '\n'
        ai_label = customtkinter.CTkLabel(master=ramcia, text=tekostr, wraplength=500, anchor='w', justify='left', corner_radius=25, font=my_font3, text_color='#00ffff')
        ai_label.pack(pady=10, padx=10, anchor='w')

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "sec-ch-ua": """"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109" """,
            "sec-ch-ua-platform": "Windows",
            "sec-ch-ua-mobile": "?0",
            "referer": "https://google.com",
            "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        
        
        teksty = []
        daneDoAI = []
        
        
        
        visionprogresbar = customtkinter.CTkProgressBar(master=ramcia, orientation='horizontal', determinate_speed=3, height=3, progress_color='#00ffff')
        visionprogresbar.pack(pady=10, padx=25, anchor='w')
        visionprogresbar.set(0)
        liczniklink = 0.2
        for inmo in linki:
            try:
                visionprogresbar.set(liczniklink)
                liczniklink += 0.2
                r = requests.get(inmo, headers=headers)
                soup = BeautifulSoup(r.content, "html.parser")
                for script_or_style in soup(['script', 'style']):
                    script_or_style.decompose()
                soup = soup.get_text()
                soup = soup.strip()
                if len(soup) > 5000:
                    pass
                teks = soup.strip()
                
                dek2 = teks.replace("  ", " ")
                
                teksty.append(dek2)
            except:
                teksty.append('\n\nBłędny link\n\n')
        
        
        histconv.append({"role": "user", 
                         "content": 'Wklejam Ci informacje z internetu:' + '\n\n' + '<informacje>' + '\n\n-------------------------------------------\n\n'.join(teksty) + '</informacje>\n\nBazując na tych wiadomościach odpowiedz na pytanie:\n\n' + olok.split('web: ')[0]})

    if olok == 'vision':
        addusermes = False
        butvi.configure(image=vii2)
        inpp.delete(0, 'end')
        ai_label = customtkinter.CTkLabel(master=ramcia, text='👁️‍🗨️' + ' Okey, rzucę okiem na Twój ekran..', wraplength=500, anchor='w', justify='left', corner_radius=25, font=my_font2, text_color='#00ffff')
        ai_label.pack(pady=10, padx=10, anchor='w')
        visionprogresbar = customtkinter.CTkProgressBar(master=ramcia, orientation='horizontal', determinate_speed=3, height=3, progress_color='#00ffff')
        visionprogresbar.pack(pady=10, padx=25, anchor='w')
        visionprogresbar.set(0)
        screenshot = pyautogui.screenshot(region=(2460, 0, 2660, 1440))
        screenshot.save('screenshot.jpg',)
        
        for t in range(10):
            print(t)
            visionprogresbar.step()
            visionprogresbar.update_idletasks()
            time.sleep(0.2)
        with open("screenshot.jpg", "rb") as image_file:
            ssss = base64.b64encode(image_file.read()).decode('utf-8')
        visionprogresbar.set(0.8)
        
        if model_llm == 'gpt4':
            visioprom = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Udostępniam Ci widok mojego pulpitu komputera i zaraz powiem Ci co chce żebyć zrobił."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{ssss}"
                                            },
                            }
                        ]
                    }
                ]
        elif model_llm == 'claude':
            visioprom = [
                    {
                        "role": "user",
                        "content": [
                            
                            {
                                "type": "image",
                                "source": {
                                    "type": 'base64',
                                    "media_type": "image/jpeg",
                                    "data": ssss
                                            },
                            }
                        ]
                    }
                ]
            
        histconv.append(visioprom[0])
        
        butvi.configure(image=vii)
    elif olok == 'clear':
        
        histconv.clear()
        olok = 'Cześć, zacznijmy nową rozmowę...'
        histconv.append({"role": "user", "content": olok})

    elif olok == 'clear vision':
        for i in histconv:
            if i['role'] == 'user':
                print(type(i['content']))
                if type(i['content']) == 'list':
                    i['content'] = i['content'][0]['text']
        
        olok = 'W porządku..'
        histconv.append({"role": "user", "content": olok})

    else:
        if not olok.strip():  
            return
        
        histconv.append({"role": "user", "content": olok})
    if addusermes:
        add_message_to_chat(olok, is_user=True)
    else:
        addusermes = True
    
    kropa = '⏺'

    ai_label = customtkinter.CTkLabel(master=ramcia, text='', wraplength=500, anchor='w', justify='left', corner_radius=25, font=my_font)
    ai_label.pack(pady=10, padx=10, anchor='w')
    ramcia._parent_canvas.yview_moveto(1.0)
    app.update()
    
    full_response = ""
    tekstdowyp = ""
    teksopat = r'[A-Za-z]*[,.!?]$'
    if visionprogresbar is not None:
        visionprogresbar.set(0.9)
    
    def get_llm():
        global model_llm
        wybrany = model_llm
        return wybrany
    global genAi

    if get_llm() == 'gpt4':
        global dodaniepliku
        global dodanielinku
        global webs
        if dodaniepliku == True or dodanielinku == True or webs == True:
            if histconv[len(histconv) - 1]['role'] == 'user' and histconv[len(histconv) - 2]['role'] == 'user':
                    
                    nownow = histconv[len(histconv) - 2]['content'] + '\n\n' + histconv[len(histconv) - 1]['content']
                    histconv[len(histconv) - 2]['content'] = nownow
                    histconvch()
            dodaniepliku = False
            dodanielinku = False
            webs = False
        completion = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant named EvaAI. Chce żebyć zawsze odpowiadał jako kobieta. Musisz udzielać odpowiedzi w sposób bardzo konwersacyjny i ludzki. Nawiązuj do uczuć i człowieczeństwa. Staraj się udzielać odpowiedzi w jak najbardziej ludzki sposób. Odpowiedzi mają być trochę ironiczne kiedy tematy są luźne. Ja mam na imię Bartek."}
            ] + histconv,
            stream=True
        )
        
        if visionprogresbar is not None:
            visionprogresbar.set(1)
        for chunk in completion:
            
            if genAi == False:
                
                genAi = True
                ai_label.configure(text=full_response.strip() + '...')
                break
            getlogotop = random.choice([logo2, logo21, logo22, logo23, logo24, logo25])
            butmilog.configure(image=getlogotop)
            butstop.configure(text='◼')
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                
                ai_label.configure(text=full_response.strip() + ' 💬')
                ramcia._parent_canvas.yview_moveto(1.0)
                app.update()
            else:
                ai_label.configure(text=full_response.strip())

    if get_llm() == 'claude':
        dodaniepliku = False
        dodanielinku = False
        webs = False
        if len(histconv) > 1:
            if histconv[len(histconv) - 1]['role'] == 'user' and histconv[len(histconv) - 2]['role'] == 'user':
                    
                    nownow = histconv[len(histconv) - 2]['content'] + '\n\n' + histconv[len(histconv) - 1]['content']
                    histconv[len(histconv) - 2]['content'] = nownow
                    histconvch()
                
            
        with anthropic_client.messages.stream(
            max_tokens=3894,
            model="claude-3-5-sonnet-20240620",
            system="You are a helpful assistant named EvaAI. Chce żebyć zawsze odpowiadał jako kobieta. Musisz udzielać odpowiedzi w sposób bardzo konwersacyjny i ludzki. Nawiązuj do uczuć i człowieczeństwa. Staraj się udzielać odpowiedzi w jak najbardziej ludzki sposób. Odpowiedzi mają być trochę ironiczne kiedy tematy są luźne. Ja mam na imię Bartek.",
            messages=histconv,
            
        ) as stream:
        
        
            for chunk in stream.text_stream:
                
                if genAi == False:
                    
                    genAi = True
                    ai_label.configure(text=full_response.strip() + '...')
                    break
                getlogotop = random.choice([logo2, logo21, logo22, logo23, logo24, logo25])
                butmilog.configure(image=getlogotop)
                butstop.configure(text='◼')
                full_response += chunk
                # tekstdowyp += chunk.choices[0].delta.content
                
                ai_label.configure(text=full_response.strip() + ' 💬')
                ramcia._parent_canvas.yview_moveto(1.0)
                app.update()
            
            
            ai_label.configure(text=full_response.strip())

    butmilog.configure(image=logo)
    butstop.configure(text='')
    if voicemode:
        openaitts(full_response)
        
    app.clipboard_clear()
    app.clipboard_append(full_response)
    
    

    histconv.append({"role": "assistant", "content": full_response})
    def histplik(hist):
        def zapisanie(hist):
            with open('histconv.txt', 'w', encoding='utf-8') as plipli:
                plipli.writelines(str(hist))
        threading.Thread(target=zapisanie(hist)).start()
        
    histplik(histconv)
    

def visionscreen(event=None):
    inpp.insert(0, 'vision')   
    send_gpt()             
    
    

toop = customtkinter.CTkFrame(master=app, height=100, width=600, fg_color='#202020')
toop.pack(side='top', pady=20)

topmic = customtkinter.CTkFrame(master=toop, fg_color='#202020', width=190, height=100)
topmic.pack(side='left')

butmi = customtkinter.CTkButton(master=topmic, text='', width=190, height=100, fg_color='transparent', image=mici, command=openaitts)
butmi.pack()

tophist = customtkinter.CTkFrame(master=toop, fg_color='#202020', width=190, height=100)
tophist.pack(side='left')
butmilog = customtkinter.CTkButton(master=tophist, text='', width=190, height=100, fg_color='transparent', image=logo)
butmilog.pack()

topview = customtkinter.CTkFrame(master=toop, fg_color='#202020', width=190, height=100)
topview.pack(side='left')

butvi = customtkinter.CTkButton(master=topview, text='', width=190, height=100, fg_color='transparent', image=vii,command=visionscreen)
butvi.pack()

moop = customtkinter.CTkFrame(master=app, height=450, width=600, fg_color='#202020')
moop.pack(side='top')


llmswi = customtkinter.CTkFrame(master=app, height=40, width=600, fg_color='#202020')
llmswi.pack(side='top', anchor='w',  padx=30, pady=10)
radio_var = tkinter.IntVar(value=1)
radiobutton_1 = customtkinter.CTkRadioButton(master=llmswi, text="GPT-4o",
                                             command=radiobutton_event, variable= radio_var, value=1, fg_color='#00ffff', border_color='white', hover_color='#00ffff', border_width_checked=4, border_width_unchecked=2, text_color='white', text_color_disabled='white')
radiobutton_1.pack(anchor='w', side='left')
radiobutton_2 = customtkinter.CTkRadioButton(master=llmswi, text="Claude-3.5-Sonet",
                                             command=radiobutton_event, variable= radio_var, value=2, fg_color='#00ffff', border_color='white', hover_color='#00ffff', border_width_checked=4, border_width_unchecked=2, text_color='white', text_color_disabled='white')
radiobutton_2.pack(anchor='w', side='left')


butstop = customtkinter.CTkButton(master=llmswi, text='', fg_color='transparent', height=20, width=30, corner_radius=25, text_color='white', command=stopgen, anchor='e')
butstop.pack(anchor='e', side='right', padx=30)


boop = customtkinter.CTkFrame(master=app, height=50, width=600, fg_color='#202020')
boop.pack(side='top', pady=10)


aibot = customtkinter.CTkFrame(master=boop, fg_color='#202020', width=600, height=50)
aibot.pack(side='left')


inpp = customtkinter.CTkEntry(master=aibot, placeholder_text="Type here or drop file..", width=570, height=40, fg_color='#202020', font=my_font, corner_radius=25)
inpp.pack()
inpp.bind('<Return>', send_gpt)
pywinstyles.apply_dnd(inpp, drop_func)

ramcia = customtkinter.CTkScrollableFrame(master=moop, 
                                          scrollbar_button_color='#202020',
                                          scrollbar_fg_color='#202020',
                                          fg_color='#202020', label_anchor='w', width=600, height=450)
ramcia.pack(expand=True, fill='both')

botto = customtkinter.CTkFrame(master=app, height=50, width=600, fg_color='#202020')
botto.pack(side='top')

bofr = customtkinter.CTkFrame(master=botto, fg_color='#202020', width=600, height=50)
bofr.pack()

bofrbut = customtkinter.CTkButton(master=bofr, text='', width=600, height=50, fg_color='transparent', image=logo3)
bofrbut.pack()


app.mainloop()


