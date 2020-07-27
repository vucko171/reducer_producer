from tkinter import *
from tkinter import scrolledtext
import re

def outAll(Under,Cammel):
    print(Under,Cammel)
    strInitOut=""
    strReduOut=""
    strActiOut=""
    for x in range(len(min(Under,Cammel))):
        if len(Under[x])!=0:
            strInitOut+=Under[x].lower()+": '',\n"
            strReduOut+="      case `@servicerequest/SET_"+Under[x].upper()+"`:\n        draft.detGeneralInfo."+Under[x].lower()+" = action.payload.data;\n        break;\n"
            strActiOut+="export function set"+Cammel[x]+"(data) {\n  return {\n    type: `@servicerequest/SET_"+Under[x].upper()+"`,\n    payload: {\n      data,\n    },\n  };\n}\n"
            print(Under[x],Cammel[x])
    InitOut.delete(1.0,"end")
    InitOut.insert(1.0,strInitOut)
    ReduOut.delete(1.0,"end")
    ReduOut.insert(1.0,strReduOut)
    ActiOut.delete(1.0,"end")
    ActiOut.insert(1.0,strActiOut)
    UInp.delete(1.0,"end")
    UInp.insert(1.0,"\n".join(Under))
    CInp.delete(1.0,"end")
    CInp.insert(1.0,"\n".join(Cammel))


def conv2Cammel(data):
    for x in range(len(data)):
        temp=re.findall('^(?:(.)(.*?)_)?(?:(.)(.*?)_)?(?:(.)(.*?)_)?(?:(.)(.*?)_)?(?:(.)(.*?)_)?(?:(.)(.*?)_)?(?:(.)(.*?)_)?(.)(.*?)$',data[x])
        str=""
        if len(temp)!=0:
            temp=temp[0]
            for y in range(len(temp)):
                str+=temp[y]*(y%2)+temp[y].upper()*((y+1)%2)
        data[x]=str
    return data

def conv2Under(data):
    for x in range(len(data)):
        temp=re.findall('^([A-Z]?[a-z]*?)(?:([A-Z][a-z]*?))?(?:([A-Z][a-z]*?))?(?:([A-Z][a-z]*?))?(?:([A-Z][a-z]*?))?(?:([A-Z][a-z]*?))?(?:([A-Z][a-z]*?))?(?:([A-Z][a-z]*?))?$',data[x])
        str=""
        if len(temp)!=0:
            temp=temp[0]
            for y in range(len(temp)-1,0,-1):
                if len(temp[y])!=0:
                    str="_"+temp[y].lower()+str
            str=temp[0].lower()+str
        data[x]=str
    return data

master = Tk()
master.resizable(0,0)
inputFrame = Frame(master, width=600)
inputFrame.pack(padx=30, pady=30)

ULbl = Label(inputFrame, text="variable(s) with underscore")
ULbl.grid(column=0,row=0)

CLbl = Label(inputFrame, text="variable(s) with camelCase")
CLbl.grid(column=2,row=0)

def onUnder(*args):
    Under=UInp.get(1.0,'end-1c').split("\n")
    Under=[x.lower() for x in Under]
    Cammel=conv2Cammel(UInp.get(1.0,'end-1c').split("\n"))
    Cammel=[x[0].upper()+x[1:] if len(x)>0 else "" for x in Cammel]
    outAll(Under,Cammel)

UInp = scrolledtext.ScrolledText(inputFrame, width=30, height=2)
UInp.grid(column=0,row=1)
UInp.focus_set()
UInp.bind('<KeyRelease>', onUnder)

blankInp = Label(inputFrame, text="", width=2)
blankInp.grid(column=1,row=1)

def onCammel(*args):
    Cammel=CInp.get(1.0,'end-1c').split("\n")
    Cammel=[x[0].upper()+x[1:] if len(x)>0 else "" for x in Cammel]
    Under=conv2Under(CInp.get(1.0,'end-1c').split("\n"))
    Under=[x.lower() for x in Under]
    outAll(Under,Cammel)

CInp = scrolledtext.ScrolledText(inputFrame, width=30, height=2)
CInp.grid(column=2,row=1)
CInp.bind('<KeyRelease>', onCammel)

outFrame = Frame(master, width=600)
outFrame.pack(padx=30, pady=30)

InitOutLbl = Label(outFrame, text="Initial value output")
InitOutLbl.grid(column=0,row=0)

ReduOutLbl = Label(outFrame, text="Reducer Action map output")
ReduOutLbl.grid(column=1,row=0)

ActiOutLbl = Label(outFrame, text="Actions output")
ActiOutLbl.grid(column=2,row=0)

InitOut = scrolledtext.ScrolledText(outFrame, width=20, height=6)
InitOut.grid(column=0,row=1)

ReduOut = scrolledtext.ScrolledText(outFrame, width=20, height=6)
ReduOut.grid(column=1,row=1)

ActiOut = scrolledtext.ScrolledText(outFrame, width=20, height=6)
ActiOut.grid(column=2,row=1)

mainloop()
