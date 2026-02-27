from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import Student, AcademicRecord
import csv
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime


# ================= SUBJECTS =================

SUBJECTS = {
    "BME": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Human Anatomy", "Programming in C"],
        2: ["Engineering Mathematics-II", "Physiology", "Electronic Devices", "Biochemistry", "Biomechanics"],
        3: ["Engineering Mathematics-III", "Biomedical Instrumentation", "Medical Imaging", "Biomaterials", "Signals and Systems"],
        4: ["Medical Electronics", "Biosensors", "Rehabilitation Engineering", "Tissue Engineering", "Digital Signal Processing"],
        5: ["Clinical Engineering", "Biomedical Signal Processing", "Medical Imaging Systems", "Artificial Organs"],
        6: ["Hospital Management", "Telemedicine", "Biomedical Optics", "Neural Engineering"],
        7: ["Bioinformatics", "Nanomedicine", "Medical Robotics", "Regulatory Affairs"],
        8: ["Biomedical Data Analysis", "Healthcare Technology", "Project Work", "Elective"]
    },
    "CIVIL": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Engineering Mechanics", "Engineering Graphics"],
        2: ["Engineering Mathematics-II", "Strength of Materials", "Surveying", "Building Materials", "Fluid Mechanics"],
        3: ["Engineering Mathematics-III", "Structural Analysis", "Geotechnical Engineering", "Hydraulics", "Concrete Technology"],
        4: ["Design of Concrete Structures", "Transportation Engineering", "Environmental Engineering", "Estimation and Costing", "Foundation Engineering"],
        5: ["Design of Steel Structures", "Water Resources Engineering", "Construction Management", "Advanced Surveying"],
        6: ["Earthquake Engineering", "Prestressed Concrete", "Remote Sensing and GIS", "Highway Engineering"],
        7: ["Bridge Engineering", "Structural Dynamics", "Waste Water Engineering", "Project Management"],
        8: ["Advanced Foundation Engineering", "Green Building Technology", "Project Work", "Elective"]
    },
    "CSD": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Design Thinking", "Programming in C"],
        2: ["Engineering Mathematics-II", "Data Structures", "Digital Logic Design", "Object Oriented Programming", "UI/UX Fundamentals"],
        3: ["Engineering Mathematics-III", "Computer Organization", "Database Management Systems", "Web Technologies", "Human Computer Interaction"],
        4: ["Design and Analysis of Algorithms", "Operating Systems", "Computer Networks", "Software Engineering", "Design Patterns"],
        5: ["Artificial Intelligence", "Mobile App Design", "Cloud Computing", "User Experience Design"],
        6: ["Machine Learning", "Full Stack Development", "Design Systems", "Information Architecture"],
        7: ["Product Design", "Interaction Design", "Data Visualization", "Accessibility Design"],
        8: ["Design Research", "Prototyping Tools", "Project Work", "Elective"]
    },
    "CSE": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Basic Electrical Engineering", "Programming in C"],
        2: ["Engineering Mathematics-II", "Data Structures", "Digital Logic Design", "Object Oriented Programming", "Discrete Mathematics"],
        3: ["Engineering Mathematics-III", "Computer Organization", "Database Management Systems", "Java Programming", "Software Engineering"],
        4: ["Design and Analysis of Algorithms", "Operating Systems", "Computer Networks", "Web Technologies", "Theory of Computation"],
        5: ["Compiler Design", "Artificial Intelligence", "Information Security", "Software Testing"],
        6: ["Machine Learning", "Cloud Computing", "Big Data Analytics", "Mobile Computing"],
        7: ["Deep Learning", "Blockchain Technology", "Internet of Things", "Cyber Security"],
        8: ["Natural Language Processing", "Computer Vision", "Project Work", "Elective"]
    },
    "EEE": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Basic Electrical Engineering", "Programming in C"],
        2: ["Engineering Mathematics-II", "Circuit Theory", "Electrical Machines-I", "Electronic Devices", "Measurements and Instrumentation"],
        3: ["Engineering Mathematics-III", "Electrical Machines-II", "Electromagnetic Fields", "Analog Electronics", "Signals and Systems"],
        4: ["Power Systems-I", "Control Systems", "Digital Electronics", "Microprocessors", "Power Electronics"],
        5: ["Power Systems-II", "Electrical Drives", "Power System Protection", "Renewable Energy Systems"],
        6: ["High Voltage Engineering", "Power System Analysis", "FACTS Devices", "Electric Vehicle Technology"],
        7: ["Smart Grid Technology", "Energy Management", "Power Quality", "Industrial Automation"],
        8: ["Distributed Generation", "Energy Storage Systems", "Project Work", "Elective"]
    },
    "ECE": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Basic Electrical Engineering", "Programming in C"],
        2: ["Engineering Mathematics-II", "Engineering Graphics", "Data Structures", "Electronic Devices", "Network Analysis"],
        3: ["Engineering Mathematics-III", "Analog Electronics", "Signals and Systems", "Electromagnetic Fields", "Digital Electronics"],
        4: ["Probability and Random Processes", "Microprocessors and Microcontrollers", "Linear Integrated Circuits", "Communication Systems", "Control Systems"],
        5: ["Digital Communication", "Digital Signal Processing", "Transmission Lines and Antennas", "VLSI Design"],
        6: ["Embedded Systems", "Optical Communication", "Wireless Communication", "IoT and Applications"],
        7: ["Microwave Engineering", "Satellite Communication", "Mobile Communication", "Digital Image Processing"],
        8: ["Radar Systems", "Wireless Sensor Networks", "Project Work", "Elective"]
    },
    "EIE": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Basic Electrical Engineering", "Programming in C"],
        2: ["Engineering Mathematics-II", "Electronic Devices", "Network Analysis", "Measurements and Instrumentation", "Digital Electronics"],
        3: ["Engineering Mathematics-III", "Analog Electronics", "Transducers and Sensors", "Control Systems", "Signals and Systems"],
        4: ["Process Control", "Microprocessors and Microcontrollers", "Industrial Instrumentation", "Linear Integrated Circuits", "Digital Signal Processing"],
        5: ["Analytical Instrumentation", "Biomedical Instrumentation", "Data Acquisition Systems", "Virtual Instrumentation"],
        6: ["Embedded Systems", "Optical Instrumentation", "VLSI Design", "Industrial Automation"],
        7: ["Robotics and Automation", "Smart Sensors", "IoT Systems", "SCADA Systems"],
        8: ["Advanced Control Systems", "Instrumentation Project Management", "Project Work", "Elective"]
    },
    "ISE": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Basic Electrical Engineering", "Programming in C"],
        2: ["Engineering Mathematics-II", "Data Structures", "Digital Logic Design", "Object Oriented Programming", "Discrete Mathematics"],
        3: ["Engineering Mathematics-III", "Computer Organization", "Database Management Systems", "Java Programming", "Software Engineering"],
        4: ["Design and Analysis of Algorithms", "Operating Systems", "Computer Networks", "Web Technologies", "Information Theory"],
        5: ["Information Security", "Data Mining", "Artificial Intelligence", "Software Testing"],
        6: ["Machine Learning", "Cloud Computing", "Big Data Analytics", "Network Security"],
        7: ["Cyber Security", "Information Retrieval", "Blockchain Technology", "DevOps"],
        8: ["Ethical Hacking", "Data Science", "Project Work", "Elective"]
    },
    "MECH": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Engineering Mechanics", "Engineering Graphics"],
        2: ["Engineering Mathematics-II", "Strength of Materials", "Thermodynamics", "Manufacturing Processes", "Material Science"],
        3: ["Engineering Mathematics-III", "Fluid Mechanics", "Kinematics of Machinery", "Metal Cutting and Machine Tools", "Engineering Metrology"],
        4: ["Heat Transfer", "Dynamics of Machinery", "Design of Machine Elements", "Hydraulics and Pneumatics", "Production Planning and Control"],
        5: ["Thermal Engineering", "Finite Element Analysis", "CAD/CAM", "Mechatronics"],
        6: ["Automobile Engineering", "Refrigeration and Air Conditioning", "Operations Research", "Industrial Engineering"],
        7: ["Robotics", "Composite Materials", "Renewable Energy Sources", "Advanced Manufacturing"],
        8: ["Computational Fluid Dynamics", "Additive Manufacturing", "Project Work", "Elective"]
    },
    "MECT": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Engineering Mechanics", "Engineering Graphics"],
        2: ["Engineering Mathematics-II", "Strength of Materials", "Electronic Devices", "Manufacturing Processes", "Thermodynamics"],
        3: ["Engineering Mathematics-III", "Sensors and Actuators", "Microcontrollers", "Fluid Mechanics", "Control Systems"],
        4: ["Robotics", "Mechatronics System Design", "Digital Electronics", "Hydraulics and Pneumatics", "CAD/CAM"],
        5: ["Industrial Automation", "Embedded Systems", "Machine Design", "PLC and SCADA"],
        6: ["Artificial Intelligence in Mechatronics", "Automotive Electronics", "Flexible Manufacturing Systems", "IoT Applications"],
        7: ["Advanced Robotics", "Autonomous Systems", "Smart Manufacturing", "Machine Vision"],
        8: ["Intelligent Control Systems", "Cyber Physical Systems", "Project Work", "Elective"]
    },
    "AGE": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Engineering Mechanics", "Engineering Graphics"],
        2: ["Engineering Mathematics-II", "Soil Science", "Agricultural Meteorology", "Farm Machinery", "Surveying"],
        3: ["Engineering Mathematics-III", "Irrigation Engineering", "Soil and Water Conservation", "Farm Power", "Crop Production"],
        4: ["Agricultural Processing", "Renewable Energy", "Watershed Management", "Tractor Design", "Dairy Engineering"],
        5: ["Post Harvest Technology", "Precision Agriculture", "Drip Irrigation", "Food Processing"],
        6: ["Agricultural Structures", "Farm Management", "Agro-based Industries", "Rural Development"],
        7: ["Smart Farming", "Agricultural Robotics", "Greenhouse Technology", "Organic Farming"],
        8: ["Sustainable Agriculture", "Agricultural Economics", "Project Work", "Elective"]
    },
    "AIDS": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Programming in Python", "Statistics"],
        2: ["Engineering Mathematics-II", "Data Structures", "Probability and Statistics", "Database Management Systems", "Linear Algebra"],
        3: ["Engineering Mathematics-III", "Machine Learning", "Data Visualization", "Big Data Analytics", "Computer Networks"],
        4: ["Deep Learning", "Natural Language Processing", "Data Mining", "Cloud Computing", "Operating Systems"],
        5: ["Artificial Intelligence", "Neural Networks", "Computer Vision", "Data Science"],
        6: ["Reinforcement Learning", "Time Series Analysis", "MLOps", "Business Intelligence"],
        7: ["Generative AI", "Edge AI", "Explainable AI", "Data Engineering"],
        8: ["AI Ethics", "Advanced Deep Learning", "Project Work", "Elective"]
    },
    "AIML": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Programming in Python", "Statistics"],
        2: ["Engineering Mathematics-II", "Data Structures", "Probability and Statistics", "Database Management Systems", "Linear Algebra"],
        3: ["Engineering Mathematics-III", "Machine Learning", "Data Analytics", "Computer Organization", "Discrete Mathematics"],
        4: ["Deep Learning", "Natural Language Processing", "Computer Vision", "Operating Systems", "Algorithm Design"],
        5: ["Artificial Intelligence", "Neural Networks", "Pattern Recognition", "Big Data"],
        6: ["Reinforcement Learning", "Ensemble Methods", "MLOps", "Cloud Computing"],
        7: ["Advanced Machine Learning", "Generative Models", "AutoML", "AI Applications"],
        8: ["Federated Learning", "Transfer Learning", "Project Work", "Elective"]
    },
    "BT": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Biology", "Biochemistry"],
        2: ["Engineering Mathematics-II", "Microbiology", "Cell Biology", "Genetics", "Organic Chemistry"],
        3: ["Molecular Biology", "Bioprocess Engineering", "Immunology", "Bioinformatics", "Enzymology"],
        4: ["Genetic Engineering", "Fermentation Technology", "Plant Biotechnology", "Animal Biotechnology", "Biostatistics"],
        5: ["Industrial Biotechnology", "Environmental Biotechnology", "Protein Engineering", "Bioreactor Design"],
        6: ["Pharmaceutical Biotechnology", "Nanobiotechnology", "Stem Cell Technology", "Biosensors"],
        7: ["Genomics and Proteomics", "Tissue Engineering", "Biopharmaceuticals", "Metabolic Engineering"],
        8: ["Synthetic Biology", "Bioethics", "Project Work", "Elective"]
    },
    "CSBS": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Programming in C", "Business Communication"],
        2: ["Engineering Mathematics-II", "Data Structures", "Digital Logic Design", "Object Oriented Programming", "Financial Accounting"],
        3: ["Engineering Mathematics-III", "Database Management Systems", "Computer Organization", "Business Analytics", "Microeconomics"],
        4: ["Operating Systems", "Computer Networks", "Software Engineering", "Management Information Systems", "Marketing Management"],
        5: ["Artificial Intelligence", "E-Commerce", "Enterprise Resource Planning", "Business Intelligence"],
        6: ["Machine Learning", "Cloud Computing", "Supply Chain Management", "Financial Management"],
        7: ["Data Science", "Digital Marketing", "Business Process Management", "Entrepreneurship"],
        8: ["Strategic Management", "Project Management", "Project Work", "Elective"]
    },
    "CT": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Programming in C", "Digital Electronics"],
        2: ["Engineering Mathematics-II", "Data Structures", "Computer Organization", "Object Oriented Programming", "Microprocessors"],
        3: ["Engineering Mathematics-III", "Database Management Systems", "Operating Systems", "Computer Networks", "Software Engineering"],
        4: ["Design and Analysis of Algorithms", "Web Technologies", "Embedded Systems", "Computer Graphics", "Theory of Computation"],
        5: ["Artificial Intelligence", "Compiler Design", "Mobile Computing", "Information Security"],
        6: ["Machine Learning", "Cloud Computing", "IoT", "Distributed Systems"],
        7: ["Big Data Analytics", "Cyber Security", "Blockchain", "Software Testing"],
        8: ["Advanced Computing", "DevOps", "Project Work", "Elective"]
    },
    "FT": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Food Microbiology", "Biochemistry"],
        2: ["Engineering Mathematics-II", "Food Chemistry", "Unit Operations", "Nutrition", "Food Analysis"],
        3: ["Food Processing", "Food Preservation", "Food Packaging", "Dairy Technology", "Cereal Technology"],
        4: ["Fruit and Vegetable Processing", "Meat and Fish Technology", "Food Biotechnology", "Food Engineering", "Quality Control"],
        5: ["Food Safety", "Bakery Technology", "Beverage Technology", "Food Plant Design"],
        6: ["Food Additives", "Fermentation Technology", "Nutraceuticals", "Food Laws"],
        7: ["Novel Food Processing", "Food Product Development", "Waste Management", "Food Business Management"],
        8: ["Food Toxicology", "Functional Foods", "Project Work", "Elective"]
    },
    "FASH": {
        1: ["Textile Science", "Fashion Illustration", "Elements of Design", "Pattern Making", "Sewing Techniques"],
        2: ["Fabric Study", "Fashion History", "Draping", "Garment Construction", "Color Theory"],
        3: ["Fashion Design", "Computer Aided Design", "Textile Testing", "Apparel Manufacturing", "Fashion Merchandising"],
        4: ["Fashion Marketing", "Costume Design", "Surface Ornamentation", "Quality Control", "Fashion Forecasting"],
        5: ["Fashion Communication", "Retail Management", "Accessory Design", "Knitwear Design"],
        6: ["Fashion Photography", "Brand Management", "Sustainable Fashion", "Fashion Entrepreneurship"],
        7: ["Fashion Show Production", "Digital Fashion", "Luxury Brand Management", "Fashion Styling"],
        8: ["Fashion Portfolio", "Fashion Business", "Project Work", "Elective"]
    },
    "IT": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Programming in C", "Basic Electrical Engineering"],
        2: ["Engineering Mathematics-II", "Data Structures", "Digital Logic Design", "Object Oriented Programming", "Discrete Mathematics"],
        3: ["Engineering Mathematics-III", "Database Management Systems", "Computer Organization", "Java Programming", "Software Engineering"],
        4: ["Design and Analysis of Algorithms", "Operating Systems", "Computer Networks", "Web Technologies", "Theory of Computation"],
        5: ["Information Security", "Data Mining", "Artificial Intelligence", "Mobile Application Development"],
        6: ["Machine Learning", "Cloud Computing", "Big Data Analytics", "Network Security"],
        7: ["Cyber Security", "Internet of Things", "Blockchain Technology", "DevOps"],
        8: ["Data Science", "Advanced Networking", "Project Work", "Elective"]
    },
    "TT": {
        1: ["Engineering Mathematics-I", "Engineering Physics", "Engineering Chemistry", "Textile Fibers", "Engineering Graphics"],
        2: ["Engineering Mathematics-II", "Yarn Manufacturing", "Fabric Manufacturing", "Textile Chemistry", "Textile Testing"],
        3: ["Engineering Mathematics-III", "Weaving Technology", "Knitting Technology", "Textile Processing", "Textile Mechanics"],
        4: ["Dyeing and Printing", "Nonwoven Technology", "Apparel Manufacturing", "Textile Design", "Quality Control"],
        5: ["Technical Textiles", "Textile Wet Processing", "Garment Technology", "Textile Machinery"],
        6: ["Smart Textiles", "Textile Management", "Fashion Technology", "Textile CAD"],
        7: ["Sustainable Textiles", "Textile Marketing", "Advanced Textile Processing", "Textile Innovation"],
        8: ["Textile Entrepreneurship", "Textile Research", "Project Work", "Elective"]
    }
}


