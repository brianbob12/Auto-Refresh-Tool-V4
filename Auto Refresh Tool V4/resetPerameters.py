import time
print("this will clear all saved emails websites and keywords")
choice=input("are you sure you would like to do this(y/n):").lower()
print("reseting perameters")
if choice=="y":
    with open("emails.txt","w") as f:
        f.write("exampleemail@example.com\n")
    with open("watchList.txt","w") as f:
        f.write("example site::https://www.example.com\n")
    with open("keywords.txt","w")as f:
        f.write("keyword1,keyword2,keyword3\n")
time.sleep(5)
print("done\nclosing")
time.sleep(5)
print()
