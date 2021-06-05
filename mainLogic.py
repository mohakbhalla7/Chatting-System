'''

Project: Chatting System
Name: Mohak Bhalla
'''

import pyrebase
from time import localtime, strftime, sleep
import sys
import os
import threading

config = {
  "apiKey": "apiKey",
  "authDomain": "chatting-system-57f73-default-rtdb.firebaseapp.com",
  "databaseURL": "https://chatting-system-57f73-default-rtdb.firebaseio.com",
  "storageBucket": "chatting-system-57f73-default-rtdb.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#Clear function
def clear():
    if os.name == 'nt': 
        _ = os.system('cls')  
    else: 
        _ = os.system('clear')

#Enrollment function
def enroll():
    flag = 0
    while(flag == 0):
        userid=input("Enter username: ")
        dataf=db.child("Login Data").get().val()
        if userid in dataf:
            print("""Username Already Exists.
Please try again.""")
            print("")
        else:
            userpwd=input("Enter your password: ")
            temp = {userid: userpwd}
            db.child("Login Data").update(temp)
            print("Enrolled Successfully")
            flag=1
    sleep(4)
    
#Authentication function
def auth():
    count=1
    id = ''
    while(count<=5):
        temp=db.child("Login Data").get().val()
        userid=input("Enter username: ")
        if userid not in temp:
            print("Username does not exist.")
            print("")
            ch=input("Get a new Enrollment(y/n): ")
            if(ch == 'y' or ch == 'Y'):
                enroll()
                id=userid
                return state
        else:
            userpwd=input("Enter your password: ")
        
            if ((userid in temp) and (temp[userid]==userpwd)):
                    id=userid
                    return id
            else:
                print("Invalid Username or Password.")
                print(5-count,"Try(s) left.")
        print("")
        count+=1
    return id

#Quit function
def closeMP():
    print("Later Aligator!")
    sleep(4)
    sys.exit()

#Live chat function
def stream_handler(message):
    #print(message["path"])
    info=message["data"]
    print("")
    for sender in info:
        msg=info[sender]
        if msg[1]=="0":
            print(sender)
            print(msg[0])
            print("")
            msg[1]="1";
            #db.child("Message Data/"+userid+"/"+friend).update({msg.key(): msg.val()})

#Message function
def msg_sys(userid):
    while(1):
        sleep(3)
        clear()
        print("\nSelect a user to send message")
        all_users = db.child("Login Data").get()
        for user in all_users.each():
            print(user.key())
        print("Or enter 'BACK' to go back.")
        friend=input("Enter your choice: ")
        print("")
        if friend == 'BACK':
            break
        if friend not in all_users.val():
            print("Please select a valid user.")
            print("")
        else:
            sleep(3)
            clear()
            print(friend+"'s message window")
            print("")   
            ch=input("View unread messages(y/n): ")
            print("")
            if ch=='Y' or ch=='y':
                c=0
                #c= received_msgs(userid, friend);
                if userid in db.child("Message Data").get().val() and friend in db.child("Message Data/"+userid).get().val():
                    dataf = db.child("Message Data/"+userid+"/"+friend).get()
                    for msg in dataf.each():
                        if(msg.val()[1]=="0"):
                            c+=1
                            print(msg.key())
                            print(msg.val()[0])
                            msg.val()[1]="1"
                            db.child("Message Data/"+userid+"/"+friend).update({msg.key(): msg.val()})
                if c==0:
                    print("No unread messages")
            print("")
            print("Enter 'EXIT' to exit")
            print("Start typing...")
            print("")
            '''
            t1= threading.Thread(target = send_msgs, args=(userid, friend,))
            t2= threading.Thread(target = receive_stream, args=(userid, friend,))

            t2.start()
            t1.start()

            if t1.join():
                t2.stop()'''
            msg=''
            while(msg != 'EXIT'):
                msg=input()
                if msg != 'EXIT' and msg != ' ':
                    t=strftime("(%d-%m-%y,%H:%M:%S)", localtime())
                    key=t+userid
                    value={0:msg, 1:"-"}
                    temp={key:value}
                    address="Message Data/"+userid+"/"+friend
                    db.child(address).update(temp)          #Updating user data

                    value={0:msg, 1:"0"}
                    temp={key:value}
                    address="Message Data/"+friend+"/"+userid
                    db.child(address).update(temp)          #Updating friend data

'''def send_msgs(userid, friend):
    msg=''
    while(msg != 'EXIT'):
        msg=input()
        if msg != 'EXIT' and msg != ' ':
            t=strftime("(%d-%m-%y,%H:%M:%S)", localtime())
            key=t+userid
            value={0:msg, 1:"-"}
            temp={key:value}
            address="Message Data/"+userid+"/"+friend
            db.child(address).update(temp)          #Updating user data

            value={0:msg, 1:"0"}
            temp={key:value}
            address="Message Data/"+friend+"/"+userid
            db.child(address).update(temp)          #Updating friend data


#Received message interrupt function
def receive_stream(userid, friend):
    while(1):
        my_stream = db.child("Message Data/"+userid+"/"+friend).stream(stream_handler)
    my_steam.close()

    
def received_msgs(userid, friend):
    c=0
    if userid in db.child("Message Data").get().val() and friend in db.child("Message Data/"+userid).get().val():
        dataf = db.child("Message Data/"+userid+"/"+friend).get()
        for msg in dataf.each():
            if(msg.val()[1]=="0"):
                c+=1
                print(msg.key())
                print(msg.val()[0])
                msg.val()[1]="1"
                db.child("Message Data/"+userid+"/"+friend).update({msg.key(): msg.val()})
    return c
'''
    
#Update password function
def updatepsw(userid):
    sleep(3)
    clear()
    userdata = db.child("Login Data").get().val()
    flag=0
    while flag==0:
        newpsw=input("Enter new password: ")
        if userdata[userid] == newpsw:
            print("/nNew password can't be the old password.")
        else:
            userdata[userid] = newpsw
            flag=1
    db.child("Login Data").update(userdata)
    print("\nPassword updated successfully.")
    
#MainLogic
while(1):
    clear()
    userid=''
    print("\n420 Messaging Platform")
    x=input("""\nEnter 'e' to enroll.
Enter 's' to sign-in.
Enter 'c' to close.
Your Choice: """)
    print("")
    x=x.upper()
    if(x=='E'):
        enroll()
    elif(x=='S'):
        userid = auth()
    elif(x=='C'):
        closeMP()
    else:
        print("Invalid Input.")

    if userid != '':
        while(1):
            sleep(3)
            clear()
            print("\nWelcome to Message-box")
            print("""\nEnter 'm' to message.
Enter 'u' to update password.
Enter 's' to sign-out.""")
            ch=input("Your choice: ")
            ch=ch.upper()
            if(ch=='M'):
                msg_sys(userid)
            elif(ch=='U'):
                updatepsw(userid)
            elif(ch=='S'):
                break
            else:
                print("\nInvalid Input.")