# ================= HELPER =================

def get_subjects(department, semester):
    return SUBJECTS.get(department, {}).get(semester, [])

# ================= RESOURCES =================

RESOURCES = {
    "Engineering Mathematics-I": {
        "books": ["Higher Engineering Mathematics by B.S. Grewal", "Advanced Engineering Mathematics by Erwin Kreyszig"],
        "online": ["NPTEL - Mathematics I", "Khan Academy - Calculus", "MIT OCW - Single Variable Calculus"],
        "practice": ["Brilliant.org", "WolframAlpha", "Symbolab"]
    },
    "Engineering Mathematics-II": {
        "books": ["Higher Engineering Mathematics by B.S. Grewal", "Advanced Engineering Mathematics by Erwin Kreyszig"],
        "online": ["NPTEL - Mathematics II", "Khan Academy - Multivariable Calculus", "MIT OCW - Multivariable Calculus"],
        "practice": ["Brilliant.org", "WolframAlpha", "Paul's Online Math Notes"]
    },
    "Engineering Mathematics-III": {
        "books": ["Higher Engineering Mathematics by B.S. Grewal", "Probability and Statistics by Schaum's Outline"],
        "online": ["NPTEL - Probability and Statistics", "Khan Academy - Statistics", "MIT OCW - Probability"],
        "practice": ["Brilliant.org", "StatTrek.com", "R Programming Practice"]
    },
    "Engineering Physics": {
        "books": ["Engineering Physics by Gaur and Gupta", "Concepts of Modern Physics by Arthur Beiser"],
        "online": ["NPTEL - Physics", "MIT OCW - Physics I", "Khan Academy - Physics"],
        "practice": ["PhET Simulations", "HyperPhysics", "Physics Classroom"]
    },
    "Engineering Chemistry": {
        "books": ["Engineering Chemistry by Jain and Jain", "A Textbook of Engineering Chemistry by Shashi Chawla"],
        "online": ["NPTEL - Chemistry", "Khan Academy - Chemistry", "MIT OCW - Chemistry"],
        "practice": ["ChemCollective", "Virtual Labs", "Chemistry LibreTexts"]
    },
    "Programming in C": {
        "books": ["Let Us C by Yashavant Kanetkar", "The C Programming Language by Kernighan and Ritchie"],
        "online": ["GeeksforGeeks C Tutorial", "Programiz C", "Tutorialspoint C"],
        "practice": ["HackerRank", "LeetCode", "Codeforces"]
    },
    "Programming in Python": {
        "books": ["Python Crash Course by Eric Matthes", "Automate the Boring Stuff with Python"],
        "online": ["Python.org Tutorial", "Real Python", "Coursera - Python for Everybody"],
        "practice": ["HackerRank", "LeetCode", "Codewars"]
    },
    "Data Structures": {
        "books": ["Data Structures Using C by Reema Thareja", "Introduction to Algorithms by CLRS"],
        "online": ["GeeksforGeeks DSA", "Abdul Bari YouTube", "MIT OCW - Data Structures"],
        "practice": ["LeetCode", "HackerRank", "InterviewBit"]
    },
    "Database Management Systems": {
        "books": ["Database System Concepts by Korth", "Fundamentals of Database Systems by Elmasri and Navathe"],
        "online": ["NPTEL - DBMS", "Stanford DB Course", "W3Schools SQL"],
        "practice": ["SQLZoo", "HackerRank SQL", "LeetCode Database"]
    },
    "Operating Systems": {
        "books": ["Operating System Concepts by Silberschatz", "Modern Operating Systems by Tanenbaum"],
        "online": ["NPTEL - Operating Systems", "MIT OCW - OS", "GeeksforGeeks OS"],
        "practice": ["OS Simulator", "Practice Problems on GFG", "Previous Year GATE Questions"]
    },
    "Computer Networks": {
        "books": ["Computer Networks by Tanenbaum", "Data Communications and Networking by Forouzan"],
        "online": ["NPTEL - Computer Networks", "Coursera - Computer Networks", "GeeksforGeeks Networks"],
        "practice": ["Cisco Packet Tracer", "Wireshark Practice", "Network Simulators"]
    },
    "Design and Analysis of Algorithms": {
        "books": ["Introduction to Algorithms by CLRS", "Algorithm Design by Kleinberg and Tardos"],
        "online": ["MIT OCW - Algorithms", "Abdul Bari Algorithms", "GeeksforGeeks Algorithms"],
        "practice": ["LeetCode", "Codeforces", "TopCoder"]
    },
    "Machine Learning": {
        "books": ["Pattern Recognition and Machine Learning by Bishop", "Hands-On Machine Learning by Aurélien Géron"],
        "online": ["Coursera - Andrew Ng ML", "Fast.ai", "Google ML Crash Course"],
        "practice": ["Kaggle", "Google Colab", "UCI ML Repository"]
    },
    "Artificial Intelligence": {
        "books": ["Artificial Intelligence: A Modern Approach by Russell and Norvig", "AI by Rich and Knight"],
        "online": ["MIT OCW - AI", "Stanford CS221", "edX - AI"],
        "practice": ["AI Challenges on Kaggle", "OpenAI Gym", "Project Euler"]
    },
    "Deep Learning": {
        "books": ["Deep Learning by Goodfellow", "Neural Networks and Deep Learning by Michael Nielsen"],
        "online": ["Coursera - Deep Learning Specialization", "Fast.ai", "DeepLearning.AI"],
        "practice": ["Kaggle", "TensorFlow Playground", "PyTorch Tutorials"]
    },
    "Digital Logic Design": {
        "books": ["Digital Design by Morris Mano", "Digital Electronics by Malvino"],
        "online": ["NPTEL - Digital Circuits", "Neso Academy", "All About Circuits"],
        "practice": ["Logisim", "CircuitVerse", "Digital Logic Simulators"]
    },
    "Computer Organization": {
        "books": ["Computer Organization and Architecture by William Stallings", "COA by Hamacher"],
        "online": ["NPTEL - Computer Architecture", "MIT OCW - Computer Architecture", "GeeksforGeeks COA"],
        "practice": ["MIPS Simulator", "Assembly Practice", "Previous Year Questions"]
    },
    "Software Engineering": {
        "books": ["Software Engineering by Pressman", "Software Engineering by Sommerville"],
        "online": ["NPTEL - Software Engineering", "Coursera - Software Engineering", "Udacity"],
        "practice": ["GitHub Projects", "Open Source Contributions", "Case Studies"]
    },
    "Web Technologies": {
        "books": ["HTML and CSS by Jon Duckett", "JavaScript: The Good Parts by Douglas Crockford"],
        "online": ["MDN Web Docs", "W3Schools", "FreeCodeCamp"],
        "practice": ["CodePen", "Frontend Mentor", "JavaScript30"]
    },
    "Cloud Computing": {
        "books": ["Cloud Computing by Rajkumar Buyya", "Architecting the Cloud by Michael Kavis"],
        "online": ["AWS Training", "Google Cloud Skills Boost", "Azure Learn"],
        "practice": ["AWS Free Tier", "Google Cloud Free Trial", "Qwiklabs"]
    },
    "Cyber Security": {
        "books": ["The Web Application Hacker's Handbook", "Metasploit by David Kennedy"],
        "online": ["Cybrary", "OWASP", "Hack The Box Academy"],
        "practice": ["TryHackMe", "HackTheBox", "PentesterLab"]
    },
    "Object Oriented Programming": {
        "books": ["Object-Oriented Programming with C++ by Balagurusamy", "Head First Java"],
        "online": ["GeeksforGeeks OOP", "Java Tutorials by Oracle", "C++ Tutorials"],
        "practice": ["HackerRank", "Codingbat", "Practice Projects"]
    },
    "Java Programming": {
        "books": ["Head First Java", "Effective Java by Joshua Bloch"],
        "online": ["Oracle Java Tutorials", "JavaTpoint", "Baeldung"],
        "practice": ["HackerRank Java", "Codewars", "LeetCode"]
    },
    "Theory of Computation": {
        "books": ["Introduction to Automata Theory by Hopcroft", "Theory of Computation by Sipser"],
        "online": ["NPTEL - TOC", "MIT OCW - Theory of Computation", "GeeksforGeeks TOC"],
        "practice": ["JFLAP", "Previous Year GATE Questions", "Practice Problems"]
    },
    "Compiler Design": {
        "books": ["Compilers: Principles, Techniques, and Tools by Aho (Dragon Book)", "Compiler Design by Ullman"],
        "online": ["NPTEL - Compiler Design", "Stanford Compilers Course", "GeeksforGeeks Compiler"],
        "practice": ["Lex and Yacc Practice", "Build a Compiler Project", "Previous Year Questions"]
    },
    "Strength of Materials": {
        "books": ["Strength of Materials by R.K. Bansal", "Mechanics of Materials by Beer and Johnston"],
        "online": ["NPTEL - Strength of Materials", "MIT OCW - Mechanics", "Engineering Tutorials"],
        "practice": ["Numerical Problems", "Previous Year Questions", "Virtual Labs"]
    },
    "Thermodynamics": {
        "books": ["Engineering Thermodynamics by P.K. Nag", "Thermodynamics by Cengel and Boles"],
        "online": ["NPTEL - Thermodynamics", "MIT OCW - Thermodynamics", "Khan Academy"],
        "practice": ["Numerical Problems", "Steam Tables Practice", "Previous Year Questions"]
    },
    "Fluid Mechanics": {
        "books": ["Fluid Mechanics by R.K. Bansal", "Fluid Mechanics by Frank White"],
        "online": ["NPTEL - Fluid Mechanics", "MIT OCW - Fluid Dynamics", "Engineering Lectures"],
        "practice": ["CFD Simulations", "Numerical Problems", "Lab Experiments"]
    },
    "Control Systems": {
        "books": ["Control Systems Engineering by Nagrath and Gopal", "Modern Control Engineering by Ogata"],
        "online": ["NPTEL - Control Systems", "MIT OCW - Control Systems", "Brian Douglas YouTube"],
        "practice": ["MATLAB Simulink", "Control System Toolbox", "Previous Year Questions"]
    },
    "Digital Signal Processing": {
        "books": ["Digital Signal Processing by Proakis", "DSP by Oppenheim and Schafer"],
        "online": ["NPTEL - DSP", "MIT OCW - Signals and Systems", "DSP Lectures"],
        "practice": ["MATLAB DSP Toolbox", "Python Signal Processing", "Lab Assignments"]
    },
    "Microprocessors and Microcontrollers": {
        "books": ["Microprocessor Architecture by Ramesh Gaonkar", "The 8051 Microcontroller by Mazidi"],
        "online": ["NPTEL - Microprocessors", "Tutorials on 8086/8051", "Embedded Systems Tutorials"],
        "practice": ["8086 Emulator", "Arduino Projects", "Assembly Programming"]
    },
    "Embedded Systems": {
        "books": ["Embedded Systems by Rajkamal", "Programming Embedded Systems by Michael Barr"],
        "online": ["NPTEL - Embedded Systems", "Embedded.com", "Arduino/Raspberry Pi Tutorials"],
        "practice": ["Arduino Projects", "Raspberry Pi Projects", "Tinkercad Circuits"]
    },
    "VLSI Design": {
        "books": ["CMOS VLSI Design by Weste and Harris", "VLSI Design by Debaprasad Das"],
        "online": ["NPTEL - VLSI Design", "VLSI Tutorials", "Cadence Tutorials"],
        "practice": ["Verilog/VHDL Practice", "EDA Tools", "Design Projects"]
    },
    "Power Electronics": {
        "books": ["Power Electronics by M.H. Rashid", "Power Electronics by P.S. Bimbhra"],
        "online": ["NPTEL - Power Electronics", "MIT OCW - Power Electronics", "Video Lectures"],
        "practice": ["MATLAB Simulations", "Circuit Simulations", "Lab Experiments"]
    },
    "Electrical Machines-I": {
        "books": ["Electrical Machines by P.S. Bimbhra", "Electric Machinery by Fitzgerald"],
        "online": ["NPTEL - Electrical Machines", "MIT OCW - Electric Machines", "Video Tutorials"],
        "practice": ["Numerical Problems", "Lab Experiments", "Previous Year Questions"]
    },
    "Electrical Machines-II": {
        "books": ["Electrical Machines by P.S. Bimbhra", "Electric Machinery Fundamentals by Chapman"],
        "online": ["NPTEL - Electrical Machines II", "Video Lectures", "Engineering Tutorials"],
        "practice": ["Numerical Problems", "MATLAB Simulations", "Lab Work"]
    },
    "Big Data Analytics": {
        "books": ["Big Data Analytics by Seema Acharya", "Hadoop: The Definitive Guide"],
        "online": ["Coursera - Big Data Specialization", "edX - Big Data", "Hadoop Tutorials"],
        "practice": ["Kaggle Datasets", "Hadoop Practice", "Spark Tutorials"]
    },
    "Internet of Things": {
        "books": ["IoT Fundamentals by David Hanes", "Internet of Things by Arshdeep Bahga"],
        "online": ["Coursera - IoT Specialization", "IBM IoT Course", "Arduino IoT Tutorials"],
        "practice": ["Arduino IoT Projects", "Raspberry Pi IoT", "ThingSpeak"]
    },
    "Blockchain Technology": {
        "books": ["Mastering Blockchain by Imran Bashir", "Blockchain Basics by Daniel Drescher"],
        "online": ["Coursera - Blockchain", "IBM Blockchain", "Ethereum Tutorials"],
        "practice": ["Solidity Practice", "Build DApps", "Blockchain Projects"]
    },
    "Natural Language Processing": {
        "books": ["Speech and Language Processing by Jurafsky", "NLP with Python by Bird"],
        "online": ["Stanford NLP Course", "Coursera - NLP", "Hugging Face Tutorials"],
        "practice": ["Kaggle NLP", "NLTK Practice", "spaCy Tutorials"]
    },
    "Computer Vision": {
        "books": ["Computer Vision by Szeliski", "Digital Image Processing by Gonzalez"],
        "online": ["Stanford CS231n", "OpenCV Tutorials", "PyImageSearch"],
        "practice": ["Kaggle Computer Vision", "OpenCV Projects", "Image Processing Tasks"]
    },
    "Human Anatomy": {
        "books": ["Gray's Anatomy", "Human Anatomy by B.D. Chaurasia"],
        "online": ["Khan Academy - Anatomy", "Visible Body", "Anatomy Zone YouTube"],
        "practice": ["Anatomy Practice Tests", "3D Anatomy Apps", "Previous Year Questions"]
    },
    "Physiology": {
        "books": ["Textbook of Medical Physiology by Guyton", "Physiology by Linda Costanzo"],
        "online": ["Khan Academy - Physiology", "Physiology Web", "Armando Hasudungan YouTube"],
        "practice": ["Physiology MCQs", "Case Studies", "Lab Simulations"]
    },
    "Electronic Devices": {
        "books": ["Electronic Devices by Floyd", "Semiconductor Physics and Devices by Neamen"],
        "online": ["NPTEL - Electronic Devices", "All About Circuits", "Electronics Tutorials"],
        "practice": ["Circuit Simulations", "SPICE Practice", "Previous Year Questions"]
    },
    "Biochemistry": {
        "books": ["Lehninger Principles of Biochemistry", "Harper's Illustrated Biochemistry"],
        "online": ["Khan Academy - Biochemistry", "MIT OCW - Biochemistry", "Biochemistry Lectures"],
        "practice": ["Biochemistry MCQs", "Metabolic Pathway Practice", "Lab Exercises"]
    },
    "Biomechanics": {
        "books": ["Biomechanics by Nigg and Herzog", "Basic Biomechanics by Susan Hall"],
        "online": ["Biomechanics Lectures", "OpenSim Tutorials", "Biomechanics Videos"],
        "practice": ["Motion Analysis Software", "Biomechanics Problems", "Lab Experiments"]
    },
    "Biomedical Instrumentation": {
        "books": ["Biomedical Instrumentation by Khandpur", "Medical Instrumentation by Webster"],
        "online": ["NPTEL - Biomedical Instrumentation", "MIT OCW", "Biomedical Engineering Lectures"],
        "practice": ["Instrument Simulations", "Lab Experiments", "Previous Year Questions"]
    },
    "Medical Imaging": {
        "books": ["Medical Imaging Signals and Systems by Prince", "The Essential Physics of Medical Imaging"],
        "online": ["Coursera - Medical Imaging", "Radiopaedia", "Medical Imaging Lectures"],
        "practice": ["Image Processing Software", "DICOM Practice", "Case Studies"]
    },
    "Biomaterials": {
        "books": ["Biomaterials Science by Ratner", "Introduction to Biomaterials by Narayan"],
        "online": ["MIT OCW - Biomaterials", "Biomaterials Lectures", "Materials Science Videos"],
        "practice": ["Material Selection Problems", "Lab Experiments", "Case Studies"]
    },
    "Signals and Systems": {
        "books": ["Signals and Systems by Oppenheim", "Signals and Systems by Nagoor Kani"],
        "online": ["NPTEL - Signals and Systems", "MIT OCW", "Signal Processing Videos"],
        "practice": ["MATLAB Practice", "Signal Analysis Problems", "Previous Year Questions"]
    },
    "Engineering Mechanics": {
        "books": ["Engineering Mechanics by Beer and Johnston", "Engineering Mechanics by Timoshenko"],
        "online": ["NPTEL - Engineering Mechanics", "MIT OCW - Statics and Dynamics", "Engineering Lectures"],
        "practice": ["Numerical Problems", "Previous Year Questions", "Virtual Labs"]
    },
    "Engineering Graphics": {
        "books": ["Engineering Drawing by N.D. Bhatt", "Engineering Graphics by Agrawal"],
        "online": ["NPTEL - Engineering Drawing", "AutoCAD Tutorials", "Engineering Graphics Videos"],
        "practice": ["AutoCAD Practice", "Drawing Exercises", "Projection Problems"]
    },
    "Discrete Mathematics": {
        "books": ["Discrete Mathematics by Kenneth Rosen", "Discrete Mathematics by Tremblay"],
        "online": ["MIT OCW - Discrete Mathematics", "Coursera - Discrete Math", "GeeksforGeeks Discrete Math"],
        "practice": ["Practice Problems", "Previous Year GATE Questions", "Online Quizzes"]
    },
    "Statistics": {
        "books": ["Statistics by Gupta and Kapoor", "Introduction to Probability and Statistics"],
        "online": ["Khan Academy - Statistics", "StatQuest YouTube", "Coursera - Statistics"],
        "practice": ["R Programming", "Statistical Analysis Problems", "Practice Datasets"]
    },
    "Linear Algebra": {
        "books": ["Linear Algebra by Gilbert Strang", "Linear Algebra by Hoffman and Kunze"],
        "online": ["MIT OCW - Linear Algebra (Gilbert Strang)", "Khan Academy", "3Blue1Brown YouTube"],
        "practice": ["Matrix Problems", "Computational Practice", "Previous Year Questions"]
    },
    "Probability and Statistics": {
        "books": ["Probability and Statistics by Schaum's", "Introduction to Probability by Bertsekas"],
        "online": ["MIT OCW - Probability", "Khan Academy", "StatQuest YouTube"],
        "practice": ["Statistical Software Practice", "Problem Sets", "Data Analysis"]
    },
    "Basic Electrical Engineering": {
        "books": ["Basic Electrical Engineering by D.C. Kulshreshtha", "Electrical Engineering Fundamentals"],
        "online": ["NPTEL - Basic Electrical Engineering", "All About Circuits", "Electrical4U"],
        "practice": ["Circuit Simulations", "Numerical Problems", "Lab Experiments"]
    },
    "Circuit Theory": {
        "books": ["Network Analysis by Van Valkenburg", "Circuit Theory by Chakrabarti"],
        "online": ["NPTEL - Circuit Theory", "MIT OCW - Circuits", "All About Circuits"],
        "practice": ["Circuit Simulations", "Network Problems", "Previous Year Questions"]
    },
    "Analog Electronics": {
        "books": ["Integrated Electronics by Millman Halkias", "Electronic Devices by Boylestad"],
        "online": ["NPTEL - Analog Circuits", "All About Electronics", "Electronics Tutorials"],
        "practice": ["Circuit Simulations", "Amplifier Design", "Lab Experiments"]
    },
    "Digital Electronics": {
        "books": ["Digital Electronics by Morris Mano", "Digital Principles by Malvino"],
        "online": ["NPTEL - Digital Electronics", "Neso Academy", "Electronics Hub"],
        "practice": ["Logisim", "Digital Circuit Simulations", "Previous Year Questions"]
    },
    "Microprocessors": {
        "books": ["Microprocessor 8086 by Ramesh Gaonkar", "Microprocessors and Interfacing by Hall"],
        "online": ["NPTEL - Microprocessors", "8086 Tutorials", "Assembly Language Videos"],
        "practice": ["8086 Emulator", "Assembly Programming", "Interfacing Projects"]
    },
    "Information Security": {
        "books": ["Cryptography and Network Security by Forouzan", "Information Security by Mark Stamp"],
        "online": ["Coursera - Cybersecurity", "Cybrary", "OWASP Resources"],
        "practice": ["TryHackMe", "Cryptography Challenges", "Security Labs"]
    },
    "Data Mining": {
        "books": ["Data Mining Concepts and Techniques by Han", "Introduction to Data Mining by Tan"],
        "online": ["Coursera - Data Mining", "Stanford Data Mining", "Data Mining Tutorials"],
        "practice": ["Kaggle", "Weka Practice", "Data Mining Projects"]
    },
    "Software Testing": {
        "books": ["Software Testing by Ron Patton", "The Art of Software Testing by Myers"],
        "online": ["ISTQB Resources", "Software Testing Help", "Guru99 Testing"],
        "practice": ["Selenium Practice", "Test Case Writing", "Bug Tracking Tools"]
    },
    "Network Security": {
        "books": ["Network Security Essentials by Stallings", "Network Security by Kaufman"],
        "online": ["Coursera - Network Security", "Cybrary", "Network Security Tutorials"],
        "practice": ["Wireshark Labs", "Security Tools Practice", "CTF Challenges"]
    },
    "Information Retrieval": {
        "books": ["Introduction to Information Retrieval by Manning", "Modern Information Retrieval"],
        "online": ["Stanford IR Course", "Information Retrieval Lectures", "Search Engine Tutorials"],
        "practice": ["Lucene/Solr Practice", "Search Engine Projects", "IR Assignments"]
    },
    "DevOps": {
        "books": ["The DevOps Handbook", "Continuous Delivery by Jez Humble"],
        "online": ["DevOps Roadmap", "Docker Tutorials", "Kubernetes Documentation"],
        "practice": ["Docker Practice", "CI/CD Pipeline Projects", "Cloud Labs"]
    },
    "Ethical Hacking": {
        "books": ["The Hacker Playbook by Peter Kim", "Penetration Testing by Georgia Weidman"],
        "online": ["Hack The Box Academy", "TryHackMe", "Cybrary Ethical Hacking"],
        "practice": ["HackTheBox", "TryHackMe Labs", "VulnHub"]
    },
    "Data Science": {
        "books": ["Python for Data Analysis by McKinney", "Data Science from Scratch by Joel Grus"],
        "online": ["Coursera - Data Science", "DataCamp", "Kaggle Learn"],
        "practice": ["Kaggle Competitions", "Data Analysis Projects", "Jupyter Notebooks"]
    },
    "Manufacturing Processes": {
        "books": ["Manufacturing Processes by Kalpakjian", "Workshop Technology by Hajra Choudhury"],
        "online": ["NPTEL - Manufacturing", "MIT OCW - Manufacturing", "Manufacturing Videos"],
        "practice": ["Workshop Practice", "Process Selection Problems", "Lab Experiments"]
    },
    "Material Science": {
        "books": ["Materials Science and Engineering by Callister", "Material Science by Raghavan"],
        "online": ["MIT OCW - Materials Science", "NPTEL - Materials", "Materials Engineering Videos"],
        "practice": ["Material Testing Labs", "Phase Diagram Problems", "Case Studies"]
    },
    "Design Thinking": {
        "books": ["Design Thinking by Tim Brown", "Creative Confidence by Tom Kelley"],
        "online": ["IDEO U", "Stanford d.school", "Coursera - Design Thinking"],
        "practice": ["Design Challenges", "Prototyping Projects", "Case Studies"]
    },
    "UI/UX Fundamentals": {
        "books": ["Don't Make Me Think by Steve Krug", "The Design of Everyday Things by Don Norman"],
        "online": ["Coursera - UI/UX Design", "Google UX Design", "Nielsen Norman Group"],
        "practice": ["Figma Practice", "Design Challenges", "User Research Projects"]
    },
    "Surveying": {
        "books": ["Surveying by Punmia", "Surveying and Levelling by Kanetkar"],
        "online": ["NPTEL - Surveying", "Surveying Lectures", "Total Station Tutorials"],
        "practice": ["Field Practice", "Surveying Problems", "Lab Experiments"]
    },
    "Building Materials": {
        "books": ["Building Materials by Rangwala", "Construction Materials by Somayaji"],
        "online": ["NPTEL - Building Materials", "Construction Materials Videos", "Material Testing Tutorials"],
        "practice": ["Material Testing Labs", "Quality Control Problems", "Case Studies"]
    },
    "Structural Analysis": {
        "books": ["Structural Analysis by Hibbeler", "Structural Analysis by Ramamrutham"],
        "online": ["NPTEL - Structural Analysis", "MIT OCW - Structures", "Engineering Lectures"],
        "practice": ["SAP2000 Practice", "Structural Problems", "Previous Year Questions"]
    },
    "Geotechnical Engineering": {
        "books": ["Soil Mechanics by Terzaghi", "Geotechnical Engineering by Murthy"],
        "online": ["NPTEL - Geotechnical Engineering", "MIT OCW", "Soil Mechanics Videos"],
        "practice": ["Soil Testing Labs", "Foundation Design Problems", "Case Studies"]
    },
    "Hydraulics": {
        "books": ["Hydraulics by Modi and Seth", "Fluid Mechanics and Hydraulics by Bansal"],
        "online": ["NPTEL - Hydraulics", "Open Channel Flow Videos", "Hydraulics Tutorials"],
        "practice": ["Hydraulic Simulations", "Flow Problems", "Lab Experiments"]
    },
    "Concrete Technology": {
        "books": ["Concrete Technology by M.S. Shetty", "Properties of Concrete by Neville"],
        "online": ["NPTEL - Concrete Technology", "Concrete Mix Design Videos", "Construction Tutorials"],
        "practice": ["Mix Design Problems", "Concrete Testing Labs", "Quality Control"]
    },
    "Transducers and Sensors": {
        "books": ["Instrumentation and Control Systems by W. Bolton", "Sensors and Transducers by D. Patranabis"],
        "online": ["NPTEL - Instrumentation", "Sensor Technology Tutorials", "Electronics Hub Sensors"],
        "practice": ["Sensor Interfacing Projects", "Arduino Sensor Labs", "Calibration Exercises"]
    },
    "Process Control": {
        "books": ["Process Control Instrumentation Technology by Curtis Johnson", "Process Control by Stephanopoulos"],
        "online": ["NPTEL - Process Control", "Control Engineering Videos", "Process Control Tutorials"],
        "practice": ["MATLAB Control Simulations", "PID Tuning Exercises", "Control System Design"]
    },
    "Industrial Instrumentation": {
        "books": ["Industrial Instrumentation by Krishna Kant", "Process Instrumentation by Norman Anderson"],
        "online": ["NPTEL - Industrial Instrumentation", "Instrumentation Videos", "Process Control Tutorials"],
        "practice": ["Instrumentation Projects", "Calibration Labs", "Field Instruments Practice"]
    },
    "Linear Integrated Circuits": {
        "books": ["Op-Amps and Linear Integrated Circuits by Ramakant Gayakwad", "Linear Integrated Circuits by Roy Choudhary"],
        "online": ["NPTEL - Linear IC", "Op-Amp Tutorials", "Electronics Tutorials"],
        "practice": ["Circuit Simulations", "Op-Amp Design Problems", "Lab Experiments"]
    },
    "Analytical Instrumentation": {
        "books": ["Analytical Instrumentation by Kalsi", "Instrumental Methods of Analysis by Willard"],
        "online": ["Analytical Chemistry Videos", "Instrumentation Lectures", "Spectroscopy Tutorials"],
        "practice": ["Spectroscopy Problems", "Chromatography Labs", "Instrument Operation"]
    },
    "Data Acquisition Systems": {
        "books": ["Data Acquisition Systems by Park", "Data Acquisition Handbook by Omega"],
        "online": ["LabVIEW Tutorials", "DAQ System Videos", "National Instruments Resources"],
        "practice": ["LabVIEW Projects", "DAQ Hardware Practice", "Signal Conditioning"]
    },
    "Virtual Instrumentation": {
        "books": ["LabVIEW for Everyone by Travis", "Virtual Instrumentation by Sumathi"],
        "online": ["LabVIEW Training", "NI LabVIEW Tutorials", "Virtual Instrumentation Videos"],
        "practice": ["LabVIEW Projects", "VI Development", "Instrument Control"]
    },
    "Optical Instrumentation": {
        "books": ["Optical Instrumentation by Malacara", "Fundamentals of Photonics by Saleh"],
        "online": ["Optics Lectures", "Photonics Tutorials", "Optical Engineering Videos"],
        "practice": ["Optical System Design", "Photonics Labs", "Laser Applications"]
    },
    "Robotics and Automation": {
        "books": ["Robotics by Groover", "Introduction to Robotics by Craig"],
        "online": ["NPTEL - Robotics", "MIT OCW - Robotics", "ROS Tutorials"],
        "practice": ["Robot Simulation", "ROS Projects", "Automation Labs"]
    },
    "Smart Sensors": {
        "books": ["Smart Sensors and MEMS by Yurish", "Intelligent Sensor Systems by Meijer"],
        "online": ["Smart Sensor Technology", "IoT Sensor Tutorials", "MEMS Lectures"],
        "practice": ["Smart Sensor Projects", "IoT Integration", "Sensor Networks"]
    },
    "IoT Systems": {
        "books": ["IoT Fundamentals by Hanes", "Building the Internet of Things by Kranz"],
        "online": ["IoT Tutorials", "AWS IoT", "Azure IoT Hub"],
        "practice": ["IoT Projects", "Cloud Integration", "Sensor Networks"]
    },
    "SCADA Systems": {
        "books": ["SCADA Systems by Boyer", "Practical SCADA for Industry by Macdonald"],
        "online": ["SCADA Tutorials", "Industrial Automation Videos", "HMI Design"],
        "practice": ["SCADA Software Practice", "HMI Development", "Industrial Projects"]
    },
    "Advanced Control Systems": {
        "books": ["Modern Control Engineering by Ogata", "Advanced Control System Design by Levine"],
        "online": ["MIT OCW - Advanced Control", "Control Theory Videos", "MATLAB Control Tutorials"],
        "practice": ["MATLAB Simulations", "Control Design Projects", "State Space Analysis"]
    },
    "Instrumentation Project Management": {
        "books": ["Project Management by PMI", "Engineering Project Management by Badiru"],
        "online": ["Project Management Tutorials", "PMI Resources", "Engineering Management Videos"],
        "practice": ["Project Planning Exercises", "Case Studies", "MS Project Practice"]
    },
    "Measurements and Instrumentation": {
        "books": ["Electrical and Electronic Measurements by Sawhney", "Instrumentation Measurement by Morris"],
        "online": ["NPTEL - Measurements", "Instrumentation Videos", "Measurement Techniques"],
        "practice": ["Measurement Labs", "Calibration Exercises", "Error Analysis"]
    },
    "Network Analysis": {
        "books": ["Network Analysis by Van Valkenburg", "Circuit Analysis by Hayt"],
        "online": ["NPTEL - Network Analysis", "Circuit Theory Videos", "Network Theorems"],
        "practice": ["Circuit Problems", "Network Simulations", "Previous Year Questions"]
    },
    "Electromagnetic Fields": {
        "books": ["Engineering Electromagnetics by Hayt", "Electromagnetics by Sadiku"],
        "online": ["NPTEL - Electromagnetics", "MIT OCW - EM Fields", "EM Theory Videos"],
        "practice": ["Field Problems", "Maxwell Equations Practice", "Wave Propagation"]
    },
    "Probability and Random Processes": {
        "books": ["Probability and Random Processes by Stark", "Probability Random Variables by Papoulis"],
        "online": ["MIT OCW - Probability", "Random Processes Lectures", "Stochastic Processes"],
        "practice": ["Probability Problems", "Statistical Analysis", "Random Process Simulations"]
    },
    "Communication Systems": {
        "books": ["Communication Systems by Simon Haykin", "Principles of Communication by Taub and Schilling"],
        "online": ["NPTEL - Communication Systems", "MIT OCW - Communications", "Modulation Tutorials"],
        "practice": ["MATLAB Communication Simulations", "Modulation Problems", "Signal Analysis"]
    },
    "Digital Communication": {
        "books": ["Digital Communications by Proakis", "Digital Communication by Sklar"],
        "online": ["NPTEL - Digital Communication", "Digital Modulation Videos", "Communication Theory"],
        "practice": ["MATLAB Simulations", "Error Correction Coding", "Digital Modulation"]
    },
    "Transmission Lines and Antennas": {
        "books": ["Antenna Theory by Balanis", "Transmission Lines and Networks by Chipman"],
        "online": ["NPTEL - Antennas", "Antenna Design Videos", "RF Engineering Tutorials"],
        "practice": ["Antenna Design Software", "Smith Chart Problems", "RF Simulations"]
    },
    "Optical Communication": {
        "books": ["Optical Fiber Communications by Gerd Keiser", "Fiber Optic Communications by Palais"],
        "online": ["NPTEL - Optical Communication", "Fiber Optics Videos", "Photonics Tutorials"],
        "practice": ["Fiber Optic Labs", "Link Budget Calculations", "Optical System Design"]
    },
    "Wireless Communication": {
        "books": ["Wireless Communications by Rappaport", "Wireless Communication by Goldsmith"],
        "online": ["NPTEL - Wireless Communication", "5G Technology Videos", "Mobile Communications"],
        "practice": ["Wireless System Design", "Channel Modeling", "Network Simulations"]
    },
    "IoT and Applications": {
        "books": ["Internet of Things by Raj Kamal", "IoT Fundamentals by Hanes"],
        "online": ["IoT Specialization Coursera", "AWS IoT", "IoT Tutorials"],
        "practice": ["IoT Projects", "Sensor Integration", "Cloud Platforms"]
    },
    "Microwave Engineering": {
        "books": ["Microwave Engineering by Pozar", "Microwave Devices and Circuits by Liao"],
        "online": ["NPTEL - Microwave Engineering", "RF and Microwave Videos", "Microwave Tutorials"],
        "practice": ["Microwave Design Software", "S-Parameter Analysis", "RF Simulations"]
    },
    "Satellite Communication": {
        "books": ["Satellite Communications by Dennis Roddy", "Satellite Communication by Pratt"],
        "online": ["NPTEL - Satellite Communication", "Space Communication Videos", "Satellite Systems"],
        "practice": ["Link Budget Calculations", "Orbital Mechanics", "Satellite System Design"]
    },
    "Mobile Communication": {
        "books": ["Mobile Communications by Jochen Schiller", "Wireless and Mobile Communications by Mishra"],
        "online": ["NPTEL - Mobile Communication", "4G/5G Technology", "Cellular Networks"],
        "practice": ["Network Planning", "Mobile System Simulations", "Protocol Analysis"]
    },
    "Digital Image Processing": {
        "books": ["Digital Image Processing by Gonzalez and Woods", "Image Processing by Jain"],
        "online": ["NPTEL - Image Processing", "OpenCV Tutorials", "MATLAB Image Processing"],
        "practice": ["Image Processing Projects", "OpenCV Practice", "MATLAB Assignments"]
    },
    "Radar Systems": {
        "books": ["Introduction to Radar Systems by Skolnik", "Radar Principles by Nadav Levanon"],
        "online": ["NPTEL - Radar Systems", "Radar Engineering Videos", "Signal Processing for Radar"],
        "practice": ["Radar Simulations", "Signal Processing", "Target Detection"]
    },
    "Wireless Sensor Networks": {
        "books": ["Wireless Sensor Networks by Kazem Sohraby", "WSN by Holger Karl"],
        "online": ["Coursera - WSN", "Sensor Network Tutorials", "IoT and WSN"],
        "practice": ["Network Simulations", "Sensor Deployment", "Protocol Implementation"]
    },
    "Microcontrollers": {
        "books": ["The 8051 Microcontroller by Mazidi", "PIC Microcontroller by Mazidi"],
        "online": ["Microcontroller Tutorials", "Arduino Programming", "Embedded C"],
        "practice": ["Arduino Projects", "8051 Programming", "Interfacing Labs"]
    },
    "Robotics": {
        "books": ["Introduction to Robotics by Craig", "Robotics Vision and Control by Corke"],
        "online": ["MIT OCW - Robotics", "ROS Tutorials", "Robot Programming"],
        "practice": ["Robot Simulations", "ROS Projects", "Kinematics Problems"]
    },
    "Mechatronics System Design": {
        "books": ["Mechatronics by Bolton", "Mechatronics System Design by Shetty"],
        "online": ["NPTEL - Mechatronics", "System Design Videos", "Mechatronics Tutorials"],
        "practice": ["System Integration Projects", "Design Problems", "Simulation Software"]
    },
    "Hydraulics and Pneumatics": {
        "books": ["Hydraulics and Pneumatics by Andrew Parr", "Fluid Power by Anthony Esposito"],
        "online": ["NPTEL - Hydraulics", "Pneumatic Systems Videos", "Fluid Power Tutorials"],
        "practice": ["Circuit Design", "System Simulations", "Lab Experiments"]
    },
    "CAD/CAM": {
        "books": ["CAD/CAM by Groover", "Computer Aided Design by Zeid"],
        "online": ["NPTEL - CAD/CAM", "AutoCAD Tutorials", "CATIA Training"],
        "practice": ["CAD Software Practice", "3D Modeling", "CNC Programming"]
    },
    "PLC and SCADA": {
        "books": ["Programmable Logic Controllers by Petruzella", "PLC Programming by Bolton"],
        "online": ["PLC Tutorials", "Ladder Logic Programming", "SCADA Systems"],
        "practice": ["PLC Programming Software", "Ladder Logic Exercises", "Industrial Automation"]
    },
    "Artificial Intelligence in Mechatronics": {
        "books": ["AI for Robotics", "Intelligent Mechatronics Systems"],
        "online": ["AI in Robotics Courses", "Machine Learning for Mechatronics", "Intelligent Systems"],
        "practice": ["AI Projects", "Robot Learning", "Intelligent Control"]
    },
    "Automotive Electronics": {
        "books": ["Automotive Electronics by Ribbens", "Automotive Electrical Systems"],
        "online": ["Automotive Electronics Videos", "Vehicle Systems Tutorials", "ECU Programming"],
        "practice": ["Automotive Projects", "CAN Bus Practice", "Vehicle Diagnostics"]
    },
    "Flexible Manufacturing Systems": {
        "books": ["Flexible Manufacturing Systems by Groover", "Automation Production Systems by Groover"],
        "online": ["NPTEL - Manufacturing Systems", "FMS Videos", "Industrial Automation"],
        "practice": ["System Design", "Simulation Software", "Case Studies"]
    },
    "IoT Applications": {
        "books": ["IoT Applications by Raj Kamal", "Practical IoT Projects"],
        "online": ["IoT Project Tutorials", "Cloud IoT Platforms", "Sensor Integration"],
        "practice": ["IoT Projects", "Cloud Integration", "Real-world Applications"]
    },
    "Advanced Robotics": {
        "books": ["Advanced Robotics by Siciliano", "Robot Modeling and Control by Spong"],
        "online": ["Advanced Robotics Courses", "Robot Control Videos", "ROS Advanced"],
        "practice": ["Advanced Robot Projects", "Control Algorithms", "Vision Systems"]
    },
    "Autonomous Systems": {
        "books": ["Autonomous Robots by Siegwart", "Probabilistic Robotics by Thrun"],
        "online": ["Self-Driving Car Courses", "Autonomous Systems Videos", "SLAM Tutorials"],
        "practice": ["Autonomous Navigation", "Path Planning", "Sensor Fusion"]
    },
    "Smart Manufacturing": {
        "books": ["Industry 4.0 by Ustundag", "Smart Manufacturing Systems"],
        "online": ["Industry 4.0 Courses", "Smart Factory Videos", "Digital Manufacturing"],
        "practice": ["IoT in Manufacturing", "Digital Twin Projects", "Automation Systems"]
    },
    "Machine Vision": {
        "books": ["Machine Vision by Jain", "Computer Vision for Industrial Applications"],
        "online": ["Machine Vision Tutorials", "OpenCV Industrial", "Vision System Design"],
        "practice": ["Vision Projects", "Image Processing", "Quality Inspection Systems"]
    },
    "Intelligent Control Systems": {
        "books": ["Intelligent Control Systems by Gupta", "Fuzzy Logic and Neural Networks"],
        "online": ["Intelligent Control Courses", "Fuzzy Logic Tutorials", "Neural Control"],
        "practice": ["Fuzzy Control Projects", "Neural Network Control", "Adaptive Systems"]
    },
    "Cyber Physical Systems": {
        "books": ["Cyber-Physical Systems by Lee", "Introduction to CPS"],
        "online": ["CPS Courses", "Embedded Systems Videos", "IoT and CPS"],
        "practice": ["CPS Projects", "System Integration", "Real-time Systems"]
    },
    "Bioinformatics": {
        "books": ["Bioinformatics by Rastogi", "Introduction to Bioinformatics by Lesk"],
        "online": ["Coursera - Bioinformatics", "Rosalind Platform", "NCBI Tutorials"],
        "practice": ["Rosalind Problems", "Bioinformatics Projects", "Sequence Analysis"]
    },
    "Nanomedicine": {
        "books": ["Nanomedicine by Freitas", "Nanotechnology in Medicine"],
        "online": ["Nano Medicine Courses", "Nanotechnology Videos", "Research Papers"],
        "practice": ["Research Projects", "Case Studies", "Lab Work"]
    },
    "Medical Robotics": {
        "books": ["Medical Robotics by Rosen", "Surgical Robotics Systems"],
        "online": ["Medical Robotics Courses", "Surgical Robotics Videos", "IEEE Papers"],
        "practice": ["Robotics Simulations", "Medical Device Projects", "Case Studies"]
    },
    "Regulatory Affairs": {
        "books": ["Regulatory Affairs by Guarino", "FDA Regulations Handbook"],
        "online": ["FDA Guidelines", "Regulatory Affairs Courses", "Compliance Training"],
        "practice": ["Regulatory Documentation", "Compliance Projects", "Case Studies"]
    },
    "Biomedical Data Analysis": {
        "books": ["Biomedical Data Science", "Medical Data Analysis"],
        "online": ["Coursera - Medical Data", "Kaggle Medical Datasets", "Python for Healthcare"],
        "practice": ["Kaggle Competitions", "Medical Data Projects", "Statistical Analysis"]
    },
    "Healthcare Technology": {
        "books": ["Healthcare Information Systems", "Digital Health Technology"],
        "online": ["Healthcare IT Courses", "Digital Health Videos", "Health Tech Blogs"],
        "practice": ["Healthcare Projects", "EHR Systems", "Telemedicine Apps"]
    },
    "Biosensors": {
        "books": ["Biosensors by Eggins", "Principles of Biosensors"],
        "online": ["Biosensor Technology Courses", "Sensor Design Videos", "Research Papers"],
        "practice": ["Sensor Design Projects", "Lab Experiments", "Prototyping"]
    },
    "Rehabilitation Engineering": {
        "books": ["Rehabilitation Engineering by Cooper", "Assistive Technology"],
        "online": ["Rehabilitation Engineering Courses", "Assistive Tech Videos", "Clinical Engineering"],
        "practice": ["Device Design Projects", "Clinical Trials", "Case Studies"]
    },
    "Tissue Engineering": {
        "books": ["Tissue Engineering by Lanza", "Principles of Tissue Engineering"],
        "online": ["Tissue Engineering Courses", "Regenerative Medicine Videos", "Research Papers"],
        "practice": ["Lab Projects", "Cell Culture", "Biomaterial Testing"]
    },
    "Medical Electronics": {
        "books": ["Medical Electronics by Khandpur", "Biomedical Electronics"],
        "online": ["Medical Electronics Courses", "Biomedical Circuits", "Device Design"],
        "practice": ["Circuit Design", "Medical Device Projects", "Lab Experiments"]
    },
    "Clinical Engineering": {
        "books": ["Clinical Engineering Handbook", "Medical Equipment Management"],
        "online": ["Clinical Engineering Courses", "Hospital Technology", "Equipment Management"],
        "practice": ["Equipment Maintenance", "Safety Testing", "Hospital Projects"]
    },
    "Medical Imaging Systems": {
        "books": ["Medical Imaging Systems by Bushberg", "Imaging Physics"],
        "online": ["Medical Imaging Courses", "Radiology Physics", "Image Processing"],
        "practice": ["Image Analysis Projects", "DICOM Processing", "Imaging Simulations"]
    },
    "Artificial Organs": {
        "books": ["Artificial Organs by Bronzino", "Bioartificial Organs"],
        "online": ["Artificial Organs Research", "Bioengineering Videos", "Clinical Studies"],
        "practice": ["Design Projects", "Research Papers", "Case Studies"]
    },
    "Telemedicine": {
        "books": ["Telemedicine Technologies", "Telehealth Practice"],
        "online": ["Telemedicine Courses", "Digital Health Platforms", "Remote Care Systems"],
        "practice": ["Telehealth Projects", "Platform Development", "Case Studies"]
    },
    "Biomedical Optics": {
        "books": ["Biomedical Optics by Wang", "Tissue Optics"],
        "online": ["Biomedical Optics Courses", "Optical Imaging", "Photonics in Medicine"],
        "practice": ["Optical System Design", "Imaging Projects", "Lab Experiments"]
    },
    "Neural Engineering": {
        "books": ["Neural Engineering by He", "Brain-Computer Interfaces"],
        "online": ["Neural Engineering Courses", "BCI Tutorials", "Neurotechnology"],
        "practice": ["BCI Projects", "Neural Signal Processing", "Research Projects"]
    },
    "Hospital Management": {
        "books": ["Hospital Administration by Kunders", "Healthcare Management"],
        "online": ["Hospital Management Courses", "Healthcare Administration", "Hospital Operations"],
        "practice": ["Management Case Studies", "Hospital Projects", "Quality Improvement"]
    },
    "Elective": {
        "books": ["Refer to elective-specific textbooks", "Consult course instructor"],
        "online": ["Course-specific online resources", "NPTEL", "Coursera"],
        "practice": ["Course assignments", "Projects", "Previous year questions"]
    },
    "Project Work": {
        "books": ["Project Management by PMI", "Research Methodology"],
        "online": ["Project Management Courses", "Research Methods", "Technical Writing"],
        "practice": ["Project Development", "Documentation", "Presentations"]
    },
    "Advanced Manufacturing": {
        "books": ["Advanced Manufacturing Processes", "Modern Manufacturing Technology"],
        "online": ["NPTEL - Advanced Manufacturing", "Manufacturing Videos", "Industry 4.0"],
        "practice": ["Manufacturing Projects", "Process Optimization", "Automation"]
    },
    "Additive Manufacturing": {
        "books": ["Additive Manufacturing by Gibson", "3D Printing Handbook"],
        "online": ["3D Printing Courses", "Additive Manufacturing Videos", "CAD for AM"],
        "practice": ["3D Printing Projects", "Design for AM", "Material Testing"]
    },
    "Computational Fluid Dynamics": {
        "books": ["CFD by Anderson", "Computational Fluid Dynamics by Versteeg"],
        "online": ["CFD Courses", "ANSYS Fluent Tutorials", "OpenFOAM"],
        "practice": ["CFD Simulations", "ANSYS Projects", "Flow Analysis"]
    },
    "Automobile Engineering": {
        "books": ["Automobile Engineering by Kirpal Singh", "Automotive Mechanics"],
        "online": ["NPTEL - Automobile", "Automotive Engineering Videos", "Vehicle Dynamics"],
        "practice": ["Vehicle Design Projects", "Engine Analysis", "Automotive Systems"]
    },
    "Refrigeration and Air Conditioning": {
        "books": ["Refrigeration and Air Conditioning by Arora", "HVAC Systems"],
        "online": ["NPTEL - RAC", "HVAC Design Courses", "Refrigeration Cycles"],
        "practice": ["HVAC Design Projects", "System Calculations", "Lab Experiments"]
    },
    "Operations Research": {
        "books": ["Operations Research by Taha", "Introduction to OR by Hillier"],
        "online": ["NPTEL - Operations Research", "OR Tutorials", "Optimization Methods"],
        "practice": ["OR Problems", "Linear Programming", "Optimization Projects"]
    },
    "Industrial Engineering": {
        "books": ["Industrial Engineering by Groover", "Production Systems"],
        "online": ["NPTEL - Industrial Engineering", "IE Courses", "Lean Manufacturing"],
        "practice": ["Process Improvement", "Time Studies", "Facility Layout"]
    },
    "Composite Materials": {
        "books": ["Composite Materials by Mallick", "Mechanics of Composite Materials"],
        "online": ["Composite Materials Courses", "Material Science Videos", "FRP Technology"],
        "practice": ["Material Testing", "Composite Design", "Lab Experiments"]
    },
    "Renewable Energy Sources": {
        "books": ["Renewable Energy by Twidell", "Non-Conventional Energy Sources"],
        "online": ["NPTEL - Renewable Energy", "Solar Energy Courses", "Wind Energy"],
        "practice": ["Solar Projects", "Wind Turbine Design", "Energy Calculations"]
    },
    "Transportation Engineering": {
        "books": ["Transportation Engineering by Khanna", "Highway Engineering"],
        "online": ["NPTEL - Transportation", "Traffic Engineering", "Highway Design"],
        "practice": ["Highway Design Projects", "Traffic Analysis", "Pavement Design"]
    },
    "Environmental Engineering": {
        "books": ["Environmental Engineering by Peavy", "Water Supply Engineering"],
        "online": ["NPTEL - Environmental Engineering", "Water Treatment", "Pollution Control"],
        "practice": ["Treatment Plant Design", "Environmental Projects", "Lab Analysis"]
    },
    "Estimation and Costing": {
        "books": ["Estimating and Costing by Dutta", "Construction Estimation"],
        "online": ["Estimation Tutorials", "Quantity Surveying", "Cost Analysis"],
        "practice": ["Estimation Problems", "BOQ Preparation", "Rate Analysis"]
    },
    "Foundation Engineering": {
        "books": ["Foundation Engineering by Bowles", "Soil Mechanics and Foundation"],
        "online": ["NPTEL - Foundation Engineering", "Deep Foundation", "Shallow Foundation"],
        "practice": ["Foundation Design", "Bearing Capacity", "Settlement Analysis"]
    },
    "Earthquake Engineering": {
        "books": ["Earthquake Engineering by Pankaj Agarwal", "Seismic Design"],
        "online": ["NPTEL - Earthquake Engineering", "Seismic Analysis", "Structural Dynamics"],
        "practice": ["Seismic Design Projects", "Dynamic Analysis", "Response Spectrum"]
    },
    "Prestressed Concrete": {
        "books": ["Prestressed Concrete by Krishna Raju", "Design of Prestressed Concrete"],
        "online": ["NPTEL - Prestressed Concrete", "PSC Design", "Prestressing Systems"],
        "practice": ["PSC Design Problems", "Prestress Calculations", "Beam Design"]
    },
    "Remote Sensing and GIS": {
        "books": ["Remote Sensing by Lillesand", "GIS Fundamentals"],
        "online": ["NPTEL - Remote Sensing", "GIS Tutorials", "QGIS/ArcGIS"],
        "practice": ["GIS Projects", "Image Processing", "Spatial Analysis"]
    },
    "Highway Engineering": {
        "books": ["Highway Engineering by Khanna", "Principles of Highway Engineering"],
        "online": ["NPTEL - Highway Engineering", "Pavement Design", "Geometric Design"],
        "practice": ["Highway Design", "Pavement Analysis", "Traffic Engineering"]
    },
    "Bridge Engineering": {
        "books": ["Bridge Engineering by Ponnuswamy", "Design of Bridges"],
        "online": ["NPTEL - Bridge Engineering", "Bridge Design", "Structural Analysis"],
        "practice": ["Bridge Design Projects", "Load Analysis", "Structural Modeling"]
    },
    "Waste Water Engineering": {
        "books": ["Wastewater Engineering by Metcalf", "Water and Wastewater Treatment"],
        "online": ["NPTEL - Wastewater", "Treatment Processes", "Sewage Treatment"],
        "practice": ["Treatment Plant Design", "Process Calculations", "Lab Work"]
    },
    "Project Management": {
        "books": ["Project Management by PMI", "Construction Project Management"],
        "online": ["NPTEL - Project Management", "PMP Courses", "MS Project"],
        "practice": ["Project Planning", "CPM/PERT", "Resource Management"]
    },
    "Green Building Technology": {
        "books": ["Green Building by Yudelson", "Sustainable Construction"],
        "online": ["Green Building Courses", "LEED Certification", "Sustainable Design"],
        "practice": ["Green Building Projects", "Energy Modeling", "LEED Projects"]
    }
}

