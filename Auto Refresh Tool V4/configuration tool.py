import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import messagebox
import os

watching=[]
def loadStuff():
    with open("watchList.txt","r") as f:
        r=f.readlines()
        t=[i[:-1].split("::") for i in r]
    with open("keyWords.txt","r") as f:
        r=f.readlines()
        k=[i.split(",")[:-1] for i in r]
    with open("emails.txt","r") as f:
        r=f.readlines()
        e=[i[:-1] for i in r]
    return t,k,e



watching,keyWords,emails=loadStuff()
#index of what watch is on


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Auto Refresh Tool")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.showFrame(-2,False)
        self.showFrame(-1,False)


    def showFrame(self, index,danger):
        
        if index==-1:
            frame=StartPage(parent=self.container,controller=self)
            frame.grid(row=0, column=0, sticky="nsew")
        elif index==-2:
            frame=newSitePage(parent=self.container,controller=self)
            frame.grid(row=0, column=0, sticky="nsew")
        elif index==-3:
            frame=EmailPage(parent=self.container,controller=self)
            frame.grid(row=0,column=0,sticky="nsew")
        else:
            frame = IndexedPage(index,danger,parent=self.container,controller=self)
            frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the home page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        webLabel=tk.Label(self,text="Webpages:")
        webLabel.pack()
        
        self.buttons=[]

        for ix,thing in enumerate(watching):
            b=tk.Button(self,text=thing[0],command=self.clickHandeler(ix))
            b.pack()
            self.buttons.append(b)

        actionLabel=tk.Label(self,text="\nActions:")
        actionLabel.pack()
        
        addNewButton=tk.Button(self,text="add a new website",bg="light blue",command=self.clickHandeler(-2))
        addNewButton.pack()

        addNewButton=tk.Button(self,text="configure emails",bg="light blue",command=self.clickHandeler(-3))
        addNewButton.pack()

        launchButton=tk.Button(self,text="start the tool",bg="light green",command=lambda: os.system("start main.py"))
        launchButton.pack()
        
    def clickHandeler(self,num):
        return lambda: self.controller.showFrame(num,False)



class IndexedPage(tk.Frame):
    def __init__(self,index,danger,parent,controller):
        self.danger=danger
        self.index=index
        tk.Frame.__init__(self,parent)
        self.controller=controller
        label=tk.Label(self,text=watching[index][0],font=controller.title_font)
        label.pack(side="top",fill="x",pady=10)

        link=tk.Label(self,text=watching[index][1],fg="blue",cursor="hand2")
        link.pack()
        link.bind("<Button-1>", lambda e: os.system("start "+watching[index][1]))
        
        self.entry=tk.Entry(self)
        self.entry.configure(width=40)
        self.entry.pack()
        addNewButton=tk.Button(self,text="Add new keyword",command=self.addNew,bg="light green")
        addNewButton.pack()

        self.buttons=[]
        for ix,thing in enumerate(keyWords[index]):
            b=tk.Button(self,text=keyWords[index][ix],command=self.clickHandeler(ix),bg="red")
            b.pack(side="left")
            self.buttons.append(b)
            
        
        if danger:
            removeButton=tk.Button(self,text="Remove this webpage",command=self.removeURL,bg="red")
        else:
            removeButton=tk.Button(self,text="Remove this webpage",command=self.removeURL)
            
        removeButton.pack(side="bottom")

        button=tk.Button(self,text="Go to home page",command=lambda:controller.showFrame(-1,False),pady=10)
        button.pack(side="bottom")
        
    def clickHandeler(self,num):
        return lambda:self.removeKeyword(num)
    
    def removeKeyword(self,j):
        i=self.index
        if len(keyWords[i])<2:
            tk.messagebox.showwarning(title="Removing The Last Keyword",message="There must always be at least one keyword per webpage.\nPlease add a new keyword before removing this one.")
            print("there must always be at least one keyword per webpage")
            return
        print("remove keyword:",i,j)
        del keyWords[i][j]
        toW=""
        for ii in keyWords:
            for ij in  ii:
                toW+=ij+","
            toW+="\n"
        with open("keyWords.txt","w")as f:
            f.write(toW)
        self.controller.showFrame(i,False)

    def addNew(self):
        text=self.entry.get()
        if len(text)<=1:
            return
        print("adding new keyword:",text)
        keyWords[self.index].append(text)
        toW=""
        for ii in keyWords:
            for ij in  ii:
                toW+=ij+","
            toW+="\n"
        with open("keyWords.txt","w")as f:
            f.write(toW)
        self.controller.showFrame(self.index,False)

    def removeURL(self):
        if self.danger:
            ix=self.index
            print("removing",ix)
            del keyWords[ix]
            del watching[ix]

            toW=""
            for thing in watching:
                toW+=thing[0]+"::"+thing[1]+"\n"
            with open("watchList.txt","w") as f:
                f.write(toW)
            toW=""
            for ii in keyWords:
                for ij in  ii:
                    toW+=ij+","
                toW+="\n"
            with open("keyWords.txt","w")as f:
                f.write(toW)
            self.controller.showFrame(-1,False)
        else:
            self.controller.showFrame(self.index,True)
        
