import requests
from bs4 import BeautifulSoup
import json
import tkinter

url = "https://nightwalker.nexon.com/ranking/rank"

# 220 : 마야
# 221 : 바르바토스

# 1 : 마리 (아발란체 / 아이언피스트)
# 2 : 맥 (바이퍼 / 트러블슈터)
# 6 : 오드리 (헤비암즈 / 센티넬)
# 8 : 아라 (파랑매 / 네레이스)
# 11 : 갈가마귀 (그림자의 왕 / 그림자 인형사)
# 14 : B (적면귀 / 팬텀 블레이드)

rank = {
    220 : {
        1 : {
            1 : {},
            2 : {}
        },
        2 : {
            1 : {},
            2 : {}
        },
        6 : {
            1 : {},
            2 : {}
        },
        8 : {
            1 : {},
            2 : {}
        },
        11 : {
            1 : {},
            2 : {}
        },
        14 : {
            1 : {},
            2 : {}
        },
    },
    221 : {
        1 : {
            1 : {},
            2 : {}
        },
        2 : {
            1 : {},
            2 : {}
        },
        6 : {
            1 : {},
            2 : {}
        },
        8 : {
            1 : {},
            2 : {}
        },
        11 : {
            1 : {},
            2 : {}
        },
        14 : {
            1 : {},
            2 : {}
        },
    }
}

for world_id in rank:
    for job in rank[220]:
        for job_type in range(1,3):
            payload = {
                'type' : "score",
                'world_id' : world_id,
                'job' : job,
                'job_type' : job_type
                }

            response1 = requests.post(url, json = payload)
            source = json.loads(response1.text)

            UnitRank = {}
            highscore = int(source['msg']['ranking_list'][0]['score'])//1000

            for i in range(1000):
                if int(source['msg']['ranking_list'][i]['score'])//1000 < highscore:
                    UnitRank[str(highscore)+'k'] = source['msg']['ranking_list'][i]['rank']-1
                    highscore = int(source['msg']['ranking_list'][i]['score'])//1000

            rank[world_id][job][job_type] = UnitRank

        with open('data.json', 'w') as f:
            json.dump(rank, f)

with open('data.json', 'r') as f:
    rank = json.load(f)

window = tkinter.Tk()

window.title("NightwalkerRank")
window.geometry("200x350")

joblist = ['아발란체', '아이언피스트', '바이퍼', '트러블슈터', '헤비암즈', '센티넬', '파랑매', '네레이스', '그림자의 왕', '그림자 인형사', '적면귀', '팬텀 블레이드']
jobcode = {
    '아발란체' : 2,
    '아이언피스트' : 3,
    '바이퍼' : 4,
    '트러블슈터' : 5,
    '헤비암즈' : 12,
    '센티넬' : 13,
    '파랑매' : 16,
    '네레이스' : 17,
    '그림자의 왕' : 22,
    '그림자 인형사' : 23,
    '적면귀' : 28,
    '팬텀 블레이드' : 29
    }

joblistbox = tkinter.Listbox(window, selectmode='browse', height=0, width=0, activestyle='none')
for i in jobcode:
    joblistbox.insert(jobcode[i], i)
joblistbox.grid(row=1,column=1,pady=10,padx=10)

def select():
    name = joblist[joblistbox.curselection()[0]]
    if server.get() == 220:
        jobname.configure(text='마야서버\n' + name)
    else:
        jobname.configure(text='바르바토스서버\n' + name)

    a = 0
    b = 1
    if (jobcode[f'{name}'] % 2) == 0:
        a = jobcode[f'{name}'] // 2
    else:
        a = (jobcode[f'{name}'] - 1) // 2
        b = 2

    source = rank[f'{server.get()}'][f'{a}'][f'{b}']
    
    script = f'{list(source.keys())[0]} : {list(source.values())[0]}명'
    for i in range(1,len(source)):
        script = script + f'\n{list(source.keys())[i]} : {list(source.values())[i]}명'
    ranking.configure(text=script)

jobname = tkinter.Label(window, text='서버명\n직업명')
jobname.grid(row=2,column=1)

selcectButton = tkinter.Button(window, command=select, text='랭킹확인')
selcectButton.grid(row=3,column=1,pady=5)

server = tkinter.IntVar()
server1 = tkinter.Radiobutton(window, text='마야', value=220, variable=server)
server2 = tkinter.Radiobutton(window, text='바르바토스', value=221, variable=server)
server1.grid(row=4,column=1)
server2.grid(row=5,column=1)
server1.select()

ranking = tkinter.Label(window)
ranking.grid(row=1,column=2,rowspan=99,padx=5)

window.mainloop()