Cyber Threat Console - Real-Time SIEM Dashboard
A full-stack, real-time cybersecurity threat console built with Python, MariaDB, and a 3D-animated JavaScript frontend to visualize and respond to simulated cyber attacks.

🚀 Live Demo
(It is highly recommended to record a short GIF of your project in action and place it here. This is the best way to impress viewers instantly. You can use free tools like LICEcap or ScreenToGif.)

📖 Introduction
In today's digital landscape, security teams are overwhelmed by "alert fatigue"—a constant stream of data from disconnected systems that makes it difficult to identify genuine threats. This project, the Cyber Threat Console, was built to solve this problem by providing a centralized, intelligent platform that transforms raw security data into clear, actionable insights. It's a prototype of a modern Security Information and Event Management (SIEM) tool designed to give security analysts clarity in the chaos.

✨ Key Features
This project is more than just a data log; it's an interactive and intelligent monitoring system with several advanced features:

🖥️ Live "Hacker-Style" Dashboard: A custom-built frontend with a 3D "Matrix" background (powered by Three.js), CRT scanline effects, and a dynamic "Threat Acquisition" panel that simulates tracing high-risk threats.

🧠 Intelligent Risk Scoring: The system goes beyond static rules by simulating a predictive model. It calculates a dynamic risk score for each incident based on threat severity, asset criticality, time of day, source country reputation, and historical attacker activity.

🌍 Real-Time Geolocation: Automatically enriches threat data by looking up the source IP address to identify the city and country of origin, providing crucial context for each incident.

🤖 Automated SOAR Simulation: Demonstrates a proof-of-concept for Security Orchestration, Automation, and Response (SOAR). For incidents exceeding a critical risk threshold, the system automatically triggers a defensive action by adding the attacker's IP to a simulated firewall blocklist.

⚙️ Full-Stack Architecture: Built with a robust Python (Flask) REST API on the backend and a responsive vanilla JavaScript frontend, all connected to a persistent MariaDB/MySQL database.

🛠️ Technology Stack
Category	Technology
Backend	Python, Flask, Pandas, Requests, MariaDB Connector
Frontend	HTML5, CSS3, Vanilla JavaScript (ES6+), Three.js
Database	MariaDB / MySQL
Tooling	Git, GitHub, Python venv

Export to Sheets
🏗️ System Architecture
The application follows a real-time, event-driven workflow:

Automated Attacker (attacker.py) → Python Flask API (app.py) → MariaDB Database → Frontend Dashboard

When a high-risk event is detected, a secondary workflow is triggered:

High-Risk Event in app.py → SOAR Script (block_ip.py) → Simulated Firewall (blocked_ips.txt)

🚀 Getting Started
To get a local copy up and running, follow these simple steps.

Prerequisites
Python 3.x

MariaDB Server or MySQL Server

Git

Installation & Setup
Clone the repository:

Bash

git clone https://github.com/pk859/CYBER-THREAT-CONSOLE.git
cd cyber-threat-console
Set up the Python backend:

Bash

# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate  # On Windows
# source venv/bin/activate # On macOS/Linux

# Install required packages
pip install -r requirements.txt
(Note: You will need to create a requirements.txt file by running pip freeze > requirements.txt in your activated environment.)

Set up the database:

Connect to your MariaDB/MySQL server.

Run the SQL script provided in setup.sql to create the database and tables. (You will need to create this file and add the SQL commands we used.)

Configure your environment:

Open app.py and update the db_config dictionary with your database username and password.

Run the application:

Terminal 1: Start the backend server.

Bash

python app.py
Terminal 2: Start the threat simulator.

Bash

python attacker.py
Browser: Open the index.html file in your web browser.

🔮 Future Scope
This project provides a strong foundation for a commercial-grade security tool. Future enhancements could include:

Threat Intelligence Integration: Connect to live feeds like VirusTotal to check IPs/domains against global blocklists.

Machine Learning: Implement a true ML model to move from simulated predictive scoring to genuine anomaly detection.

Full SOAR Implementation: Integrate with real enterprise tools like Jira (for ticketing) and firewall APIs (for actual IP blocking).

3D Globe Visualization: Replace the Matrix background with an interactive 3D globe that visualizes attack paths in real-time.