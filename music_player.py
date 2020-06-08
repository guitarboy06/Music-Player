from tkinter import *
from ttkthemes import themed_tk as tk
import tkinter.messagebox as mb
from tkinter import ttk
from tkinter import filedialog
from pygame import mixer
import os
import time
from mutagen.mp3 import MP3
import threading

'''
METHODS
'''


def start():
    global unpause, start_btn
    global music_path
    global total, current
    global select_music
    global value
    t1 = threading.Thread(target=show_details)
    try:
        if unpause:
            selected = play_list.curselection()
            select_music = int(selected[0])
            music_path = music_list[select_music]
            if start_btn:
                current = 0
                unpause = True
                song = os.path.basename(music_path)
                audio = MP3(music_path)
                total = int(audio.info.length)
                min, sec = divmod(total, 60)
                mins = round(min)
                secs = round(sec)
                stat = '{:02d}:{:02d}'.format(mins, secs)
                value = 100 / total
                statusbar['text'] = f'Playing Music {song}'
                music_total_time['text'] = stat
                mixer.music.load(music_path)
                mixer.music.play()
                music_name['text'] = song
                start_btn = False
                t1.start()
            else:
                pass
        else:
            unpause = True
            start_btn = False
            mixer.music.unpause()
            statusbar['text'] = 'Music unpaused'
            t1.start()
    except Exception:
        mb.showerror('Start error', 'No music is selected')


def stop():
    global unpause, start_btn
    global total, current, prog_stat
    global music_path
    statusbar['text'] = 'Music Stopped'
    mixer.music.stop()
    current = total + 1
    unpause = True
    music_name['text'] = 'Nothing is playing'
    music_total_time['text'] = '--:--'
    music_current_time['text'] = '--:--'
    music_path = None
    total = 0
    prog_stat = 0
    p_bar['value'] = prog_stat
    window.update_idletasks()
    start_btn = True


def pause():
    if total != 0:
        global unpause
        unpause = False
        mixer.music.pause()
        statusbar['text'] = 'Music Paused'
    else:
        mb.showerror('Pause error', 'No music is selected')


def rewind():
    try:
        if unpause:
            global current, prog_stat
            mixer.music.load(music_path)
            mixer.music.play()
            statusbar['text'] = 'Music reloaded'
            current = 0
            prog_stat = 0
            p_bar['value']=prog_stat
            window.update_idletasks()
            time.sleep(0.2)
        else:
            mb.showerror('Rewind error', 'Music is paused')
    except Exception:
        mb.showerror('Rewind error', 'No music is selected yet')


def set_vol(val):
    global vol_warning
    global volume
    global mute_vol
    volume = float(val) / 100
    if volume > 0.85:
        if vol_warning < 2:
            vol_warning += 1
            mb.showwarning('Warning!!', 'High volume can damage your ears')

    mixer.music.set_volume(volume)
    volume_btn.configure(image=volume_img)
    mute_vol = False


def mute():
    global mute_vol
    if mute_vol:
        mixer.music.set_volume(volume)
        mute_vol = False
        statusbar['text'] = 'Volume Unmuted'
        volume_btn.configure(image=volume_img)
    else:
        mixer.music.set_volume(0.0)
        statusbar['text'] = 'Volume Muted'
        volume_btn.configure(image=mute_img)
        mute_vol = True


def show_details():
    global current, value, prog_stat
    while current <= total and unpause:
        min, sec = divmod(current, 60)
        mins = round(min)
        secs = round(sec)
        stat = '{:02d}:{:02d}'.format(mins, secs)
        p_bar['value'] = prog_stat
        window.update_idletasks()
        # print(value)
        music_current_time['text'] = stat
        time.sleep(1)
        current += 1
        prog_stat += value


def about_us():
    mb.showinfo('About us', 'Hi! I am Arkadeep Nandi and this app is made by me, thanks')


def browse_file():
    global filename
    filename = filedialog.askopenfilename()


def add_to_list():
    try:
        global filename
        global music_list
        f = os.path.basename(filename)
        index = 0
        play_list.insert(index, f)
        music_list.insert(index, filename)
        index += 1
        filename = None
    except Exception:
        mb.showerror('Music List Error', 'No music is selected')


def del_music():
    try:
        global music_list
        selected = play_list.curselection()
        play_list.delete(int(selected[0]))
        music_list.pop(int(selected[0]))
    except Exception:
        mb.showerror('Music List Error', 'No music is seleced from the music list')


