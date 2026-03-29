# vote11.py -- Final full file with Change Password (button inside Voting Desk)
# - Signup -> Login -> Face Authentication -> Vote (BJP/Congress/JDS)
# - Admin: View Voter List, Results
# - Change Password button inside Voting Desk (Old / New / Confirm)
# - Uses change.png (fallback to uploaded image path if missing)
# - Assumes MySQL DB 'votingsystem' with tables 'facerec' and 'result'
# - Requires opencv-contrib-python for cv2.face.LBPHFaceRecognizer_create

import os
import sys
from tkinter import *
import tkinter as tk
import tkinter.messagebox
from PIL import Image, ImageTk, ImageOps
import mysql.connector
import csv
import cv2
import numpy as np
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
from functools import partial

# fallback uploaded image path (assistant-provided)
_UPLOADED_FALLBACK = "/mnt/data/af7faacc-c018-4470-97e8-1258142a1c9f.png"

# ------------------------------- Utility helpers -------------------------------------------------

def safe_load_image(path, size):
    """
    Load image and resize to fit within 'size' (width, height).
    Returns an ImageTk.PhotoImage; on failure returns a neutral placeholder.
    """
    try:
        # Check direct path then script-relative, then fallback to uploaded image
        if not os.path.exists(path):
            base = os.path.dirname(os.path.abspath(__file__))
            alt = os.path.join(base, path)
            if os.path.exists(alt):
                path = alt
            elif os.path.exists(_UPLOADED_FALLBACK) and os.path.basename(path).lower().startswith("change"):
                path = _UPLOADED_FALLBACK
            elif os.path.exists(_UPLOADED_FALLBACK) and os.path.basename(path).lower().startswith("register"):
                path = _UPLOADED_FALLBACK

        img = Image.open(path)
        img = ImageOps.contain(img, size)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"[safe_load_image] cannot open '{path}': {e}", file=sys.stderr)
        img = Image.new('RGB', size, color=(200, 200, 200))
        return ImageTk.PhotoImage(img)

# ------------------------------- Database ------------------------------------------------------

def database():
    """Return a live MySQL connection. Update credentials here if needed."""
    return mysql.connector.connect(host='localhost', port=3306, user="root", password="Highmonk@5253", db="votingsystem")

# ------------------------------------------------ Home Page ------------------------------------

def main():
    root = Tk()
    root.geometry('900x600')
    root.title('Home Page')

    photo_image = safe_load_image('Homepage.png', (900, 600))
    label1 = Label(root, image=photo_image)
    label1.image = photo_image
    label1.place(x=0, y=0)

    la = Label(root, text="SMART VOTING SYSTEM WITH FACE RECOGNITION", font=('algerian', 15, 'bold'))
    la.place(x=200, y=100)

    Registerbt = Button(root, text="ADMIN", width=17, height=2, font=('algerian', 15, 'bold'),
                        justify='center', bg="light blue", relief=SUNKEN, command=Admin)
    Registerbt.place(x=180, y=475)

    photo_image1 = safe_load_image('Admin-icon.png', (250, 250))
    label2 = Label(root, image=photo_image1)
    label2.image = photo_image1
    label2.place(x=170, y=200)

    loginbt = Button(root, text="USERS", width=17, height=2, font=('algerian', 15, 'bold'),
                     justify='center', bg="light blue", relief=SUNKEN, command=login)
    loginbt.place(x=510, y=475)

    photo_image2 = safe_load_image('user.png', (250, 250))
    label3 = Label(root, image=photo_image2)
    label3.image = photo_image2
    label3.place(x=500, y=200)

    root.mainloop()

# ---------------------------- Face Detection ----------------------------------------------------

