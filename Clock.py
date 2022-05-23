import PySimpleGUI as sg
import threading
import datetime
import time

sg.theme('Dark Grey 13')

First = False
paused = False 
stop_flag = False
Second = 0

secondList = ['第' + str(i) + '秒' for i in range(1, 61)]

layout = [[sg.Text('每分鐘提醒秒數：', size=(14,0)), sg.DropDown(secondList, enable_events=True, key='-Second-',  default_value = '第1秒', size=(7,1), readonly=True), sg.OK('Setting')],
          [sg.Button('Exit'),  sg.Text('                             '),sg.Text('', font=('Helvetica', 14),justification='right', key='text')]]

iconBase64=b'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'

window = sg.Window('NPUST-Servitor-Auto-Sign-In', layout, icon = iconBase64)#icon = iconBase64

def time_as_int():
    return int(round(time.time() * 100))

start_time = time_as_int()

def ifTime(stop_flag):
    while True:
        if Second == 0:
            pass
        else:
            if datetime.datetime.now().strftime('%S') == str(Second.zfill(2)):
                window.write_event_value('thread task done', "success")
        time.sleep(1)

while True:
    if not paused:
        event, values = window.read(timeout=10)
    else:
        event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        stop_flag = True  
        break

    if First == False:
        First = True
        threading.Thread(target=ifTime, args=(lambda : stop_flag,)).start()

    if event == 'thread task done':
        sg.Popup('現在時間：' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), title='System Message', keep_on_top=False, icon=iconBase64)

    if event == 'Exit':
        stop_flag = True  
        window.close()

    if event == 'Setting':
        Second = values['-Second-'].split('第')[1].split('秒')[0]
        sg.Popup('秒數設定成功！', title='System Message', keep_on_top=False, icon=iconBase64)
    
    window['text'].update(datetime.datetime.now().strftime('%H:%M:%S'))

window.close()