def on_close():
    stop()
    window.destroy()


'''
def browse_directory():
    global song_list
    global menu
    f = filedialog.askdirectory()
    song_list = os.listdir(f)
    song_listbox = StringVar(window)
    song_listbox.set("Song list")
    menu = OptionMenu(window, song_listbox)
    menu.place(x=220, y=150)
'''

'''
DECLARATION OF LAYOUTS 
'''

window = tk.ThemedTk()
window.get_themes()
window.set_theme('plastik')
# window.configure()
mixer.init()
menubar = Menu(window)
window.config(menu=menubar)
unpause = True
vol_warning = 0
# menu = None
mute_vol = False
start_btn = True
total = 0
prog_stat = 0
# current = 0
music_list = []

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open Dir", command=browse_file)
subMenu.add_command(label="Exit", command=window.destroy)

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About us", command=about_us)

# window.config(bg='Red')
window.geometry("600x400")
window.title("Music Player")
window.iconbitmap(r'C:/Users/hp/Documents/Python Files/music player/favicon.ico')
left_frame = Frame(window)
# left_frame.config(bg='#856ff8')
right_frame = Frame(window)
# right_frame.config(bg='#856ff8')
right_button_frame = Frame(right_frame)
left_button_frame = Frame(left_frame)
time_frame = Frame(right_frame, relief=SOLID)
vol_frame = Frame(right_frame)
play_img = PhotoImage(file=r'play-button.png')
stop_img = PhotoImage(file=r'stop.png')
pause_img = PhotoImage(file=r'pause-button.png')
rewind_img = PhotoImage(file='rewind.png')
volume_img = PhotoImage(file='volume.png')
mute_img = PhotoImage(file='mute.png')
p_bar = ttk.Progressbar(time_frame, orient=HORIZONTAL, length=100, mode='determinate')

l1 = Label(window, text="MUSIC PLAYER", font="times 20")
music_total_time = Label(time_frame, text='--:--')
music_current_time = Label(time_frame, text='--:--')
play_btn = ttk.Button(right_button_frame, image=play_img, command=start)
stop_btn = ttk.Button(right_button_frame, image=stop_img, command=stop)
pause_btn = ttk.Button(right_button_frame, image=pause_img, command=pause)
rewind_btn = ttk.Button(right_button_frame, image=rewind_img, command=rewind)
volume_btn = ttk.Button(vol_frame, image=volume_img, command=mute)
scale = ttk.Scale(vol_frame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(45.0)
set_vol(45.0)
statusbar = ttk.Label(window, text="Welcome to Music Player", anchor=W, relief=GROOVE, font='times 12 italic')
music_name = ttk.Label(right_frame, text='Nothing is playing', relief=SOLID, anchor=CENTER)
play_list = Listbox(left_frame)
add_btn = ttk.Button(left_button_frame, text='+ ADD', command=add_to_list)
del_btn = ttk.Button(left_button_frame, text='- DELETE', command=del_music)

'''
# song_list = os.listdir("C:/Users/hp/Documents/Python Files/music player/Disc 01")
song_listbox = StringVar(window)
song_listbox.set("Song list")
menu = OptionMenu(window, song_listbox)
'''

'''
LAYOUT PACKING IN WINDOW
'''

l1.pack()
statusbar.pack(side=BOTTOM, fill=X)
left_frame.pack(side=LEFT, padx=30)
play_list.pack()
left_button_frame.pack()
add_btn.pack(side=LEFT, padx=10, pady=5)
del_btn.pack(side=LEFT, padx=10, pady=5)
right_frame.pack(padx=5)
music_name.pack(fill=X, pady=10)
time_frame.pack()
music_total_time.pack(side=LEFT, padx=5, pady=5)
p_bar.pack(side=LEFT, padx=5, pady=5)
music_current_time.pack(side=LEFT, padx=5, pady=5)
right_button_frame.pack(pady=5)
rewind_btn.grid(row=0, column=0, padx=10)
play_btn.grid(row=0, column=1, padx=10)
pause_btn.grid(row=0, column=2, padx=10)
stop_btn.grid(row=1, column=1, pady=15)
vol_frame.pack(pady=10)
volume_btn.grid(row=0, column=0, padx=10)
scale.grid(row=0, column=1, padx=10)

# menu.place(x=220, y=150)


window.resizable(0, 0)
window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()
