import smtplib, ssl,time,datetime,subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def loadup():
    urls=[]
    urlLabels=[]
    temp=[]
    KWords=[]
    with open("watchList.txt","r") as f:
        temp=[i.split("::") for i in f.readlines()]
    with open("keywords.txt","r") as f:
        KWords=[i.lower().split(",")[:-1] for i in f.readlines()]
    for i in temp:
        urlLabels.append(i[0])
        urls.append(i[1])
    return urls,urlLabels,KWords

def sendEmail(index,newWords):
    print("sending email...")
    emailList=[]
    try:
        emailsFile="emails.txt"
        with open(emailsFile,"r")as f:
            emailList=[i for i in f.readlines()]
        print(emailList)
    except Exception as e:
        error3(e,3,0,index)
    changedWords=[]
    for i,v in enumerate(newWords):
        if v!=keyWordCount[index][i]:
            changedWords.append(keyWords[index][i])
            
    keyWordMessage="the keywords: "
    
    for i,word in enumerate(changedWords):
        if i==len(changedWords)-1:
            keyWordMessage+="'"+word+"'.\n"
        elif i==len(chnagedWords)-2:
            keyWordMEssage+="'"+word+"' and "
        else:
            keyWordMessage+="'"+word+"', "
    
    port = 465  # For SSL
    password = "testingPass"
    senderEmail="autoemailmachine@gmail.com"
    subject="Refresh Tool: "+labels[index]+" updated"
    try:
        text=""
        htmlPart="<html>\n<body>\n<p>\n"
        text+="The webpage:"+labels[index]+" was updated\n"
        htmlPart+="The webpage:<b>"+labels[index]+"</b> was updated<br>\n"
        text+=links[index]+" was updated\n"
        htmlPart+=keyWordMessage[:-2]+"<br>"
        text+=keyWordMessage
        htmlPart+='<a href="'+links[index]+'">'+links[index]+'</a><br>\n'
        text+="date and time: "+str(datetime.datetime.now())+" (US format)\n"
        htmlPart+="date and time: "+str(datetime.datetime.now())+" (US format)<br>\n"
        htmlPart+="</p>\n</body>\n</html>"
    except Exception as e:
        error3(e,3,1,index)


    # Create a secure SSL context
    try:
        context = ssl.create_default_context()
    except Exception as e:
        error(e,3,2,index)

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        try:
            server.login(senderEmail, password)
        except Exception as e:
            error(e,3,3,index)
        for i in emailList:
            try:
                message=MIMEMultipart("alternative")
                message["Subject"]=subject
                message["From"]=senderEmail
                message["To"]=i
                part1=MIMEText(text,"plain")
                part2=MIMEText(htmlPart,"html")
                message.attach(part1)
                message.attach(part2)
            except Exception as e:
                error(e,3,4,i)
            try:
                server.sendmail(senderEmail,i,message.as_string())
            except Exception as e:
                error(e,3,5,i)
            
    print("email sent")

def getHTML():
    out=[]
    for i in links:
        if i=="dud":
            out.append("dud")
        else:
            try:
                res=subprocess.check_output(["curl",i[:-1]])
                out.append(res)
            except Exception as e:
                error2(e,1,i)
    return [i.lower() for i in out]

def countKeyWords(index,code):
    words=keyWords[index]
    new=[]
    for i in range(len(words)):
        new.append(code.count(words[i].encode()))
    return new

def error(e,decCode):
    print(e)
    print("-"*20)
    print(datetime.datetime.now())
    print("error code:",hex(decCode))
    print("-"*20)
    input("press enter to exit")
    exit()

def error2(e,decCode,adV):
    print(e)
    print("-"*20)
    print(datetime.datetime.now())
    print("error code:",hex(decCode))
    print("adV:",adV)
    print("-"*20)
    input("press enter to exit")
    exit()
    
def error3(e,decCode,sub,adV):
    print(e)
    print("-"*20)
    print(datetime.datetime.now())
    print("error code:",str(hex(decCode))+"-"+str(sub))
    print("adV:",adV)
    print("-"*20)
    input("press enter to exit")
    exit()

try:
    links,labels,keyWords=loadup()
except Exception as e:
    error(e,0)
HTML=getHTML()
try:
    keyWordCount=[countKeyWords(i,HTML[i]) for i in range(len(links))]
    keyWordCount=[i for i in keyWordCount]
except Exception as e:
    error(e,2)

while True:
    new=getHTML()
    for index,value in enumerate(new):
        if value!=HTML[index]:
            print("\n\n"+labels[index],"updated")
            try:
                newWords=countKeyWords(index,value)
            except Exception as e:
                error2(e,4,index)
            if newWords!=keyWordCount[index]:
                print("key words changed")
                HTML[index]=value
                try:
                    sendEmail(index,newWords)
                except Exception as e:
                    error2(e,3,index)
                keyWordCount[index]=[i for i in newWords]
                time.sleep(30)
            else:
                print("keywords unchanged")
                print("\t",newWords,"\t",keyWordCount[index])
    time.sleep(1)
