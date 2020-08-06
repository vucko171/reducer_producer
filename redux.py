from tkinter import *
from tkinter import scrolledtext
import re

def outAll():
    Under=UInp.get(1.0,'end-1c').split("\n")
    Under=[x.lower() for x in Under]
    Cammel=CInp.get(1.0,'end-1c').split("\n")
    Cammel=[x[0].upper()+x[1:] if len(x)>0 else "" for x in Cammel]
    Reducer=RInp.get(1.0,'end-1c').split("\n")[0]
    Variable=VInp.get(1.0,'end-1c').split("\n")[0]
    group=int(check.get())
    strInitOut=""
    strReduOut=""
    strActiOut=""
    strVarOut=""
    strSetOut=""
    if group:
        strReduOut+="      case `"+Reducer+"/SET_"+Under[0].upper()+"`:\n"
        strActiOut+="export function set"+Cammel[0]+"(data) {\n  return {\n    type: `@servicerequest/SET_"+Under[0].upper()+"`,\n    payload: {\n      data,\n    },\n  };\n}\n"
        strSetOut+="set"+Cammel[0]+",\n"
    for x in range(len(min(Under,Cammel))):
        if len(Under[x])!=0:
            if group:
                strReduOut+="        "+Variable+"."+Under[x].lower()+" = action.payload.data."+Under[x].lower()+";\n"
            else:
                strReduOut+="      case `"+Reducer+"/SET_"+Under[x].upper()+"`:\n        "+Variable+"."+Under[x].lower()+" = action.payload.data;\n        break;\n"
                strActiOut+="export function set"+Cammel[x]+"(data) {\n  return {\n    type: `@servicerequest/SET_"+Under[x].upper()+"`,\n    payload: {\n      data,\n    },\n  };\n}\n"
                strSetOut+="set"+Cammel[x]+",\n"
            strInitOut+=Under[x].lower()+": '',\n"
            strVarOut+=Under[x].lower()+",\n"
    if group:
        strReduOut+="        break;\n"
    InitOut.delete(1.0,"end")
    InitOut.insert(1.0,strInitOut)
    ReduOut.delete(1.0,"end")
    ReduOut.insert(1.0,strReduOut)
    ActiOut.delete(1.0,"end")
    ActiOut.insert(1.0,strActiOut)
    ImpVarOut.delete(1.0,"end")
    ImpVarOut.insert(1.0,strVarOut)
    ImpSetOut.delete(1.0,"end")
    ImpSetOut.insert(1.0,strSetOut)
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
        temp=re.findall('^([A-Z]?[a-z]*?|\d+)(?:([A-Z][a-z]*?|\d+))?(?:([A-Z][a-z]*?|\d+))?(?:([A-Z][a-z]*?|\d+))?(?:([A-Z][a-z]*?|\d+))?(?:([A-Z][a-z]*?|\d+))?(?:([A-Z][a-z]*?|\d+))?(?:([A-Z][a-z]*?|\d+))?$',data[x])
        str=""
        if len(temp)!=0:
            temp=temp[0]
            for y in range(len(temp)-1,0,-1):
                if len(temp[y])!=0:
                    str="_"+temp[y].lower()+str
            str=temp[0].lower()+str
        data[x]=str
    return data

def onUnder(*args):
    Cammel=conv2Cammel(UInp.get(1.0,'end-1c').split("\n"))
    Cammel=[x[0].upper()+x[1:] if len(x)>0 else "" for x in Cammel]
    CInp.delete(1.0,"end")
    CInp.insert(1.0,"\n".join(Cammel))
    outAll()

def onCammel(*args):
    Under=conv2Under(CInp.get(1.0,'end-1c').split("\n"))
    Under=[x.lower() for x in Under]
    UInp.delete(1.0,"end")
    UInp.insert(1.0,"\n".join(Under))
    outAll()

master = Tk()
master.resizable(0,0)


topFrame = Frame(master, width=600)
topFrame.pack(padx=30, pady=30)

inputFrame = Frame(topFrame, width=600)
inputFrame.pack()


RLbl = Label(inputFrame, text="Reducer")
RLbl.grid(column=0,row=0)

RInp = Text(inputFrame, width=32, height=1)
RInp.insert(1.0, "@servicerequest")
RInp.grid(column=0,row=1)

VLbl = Label(inputFrame, text="Variable/Object (leave \"draft\" if none)")
VLbl.grid(column=2,row=0)

VInp = Text(inputFrame, width=32, height=1)
VInp.insert(1.0, "draft.detGeneralInfo")
VInp.grid(column=2,row=1)


ULbl = Label(inputFrame, text="variable(s) with underscore")
ULbl.grid(column=0,row=2)

UInp = scrolledtext.ScrolledText(inputFrame, width=30, height=2)
UInp.grid(column=0,row=3)
UInp.focus_set()
UInp.bind('<KeyRelease>', onUnder)

blankInp = Label(inputFrame, text="", width=2)
blankInp.grid(column=1,row=3)

CLbl = Label(inputFrame, text="variable(s) with camelCase")
CLbl.grid(column=2,row=2)

CInp = scrolledtext.ScrolledText(inputFrame, width=30, height=2)
CInp.grid(column=2,row=3)
CInp.bind('<KeyRelease>', onCammel)


checkFrame = Frame(topFrame, width=600)
checkFrame.pack()

check = IntVar()
groupCheck = Checkbutton(checkFrame, text='Group variables in one setter',variable=check, onvalue=1, offvalue=0, command=outAll)
groupCheck.grid(sticky = W,column=0,row=0)



bottomFrame = Frame(master, width=600)
bottomFrame.pack(padx=30, pady=30)

outFrame = Frame(bottomFrame, width=600)
outFrame.pack()


InitOutLbl = Label(outFrame, text="Initial value output")
InitOutLbl.grid(column=0,row=0)

InitOut = scrolledtext.ScrolledText(outFrame, width=20, height=6)
InitOut.grid(column=0,row=1)

ReduOutLbl = Label(outFrame, text="Reducer Action map output")
ReduOutLbl.grid(column=1,row=0)

ReduOut = scrolledtext.ScrolledText(outFrame, width=20, height=6)
ReduOut.grid(column=1,row=1)

ActiOutLbl = Label(outFrame, text="Actions output")
ActiOutLbl.grid(column=2,row=0)

ActiOut = scrolledtext.ScrolledText(outFrame, width=20, height=6)
ActiOut.grid(column=2,row=1)


extraFrame = Frame(bottomFrame, width=600)
extraFrame.pack()


ImpVarLbl = Label(extraFrame, text="import variables")
ImpVarLbl.grid(column=0,row=0)

ImpVarOut = scrolledtext.ScrolledText(extraFrame, width=20, height=6)
ImpVarOut.grid(column=0,row=1)

blankInp2 = Label(inputFrame, text="", width=2)
blankInp2.grid(column=1,row=0)

ImpSetLbl = Label(extraFrame, text="import setters")
ImpSetLbl.grid(column=2,row=0)

ImpSetOut = scrolledtext.ScrolledText(extraFrame, width=20, height=6)
ImpSetOut.grid(column=2,row=1)


mainloop()
