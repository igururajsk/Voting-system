from tkinter import *
import tkinter.messagebox
from PIL import Image,ImageTk
import mysql.connector
from mail import report
import csv
from functools import partial
import os
def show(Consti,votev):
    print("printing the VoterID",votev)
    def database():
        aa= mysql.connector.connect(host='localhost',port= 3306,user="root",password="Highmonk@5253",db="votingsystem")
        print('connect')
        return aa

    def Thank_you(party):
        print("Thank you for voting")
        q7=database()
        query7 = q7.cursor()
        print("*******VoterID********",votev)
        query7.execute('SELECT * FROM facerec WHERE Votercardnos = %s  ', (votev, ))
        result=query7.fetchall()
        for row in result:
            username=row[0]
            Userid=row[3]
            votecardnum=row[4]
            emailid=row[5]
            Consti=row[11]
        report(username,Userid,votecardnum,emailid,Consti)
        valid_parties = {"bjp","congress","jds"}
        if party not in valid_parties:
            raise ValueError("Invalid party provided")
        query7.execute("UPDATE facerec SET VoteAuth = 'yes' WHERE Votercardnos = %s", (votev,))
        query7.execute(f"UPDATE result SET {party} = {party} + 1")
        q7.commit()
        q7.close()
        
        def main1():
            R6.destroy()
            
        R6=tkinter.Toplevel()
        R6.geometry('900x600')
        R6.title('Thank you')
        image=Image.open('ThankYou.jpg')
        image1=image.resize((900,600))
        img = ImageTk.PhotoImage(image1)
        
        panel = Label(R6, image = img)
        panel.pack(side = "bottom", fill = "both", expand = "yes")

        
        btn = Button(R6, text="Logout", width=10, height=2,fg="black",font=('algerian',15,'bold'),justify='center',bg="light blue",command=main1)
        btn.place(x=380, y=450)

        R6.mainloop()

    def _update_local_result(Consti, suffix):
        os.makedirs("results", exist_ok=True)
        filename=os.path.join("results", f"{Consti}{suffix}.txt")
        try:
            with open(filename, "r") as f:
                count=int(f.read() or 0)
        except FileNotFoundError:
            count=0
        count+=1
        with open(filename,"w") as f:
            f.write(str(count))

    def bjp(Consti):
        print("am in bjp",Consti)
        tkinter.messagebox.showinfo("DONE","Thank You For Voting....!!")
        _update_local_result(Consti,"bjp")
        Thank_you('bjp')
        
    def cong(Consti):
        print("am in cong",Consti)
        tkinter.messagebox.showinfo("DONE","Thank You For Voting....!!")
        _update_local_result(Consti,"cong")
        Thank_you('congress')
        
    def jds(Consti):
        print("am in jds")
        tkinter.messagebox.showinfo("DONE","Thank You For Voting....!!")
        _update_local_result(Consti,"jds")
        Thank_you('jds')
  
        

    def dasarahalli(Consti):
        def call1(Consti):
            window1.destroy()
            bjp(Consti)
        def call2(Consti):
            window1.destroy()
            cong(Consti)
        def call3(Consti):
            window1.destroy()
            jds(Consti)
        print(Consti)
        window1=Toplevel()
        window1.geometry('800x600')

        image4=Image.open('Homepage.png')
        window1.title('Vote')
        image=image4.resize((800,600))
        photo_image4=ImageTk.PhotoImage(image4)
        label4=Label(window1,image=photo_image4)
        label4.place(x=0,y=0)

        l1=Label (window1, text="BE PREPARED TO VOTE",font=("Helvetica", 18, "bold"))  
        l1.place(x=200,y=10)


        lbjp=Label (window1, text="BJP",font=("Helvetica", 18, "bold"))  
        lbjp.place(x=80,y=110)

        lcon=Label (window1, text="CONGRESS",font=("Helvetica", 18, "bold"))  
        lcon.place(x=80,y=210)

        ljds=Label (window1, text="JDS",font=("Helvetica", 18, "bold"))  
        ljds.place(x=80,y=310)



        image=Image.open('b.png')
        print(image)
        image=image.resize((80,60))
        photo_image=ImageTk.PhotoImage(image)
        label1=Label(window1,image=photo_image)
        label1.place(x=500,y=100)

        image1=Image.open('c.jpg')
        image1=image1.resize((80,60))
        photo_image1=ImageTk.PhotoImage(image1)
        label2=Label(window1,image=photo_image1)
        label2.place(x=500,y=200)

        image2=Image.open('jds.jpg')
        image2=image2.resize((80,60))
        photo_image2=ImageTk.PhotoImage(image2)
        label3=tkinter.Label(window1,image=photo_image2)
        label3.place(x=500,y=300)
        
        b1jp=Button(window1,text = "BJP",width=15,height=3,bg="green",command=partial(call1,Consti))
        b1jp.place(x=300,y=100)

        cong1=tkinter.Button(window1,text = "CONGRESS",width=15,height=3,bg="green",command=partial(call2,Consti))
        cong1.place(x=300,y=200)

        jds1=tkinter.Button(window1,text = "JDS",width=15,height=3,bg="green",command=partial(call3,Consti))
        jds1.place(x=300,y=300)

        window1.mainloop()


    def Mahalakshmi(Consti):
        

        window1=Toplevel()
        window1.geometry('800x600')

        image4=Image.open('Homepage.png')
        window1.title('Vote')
        image=image4.resize((800,600))
        photo_image4=ImageTk.PhotoImage(image4)
        label4=tkinter.Label(window1,image=photo_image4)
        label4.place(x=0,y=0)

        l1=Label (window1, text="BE PREPARED TO VOTE",font=("Helvetica", 18, "bold"))  
        l1.place(x=200,y=10)


        lbjp=Label (window1, text="BJP",font=("Helvetica", 18, "bold"))  
        lbjp.place(x=80,y=110)



        ljds=Label (window1, text="JDS",font=("Helvetica", 18, "bold"))  
        ljds.place(x=80,y=310)

        bjp1=Button(window1,text = "BJP",width=15,height=3,bg="green",command=partial(bjp,Consti))
        bjp1.place(x=300,y=100)

        jds1=tkinter.Button(window1,text = "JDS",width=15,height=3,bg="green",command=partial(jds,Consti))
        jds1.place(x=300,y=300)

        image=Image.open('b.png')
        print(image)
        image=image.resize((80,60))
        photo_image=ImageTk.PhotoImage(image)
        label1=Label(window1,image=photo_image)
        label1.place(x=500,y=100)



        image2=Image.open('jds.jpg')
        image2=image2.resize((80,60))
        photo_image2=ImageTk.PhotoImage(image2)
        label3=tkinter.Label(window1,image=photo_image2)
        label3.place(x=500,y=300)

        window1.mainloop()
    def Malleshwara(Consti):
        
        print("Malleshwara")

        window1=Toplevel()
        window1.geometry('800x600')

        image4=Image.open('Homepage.png')
        window1.title('Vote')
        image=image4.resize((800,600))
        photo_image4=ImageTk.PhotoImage(image4)
        label4=tkinter.Label(window1,image=photo_image4)
        label4.place(x=0,y=0)

        l1=Label (window1, text="BE PREPARED TO VOTE",font=("Helvetica", 18, "bold"))  
        l1.place(x=200,y=10)




        lcon=Label (window1, text="CONGRESS",font=("Helvetica", 18, "bold"))  
        lcon.place(x=80,y=210)

        ljds=Label (window1, text="JDS",font=("Helvetica", 18, "bold"))  
        ljds.place(x=80,y=310)


        cong1=tkinter.Button(window1,text = "CONGRESS",width=15,height=3,bg="green",command=partial(cong,Consti))
        cong1.place(x=300,y=200)

        jds1=tkinter.Button(window1,text = "JDS",width=15,height=3,bg="green",command=partial(jds,Consti))
        jds1.place(x=300,y=300)



        image1=Image.open('c.jpg')
        image1=image1.resize((80,60))
        photo_image1=ImageTk.PhotoImage(image1)
        label2=Label(window1,image=photo_image1)
        label2.place(x=500,y=200)

        image2=Image.open('jds.jpg')
        image2=image2.resize((80,60))
        photo_image2=ImageTk.PhotoImage(image2)
        label3=tkinter.Label(window1,image=photo_image2)
        label3.place(x=500,y=300)

        window1.mainloop()
    def Hebbal(Consti):
        
        print("Hebbal")

        window1=Toplevel()
        window1.geometry('800x600')

        image4=Image.open('Homepage.png')
        window1.title('Vote')
        image=image4.resize((800,600))
        photo_image4=ImageTk.PhotoImage(image4)
        label4=tkinter.Label(window1,image=photo_image4)
        label4.place(x=0,y=0)

        l1=Label (window1, text="BE PREPARED TO VOTE",font=("Helvetica", 18, "bold"))  
        l1.place(x=200,y=10)


        lbjp=Label (window1, text="BJP",font=("Helvetica", 18, "bold"))  
        lbjp.place(x=80,y=110)

        lcon=Label (window1, text="CONGRESS",font=("Helvetica", 18, "bold"))  
        lcon.place(x=80,y=210)


        bjp1=Button(window1,text = "BJP",width=15,height=3,bg="green",command=partial(bjp,Consti))
        bjp1.place(x=300,y=100)

        cong1=tkinter.Button(window1,text = "CONGRESS",width=15,height=3,bg="green",command=partial(cong,Consti))
        cong1.place(x=300,y=200)


        image=Image.open('b.png')
        print(image)
        image=image.resize((80,60))
        photo_image=ImageTk.PhotoImage(image)
        label1=Label(window1,image=photo_image)
        label1.place(x=500,y=100)

        image1=Image.open('c.jpg')
        image1=image1.resize((80,60))
        photo_image1=ImageTk.PhotoImage(image1)
        label2=Label(window1,image=photo_image1)
        label2.place(x=500,y=200)



        window1.mainloop()

    if "Dasarahalli"==Consti:
        dasarahalli(Consti)
    if "Mahalakshmi"==Consti:
        Mahalakshmi(Consti)
    if "Malleshwara"==Consti:
        Malleshwara(Consti)
    if "Hebbal"==Consti:
        Hebbal(Consti)

#show('Dasarahalli',123456)