def faceDetect(vcn, un, ei):
    """Capture face images for user and train recognizer immediately after capture."""
    def TakeImages(vcn, un, ei):
        top.destroy()
        Id = str(vcn)
        name = str(un)
        eid = str(ei)

        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            tkinter.messagebox.showerror("Camera", "Could not open camera.")
            return

        harcascadePath = "haarcascade_frontalface_default.xml"
        if not os.path.exists(harcascadePath):
            tkinter.messagebox.showerror("Missing file", f"{harcascadePath} not found.")
            cam.release()
            return

        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        os.makedirs('TrainingImage', exist_ok=True)

        while True:
            ret, img = cam.read()
            if not ret:
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                filename = os.path.join("TrainingImage", f"{name}.{Id}.{sampleNum}.jpg")
                cv2.imwrite(filename, gray[y:y + h, x:x + w])
                cv2.imshow('frame', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            if sampleNum >= 60:
                break

        cam.release()
        cv2.destroyAllWindows()

        # Append voter details
        os.makedirs('VoterDetails', exist_ok=True)
        vfile = os.path.join('VoterDetails', 'VoterDetails.csv')
        with open(vfile, 'a+', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([Id, name, eid])

        TrainImages()

    def TrainImages():
        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
        except Exception as e:
            tkinter.messagebox.showerror("OpenCV", "cv2.face.LBPHFaceRecognizer_create not available. Install opencv-contrib-python.")
            print("cv2.face error:", e, file=sys.stderr)
            return

        faces, Ids = getImagesAndLabels("TrainingImage")
        if len(faces) == 0:
            tkinter.messagebox.showwarning("Train", "No training images found. Capture faces first.")
            return

        recognizer.train(faces, np.array(Ids))
        os.makedirs('TrainingImageLabel', exist_ok=True)
        trainer_path = os.path.join("TrainingImageLabel", "Trainner.yml")
        recognizer.save(trainer_path)
        print('Training completed, saved to', trainer_path)
        tkinter.messagebox.showinfo("Face", "Captured and successfully registered")

    def getImagesAndLabels(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        faces = []
        Ids = []
        for imagePath in imagePaths:
            try:
                pilImage = Image.open(imagePath).convert('L')
                imageNp = np.array(pilImage, 'uint8')
                Id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces.append(imageNp)
                Ids.append(Id)
            except Exception:
                continue
        return faces, Ids

    top = Toplevel()
    top.geometry('800x600')
    top.title("Face Capture")

    photo = safe_load_image('Homepage.png', (800, 600))
    label1 = Label(top, image=photo)
    label1.image = photo
    label1.place(x=0, y=0)

    photo_face = safe_load_image('face.jpg', (200, 200))
    label3 = Label(top, image=photo_face)
    label3.image = photo_face
    label3.place(x=280, y=150)

    btn = Button(top, text="Capture Face Here", width=25, height=2, fg="black",
                 font=('algerian', 15, 'bold'), justify='center', bg="light blue",
                 command=partial(TakeImages, vcn, un, ei))
    btn.place(x=280, y=400)
    return

# --------------------------- Register & Admin Page ------------------------------------------------------

def Admin():
    def result_time():
        """Show results in a small window."""
        try:
            q = database()
            cur = q.cursor()
            cur.execute("SELECT bjp, congress, jds FROM result")
            row = cur.fetchone()
            if not row:
                tkinter.messagebox.showinfo("Results", "No results found in DB.")
                return
            Bjp, Congress, Jds = (row[0] or 0, row[1] or 0, row[2] or 0)
            total = Bjp + Congress + Jds

            res_win = Toplevel()
            res_win.title("Election Results")
            res_win.geometry("400x260")
            Label(res_win, text="Election Results", font=('algerian', 16, 'bold')).pack(pady=10)
            Label(res_win, text=f"Total votes: {total}", font=("bold", 12)).pack(pady=4)
            Label(res_win, text=f"BJP: {Bjp}", font=("bold", 11)).pack()
            Label(res_win, text=f"Congress: {Congress}", font=("bold", 11)).pack()
            Label(res_win, text=f"JDS: {Jds}", font=("bold", 11)).pack()

            if Bjp >= Congress and Bjp >= Jds:
                winner_msg = f'BJP won ({Bjp})'
            elif Congress >= Bjp and Congress >= Jds:
                winner_msg = f'Congress won ({Congress})'
            elif Jds >= Bjp and Jds >= Congress:
                winner_msg = f'JDS won ({Jds})'
            else:
                winner_msg = 'Draw'
            Label(res_win, text=winner_msg, font=("bold", 12)).pack(pady=10)
            Button(res_win, text="Close", command=res_win.destroy).pack(pady=6)
        except Exception as e:
            print("result_time error:", e, file=sys.stderr)
            tkinter.messagebox.showerror("Error", f"Could not fetch results: {e}")

    def table():
        """Open a Toplevel window and show voters in a Treeview."""
        try:
            q = database()
            cur = q.cursor()
            cur.execute("SELECT usernames, Votercardnos, emails FROM facerec")
            rows = cur.fetchall()
            if not rows:
                tkinter.messagebox.showinfo("Voter List", "No voters found.")
                return

            win = Toplevel()
            win.title("Voter List")
            win.geometry('650x400')

            frm = Frame(win)
            frm.pack(fill="both", expand=True, padx=10, pady=10)

            cols = ("Name", "Voter ID", "Email")
            tv = ttk.Treeview(frm, columns=cols, show="headings")
            for c in cols:
                tv.heading(c, text=c)
                tv.column(c, width=200, anchor='center')

            vsb = ttk.Scrollbar(frm, orient="vertical", command=tv.yview)
            hsb = ttk.Scrollbar(frm, orient="horizontal", command=tv.xview)
            tv.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

            tv.grid(row=0, column=0, sticky='nsew')
            vsb.grid(row=0, column=1, sticky='ns')
            hsb.grid(row=1, column=0, sticky='ew')

            frm.grid_rowconfigure(0, weight=1)
            frm.grid_columnconfigure(0, weight=1)

            for r in rows:
                try:
                    tv.insert('', 'end', values=(r[0], r[1], r[2]))
                except Exception as ex:
                    print("Failed to insert row:", r, ex, file=sys.stderr)
        except Exception as e:
            print("table() error:", e, file=sys.stderr)
            tkinter.messagebox.showerror("Error", f"Could not load voter list: {e}")

    def signup():
        top.destroy()  # close admin initial window

        def Signup_db():
            username = ent_username.get().strip()
            password = ent_password.get().strip()
            Userid = ent_userid.get().strip()
            Votercardno = ent_voter.get().strip()
            emails = ent_email.get().strip()
            phoneno = ent_phone.get().strip()
            Adreses = ent_address.get().strip()
            Consti = clicked.get().strip()

            if not (username and password and Userid and Votercardno and emails and phoneno and Adreses and Consti and Consti != "Select"):
                tkinter.messagebox.showinfo("sorry", "Please fill the required information")
                return

            q1 = database()
            cur = q1.cursor()
            cur.execute("SELECT Votercardnos FROM facerec WHERE Votercardnos = %s", (Votercardno,))
            if cur.fetchone():
                tkinter.messagebox.showinfo("sorry", "Already Exist")
                return

            sql = ("INSERT INTO facerec (usernames,password,Userids,Votercardnos,emails,phonenos,Adresess,LoginAuth,FaceAuth,VoteAuth,Constituency)"
                   " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            data = (username, password, Userid, Votercardno, emails, phoneno, Adreses, 'no', 'no', 'no', Consti)
            cur.execute(sql, data)
            q1.commit()
            # proceed to face capture after signup
            signup_win.destroy()
            faceDetect(Votercardno, username, emails)

        signup_win = Toplevel()
        signup_win.geometry('800x600')
        signup_win.title('Register Page')

        photo = safe_load_image('Homepage.png', (800, 600))
        label1 = Label(signup_win, image=photo)
        label1.image = photo
        label1.place(x=0, y=0)

        Label(signup_win, text="USERNAME", fg="black", font=("bold", 15)).place(x=200, y=90)
        Label(signup_win, text="PASSWORD", fg="black", font=("bold", 15)).place(x=200, y=140)
        Label(signup_win, text="USER ID", fg="black", font=("bold", 15)).place(x=200, y=190)
        Label(signup_win, text="VOTERCARD ID", fg="black", font=("bold", 15)).place(x=200, y=240)
        Label(signup_win, text="EMAIL", fg="black", font=("bold", 15)).place(x=200, y=290)
        Label(signup_win, text="PHONE NUM", fg="black", font=("bold", 15)).place(x=200, y=340)
        Label(signup_win, text="ADDRESS", fg="black", font=("bold", 15)).place(x=200, y=390)
        Label(signup_win, text="Constituency", fg="black", font=("bold", 15)).place(x=200, y=440)

        ent_username = Entry(signup_win, width=20, font=("bold", 15), highlightthickness=2)
        ent_username.place(x=360, y=90)
        ent_password = Entry(signup_win, show="*", width=20, font=("bold", 15), highlightthickness=2)
        ent_password.place(x=360, y=140)
        ent_userid = Entry(signup_win, width=20, font=("bold", 15), highlightthickness=2)
        ent_userid.place(x=360, y=190)
        ent_voter = Entry(signup_win, width=20, font=("bold", 15), highlightthickness=2)
        ent_voter.place(x=360, y=240)
        ent_email = Entry(signup_win, width=20, font=("bold", 15), highlightthickness=2)
        ent_email.place(x=360, y=290)
        ent_phone = Entry(signup_win, width=20, font=("bold", 15), highlightthickness=2)
        ent_phone.place(x=360, y=340)
        ent_address = Entry(signup_win, width=20, font=("bold", 15), highlightthickness=2)
        ent_address.place(x=360, y=390)

        options = ["Select", "Dasarahalli", "Mahalakshmi", "Malleshwara", "Hebbal", "vijaynagar"]
        clicked = StringVar()
        clicked.set("Select")
        Constis = OptionMenu(signup_win, clicked, *options)
        Constis.place(x=350, y=440)

        signUpbt = Button(signup_win, text=" SAVE ", width=10, height=2, fg="black",
                          font=('algerian', 15, 'bold'), justify='center', bg="light blue",
                          command=Signup_db)
        signUpbt.place(x=350, y=490)

        return

    # Admin landing window
    top = Toplevel()
    top.geometry('800x600')
    top.title('Admin Home')

    photo_image = safe_load_image('Homepage.png', (800, 600))
    label1 = Label(top, image=photo_image)
    label1.image = photo_image
    label1.place(x=0, y=0)

    la = Label(top, text="Hello Admin!!!", font=('algerian', 15, 'bold'))
    la.place(x=200, y=100)

    Registerbt = Button(top, text="REGISTER HERE", width=20, height=2, font=('algerian', 15, 'bold'),
                        justify='center', bg="light blue", relief=SUNKEN, command=signup)
    Registerbt.place(x=20, y=475)

    photo_image1 = safe_load_image('register1.png', (250, 250))
    label2 = Label(top, image=photo_image1)
    label2.image = photo_image1
    label2.place(x=20, y=200)

    loginbt = Button(top, text="VIEW VOTER LIST", width=17, height=2, font=('algerian', 15, 'bold'),
                     justify='center', bg="light blue", relief=SUNKEN, command=table)
    loginbt.place(x=280, y=475)

    photo_image2 = safe_load_image('docu.png', (250, 250))
    label3 = Label(top, image=photo_image2)
    label3.image = photo_image2
    label3.place(x=280, y=200)

    res = Button(top, text="Result", width=17, height=2, font=('algerian', 15, 'bold'),
                 justify='center', bg="light blue", relief=SUNKEN, command=result_time)
    res.place(x=530, y=475)

    photo_image3 = safe_load_image('result.jpg', (250, 250))
    label4 = Label(top, image=photo_image3)
    label4.image = photo_image3
    label4.place(x=530, y=200)

# ------------------------------------------------ Login -------------------------------------------------

def login():
    def login_db():
        Username_entry = ent_user.get().strip()
        VoterId_entry = ent_voter.get().strip()
        Password_entry = ent_pass.get().strip()

        if not (Username_entry and VoterId_entry and Password_entry):
            tkinter.messagebox.showinfo("sorry", "Please complete the required field")
            return

        try:
            q3 = database()
            cur = q3.cursor()
            # fetch the constituency also so voting_frame has it
            cur.execute('SELECT usernames, password, Votercardnos, Constituency FROM facerec WHERE usernames = %s', (Username_entry,))
            rows = cur.fetchall()
            if not rows:
                tkinter.messagebox.showinfo("Sorry", "No account with that username")
                return

            db_username, db_password, db_votercard, db_constituency = rows[0]
            db_username = (db_username or "").strip()
            db_password = (db_password or "").strip()
            db_votercard = str(db_votercard or "").strip()
            db_constituency = (db_constituency or "").strip()

            if Username_entry == db_username and VoterId_entry == db_votercard and Password_entry == db_password:
                tkinter.messagebox.showinfo(f"Welcome {Username_entry}", "Logged in successfully")
                top_login.destroy()
                # pass the constituency into voting_frame
                voting_frame(db_username, db_votercard, "", db_constituency)
            else:
                parts = []
                if Username_entry != db_username:
                    parts.append("username")
                if VoterId_entry != db_votercard:
                    parts.append("voter ID")
                if Password_entry != db_password:
                    parts.append("password")
                tkinter.messagebox.showinfo("Sorry", "Wrong " + ", ".join(parts))
        except Exception as e:
            print("login_db error:", e, file=sys.stderr)
            tkinter.messagebox.showerror("Error", f"Login failed: {e}")

    top_login = Toplevel()
    top_login.geometry('800x600')
    top_login.title("LOGIN NOW")

    photo_image = safe_load_image('Homepage.png', (800, 600))
    label1 = Label(top_login, image=photo_image)
    label1.image = photo_image
    label1.place(x=0, y=0)

    Label(top_login, text="USERNAME", fg="black", font=("bold", 15)).place(x=230, y=200)
    Label(top_login, text="VOTERCARD ID", fg="black", font=("bold", 15)).place(x=230, y=300)
    Label(top_login, text="PASSWORD", fg="black", font=("bold", 15)).place(x=230, y=250)

    ent_user = Entry(top_login, width=15, font=("bold", 17), highlightthickness=2, bg="WHITE", relief=SUNKEN)
    ent_user.place(x=400, y=190)

    ent_voter = Entry(top_login, width=15, font=("bold", 17), show="*", highlightthickness=2, bg="WHITE", relief=SUNKEN)
    ent_voter.place(x=400, y=290)

    ent_pass = Entry(top_login, width=15, font=("bold", 17), show="*", highlightthickness=2, bg="WHITE", relief=SUNKEN)
    ent_pass.place(x=400, y=240)

    btn = Button(top_login, text="LOGIN", width=10, height=2, fg="black", font=('algerian', 15, 'bold'),
                 justify='center', bg="light blue", command=login_db)
    btn.place(x=380, y=400)

# -------------------------------- Voting session -----------------------------------------------

def TrackImages(un, votev):
    """Run face recognition and mark FaceAuth=yes when matched."""
    try:
        q4 = database()
        query4 = q4.cursor()
        query4.execute('SELECT * FROM facerec WHERE Votercardnos = %s', (votev,))
        result2 = query4.fetchall()
        if not result2:
            tkinter.messagebox.showinfo("Error", "Voter not found")
            return
        row2 = result2[0]
        FaceAuth = row2[9] if len(row2) > 9 else 'no'
    except Exception as e:
        print("TrackImages DB error:", e, file=sys.stderr)
        tkinter.messagebox.showerror("DB Error", f"{e}")
        return

    if FaceAuth == 'yes':
        tkinter.messagebox.showinfo("Verified", "Face Already Verified")
        return

    trainer_path = os.path.join("TrainingImageLabel", "Trainner.yml")
    if not os.path.exists(trainer_path):
        tkinter.messagebox.showwarning("No model", "No trained model found. Please capture faces and train first.")
        return

    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
    except Exception as e:
        tkinter.messagebox.showerror("OpenCV", "cv2.face.LBPHFaceRecognizer_create not available. Install opencv-contrib-python.")
        print("cv2.face error:", e, file=sys.stderr)
        return

    try:
        recognizer.read(trainer_path)
    except Exception as e:
        print("Could not read trainer file:", e, file=sys.stderr)
        tkinter.messagebox.showerror("Model", f"Could not read trainer file: {e}")
        return

    harcascadePath = "haarcascade_frontalface_default.xml"
    if not os.path.exists(harcascadePath):
        tkinter.messagebox.showerror("Missing file", f"{harcascadePath} not found.")
        return

    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df_path = os.path.join("VoterDetails", "VoterDetails.csv")
    if not os.path.exists(df_path):
        tkinter.messagebox.showinfo("Error", "No VoterDetails file found")
        return
    df = pd.read_csv(df_path)
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        tkinter.messagebox.showerror("Camera", "Could not open camera.")
        return

    font = cv2.FONT_HERSHEY_SIMPLEX
    matched = False
    tt1 = ""

    while True:
        ret, im = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            try:
                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            except Exception:
                continue
            if conf > 50:
                try:
                    a1 = df.loc[df['Id'] == Id]['name'].values
                    a1_str = a1[0] if len(a1) > 0 else ""
                except Exception:
                    a1_str = ""
                tt = f"{Id}-{a1_str}"
                tt1 = str(Id)
                matched = True
            else:
                tt = "Unknown"
                tt1 = "Unknown"
            cv2.putText(im, str(tt), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Face Recognition - press q to quit', im)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if matched and tt1 == str(votev):
            tkinter.messagebox.showinfo("Face", "Face Recognition successful")
            try:
                q6 = database()
                query6 = q6.cursor()
                query6.execute("UPDATE facerec SET FaceAuth = 'yes' WHERE Votercardnos = %s", (votev,))
                q6.commit()
            except Exception as e:
                print("Error updating FaceAuth:", e, file=sys.stderr)
            break

    cam.release()
    cv2.destroyAllWindows()

def voting_frame(Username_Verify, VoterId_Verify, Email_Verify, Consti_from_call):
    """
    voting_frame now accepts constituency as 4th parameter (Consti_from_call).
    If Consti_from_call is empty, it will fetch from DB before calling show().
    Includes a Change Password button (in Voting Desk).
    """

    un = Username_Verify
    votev = VoterId_Verify
    Consti = Consti_from_call or ""

    def cast_vote_and_thankyou(party, consti_local, votev_local):
        """Update DB result and mark voter as voted, show thank you UI."""
        try:
            q = database()
            cur = q.cursor()
            # mark voted
            cur.execute("UPDATE facerec SET VoteAuth = 'yes' WHERE Votercardnos = %s", (votev_local,))
            # increment the appropriate column in result table
            if party == 'bjp':
                cur.execute("UPDATE result SET bjp = bjp + 1")
            elif party == 'congress':
                cur.execute("UPDATE result SET congress = congress + 1")
            elif party == 'jds':
                cur.execute("UPDATE result SET jds = jds + 1")
            q.commit()
            q.close()
        except Exception as e:
            print("cast_vote DB error:", e, file=sys.stderr)
            tkinter.messagebox.showerror("DB Error", f"Could not record vote: {e}")
            return

        # Update local per-constituency counters (audit-style)
        try:
            os.makedirs("results", exist_ok=True)
            filename = os.path.join("results", f"{consti_local}_local_counts.txt")
            with open(filename, "a") as f:
                f.write(f"{datetime.datetime.now().isoformat()} - {party}\n")
        except Exception as e:
            print("local result update error:", e, file=sys.stderr)

        # Show thank you UI
        R6 = Toplevel()
        R6.geometry('900x600')
        R6.title('Thank you')

        photo = safe_load_image('ThankYou.jpg', (900, 600))
        panel = Label(R6, image=photo)
        panel.image = photo
        panel.pack(side="bottom", fill="both", expand="yes")

        btn = Button(R6, text="Logout", width=10, height=2, fg="black", font=('algerian', 15, 'bold'),
                        justify='center', bg="light blue", command=R6.destroy)
        btn.place(x=380, y=450)

    def vote_here_ui(consti_to_use, votev_local):
        """Show a modal with BJP / CONGRESS / JDS options (images) and cast vote."""
        win = Toplevel()
        win.geometry('800x600')
        win.title('Cast Your Vote')

        photo_bg = safe_load_image('Homepage.png', (800, 600))
        bg = Label(win, image=photo_bg)
        bg.image = photo_bg
        bg.place(x=0, y=0)

        Label(win, text="Choose your party", font=('algerian', 18, 'bold')).place(x=280, y=20)

        # load party images
        b_img = safe_load_image('b.png', (120, 80))
        c_img = safe_load_image('c.jpg', (120, 80))
        j_img = safe_load_image('jds.jpg', (120, 80))

        # BJP
        lbl_b = Label(win, image=b_img)
        lbl_b.image = b_img
        lbl_b.place(x=120, y=100)
        btn_b = Button(win, text="BJP", width=12, height=2, command=lambda: [cast_vote_and_thankyou('bjp', consti_to_use, votev_local), win.destroy()])
        btn_b.place(x=120, y=200)

        # CONGRESS
        lbl_c = Label(win, image=c_img)
        lbl_c.image = c_img
        lbl_c.place(x=340, y=100)
        btn_c = Button(win, text="CONGRESS", width=12, height=2, command=lambda: [cast_vote_and_thankyou('congress', consti_to_use, votev_local), win.destroy()])
        btn_c.place(x=340, y=200)

        # JDS
        lbl_j = Label(win, image=j_img)
        lbl_j.image = j_img
        lbl_j.place(x=560, y=100)
        btn_j = Button(win, text="JDS", width=12, height=2, command=lambda: [cast_vote_and_thankyou('jds', consti_to_use, votev_local), win.destroy()])
        btn_j.place(x=560, y=200)

    def vote_here(un_local, votev_local):
        # ensure we have the constituency; if blank fetch from DB
        consti_to_use = Consti
        try:
            qtemp = database()
            curtemp = qtemp.cursor()
            curtemp.execute('SELECT Constituency, FaceAuth, VoteAuth FROM facerec WHERE Votercardnos = %s', (votev_local,))
            row = curtemp.fetchone()
            if not row:
                tkinter.messagebox.showinfo("Error", "Voter not found")
                return
            if not consti_to_use:
                consti_to_use = (row[0] or "").strip()
            FaceAuth = row[1] if len(row) > 1 else 'no'
            VoteAuth = row[2] if len(row) > 2 else 'no'
        except Exception as e:
            print("vote_here DB error:", e, file=sys.stderr)
            tkinter.messagebox.showerror("DB Error", f"{e}")
            return

        if FaceAuth == 'yes' and VoteAuth == 'yes':
            tkinter.messagebox.showinfo("Verified", "Voted Already!!!")
            return
        if FaceAuth == 'yes' and VoteAuth == 'no':
            if not consti_to_use:
                tkinter.messagebox.showinfo("Error", "Constituency not set for this voter.")
                return
            # Show the three-party selection UI (BJP, CONGRESS, JDS)
            vote_here_ui(consti_to_use, votev_local)
        else:
            tkinter.messagebox.showinfo("Alredy", "Face Registration Not verified")

    # ---------------- Change Password UI inside Voting Desk ----------------
    def open_change_password_dialog(votev_local):
        """
        Show change password dialog with:
        - Old Password
        - New Password
        - Confirm New Password
        Uses 'change.png' (fallback to uploaded image).
        Updates 'password' column in DB when successful.
        """
        dlg = Toplevel()
        dlg.geometry('500x400')
        dlg.title('Change Password')

        photo = safe_load_image('change.png', (500, 400))
        panel = Label(dlg, image=photo)
        panel.image = photo
        panel.place(x=0, y=0)

        Label(dlg, text="Change Password", font=('algerian', 16, 'bold')).place(x=170, y=20)

        Label(dlg, text="Old Password", font=("bold", 12)).place(x=60, y=100)
        lbl_old = Entry(dlg, width=25, show="*", font=("bold", 12))
        lbl_old.place(x=200, y=100)

        Label(dlg, text="New Password", font=("bold", 12)).place(x=60, y=150)
        lbl_new = Entry(dlg, width=25, show="*", font=("bold", 12))
        lbl_new.place(x=200, y=150)

        Label(dlg, text="Confirm Password", font=("bold", 12)).place(x=60, y=200)
        lbl_confirm = Entry(dlg, width=25, show="*", font=("bold", 12))
        lbl_confirm.place(x=200, y=200)

        def do_change():
            old_p = lbl_old.get().strip()
            new_p = lbl_new.get().strip()
            conf_p = lbl_confirm.get().strip()
            if not (old_p and new_p and conf_p):
                tkinter.messagebox.showinfo("Error", "Please fill all fields")
                return
            if new_p != conf_p:
                tkinter.messagebox.showinfo("Error", "New password and Confirm password do not match")
                return
            try:
                q = database()
                cur = q.cursor()
                # verify old password for this votercard
                cur.execute("SELECT password FROM facerec WHERE Votercardnos = %s", (votev_local,))
                row = cur.fetchone()
                if not row:
                    tkinter.messagebox.showinfo("Error", "Voter not found")
                    q.close()
                    return
                db_old = (row[0] or "").strip()
                if db_old != old_p:
                    tkinter.messagebox.showinfo("Error", "Old password is incorrect")
                    q.close()
                    return
                # update password
                cur.execute("UPDATE facerec SET password = %s WHERE Votercardnos = %s", (new_p, votev_local))
                q.commit()
                q.close()
                tkinter.messagebox.showinfo("Success", "Password changed successfully")
                dlg.destroy()
            except Exception as e:
                print("change password error:", e, file=sys.stderr)
                tkinter.messagebox.showerror("DB Error", f"Could not change password: {e}")

        btn_change = Button(dlg, text="Change Password", width=15, height=2, command=do_change, bg="light blue")
        btn_change.place(x=180, y=270)

    # ---------------- End Change Password UI ----------------

    top = Toplevel()
    top.geometry('800x800')
    top.title('Voting Desk Table')

    photo_image = safe_load_image('Homepage.png', (800, 600))
    label1 = Label(top, image=photo_image)
    label1.image = photo_image
    label1.place(x=0, y=0)

    la = Label(top, text="VOTING DESK TABLE", font=('algerian', 20, 'bold'))
    la.place(x=250, y=50)

    photo_image1 = safe_load_image('face.jpg', (200, 200))
    label_face = Label(top, image=photo_image1)
    label_face.image = photo_image1
    label_face.place(x=100, y=100)

    photo_image2 = safe_load_image('vote.jpg', (200, 200))
    label_vote = Label(top, image=photo_image2)
    label_vote.image = photo_image2
    label_vote.place(x=100, y=330)

    btn = Button(top, text="FACE AUTHENTICATION", width=20, height=2, fg="black",
                 font=('algerian', 15, 'bold'), justify='center', bg="light blue",
                 command=partial(TrackImages, un, votev))
    btn.place(x=450, y=150)

    btn2 = Button(top, text="VOTE_HERE", width=20, height=2, fg="black",
                  font=('algerian', 15, 'bold'), justify='center', bg="light blue",
                  command=partial(vote_here, un, votev))
    btn2.place(x=450, y=260)

    # New Change Password button inside Voting Desk (per your request)
    btn_change_pwd = Button(top, text="CHANGE PASSWORD", width=20, height=2, fg="black",
                            font=('algerian', 12, 'bold'), justify='center', bg="orange",
                            command=partial(open_change_password_dialog, votev))
    btn_change_pwd.place(x=450, y=370)

# --------------------------------- Program start -----------------------------------------------

if __name__ == '__main__':
    main()
