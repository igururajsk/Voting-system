🗳️ Smart Voting System using Face Recognition

A secure and automated voting system built using Python and OpenCV that uses face recognition (LBPH algorithm) to authenticate voters. The system ensures a fair voting process by allowing only verified users to cast their vote and preventing duplicate entries.

🚀 Features
🔐 Face-based voter authentication
📸 Image capture and dataset generation
🧠 Model training using LBPH algorithm
🗳️ One person → one vote system
📊 Real-time vote counting and result display
🗂️ SQLite database integration
⚡ Simple and interactive GUI using Tkinter

🛠️ Tech Stack
Language: Python
Libraries: OpenCV, NumPy, Tkinter
Database: SQLite
Concepts: Computer Vision, Image Processing, Biometric Authentication

⚙️ How It Works
Register Voter
Capture images using webcam
Store dataset for each user
Train Model
Train the face recognition model using LBPH
Authenticate Voter
Match live face with trained dataset
Cast Vote
Allow voting only if authentication is successful
View Results
Votes are stored and displayed in real-time

📂 Project Structure
Voting-System/
│── vote.py
│── vote11.py
│── report.py
│── votingsystem.db
│── images/
│── results/

▶️ Installation & Setup
1. Clone the Repository
git clone https://github.com/igururajsk/Voting-system.git
cd Voting-system
2. Install Dependencies
pip install opencv-python numpy
3. Run the Project
python vote.py

📌 Future Improvements
🌐 Convert to web-based system (Flask/MERN)
🔒 Add multi-factor authentication (OTP/Aadhaar integration)
📱 Mobile-friendly version
🤖 Use deep learning (CNN) for higher accuracy
🛡️ Add anti-spoofing (liveness detection)

⚠️ Limitations
LBPH has limited accuracy in poor lighting
No liveness detection (can be spoofed using images)
Not scalable for large populations

👨‍💻 Author
Gururaj S K

⭐ Support
If you like this project, consider giving it a ⭐ on GitHub!
