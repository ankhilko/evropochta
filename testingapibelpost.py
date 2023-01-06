from tkinter import Button, Tk, END, Text
import requests
import win32clipboard
from time import sleep


def copy():
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    text = text_box_1.get('1.0', END)
    text = str(text)
    win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()


def paste():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    text_box.delete('1.0', END)
    text_box.insert('1.0', data)


program_window = Tk()
program_window.title('EVROPOCHTA CHECK')
program_window.minsize(width=200, height=100)
program_window.config(padx=10, pady=10)

evropochta_url = 'https://evropochta.by/api/track.json'
belpost_api = 'https://api.belpost.by/api/v1/tracking'
headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}


def request_to_api(number):
    if len(number) > 0:
        params = {'number': number}
        request = requests.post(url=evropochta_url, params=params, headers=headers)
        reply = list(request.json()['data'])[0]
        try:
            return f"EVROPOCHTA {number} => {reply['Timex']}: {reply['InfoTrack']}"
        except KeyError:
            sleep(1)
            request2 = requests.post(url=belpost_api, params=params)
            try:
                reply2 = list(request2.json()['data'])[0]['steps'][0]
                return f"BELPOST {number} => {reply2['created_at']}: {reply2['place']}: {reply2['event']}"
            except:
                return f"{number} => {reply['ErrorDescription']}"
    return ''


def clicked_1():
    text = text_box.get('1.0', END)
    text_box_1.delete('1.0', END)
    codes = []
    for item in text.split():
        codes.append(request_to_api(item))
    text_box_1.insert('1.0', '\n'.join(codes))



text_box = Text(height=6, width=20)
text_box.grid(row=0, column=3)
button_paste = Button(text='paste', command=paste)
button_paste.grid(row=0, column=4)

button = Button(text='Check the numbers', command=clicked_1)
button.grid(row=1, column=3)

text_box_1 = Text(height=12, width=100)
text_box_1.grid(row=2, column=0, columnspan=7)
button_copy = Button(text='copy', command=copy)
button_copy.grid(row=4, column=3)

program_window.mainloop()