class newSitePage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller=controller
        label=tk.Label(self,text="add new webpage",font=controller.title_font)
        label.pack(side="top",fill="x",pady=10)

        nameLabel=tk.Label(self,text="Webpage name: ")
        nameLabel.pack(side="left")
        
        self.name=tk.Entry(self)
        self.name.configure(width=35)
        self.name.pack(side="left")

        urlLabel=tk.Label(self,text="\tURL: ")
        urlLabel.pack(side="left")
        
        self.url=tk.Entry(self)
        self.url.configure(width=35)
        self.url.pack(side="left")

        addButton=tk.Button(self,text="add site",command=self.add,bg="light green")
        addButton.config(height=1,width=6)
        addButton.pack(side="bottom")
        
        button=tk.Button(self,text="cancel",command=lambda:controller.showFrame(-1,False))
        button.pack()
        
    def add(self):
        if "::"in self.name.get():
            print("the name must not include two consecutive colongs, no '::'")
            messagebox.showerror("Name Error","The name must not include two consecutive colons, no '::'")
            return
        watching.append([self.name.get(),self.url.get()])
        keyWords.append([["exampleKeyword"]])
        print("chainging watching to:",watching)
        toW=""
        for thing in watching:
            toW+=thing[0]+"::"+thing[1]+"\n"
        with open("watchList.txt","w") as f:
            f.write(toW)
        with open("keyWords.txt","a") as f:
            f.write("exampleKeyword,\n")
        self.controller.showFrame(-1,False)
        
class EmailPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller=controller
        label=tk.Label(self,text="email list",font=controller.title_font)
        label.pack(side="top",fill="x",pady=10)

        self.entry=tk.Entry(self)
        self.entry.configure(width=40)
        self.entry.pack()
        addNewButton=tk.Button(self,text="Add new email",command=self.addNew,bg="light green")
        addNewButton.pack()

        self.buttons=[]
        for ix,email in enumerate(emails):
            b=tk.Button(self,text=email,command=self.clickHandeler(ix),bg="red")
            b.pack(side="left")
            self.buttons.append(b)
            

        button=tk.Button(self,text="Go to home page",command=lambda:controller.showFrame(-1,False),pady=10)
        button.pack(side="bottom")
        
    def clickHandeler(self,num):
        return lambda:self.removeEmail(num)
    
    def removeEmail(self,j):
        print("remove email:",j)
        del emails[j]
        toW=""
        for i in emails:
            toW+=i
            toW+="\n"
        with open("emails.txt","w")as f:
            f.write(toW)
        self.controller.showFrame(-3,False)

    def addNew(self):
        text=self.entry.get()
        if len(text)<=1:
            return
        print("adding new email:",text)
        emails.append(text)
        toW=""
        for i in emails:
            toW+=i
            toW+="\n"
        with open("emails.txt","w")as f:
            f.write(toW)
        self.controller.showFrame(-3,False)



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