def get_subject_resources(subject_name):
    """Get resources for a subject, return generic resources if not found"""
    return RESOURCES.get(subject_name, {
        "books": ["Refer to standard textbooks recommended by your professor", "Check university library for reference books"],
        "online": ["NPTEL courses", "MIT OCW", "YouTube educational channels"],
        "practice": ["Previous year question papers", "University question bank", "Online practice platforms"]
    })

# ================= LOGIN =================

def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,
                            username=username,
                            password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect("admin_dashboard")
            else:
                return redirect("student_dashboard")

        else:
            messages.error(request, "Invalid username or password")
            return render(request, "login.html")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# ================= REGISTER =================

def register_student(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register_student")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "register.html")


# ================= STUDENT DASHBOARD =================

@login_required
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    records = AcademicRecord.objects.filter(student=student).order_by('-created_at')
    
    if records.exists():
        total_records = records.count()
        avg_marks = sum(r.marks for r in records) / total_records
        avg_attendance = sum(r.attendance_percentage for r in records) / total_records
        
        weak_recommendations = []
        strong_recommendations = []
        
        for record in records:
            marks = record.marks
            attendance = record.attendance_percentage
            
            if marks < 25:
                resources = get_subject_resources(record.subject)
                weak_recommendations.append({
                    'subject': record.subject,
                    'marks': marks,
                    'attendance': attendance,
                    'internal_type': record.internal_type,
                    'books': resources['books'][:2],
                    'online': resources['online'][:2],
                    'practice': resources['practice'][:2],
                    'date': record.created_at
                })
            elif marks > 40:
                strong_recommendations.append({
                    'subject': record.subject,
                    'marks': marks,
                    'attendance': attendance,
                    'internal_type': record.internal_type,
                    'date': record.created_at
                })
        
        subject_labels = [r.subject[:20] for r in records[:10]]
        subject_marks = [r.marks for r in records[:10]]
        
        internal1_records = records.filter(internal_type='Internal 1')
        internal2_records = records.filter(internal_type='Internal 2')
        internal1_avg = sum(r.marks for r in internal1_records) / internal1_records.count() if internal1_records.exists() else 0
        internal2_avg = sum(r.marks for r in internal2_records) / internal2_records.count() if internal2_records.exists() else 0
        
        context = {
            'student': student,
            'has_data': True,
            'total_records': total_records,
            'avg_marks': round(avg_marks, 1),
            'avg_attendance': round(avg_attendance, 1),
            'weak_count': len(weak_recommendations),
            'strong_count': len(strong_recommendations),
            'subject_labels': subject_labels,
            'subject_marks': subject_marks,
            'internal1_avg': round(internal1_avg, 1),
            'internal2_avg': round(internal2_avg, 1),
            'weak_recommendations': weak_recommendations,
            'strong_recommendations': strong_recommendations,
        }
    else:
        context = {
            'student': student,
            'has_data': False,
        }
    
    return render(request, "student_dashboard.html", context)


@login_required
def student_info(request):

    if request.method == "POST":
        request.session["roll_no"] = request.POST.get("roll_no")
        request.session["name"] = request.POST.get("name")
        request.session["department"] = request.POST.get("department")
        request.session["year"] = request.POST.get("year")
        request.session["semester"] = request.POST.get("semester")
        request.session["internal_type"] = request.POST.get("internal_type")

        return redirect("student_marks")

    return render(request, "student_info.html")


@login_required
def student_marks(request):

    department = request.session.get("department")
    semester = int(request.session.get("semester", 0))
    internal_type = request.session.get("internal_type", "Internal 1")
    name = request.session.get("name")
    roll_no = request.session.get("roll_no")
    year = request.session.get("year")

    subjects = get_subjects(department, semester)

    if not subjects:
        return HttpResponse("No subjects found. Check department or semester.")

    if request.method == "POST":

        marks_data = {}
        attendance_data = {}

        student = Student.objects.get(user=request.user)
        student.name = name
        student.roll_no = roll_no
        student.department = department
        student.year = int(year) if year else None
        student.semester = semester
        student.save()

        for sub in subjects:
            internal_marks = int(request.POST.get(sub + "_marks", 0))
            attended = int(request.POST.get(sub + "_attended", 0))
            total = int(request.POST.get(sub + "_total", 1))
            attendance_percentage = (attended / total) * 100 if total > 0 else 0

            marks_data[sub] = internal_marks
            attendance_data[sub] = round(attendance_percentage, 2)

            AcademicRecord.objects.update_or_create(
                student=student,
                subject=sub,
                internal_type=internal_type,
                defaults={
                    'marks': internal_marks,
                    'attendance_attended': attended,
                    'attendance_total': total
                }
            )

        request.session["marks_data"] = marks_data
        request.session["attendance_data"] = attendance_data

        return redirect("student_recommendation")

    return render(request, "student_marks.html", {
        "subjects": subjects,
        "internal_type": internal_type
    })


@login_required
def student_recommendation(request):

    marks_data = request.session.get("marks_data", {})
    attendance_data = request.session.get("attendance_data", {})

    if not marks_data:
        messages.error(request, "No marks data found. Please enter your marks first.")
        return redirect("student_info")

    weak_recommendations = []
    strong_recommendations = []
    average_subjects = []
    weak_subjects = []
    strong_subjects = []

    for sub, marks in marks_data.items():
        attendance = attendance_data.get(sub, 0)
        
        if marks < 25:
            performance = "Needs Improvement"
            status = "weak"
            weak_subjects.append(sub)
            resources = get_subject_resources(sub)
            strategies = [
                "Focus on topics you missed or performed poorly in during internals",
                "Solve previous year question papers and practice worksheets regularly",
                "Make summary notes or flashcards for quick revision",
                "Attend extra tutorials, remedial classes, or doubt-clearing sessions",
                "Join online or offline study groups for discussion and peer learning",
                "Create a weekly study schedule allocating more time to weak topics",
                "Track your progress regularly through self-tests to see improvement",
                "Practice numerical problems daily (minimum 10-15 problems)",
                "Watch video lectures to understand difficult concepts visually",
                "Consult your professor during office hours for personalized guidance"
            ]
            if attendance < 75:
                strategies.insert(0, "⚠️ CRITICAL: Improve attendance to meet minimum requirement (75%)")
            weak_recommendations.append({
                "subject": sub,
                "marks": marks,
                "attendance": attendance,
                "performance": performance,
                "status": status,
                "books": resources["books"],
                "online": resources["online"],
                "practice": resources["practice"],
                "strategies": strategies
            })
        elif marks > 40:
            performance = "Excellent"
            status = "strong"
            strong_subjects.append(sub)
            tips = [
                "Revise advanced topics beyond the syllabus",
                "Attempt extra problems from reference books",
                "Work on mini-projects related to this subject",
                "Participate in quizzes and assignments",
                "Explore research papers in this domain",
                "Mentor peers to reinforce your understanding",
                "Aim for 100% score in end semester exam",
                "Consider certification courses or MOOCs",
                "Participate in subject competitions or hackathons",
                "Contribute to open-source projects in this area"
            ]
            strong_recommendations.append({
                "subject": sub,
                "marks": marks,
                "attendance": attendance,
                "performance": performance,
                "status": status,
                "tips": tips
            })
        else:
            performance = "Average"
            status = "average"
            average_subjects.append({
                "subject": sub,
                "marks": marks,
                "attendance": attendance,
                "performance": performance,
                "status": status
            })

    return render(request, "student_recommendation.html", {
        "weak_recommendations": weak_recommendations,
        "strong_recommendations": strong_recommendations,
        "average_subjects": average_subjects,
        "weak_subjects": weak_subjects,
        "strong_subjects": strong_subjects,
        "total_subjects": len(marks_data),
        "weak_count": len(weak_subjects),
        "strong_count": len(strong_subjects),
        "average_count": len(average_subjects)
    })



# ================= ADMIN DASHBOARD =================

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect("student_dashboard")

    # Get filter parameters
    search = request.GET.get('search', '')
    department = request.GET.get('department', '')
    year = request.GET.get('year', '')
    semester = request.GET.get('semester', '')
    sort_by = request.GET.get('sort_by', 'name')
    show_incomplete = request.GET.get('show_incomplete', '')

    # Start with all students (including those with incomplete profiles)
    students = Student.objects.select_related('user').all()

    # Apply filters
    if search:
        students = students.filter(
            models.Q(user__username__icontains=search) |
            models.Q(user__email__icontains=search) |
            models.Q(name__icontains=search) |
            models.Q(roll_no__icontains=search)
        )
    if department:
        students = students.filter(department=department)
    if year:
        students = students.filter(year=int(year))
    if semester:
        students = students.filter(semester=int(semester))
    if show_incomplete == 'yes':
        students = students.filter(
            models.Q(name__isnull=True) | models.Q(name='') |
            models.Q(department__isnull=True) | models.Q(department='')
        )

    # Apply sorting - default alphabetical by name
    if sort_by == 'name':
        students = students.order_by('name', 'user__username')
    else:
        students = students.order_by(sort_by)

    # Get unique departments for filter dropdown (including NULL)
    departments = Student.objects.values_list('department', flat=True).distinct().exclude(department__isnull=True).exclude(department='')

    return render(request, "admin_dashboard.html", {
        "students": students,
        "departments": departments,
        "search": search,
        "selected_department": department,
        "selected_year": year,
        "selected_semester": semester,
        "sort_by": sort_by,
        "show_incomplete": show_incomplete
    })


@login_required
def admin_add_student(request):
    if not request.user.is_superuser:
        return redirect("student_dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        name = request.POST.get("name")
        roll_no = request.POST.get("roll_no")
        department = request.POST.get("department")
        year = request.POST.get("year")
        semester = request.POST.get("semester")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("admin_add_student")

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Update student profile
        student = Student.objects.get(user=user)
        student.name = name
        student.roll_no = roll_no
        student.department = department
        student.year = int(year) if year else None
        student.semester = int(semester) if semester else None
        student.save()

        messages.success(request, "Student added successfully")
        return redirect("admin_dashboard")

    return render(request, "admin_add_student.html")


@login_required
def admin_edit_student(request, student_id):
    if not request.user.is_superuser:
        return redirect("student_dashboard")

    student = Student.objects.get(id=student_id)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        roll_no = request.POST.get("roll_no", "").strip()
        department = request.POST.get("department", "").strip()
        year = request.POST.get("year", "").strip()
        semester = request.POST.get("semester", "").strip()
        email = request.POST.get("email", "").strip()
        
        student.name = name if name else None
        student.roll_no = roll_no if roll_no else None
        student.department = department if department else None
        student.year = int(year) if year else None
        student.semester = int(semester) if semester else None
        student.user.email = email if email else student.user.email
        student.save()
        student.user.save()

        messages.success(request, "Student updated successfully")
        return redirect("admin_dashboard")

    return render(request, "admin_edit_student.html", {"student": student})


@login_required
def admin_delete_student(request, student_id):
    if not request.user.is_superuser:
        return redirect("student_dashboard")

    student = Student.objects.get(id=student_id)
    username = student.user.username
    student.user.delete()  # This will cascade delete the student
    
    messages.success(request, f"Student {username} deleted successfully")
    return redirect("admin_dashboard")


# ================= ACADEMIC MANAGEMENT =================

@login_required
def admin_academic_records(request):
    if not request.user.is_superuser:
        return redirect("student_dashboard")

    # Filters
    search = request.GET.get('search', '')
    department = request.GET.get('department', '')
    semester = request.GET.get('semester', '')
    subject = request.GET.get('subject', '')
    performance = request.GET.get('performance', '')

    records = AcademicRecord.objects.select_related('student__user').all()

    if search:
        records = records.filter(
            models.Q(student__user__username__icontains=search) |
            models.Q(student__name__icontains=search) |
            models.Q(student__roll_no__icontains=search)
        )
    if department:
        records = records.filter(student__department=department)
    if semester:
        records = records.filter(student__semester=int(semester))
    if subject:
        records = records.filter(subject__icontains=subject)
    if performance == 'weak':
        records = [r for r in records if r.marks < 25]
    elif performance == 'average':
        records = [r for r in records if 25 <= r.marks <= 40]
    elif performance == 'strong':
        records = [r for r in records if r.marks > 40]

    departments = Student.objects.values_list('department', flat=True).distinct().exclude(department__isnull=True)
    subjects = AcademicRecord.objects.values_list('subject', flat=True).distinct()

    return render(request, "admin_academic_records.html", {
        "records": records,
        "departments": departments,
        "subjects": subjects,
        "search": search,
        "selected_department": department,
        "selected_semester": semester,
        "selected_subject": subject,
        "selected_performance": performance
    })


@login_required
def admin_add_academic_record(request):
    if not request.user.is_superuser:
        return redirect("student_dashboard")

    if request.method == "POST":
        student_id = request.POST.get("student_id")
        subject = request.POST.get("subject")
        internal_type = request.POST.get("internal_type")
        marks = request.POST.get("marks")
        attended = request.POST.get("attended")
        total = request.POST.get("total")

        student = Student.objects.get(id=student_id)
        
        AcademicRecord.objects.update_or_create(
            student=student,
            subject=subject,
            internal_type=internal_type,
            defaults={
                'marks': int(marks),
                'attendance_attended': int(attended),
                'attendance_total': int(total)
            }
        )

        messages.success(request, "Academic record added successfully")
        return redirect("admin_academic_records")

    students = Student.objects.all()
    return render(request, "admin_add_academic_record.html", {"students": students})


@login_required
def admin_bulk_upload(request):
    if not request.user.is_superuser:
        return redirect("student_dashboard")

    if request.method == "POST" and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Please upload a CSV file")
            return redirect("admin_bulk_upload")

        try:
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            success_count = 0
            error_count = 0

            for row in reader:
                try:
                    student = Student.objects.get(roll_no=row['roll_no'])
                    
                    AcademicRecord.objects.update_or_create(
                        student=student,
                        subject=row['subject'],
                        internal_type=row['internal_type'],
                        defaults={
                            'marks': int(row['marks']),
                            'attendance_attended': int(row['attendance_attended']),
                            'attendance_total': int(row['attendance_total'])
                        }
                    )
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    continue

            messages.success(request, f"Successfully uploaded {success_count} records. {error_count} errors.")
            return redirect("admin_academic_records")

        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")
            return redirect("admin_bulk_upload")

    return render(request, "admin_bulk_upload.html")


@login_required
def admin_view_recommendations(request, student_id):
    if not request.user.is_superuser:
        return redirect("student_dashboard")

    student = Student.objects.get(id=student_id)
    records = AcademicRecord.objects.filter(student=student)

    if not records.exists():
        messages.error(request, "No academic records found for this student")
        return redirect("admin_dashboard")

    # Calculate recommendations
    weak_recommendations = []
    strong_recommendations = []
    average_subjects = []

    for record in records:
        marks = record.marks
        attendance = record.attendance_percentage
        
        if marks < 25:
            resources = get_subject_resources(record.subject)
            strategies = [
                "Focus on topics you missed or performed poorly in during internals",
                "Solve previous year question papers and practice worksheets regularly",
                "Make summary notes or flashcards for quick revision",
                "Attend extra tutorials, remedial classes, or doubt-clearing sessions",
                "Join online or offline study groups for discussion and peer learning",
                "Create a weekly study schedule allocating more time to weak topics",
                "Track your progress regularly through self-tests to see improvement",
                "Practice numerical problems daily (minimum 10-15 problems)",
                "Watch video lectures to understand difficult concepts visually",
                "Consult your professor during office hours for personalized guidance"
            ]
            if attendance < 75:
                strategies.insert(0, "⚠️ CRITICAL: Improve attendance to meet minimum requirement (75%)")
            
            weak_recommendations.append({
                "subject": record.subject,
                "marks": marks,
                "attendance": attendance,
                "internal_type": record.internal_type,
                "books": resources["books"],
                "online": resources["online"],
                "practice": resources["practice"],
                "strategies": strategies
            })
            
        elif marks > 40:
            tips = [
                "Revise advanced topics beyond the syllabus",
                "Attempt extra problems from reference books",
                "Work on mini-projects related to this subject",
                "Participate in quizzes and assignments",
                "Explore research papers in this domain",
                "Mentor peers to reinforce your understanding",
                "Aim for 100% score in end semester exam",
                "Consider certification courses or MOOCs",
                "Participate in subject competitions or hackathons",
                "Contribute to open-source projects in this area"
            ]
            
            strong_recommendations.append({
                "subject": record.subject,
                "marks": marks,
                "attendance": attendance,
                "internal_type": record.internal_type,
                "tips": tips
            })
            
        else:
            average_subjects.append({
                "subject": record.subject,
                "marks": marks,
                "attendance": attendance,
                "internal_type": record.internal_type
            })

    return render(request, "admin_view_recommendations.html", {
        "student": student,
        "weak_recommendations": weak_recommendations,
        "strong_recommendations": strong_recommendations,
        "average_subjects": average_subjects,
        "total_subjects": records.count(),
        "weak_count": len(weak_recommendations),
        "strong_count": len(strong_recommendations),
        "average_count": len(average_subjects)
    })


# ================= CREATE ADMIN =================

def create_admin(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@gmail.com",
            password="admin123"
        )
        return HttpResponse("Superuser created successfully")

    return HttpResponse("Admin already exists")


# ================= ANALYTICS =================

@login_required
def admin_analytics(request):
    if not request.user.is_superuser:
        return redirect("student_dashboard")

    # Filters
    department = request.GET.get('department', '')
    semester = request.GET.get('semester', '')
    subject = request.GET.get('subject', '')

    # Base queryset
    records = AcademicRecord.objects.select_related('student').all()
    
    if department:
        records = records.filter(student__department=department)
    if semester:
        records = records.filter(student__semester=int(semester))
    if subject:
        records = records.filter(subject__icontains=subject)

    # Get unique students with records
    student_ids = records.values_list('student_id', flat=True).distinct()
    total_students = student_ids.count()
    
    if total_students > 0:
        # Calculate student-wise performance
        student_performance = {}
        for student_id in student_ids:
            student_records = records.filter(student_id=student_id)
            total_marks = sum(r.marks for r in student_records)
            total_subjects = student_records.count()
            avg_marks = total_marks / total_subjects if total_subjects > 0 else 0
            avg_attendance = sum(r.attendance_percentage for r in student_records) / total_subjects if total_subjects > 0 else 0
            
            student_performance[student_id] = {
                'avg_marks': avg_marks,
                'avg_attendance': avg_attendance,
                'total_subjects': total_subjects
            }
        
        # Performance distribution (based on students)
        weak_students = sum(1 for p in student_performance.values() if p['avg_marks'] < 25)
        average_students = sum(1 for p in student_performance.values() if 25 <= p['avg_marks'] <= 40)
        strong_students = sum(1 for p in student_performance.values() if p['avg_marks'] > 40)
        
        # Overall averages
        avg_marks = sum(p['avg_marks'] for p in student_performance.values()) / total_students
        avg_attendance = sum(p['avg_attendance'] for p in student_performance.values()) / total_students
        
        # Department-wise statistics (student-based)
        dept_stats = {}
        for student_id, perf in student_performance.items():
            student = Student.objects.get(id=student_id)
            dept = student.department or "Unknown"
            if dept not in dept_stats:
                dept_stats[dept] = {'students': 0, 'total_marks': 0, 'weak': 0, 'strong': 0}
            dept_stats[dept]['students'] += 1
            dept_stats[dept]['total_marks'] += perf['avg_marks']
            if perf['avg_marks'] < 25:
                dept_stats[dept]['weak'] += 1
            elif perf['avg_marks'] > 40:
                dept_stats[dept]['strong'] += 1
        
        for dept in dept_stats:
            if dept_stats[dept]['students'] > 0:
                dept_stats[dept]['avg_marks'] = round(dept_stats[dept]['total_marks'] / dept_stats[dept]['students'], 2)
        
        # Subject-wise statistics (how many students struggle/excel)
        subject_stats = {}
        for record in records:
            subj = record.subject
            if subj not in subject_stats:
                subject_stats[subj] = {'students': set(), 'total_marks': 0, 'weak': 0, 'strong': 0}
            subject_stats[subj]['students'].add(record.student_id)
            subject_stats[subj]['total_marks'] += record.marks
            if record.marks < 25:
                subject_stats[subj]['weak'] += 1
            elif record.marks > 40:
                subject_stats[subj]['strong'] += 1
        
        for subj in subject_stats:
            student_count = len(subject_stats[subj]['students'])
            if student_count > 0:
                subject_stats[subj]['avg_marks'] = round(subject_stats[subj]['total_marks'] / student_count, 2)
                subject_stats[subj]['student_count'] = student_count
        
        # Top performing subjects
        top_subjects = sorted(subject_stats.items(), key=lambda x: x[1]['avg_marks'], reverse=True)[:5]
        
        # Weak subjects (most students struggling)
        weak_subjects = sorted(subject_stats.items(), key=lambda x: x[1]['weak'], reverse=True)[:5]
        
    else:
        weak_students = average_students = strong_students = 0
        avg_marks = avg_attendance = 0
        dept_stats = {}
        subject_stats = {}
        top_subjects = []
        weak_subjects = []

    departments = Student.objects.values_list('department', flat=True).distinct().exclude(department__isnull=True)
    subjects_list = AcademicRecord.objects.values_list('subject', flat=True).distinct()

    return render(request, "admin_analytics.html", {
        "total_students": total_students,
        "weak_count": weak_students,
        "average_count": average_students,
        "strong_count": strong_students,
        "avg_marks": round(avg_marks, 2),
        "avg_attendance": round(avg_attendance, 2),
        "dept_stats": dept_stats,
        "subject_stats": subject_stats,
        "top_subjects": top_subjects,
        "weak_subjects": weak_subjects,
        "departments": departments,
        "subjects_list": subjects_list,
        "selected_department": department,
        "selected_semester": semester,
        "selected_subject": subject,
        "weak_percentage": round((weak_students / total_students * 100), 1) if total_students > 0 else 0,
        "average_percentage": round((average_students / total_students * 100), 1) if total_students > 0 else 0,
        "strong_percentage": round((strong_students / total_students * 100), 1) if total_students > 0 else 0,
    })


# ================= PDF EXPORT =================

@login_required
def export_students_pdf(request):
    if not request.user.is_superuser:
        return redirect("student_dashboard")

    # Get filters
    department = request.GET.get('department', '')
    year = request.GET.get('year', '')
    semester = request.GET.get('semester', '')
    sort_order = request.GET.get('sort', 'name')  # name, performance

    # Query students
    students = Student.objects.select_related('user').filter(department__isnull=False)
    
    if department:
        students = students.filter(department=department)
    if year:
        students = students.filter(year=int(year))
    if semester:
        students = students.filter(semester=int(semester))

    # Calculate performance for sorting
    student_data = []
    for student in students:
        records = AcademicRecord.objects.filter(student=student)
        if records.exists():
            avg_marks = sum(r.marks for r in records) / records.count()
            avg_attendance = sum(r.attendance_percentage for r in records) / records.count()
            weak_subjects = [r.subject for r in records if r.marks < 25]
            strong_subjects = [r.subject for r in records if r.marks > 40]
        else:
            avg_marks = 0
            avg_attendance = 0
            weak_subjects = []
            strong_subjects = []
        
        student_data.append({
            'student': student,
            'records': records,
            'avg_marks': avg_marks,
            'avg_attendance': avg_attendance,
            'weak_subjects': weak_subjects,
            'strong_subjects': strong_subjects
        })

    # Sort
    if sort_order == 'performance':
        student_data.sort(key=lambda x: x['avg_marks'], reverse=True)
    elif sort_order == 'name_desc':
        student_data.sort(key=lambda x: x['student'].name or '', reverse=True)
    else:  # name (default)
        student_data.sort(key=lambda x: x['student'].name or '')

    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    filename = f"Student_Records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    doc = SimpleDocTemplate(response, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#0f766e'), alignment=TA_CENTER, spaceAfter=20)
    elements.append(Paragraph("Student Academic Records Report", title_style))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))

    # Filters info
    filter_text = []
    if department:
        filter_text.append(f"Department: {department}")
    if year:
        filter_text.append(f"Year: {year}")
    if semester:
        filter_text.append(f"Semester: {semester}")
    if filter_text:
        elements.append(Paragraph(f"<b>Filters:</b> {', '.join(filter_text)}", styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))

    # Summary
    elements.append(Paragraph(f"<b>Total Students:</b> {len(student_data)}", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))

    # Student records
    for idx, data in enumerate(student_data, 1):
        student = data['student']
        records = data['records']
        
        # Student header
        student_style = ParagraphStyle('StudentHeader', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#0f766e'), spaceAfter=10)
        elements.append(Paragraph(f"{idx}. {student.name or 'N/A'}", student_style))
        
        # Student details table
        details_data = [
            ['Roll No:', student.roll_no or 'N/A', 'Department:', student.department or 'N/A'],
            ['Year:', str(student.year) if student.year else 'N/A', 'Semester:', str(student.semester) if student.semester else 'N/A'],
            ['Email:', student.user.email or 'N/A', 'Avg Marks:', f"{data['avg_marks']:.1f}/50"],
            ['Username:', student.user.username, 'Avg Attendance:', f"{data['avg_attendance']:.1f}%"]
        ]
        
        details_table = Table(details_data, colWidths=[1.2*inch, 2*inch, 1.2*inch, 2*inch])
        details_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(details_table)
        elements.append(Spacer(1, 0.15*inch))

        # Academic records
        if records.exists():
            elements.append(Paragraph("<b>Academic Records:</b>", styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            records_data = [['Subject', 'Internal', 'Marks', 'Attendance', 'Status']]
            for record in records:
                status = 'Strong' if record.marks > 40 else ('Weak' if record.marks < 25 else 'Average')
                records_data.append([
                    record.subject[:30],
                    record.internal_type,
                    f"{record.marks}/50",
                    f"{record.attendance_percentage:.1f}%",
                    status
                ])
            
            records_table = Table(records_data, colWidths=[2.5*inch, 1*inch, 0.8*inch, 1*inch, 0.8*inch])
            records_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f766e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(records_table)
            elements.append(Spacer(1, 0.15*inch))

            # Weak subjects
            if data['weak_subjects']:
                weak_text = f"<b>Weak Subjects:</b> {', '.join(data['weak_subjects'][:5])}"
                if len(data['weak_subjects']) > 5:
                    weak_text += f" (+{len(data['weak_subjects'])-5} more)"
                elements.append(Paragraph(weak_text, styles['Normal']))
            
            # Strong subjects
            if data['strong_subjects']:
                strong_text = f"<b>Strong Subjects:</b> {', '.join(data['strong_subjects'][:5])}"
                if len(data['strong_subjects']) > 5:
                    strong_text += f" (+{len(data['strong_subjects'])-5} more)"
                elements.append(Paragraph(strong_text, styles['Normal']))
        else:
            elements.append(Paragraph("<i>No academic records found</i>", styles['Normal']))

        elements.append(Spacer(1, 0.3*inch))
        
        # Page break after every 2 students
        if idx % 2 == 0 and idx < len(student_data):
            elements.append(PageBreak())

    doc.build(elements)
    return response


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_superuser(username=username, password=password, email='')
        return redirect('login')
    return render(request, 'signup.html')


def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'reset_password.html')
        
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successful. Please login with your new password.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Username not found")
            return render(request, 'reset_password.html')
    
    return render(request, 'reset_password.html')
