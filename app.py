import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="IPL Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Premium Look ---
st.markdown("""
<style>
    /* Base App Theme */
    .stApp {
        background: linear-gradient(135deg, #020617 0%, #0F172A 100%);
    }
    
    /* Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@500;700;900&display=swap');
    h1, h2, h3, p, span, div {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Title Styling */
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        color: #F8FAFC;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    
    /* Group Headers */
    .group-header {
        font-family: 'Outfit', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #F8FAFC !important;
        padding-top: 2.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(56, 189, 248, 0.15);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 12px;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
    }
    
    /* Subheaders */
    h3 {
        font-family: 'Outfit', sans-serif;
        color: #CBD5E1 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 1.5rem !important;
    }
    
    /* Card Styling for Charts */
    .stPlotlyChart {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 15px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    .stPlotlyChart:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.5), 0 0 15px rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    
    /* Hide Plotly Modebar and Disable Interaction UI */
    .modebar-container, .modebar-group, .modebar {
        display: none !important;
    }
    
    /* Sidebar / Hamburger Hiding */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Header Logo from st.image */
    [data-testid="stImage"] img {
        max-width: 110px !important;
        aspect-ratio: 1 / 1;
        border-radius: 50%;
        background: #ffffff;
        padding: 5px;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.3), inset 0 0 10px rgba(0,0,0,0.1);
        border: 2px solid #38BDF8;
        object-fit: contain;
        display: block;
        margin: 0 auto;
    }
    
    .header-text-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
        margin-top: 25px; /* Vertical alignment */
    }
    .header-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.5rem;
        font-weight: 900;
        color: #F8FAFC;
        margin-bottom: 5px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        line-height: 1.1;
        letter-spacing: -0.5px;
    }
    .header-desc {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #94A3B8;
        line-height: 1.4;
    }
    
    /* Segmented Control Navigation */
    .stRadio [role=radiogroup] {
        display: flex;
        flex-direction: row;
        flex-wrap: nowrap !important;
        justify-content: center;
        background: rgba(15, 23, 42, 0.6);
        border-radius: 30px;
        padding: 6px;
        width: fit-content;
        max-width: 100%;
        margin: 0 auto;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.3);
        gap: 5px;
        overflow-x: auto;
        -ms-overflow-style: none;  /* IE and Edge */
        scrollbar-width: none;  /* Firefox */
    }
    .stRadio [role=radiogroup]::-webkit-scrollbar {
        display: none; /* Chrome, Safari and Opera */
    }
    .stRadio [role=radiogroup] label > div:first-child {
        display: none !important;
    }
    .stRadio [role=radiogroup] label {
        background: transparent !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 25px !important;
        margin: 0 !important;
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: center;
        white-space: nowrap !important;
        flex: 1 1 auto;
    }
    .stRadio [role=radiogroup] label:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        transform: none !important;
    }
    .stRadio [role=radiogroup] label:has(input:checked) {
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%) !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4) !important;
        border: none !important;
    }
    .stRadio [role=radiogroup] label p {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        color: #94A3B8 !important;
        margin: 0 !important;
    }
    .stRadio [role=radiogroup] label:has(input:checked) p {
        color: #ffffff !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Dataframes */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Responsive Media Queries for Mobile/Small Screens */
    @media (max-width: 768px) {
        .stRadio [role=radiogroup] {
            flex-direction: row !important;
            border-radius: 30px !important;
            padding: 4px !important;
            width: 100% !important;
            justify-content: space-between;
        }
        .stRadio [role=radiogroup] label {
            padding: 6px 2px !important;
            flex: 1 1 auto;
        }
        .stRadio [role=radiogroup] label p {
            font-size: 0.65rem !important;
            white-space: nowrap !important;
            letter-spacing: -0.2px;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Player Name Mapping ---
PLAYER_MAPPING = {
    "V Kohli": "Virat Kohli", "S Dhawan": "Shikhar Dhawan", "RG Sharma": "Rohit Sharma",
    "DA Warner": "David Warner", "SK Raina": "Suresh Raina", "AM Rahane": "Ajinkya Rahane",
    "MS Dhoni": "Mahendra Singh Dhoni", "KL Rahul": "KL Rahul", "RV Uthappa": "Robin Uthappa",
    "KD Karthik": "Dinesh Karthik", "F du Plessis": "Faf du Plessis", "G Gambhir": "Gautam Gambhir",
    "CH Gayle": "Chris Gayle", "AT Rayudu": "Ambati Rayudu", "AB de Villiers": "AB de Villiers",
    "SV Samson": "Sanju Samson", "MK Pandey": "Manish Pandey", "SA Yadav": "Suryakumar Yadav",
    "SS Iyer": "Shreyas Iyer", "SR Watson": "Shane Watson", "Shubman Gill": "Shubman Gill",
    "JC Buttler": "Jos Buttler", "RA Jadeja": "Ravindra Jadeja", "Q de Kock": "Quinton de Kock",
    "RR Pant": "Rishabh Pant", "KA Pollard": "Kieron Pollard", "PA Patel": "Parthiv Patel",
    "WP Saha": "Wriddhiman Saha", "YK Pathan": "Yusuf Pathan", "DA Miller": "David Miller",
    "JH Kallis": "Jacques Kallis", "BB McCullum": "Brendon McCullum", "Ishan Kishan": "Ishan Kishan",
    "M Vijay": "Murali Vijay", "Yuvraj Singh": "Yuvraj Singh", "N Rana": "Nitish Rana",
    "MA Agarwal": "Mayank Agarwal", "SR Tendulkar": "Sachin Tendulkar", "SPD Smith": "Steve Smith",
    "HH Pandya": "Hardik Pandya", "R Dravid": "Rahul Dravid", "SE Marsh": "Shaun Marsh",
    "GJ Maxwell": "Glenn Maxwell", "RD Gaikwad": "Ruturaj Gaikwad", "V Sehwag": "Virender Sehwag",
    "DR Smith": "Dwayne Smith", "KS Williamson": "Kane Williamson", "RA Tripathi": "Rahul Tripathi",
    "AJ Finch": "Aaron Finch", "JP Duminy": "JP Duminy", "MEK Hussey": "Michael Hussey",
    "AD Russell": "Andre Russell", "AC Gilchrist": "Adam Gilchrist", "DPMD Jayawardene": "Mahela Jayawardene",
    "D Padikkal": "Devdutt Padikkal", "MK Tiwary": "Manoj Tiwary", "AR Patel": "Axar Patel",
    "MP Stoinis": "Marcus Stoinis", "YBK Jaiswal": "Yashasvi Jaiswal", "N Pooran": "Nicholas Pooran",
    "KC Sangakkara": "Kumar Sangakkara", "Mandeep Singh": "Mandeep Singh", "KH Pandya": "Krunal Pandya",
    "S Dube": "Shivam Dube", "NV Ojha": "Naman Ojha", "SC Ganguly": "Sourav Ganguly",
    "PP Shaw": "Prithvi Shaw", "KK Nair": "Karun Nair", "SS Tiwary": "Saurabh Tiwary",
    "B Sai Sudharsan": "Sai Sudharsan", "DJ Bravo": "Dwayne Bravo", "S Badrinath": "S Badrinath",
    "DJ Hooda": "Deepak Hooda", "EJG Morgan": "Eoin Morgan", "JM Bairstow": "Jonny Bairstow",
    "Abhishek Sharma": "Abhishek Sharma", "R Parag": "Riyan Parag", "BJ Hodge": "Brad Hodge",
    "SP Narine": "Sunil Narine", "VR Iyer": "Venkatesh Iyer", "DJ Hussey": "David Hussey",
    "AK Markram": "Aiden Markram", "Tilak Varma": "Tilak Varma", "TM Dilshan": "Tillakaratne Dilshan",
    "SO Hetmyer": "Shimron Hetmyer", "KM Jadhav": "Kedar Jadhav", "V Shankar": "Vijay Shankar",
    "IK Pathan": "Irfan Pathan", "CA Lynn": "Chris Lynn", "MR Marsh": "Mitchell Marsh",
    "H Klaasen": "Heinrich Klaasen", "P Simran Singh": "Prabhsimran Singh", "LMP Simmons": "Lendl Simmons",
    "MM Ali": "Moeen Ali", "Y Venugopal Rao": "Venugopal Rao", "M Vohra": "Manan Vohra",
    "R Tewatia": "Rahul Tewatia", "LRPL Taylor": "Ross Taylor", "ML Hayden": "Matthew Hayden",
    "HH Gibbs": "Herschelle Gibbs", "R Ashwin": "Ravichandran Ashwin", "B Kumar": "Bhuvneshwar Kumar",
    "YS Chahal": "Yuzvendra Chahal", "PP Chawla": "Piyush Chawla", "Harbhajan Singh": "Harbhajan Singh",
    "JJ Bumrah": "Jasprit Bumrah", "A Mishra": "Amit Mishra", "Rashid Khan": "Rashid Khan",
    "UT Yadav": "Umesh Yadav", "Sandeep Sharma": "Sandeep Sharma", "SL Malinga": "Lasith Malinga",
    "TA Boult": "Trent Boult", "Mohammed Shami": "Mohammed Shami", "P Kumar": "Praveen Kumar",
    "HV Patel": "Harshal Patel", "I Sharma": "Ishant Sharma", "MM Sharma": "Mohit Sharma",
    "Mohammed Siraj": "Mohammed Siraj", "JD Unadkat": "Jaydev Unadkat", "DW Steyn": "Dale Steyn",
    "Z Khan": "Zaheer Khan", "SN Thakur": "Shardul Thakur", "R Vinay Kumar": "Vinay Kumar",
    "Kuldeep Yadav": "Kuldeep Yadav", "DL Chahar": "Deepak Chahar", "K Rabada": "Kagiso Rabada",
    "A Nehra": "Ashish Nehra", "PP Ojha": "Pragyan Ojha", "CV Varun": "Varun Chakaravarthy",
    "DS Kulkarni": "Dhawal Kulkarni", "RP Singh": "RP Singh", "Arshdeep Singh": "Arshdeep Singh",
    "JA Morkel": "Albie Morkel", "CH Morris": "Chris Morris", "RD Chahar": "Rahul Chahar",
    "M Morkel": "Morne Morkel", "Ravi Bishnoi": "Ravi Bishnoi", "Avesh Khan": "Avesh Khan",
    "PJ Cummins": "Pat Cummins", "R Bhatia": "Rajat Bhatia", "KK Ahmed": "Khaleel Ahmed",
    "KV Sharma": "Karn Sharma", "M Prasidh Krishna": "Prasidh Krishna", "AB Dinda": "Ashok Dinda",
    "M Muralitharan": "Muttiah Muralitharan", "L Balaji": "Lakshmipathy Balaji", "SK Trivedi": "Siddharth Trivedi",
    "Shakib Al Hasan": "Shakib Al Hasan", "S Nadeem": "Shahbaz Nadeem", "T Natarajan": "T Natarajan",
    "Mustafizur Rahman": "Mustafizur Rahman", "MM Patel": "Munaf Patel", "MJ McClenaghan": "Mitchell McClenaghan",
    "Imran Tahir": "Imran Tahir", "SM Curran": "Sam Curran", "MG Johnson": "Mitchell Johnson",
    "JP Faulkner": "James Faulkner", "JC Archer": "Jofra Archer", "TG Southee": "Tim Southee",
    "S Kaul": "Siddarth Kaul", "SK Warne": "Shane Warne", "M Kartik": "Murali Kartik",
    "A Nortje": "Anrich Nortje", "Washington Sundar": "Washington Sundar", "MA Starc": "Mitchell Starc",
    "SB Jakati": "Shadab Jakati", "LH Ferguson": "Lockie Ferguson", "VR Aaron": "Varun Aaron",
    "JO Holder": "Jason Holder", "TU Deshpande": "Tushar Deshpande", "S Gopal": "Shreyas Gopal",
    "A Kumble": "Anil Kumble", "MC Henriques": "Moises Henriques", "S Sreesanth": "S Sreesanth",
    "Iqbal Abdulla": "Iqbal Abdulla", "R Sharma": "Rahul Sharma", "MS Gony": "Manpreet Gony",
    "DT Christian": "Dan Christian", "Yash Dayal": "Yash Dayal", "B Lee": "Brett Lee",
    "PJ Sangwan": "Pradeep Sangwan", "M Theekshana": "Maheesh Theekshana", "M Ashwin": "Murugan Ashwin",
    "JR Hazlewood": "Josh Hazlewood", "NM Coulter-Nile": "Nathan Coulter-Nile", "ST Jayasuriya": "Sanath Jayasuriya", 
    "GC Smith": "Graeme Smith", "MD Mishra": "Mohnish Mishra",
    "A Zampa": "Adam Zampa", "WG Jacks": "Will Jacks", "GHS Garton": "George Garton", "MB Parmar": "Mohnish Parmar",
    "L Ablish": "Love Ablish", "RS Gavaskar": "Rohan Gavaskar", "KR Sen": "Kuldeep Sen", "AC Thomas": "Alfonso Thomas",
    "A Kamboj": "Anshul Kamboj", "JM Kemp": "Justin Kemp", "RP Meredith": "Riley Meredith", "SE Bond": "Shane Bond",
    "CM Gautam": "C. M. Gautam", "KT Maphaka": "Kwena Maphaka", "DAJ Bracewell": "Doug Bracewell", "Naman Dhir": "Naman Dhir",
    "MK Lomror": "Mahipal Lomror", "Azhar Mahmood": "Azhar Mahmood", "PWA Mulder": "Wiaan Mulder", "JEC Franklin": "James Franklin",
    "Kumar Kushagra": "Kumar Kushagra", "SS Sarkar": "Soumya Sarkar", "AP Majumdar": "Anustup Majumdar", "CJ Dala": "Junior Dala",
    "U Kaul": "Uday Kaul", "Rahmanullah Gurbaz": "Rahmanullah Gurbaz", "KP Pietersen": "Kevin Pietersen", "H Sharma": "Harmeet Sharma",
    "GJ Bailey": "George Bailey", "AB Barath": "Adrian Barath", "Shahid Afridi": "Shahid Afridi", "S Aravind": "Sreenath Aravind",
    "NL McCullum": "Nathan McCullum", "Priyansh Arya": "Priyansh Arya", "F Behardien": "Farhaan Behardien", "SS Prabhudessai": "Suyash Prabhudessai",
    "JDS Neesham": "Jimmy Neesham", "HE van der Dussen": "Rassie van der Dussen", "LI Meriwala": "Lukman Meriwala", "AD Hales": "Alex Hales",
    "Sediqullah Atal": "Sediqullah Atal", "NA Saini": "Navdeep Saini", "Shivam Singh": "Shivam Singh", "Harshit Rana": "Harshit Rana",
    "MF Maharoof": "Farveez Maharoof", "J Overton": "Jamie Overton", "MP Yadav": "Mayank Yadav", "JW Hastings": "John Hastings",
    "Prince Yadav": "Prince Yadav", "JG Bethell": "Jacob Bethell", "DS Lehmann": "Darren Lehmann", "C Munro": "Colin Munro",
    "Joginder Sharma": "Joginder Sharma", "RJ Harris": "Ryan Harris", "R Rampaul": "Ravi Rampaul", "MG Bracewell": "Michael Bracewell",
    "MS Bhandage": "Manoj Bhandage", "AF Milne": "Adam Milne", "AP Dole": "Abhijit Dole", "Abishek Porel": "Abishek Porel",
    "R Sai Kishore": "Sai Kishore", "DH Yagnik": "Dishant Yagnik", "R McLaren": "Ryan McLaren", "K Khejroliya": "Kulwant Khejroliya",
    "AJ Hosein": "Akeal Hosein", "Ramandeep Singh": "Ramandeep Singh", "JM Sharma": "Jitesh Sharma", "S Sohal": "Sunny Sohal",
    "S Joseph": "Shamar Joseph", "PH Solanki": "Pratik Solanki", "T Banton": "Tom Banton", "RG More": "Ronit More",
    "R Minz": "Robin Minz", "JD Ryder": "Jesse Ryder", "GR Napier": "Graham Napier", "CA Pujara": "Cheteshwar Pujara",
    "AS Joseph": "Alzarri Joseph", "VG Arora": "Vaibhav Arora", "LS Livingstone": "Liam Livingstone", "Niraj Patel": "Niraj Patel",
    "J Syed Mohammad": "Syed Mohammad", "BE Hendricks": "Beuran Hendricks", "Atharva Taide": "Atharva Taide", "A Badoni": "Ayush Badoni",
    "YV Dhull": "Yash Dhull", "CJ Jordan": "Chris Jordan", "A Choudhary": "Aniket Choudhary", "Navdeep Saini": "Navdeep Saini",
    "DR Sams": "Daniel Sams", "J Arunkumar": "J Arunkumar", "Aman Hakim Khan": "Aman Hakim Khan", "RJ Gleeson": "Richard Gleeson",
    "Abdul Samad": "Abdul Samad", "KR Mayers": "Kyle Mayers", "Mohammad Ashraful": "Mohammad Ashraful", "Suryansh Shedge": "Suryansh Shedge",
    "SM Boland": "Scott Boland", "CR Brathwaite": "Carlos Brathwaite", "RE Levi": "Richard Levi", "TR Birt": "Travis Birt",
    "A Mithun": "Abhimanyu Mithun", "Mohit Rathee": "Mohit Rathee", "Sunny Singh": "Sunny Singh", "AT Carey": "Alex Carey",
    "T Kohler-Cadmore": "Tom Kohler-Cadmore", "Y Prithvi Raj": "Prithvi Raj Yarra", "Harsh Dubey": "Harsh Dubey", "Mohammad Hafeez": "Mohammad Hafeez",
    "TS Mills": "Tymal Mills", "DP Conway": "Devon Conway", "W Jaffer": "Wasim Jaffer", "PR Shah": "Pinal Shah",
    "Nithish Kumar Reddy": "Nithish Kumar Reddy", "M Markande": "Mayank Markande", "V Puthur": "V Puthur", "SD Hope": "Shai Hope",
    "TK Curran": "Tom Curran", "DJM Short": "D'Arcy Short", "SW Billings": "Sam Billings", "MA Wood": "Mark Wood",
    "A Raghuvanshi": "Angkrish Raghuvanshi", "AA Bilakhia": "Azharuddin Bilakhia", "Ankit Soni": "Ankit Soni", "A Dananjaya": "Akila Dananjaya",
    "T Stubbs": "Tristan Stubbs", "RJW Topley": "Reece Topley", "M Shahrukh Khan": "Shahrukh Khan", "P Suyal": "Pawan Suyal",
    "Saurav Chauhan": "Saurav Chauhan", "E Malinga": "Lasith Malinga", "S Vidyut": "Vidyut Sivaramakrishnan", "JE Taylor": "Jerome Taylor",
    "ND Doshi": "Nayan Doshi", "RT Ponting": "Ricky Ponting", "J Fraser-McGurk": "Jake Fraser-McGurk", "Kamran Akmal": "Kamran Akmal",
    "I Malhotra": "Ishan Malhotra", "S Tyagi": "Sudeep Tyagi", "SSB Magala": "Sisanda Magala", "D Jansen": "Duan Jansen",
    "B Chipli": "Bharat Chipli", "AS Roy": "Anukul Roy", "RJ Peterson": "Robin Peterson", "Mukesh Choudhary": "Mukesh Choudhary",
    "Azmatullah Omarzai": "Azmatullah Omarzai", "Vishnu Vinod": "Vishnu Vinod", "SZ Mulani": "Shams Mulani", "Anmolpreet Singh": "Anmolpreet Singh",
    "KP Appanna": "KP Appanna", "C Sakariya": "Chetan Sakariya", "Sachin Baby": "Sachin Baby", "R Dhawan": "Rishi Dhawan",
    "YV Takawale": "Yogesh Takawale", "A Tomar": "Anand Rajan", "Anuj Rawat": "Anuj Rawat", "M Klinger": "Michael Klinger",
    "AS Yadav": "Arjun Yadav", "P Dubey": "Pravin Dubey", "SE Rutherford": "Sherfane Rutherford", "S Randiv": "Suraj Randiv",
    "K Goel": "Karan Goel", "Vivrant Sharma": "Vivrant Sharma", "PBB Rajapaksa": "Bhanuka Rajapaksa", "SP Goswami": "Shreevats Goswami",
    "SB Wagh": "Shrikant Wagh", "N Jagadeesan": "Narayan Jagadeesan", "C Nanda": "Chetanya Nanda", "AD Nath": "Akshdeep Nath",
    "DJ Thornely": "Dominic Thornely", "HM Amla": "Hashim Amla", "AD Mascarenhas": "Dimitri Mascarenhas", "Salman Butt": "Salman Butt",
    "ER Dwivedi": "Eklavya Dwivedi", "C Madan": "Chandan Madan", "IS Sodhi": "Ish Sodhi", "Sohail Tanvir": "Sohail Tanvir",
    "NT Ellis": "Nathan Ellis", "CK Kapugedera": "Chamara Kapugedera", "DJ Harris": "Daniel Harris", "AJ Tye": "Andrew Tye",
    "CR Woakes": "Chris Woakes", "MW Short": "Matt Short", "Pankaj Singh": "Pankaj Singh", "SW Tait": "Shaun Tait",
    "A Nel": "Andre Nel", "S Badree": "Samuel Badree", "Shoaib Akhtar": "Shoaib Akhtar", "M Kaif": "Mohammad Kaif",
    "Sameer Rizvi": "Sameer Rizvi", "AS Rajpoot": "Ankit Rajpoot", "R Sanjay Yadav": "Sanjay Yadav", "RR Raje": "Rohan Raje",
    "MJ Suthar": "Manav Suthar", "Kartik Tyagi": "Kartik Tyagi", "JJ van der Wath": "Johan van der Wath", "R Ninan": "Ryan Ninan",
    "Anureet Singh": "Anureet Singh", "RS Hangargekar": "Rajvardhan Hangargekar", "UA Birla": "Udit Birla", "PHKD Mendis": "Kamindu Mendis",
    "Ashutosh Sharma": "Ashutosh Sharma", "LA Pomersbach": "Luke Pomersbach", "N Saini": "Navdeep Saini", "A Singh": "Arshdeep Singh",
    "Anand Rajan": "Anand Rajan", "Karim Janat": "Karim Janat", "NS Naik": "Nikhil Naik", "GD McGrath": "Glenn McGrath",
    "DM Bravo": "Darren Bravo", "M Manhas": "Mithun Manhas", "K Upadhyay": "Krishnakant Upadhyay", "RA Shaikh": "Rahil Shaikh",
    "AJ Turner": "Ashton Turner", "A Symonds": "Andrew Symonds", "SA Abbott": "Sean Abbott", "V Pratap Singh": "Veer Pratap Singh",
    "A Manohar": "Abhinav Manohar", "Abdur Razzak": "Abdur Razzak", "JR Hopes": "James Hopes", "Musheer Khan": "Musheer Khan",
    "L Ngidi": "Lungi Ngidi", "AN Ahmed": "Abu Nechim", "RR Bose": "Ranadeb Bose", "MA Khote": "Musavir Khote",
    "D du Preez": "Dillon du Preez", "AA Noffke": "Ashley Noffke", "Vijaykumar Vyshak": "Vijaykumar Vyshak", "TM Srivastava": "Tanmay Srivastava",
    "Jalaj S Saxena": "Jalaj Saxena", "C Ganapathy": "Chandrasekar Ganapathy", "P Parameswaran": "Prasanth Parameswaran", "P Sahu": "Pardeep Sahu",
    "IC Pandey": "Ishwar Pandey", "RS Bopara": "Ravi Bopara", "NB Singh": "Nathu Singh", "Arshad Khan (2)": "Arshad Khan",
    "N Thushara": "Nuwan Thushara", "P Amarnath": "Palani Amarnath", "CL White": "Cameron White", "AS Raut": "Abhishek Raut",
    "T Henderson": "Tyron Henderson", "SJ Srivastava": "Shalabh Srivastava", "Shashank Singh": "Shashank Singh", "S Kaushik": "Shivil Kaushik",
    "W O'Rourke": "William O'Rourke", "T Shamsi": "Tabraiz Shamsi", "M Pathirana": "Matheesha Pathirana", "A Uniyal": "Amit Uniyal",
    "Shahbaz Ahmed": "Shahbaz Ahmed", "Sunny Gupta": "Sunny Gupta", "MJ Guptill": "Martin Guptill", "JP Inglis": "Josh Inglis",
    "SH Johnson": "Spencer Johnson", "DB Ravi Teja": "Dwaraka Ravi Teja", "SB Joshi": "Sunil Joshi", "PK Garg": "Priyam Garg",
    "HC Brook": "Harry Brook", "DP Nannes": "Dirk Nannes", "PM Sarvesh Kumar": "Sarvesh Kumar", "Zeeshan Ansari": "Zeeshan Ansari",
    "MV Boucher": "Mark Boucher", "AD Mathews": "Angelo Mathews", "BAW Mendis": "Ajantha Mendis", "T Thushara": "Thilan Thushara",
    "GS Sandhu": "Gurinder Sandhu", "BB Sran": "Barinder Sran", "AP Tare": "Aditya Tare", "DJ Mitchell": "Daryl Mitchell",
    "S Ladda": "Sarabjit Ladda", "WD Parnell": "Wayne Parnell", "D Salunkhe": "Dinesh Salunkhe", "AU Rashid": "Adil Rashid",
    "CJ Green": "Chris Green", "R Powell": "Rovman Powell", "T Kohli": "Taruwar Kohli", "Misbah-ul-Haq": "Misbah-ul-Haq",
    "SM Harwood": "Shane Harwood", "B Laughlin": "Ben Laughlin", "PV Tambe": "Pravin Tambe", "BB Samantray": "Biplab Samantray",
    "AL Menaria": "Ashok Menaria", "BJ Rohrer": "Ben Rohrer", "Fazalhaq Farooqi": "Fazalhaq Farooqi", "GH Vihari": "Hanuma Vihari",
    "Kamran Khan": "Kamran Khan", "FH Edwards": "Fidel Edwards", "Ashwani Kumar": "Ashwani Kumar", "S Midhun": "Sudhesan Midhun",
    "KMDN Kulasekara": "Nuwan Kulasekara", "A Chandila": "Ajit Chandila", "Shivam Mavi": "Shivam Mavi", "Noor Ahmad": "Noor Ahmad",
    "AUK Pathan": "Asad Pathan", "PVSN Raju": "Venkatapathy Raju", "DJ Willey": "David Willey", "Arshad Khan": "Arshad Khan",
    "C Green": "Cameron Green", "WPUJC Vaas": "Chaminda Vaas", "KAJ Roach": "Kemar Roach", "SP Jackson": "Sheldon Jackson",
    "VS Malik": "Vikramjeet Malik", "M Rawat": "Mahesh Rawat", "S Chanderpaul": "Shivnarine Chanderpaul", "DL Vettori": "Daniel Vettori",
    "RD Rickelton": "Ryan Rickelton", "Dhruv Jurel": "Dhruv Jurel", "Gurnoor Brar": "Gurnoor Brar", "L Wood": "Luke Wood",
    "R Shukla": "Rahul Shukla", "T Taibu": "Tatenda Taibu", "Simarjeet Singh": "Simarjeet Singh", "LE Plunkett": "Liam Plunkett",
    "Umran Malik": "Umran Malik", "DJ Muthuswami": "Domnic Muthuswami", "FY Fazal": "Faiz Fazal", "KMA Paul": "Keemo Paul",
    "R Ravindra": "Rachin Ravindra", "Mashrafe Mortaza": "Mashrafe Mortaza", "MDKJ Perera": "Kusal Perera", "Yashpal Singh": "Yashpal Singh",
    "I Udana": "Isuru Udana", "WA Mota": "Wilkin Mota", "SM Katich": "Simon Katich", "SK Rasheed": "Shaik Rasheed",
    "BA Bhatt": "Bhargav Bhatt", "R Goyal": "Raiphi Gomez", "K Santokie": "Krishmar Santokie", "STR Binny": "Stuart Binny",
    "MS Bisla": "Manvinder Bisla", "JL Pattinson": "James Pattinson", "Sikandar Raza": "Sikandar Raza", "AG Paunikar": "Amit Paunikar",
    "R Sathish": "Rajagopal Sathish", "RM Patidar": "Rajat Patidar", "Basil Thampi": "Basil Thampi", "MP Breetzke": "Matthew Breetzke",
    "BR Sharath": "BR Sharath", "NJ Maddinson": "Nic Maddinson", "S Sandeep Warrier": "Sandeep Warrier", "DT Patil": "Darshan Patil",
    "Y Gnaneswara Rao": "Y Gnaneswara Rao", "Swapnil Singh": "Swapnil Singh", "Shoaib Malik": "Shoaib Malik", "MJ Santner": "Mitchell Santner",
    "D Pretorius": "Dwaine Pretorius", "BJ Haddin": "Brad Haddin", "V Kaverappa": "Vidwath Kaverappa", "SM Pollock": "Shaun Pollock",
    "Mayank Dagar": "Mayank Dagar", "RK Bhui": "Ricky Bhui", "XC Bartlett": "Xavier Bartlett", "Abdul Basith": "Abdul Basith",
    "RK Singh": "Rinku Singh", "Harmeet Singh": "Harmeet Singh", "NJ Rimmington": "Nathan Rimmington", "Mohammad Nabi": "Mohammad Nabi",
    "L Ronchi": "Luke Ronchi", "Suyash Sharma": "Suyash Sharma", "KM Asif": "KM Asif", "TL Suman": "Tirumalasetti Suman",
    "Shivam Sharma": "Shivam Sharma", "KS Rathore": "Kunal Rathore", "DJG Sammy": "Daren Sammy", "RE van der Merwe": "Roelof van der Merwe",
    "S Lamichhane": "Sandeep Lamichhane", "O Thomas": "Oshane Thomas", "Liton Das": "Liton Das", "AA Jhunjhunwala": "Abhishek Jhunjhunwala",
    "D Brevis": "Dewald Brevis", "P Chopra": "Prashant Chopra", "JDP Oram": "Jacob Oram", "Lalit Yadav": "Lalit Yadav",
    "G Coetzee": "Gerald Coetzee", "Bipul Sharma": "Bipul Sharma", "DR Shorey": "Dhruv Shorey", "BMAJ Mendis": "Jeevan Mendis",
    "UBT Chand": "Unmukt Chand", "MD Shanaka": "Dasun Shanaka", "Karanveer Singh": "Karanveer Singh", "MJ Henry": "Matt Henry",
    "Gulbadin Naib": "Gulbadin Naib", "RR Bhatkal": "Raju Bhatkal", "BKG Mendis": "Kusal Mendis", "B Sumanth": "Bodapati Sumanth",
    "RS Sodhi": "Reetinder Sodhi", "Gurkeerat Singh": "Gurkeerat Singh", "PA Reddy": "Akshath Reddy", "DNT Zoysa": "Nuwan Zoysa",
    "LA Carseldine": "Lee Carseldine", "Jaskaran Singh": "Jaskaran Singh", "TD Paine": "Tim Paine", "Anirudh Singh": "Anirudh Singh",
    "Y Nagar": "Yogesh Nagar", "KS Bharat": "K.S. Bharat", "TL Seifert": "Tim Seifert", "NLTC Perera": "Thisara Perera",
    "J Suchith": "Jagadeesha Suchith", "DP Vijaykumar": "DP Vijaykumar", "SB Styris": "Scott Styris", "SMSM Senanayake": "Sachithra Senanayake",
    "CRD Fernando": "Dilhara Fernando", "MG Neser": "Michael Neser", "PVD Chameera": "Dushmantha Chameera", "N Wadhera": "Nehal Wadhera",
    "J Yadav": "Jayant Yadav", "AC Voges": "Adam Voges", "AN Ghosh": "Arindam Ghosh", "RR Rossouw": "Rilee Rossouw",
    "Urvil Patel": "Urvil Patel", "PSP Handscomb": "Peter Handscomb", "KA Jamieson": "Kyle Jamieson", "AR Bawne": "Ankit Bawne",
    "R Shepherd": "Romario Shepherd", "JR Philippe": "Josh Philippe", "Akash Deep": "Akash Deep", "JL Denly": "Joe Denly",
    "Harpreet Brar": "Harpreet Brar", "Gagandeep Singh": "Gagandeep Singh", "HR Shokeen": "Hrithik Shokeen", "Shoaib Ahmed": "Shoaib Ahmed",
    "RA Bawa": "Raj Bawa", "MN Samuels": "Marlon Samuels", "D Wiese": "David Wiese", "Monu Kumar": "Monu Kumar",
    "Mujeeb Ur Rahman": "Mujeeb Ur Rahman", "Sanvir Singh": "Sanvir Singh", "P Ray Barman": "Prayas Ray Barman", "Mohsin Khan": "Mohsin Khan",
    "DS Rathi": "Devendra Rathi", "GC Viljoen": "Hardus Viljoen", "BW Hilfenhaus": "Ben Hilfenhaus", "DB Das": "Debabrata Das",
    "S Narwal": "Sumit Narwal", "PD Collingwood": "Paul Collingwood", "J Little": "Josh Little", "JE Root": "Joe Root",
    "RV Patel": "Rohan Patel", "SD Lad": "Siddhesh Lad", "JPR Scantlebury-Searles": "Javon Searles", "RJ Quiney": "Rob Quiney",
    "Ankit Sharma": "Ankit Sharma", "J Theron": "Rusty Theron", "Akash Madhwal": "Akash Madhwal", "Tanush Kotian": "Tanush Kotian",
    "SS Cottrell": "Sheldon Cottrell", "KA Maharaj": "Keshav Maharaj", "KW Richardson": "Kane Richardson", "PD Salt": "Phil Salt",
    "D Ferreira": "Donovan Ferreira", "AA Chavan": "Ankeet Chavan", "KK Cooper": "Kevon Cooper", "Sumit Kumar": "Sumit Kumar",
    "Tejas Baroka": "Tejas Baroka", "SC Kuggeleijn": "Scott Kuggeleijn", "SA Asnodkar": "Swapnil Asnodkar", "Rasikh Salam": "Rasikh Salam",
    "K Yadav": "Kuldeep Yadav", "LPC Silva": "Chamara Silva", "M Siddharth": "Manimaran Siddharth", "B Geeves": "Brett Geeves",
    "VH Zol": "Vijay Zol", "IR Jaggi": "Ishank Jaggi", "RN ten Doeschate": "Ryan ten Doeschate", "Naveen-ul-Haq": "Naveen-ul-Haq",
    "Yash Thakur": "Yash Thakur", "JJ Roy": "Jason Roy", "TM Head": "Travis Head", "CJ McKay": "Clint McKay",
    "D Kalyankrishna": "Doddapaneni Kalyankrishna", "DJ Jacobs": "Davy Jacobs", "KL Nagarkoti": "Kamlesh Nagarkoti", "KC Cariappa": "KC Cariappa",
    "B Indrajith": "Baba Indrajith", "SB Bangar": "Sanjay Bangar", "KB Arun Karthik": "Arun Karthik", "S Rana": "Saurabh Rana",
    "S Sriram": "Sridharan Sriram", "YA Abdulla": "Yusuf Abdulla", "SP Fleming": "Stephen Fleming", "CJ Ferguson": "Callum Ferguson",
    "VVS Laxman": "VVS Laxman", "AB Agarkar": "Ajit Agarkar", "P Awana": "Parvinder Awana", "K Gowtham": "Krishnappa Gowtham",
    "SS Shaikh": "Shoaib Shaikh", "X Thalaivan Sargunam": "Thalaivan Sargunam", "S Anirudha": "Srikkanth Anirudha", "SN Khan": "Sarfaraz Khan",
    "VS Yeligati": "Vikas Yeligati", "TH David": "Tim David", "P Negi": "Pawan Negi", "AA Kazi": "Abrar Kazi",
    "CA Ingram": "Colin Ingram", "SD Chitnis": "Siddharth Chitnis", "K Kartikeya": "Kumar Kartikeya", "FA Allen": "Fabian Allen",
    "Mohammad Asif": "Mohammad Asif", "M Ntini": "Makhaya Ntini", "OF Smith": "Odean Smith", "Arjun Tendulkar": "Arjun Tendulkar",
    "V Nigam": "Vikas Nigam", "B Stanlake": "Billy Stanlake", "A Chopra": "Aakash Chopra", "PN Mankad": "Prerak Mankad",
    "OA Shah": "Owais Shah", "MC Juneja": "Manpreet Juneja", "RW Price": "Ray Price", "IC Porel": "Ishan Porel",
    "JA Richardson": "Jhye Richardson", "KJ Abbott": "Kyle Abbott", "E Lewis": "Evin Lewis", "VRV Singh": "VRV Singh",
    "Aniket Verma": "Aniket Verma", "AA Kulkarni": "Atul Kulkarni", "Harmeet Singh (2)": "Harmeet Singh Baddhan", "Akash Singh": "Akash Singh",
    "TP Sudhindra": "TP Sudhindra", "RV Gomez": "Raiphi Gomez", "PC Valthaty": "Paul Valthaty", "JP Behrendorff": "Jason Behrendorff",
    "PWH de Silva": "Wanindu Hasaranga", "A Flintoff": "Andrew Flintoff", "MS Wade": "Matthew Wade", "MJ Clarke": "Michael Clarke",
    "M Jansen": "Marco Jansen", "BA Stokes": "Ben Stokes", "RR Powar": "Ramesh Powar", "LB Williams": "Luke Williams",
    "HF Gurney": "Harry Gurney", "A Mhatre": "Abhishek Mhatre", "GD Phillips": "Glenn Phillips", "C Bosch": "Corbin Bosch",
    "MN van Wyk": "Morne van Wyk", "AM Nayar": "Abhishek Nayar", "LJ Wright": "Luke Wright", "Younis Khan": "Younis Khan",
    "DE Bollinger": "Doug Bollinger", "BR Dunk": "Ben Dunk", "AM Salvi": "Aavishkar Salvi", "SB Dubey": "Saurabh Dubey",
    "R Bishnoi": "Rajesh Bishnoi", "GB Hogg": "Brad Hogg", "H Das": "Halhadar Das", "N Burger": "Nandre Burger",
    "MJ Owen": "Michael Owen", "V Viyaskanth": "V Viyaskanth", "J Botha": "Johan Botha", "M Tiwari": "Manoj Tiwari",
    "V Suryavanshi": "V Suryavanshi", "Virat Singh": "Virat Singh", "VY Mahesh": "Yo Mahesh", "Mukesh Kumar": "Mukesh Kumar",
    "M de Lange": "Marchant de Lange", "CJ Anderson": "Corey Anderson", "B Akhil": "Balachandra Akhil", "UT Khawaja": "Usman Khawaja",
    "Harpreet Singh": "Harpreet Singh", "Umar Gul": "Umar Gul", "DG Nalkande": "Darshan Nalkande", "BCJ Cutting": "Ben Cutting",
    "OC McCoy": "Obed McCoy", "LR Shukla": "Laxmi Ratan Shukla", "CK Langeveldt": "Charl Langeveldt", "A Ashish Reddy": "Ashish Reddy",
    "DR Martyn": "Damien Martyn", "Yudhvir Singh": "Yudhvir Singh Charak", "SS Mundhe": "Shrikant Mundhe", "RR Sarwan": "Ramnaresh Sarwan",
    "P Dogra": "Paras Dogra", "AG Murtaza": "Ali Murtaza", "C de Grandhomme": "Colin de Grandhomme", "AB McDonald": "Andrew McDonald",
    "SS Agarwal": "Shubham Agarwal", "DJ Malan": "Dawid Malan", "P Prasanth": "Padmanabhan Prasanth", "KS Sharma": "Karn Sharma",
    "MJ Lumb": "Michael Lumb", "AC Blizzard": "Aiden Blizzard", "A Mukund": "Abhinav Mukund"
}

def map_player_names(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col].replace(PLAYER_MAPPING)
    return df

TEAM_MAPPING = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Rising Pune Supergiants": "Rising Pune Supergiant",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru"
}

VENUE_MAPPING = {
    "Wankhede Stadium, Mumbai": "Wankhede Stadium",
    "M Chinnaswamy Stadium, Bengaluru": "M Chinnaswamy Stadium",
    "MA Chidambaram Stadium, Chepauk, Chennai": "MA Chidambaram Stadium",
    "MA Chidambaram Stadium, Chepauk": "MA Chidambaram Stadium",
    "Eden Gardens, Kolkata": "Eden Gardens",
    "Feroz Shah Kotla": "Arun Jaitley Stadium",
    "Arun Jaitley Stadium, Delhi": "Arun Jaitley Stadium",
    "Rajiv Gandhi International Stadium, Uppal": "Rajiv Gandhi International Stadium",
    "Rajiv Gandhi International Stadium, Uppal, Hyderabad": "Rajiv Gandhi International Stadium",
    "Punjab Cricket Association Stadium, Mohali": "Punjab Cricket Association IS Bindra Stadium",
    "Punjab Cricket Association IS Bindra Stadium, Mohali": "Punjab Cricket Association IS Bindra Stadium",
    "Sardar Patel Stadium, Motera": "Narendra Modi Stadium",
    "Narendra Modi Stadium, Ahmedabad": "Narendra Modi Stadium",
    "Dr DY Patil Sports Academy, Mumbai": "Dr DY Patil Sports Academy",
    "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow": "Ekana Cricket Stadium",
    "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium": "Ekana Cricket Stadium",
    "Sawai Mansingh Stadium, Jaipur": "Sawai Mansingh Stadium",
    "Maharashtra Cricket Association Stadium, Pune": "Maharashtra Cricket Association Stadium",
    "Zayed Cricket Stadium, Abu Dhabi": "Sheikh Zayed Stadium"
}

def map_team_names(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col].replace(TEAM_MAPPING)
    return df

def map_venue_names(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col].replace(VENUE_MAPPING)
    return df

# --- Data Loading ---
@st.cache_data(show_spinner=False)
def load_data():
    matches_path = os.path.join(os.path.dirname(__file__), 'archive', 'matches_updated_ipl_upto_2025.csv')
    deliveries_path = os.path.join(os.path.dirname(__file__), 'archive', 'deliveries_updated_ipl_upto_2025.csv')
    
    matches_df = pd.read_csv(matches_path)
    deliveries_df = pd.read_csv(deliveries_path)
    
    matches_df = map_player_names(matches_df, ['player_of_match'])
    deliveries_df = map_player_names(deliveries_df, ['batsman', 'bowler', 'non_striker', 'player_dismissed'])
    
    matches_df = map_team_names(matches_df, ['team1', 'team2', 'toss_winner', 'winner'])
    deliveries_df = map_team_names(deliveries_df, ['batting_team', 'bowling_team'])
    
    matches_df = map_venue_names(matches_df, ['venue'])
    
    return matches_df, deliveries_df

matches, deliveries = load_data()

# --- Global Chart Settings & Aesthetics ---
def apply_premium_layout(fig, height=350, show_x=False):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=height,
        margin=dict(l=0, r=60, t=35, b=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=show_x, title=""),
        yaxis=dict(showgrid=False, zeroline=False, title="", tickfont=dict(color='#E2E8F0', size=13)),
        hovermode='closest',
        dragmode=False,
        font=dict(family="Inter, sans-serif", color="#94A3B8")
    )
    fig.update_traces(width=0.55, cliponaxis=False)
    return fig

CHART_THEME = "plotly_dark"

# --- Top Navigation ---
import base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    img_base64 = get_base64_of_bin_file('IPL_Logo.png')
    logo_html = f'<img src="data:image/png;base64,{img_base64}">'
except:
    logo_html = ""

st.markdown(f"""
    <style>
        .glass-header {{
            background: rgba(15, 23, 42, 0.6);
            padding: 20px 25px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 20px;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            width: fit-content;
            max-width: 100%;
        }}
        .glass-header img {{
            width: 85px;
            border-radius: 50%;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
            flex-shrink: 0;
        }}
        .glass-header h1 {{
            margin: 0; font-family: 'Outfit', sans-serif; font-size: 2.4rem; font-weight: 900; 
            background: linear-gradient(90deg, #FFFFFF, #94A3B8); -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; letter-spacing: -1px; line-height: 1.1;
        }}
        .glass-header p {{
            margin: 6px 0 0 0; color: #94A3B8; font-size: 1rem; font-family: 'Inter', sans-serif; line-height: 1.4;
        }}
        @media (max-width: 768px) {{
            .glass-header {{
                padding: 15px 15px;
                gap: 12px;
            }}
            .glass-header img {{
                width: 60px;
            }}
            .glass-header h1 {{
                font-size: 1.6rem;
            }}
            .glass-header p {{
                font-size: 0.8rem;
            }}
        }}
        .header-text-block {{
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
    </style>
    <div class="glass-header">
        {logo_html}
        <div class="header-text-block">
            <h1>IPL Analytics</h1>
            <p>Explore Indian Premier League Data (2008 - 2025) with cutting-edge analytics.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("")
page = st.radio("Navigation", ["Data Explorer", "Deep Insights", "Player Comparison"], horizontal=True, label_visibility="collapsed")
st.divider()

def plot_mini_histogram(df, column, title, color="#38BDF8"):
    counts = df[column].value_counts().reset_index()
    counts.columns = [column, 'count']
    if len(counts) > 10:
        counts = counts.head(10)
    
    fig = px.bar(counts, x=column, y='count', title=title, template=CHART_THEME, color='count', color_continuous_scale='Blues')
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0), height=150, xaxis_title=None, yaxis_title=None, 
                      xaxis_showticklabels=False, yaxis_showticklabels=False, plot_bgcolor='rgba(0,0,0,0)', 
                      paper_bgcolor='rgba(0,0,0,0)', title_font_size=14, title_font_color="#E2E8F0",
                      coloraxis_showscale=False)
    fig.update_traces(marker_line_width=0, opacity=0.9)
    return fig

# --- Page: Data Explorer ---
if page == "Data Explorer":
    st.title("Data Explorer")
    st.markdown("Browse and filter through the complete historical datasets with a high-level overview.")
    st.divider()
    
    dataset_choice = st.selectbox("Select Dataset to Explore", ["Matches Data", "Deliveries Data"])
    st.write("")
    
    if dataset_choice == "Matches Data":
        col1, col2 = st.columns(2)
        col1.metric("Total Matches", f"{matches.shape[0]:,}")
        col2.metric("Total Features", matches.shape[1])
        st.write("")
        cols = st.columns(4)
        with cols[0]: st.plotly_chart(plot_mini_histogram(matches, 'season', 'Matches per Season'), use_container_width=True)
        with cols[1]: st.plotly_chart(plot_mini_histogram(matches, 'toss_decision', 'Toss Decisions'), use_container_width=True)
        with cols[2]: st.plotly_chart(plot_mini_histogram(matches, 'winner', 'Top Winners'), use_container_width=True)
        with cols[3]: st.plotly_chart(plot_mini_histogram(matches, 'venue', 'Top Venues'), use_container_width=True)
        st.write("")
        st.dataframe(matches, height=500, use_container_width=True)
        
    elif dataset_choice == "Deliveries Data":
        col1, col2 = st.columns(2)
        col1.metric("Total Deliveries", f"{deliveries.shape[0]:,}")
        col2.metric("Total Features", deliveries.shape[1])
        st.write("")
        cols = st.columns(4)
        with cols[0]: st.plotly_chart(plot_mini_histogram(deliveries, 'batting_team', 'Batting Teams'), use_container_width=True)
        with cols[1]: st.plotly_chart(plot_mini_histogram(deliveries, 'bowling_team', 'Bowling Teams'), use_container_width=True)
        with cols[2]: st.plotly_chart(plot_mini_histogram(deliveries, 'batsman_runs', 'Runs Scored per Ball'), use_container_width=True)
        with cols[3]:
            st.plotly_chart(plot_mini_histogram(deliveries[deliveries['dismissal_kind'].notna()], 'dismissal_kind', 'Dismissal Types'), use_container_width=True)
        st.write("")
        st.dataframe(deliveries.head(10000), height=500, use_container_width=True)

# --- Page: Deep Insights ---
elif page == "Deep Insights":
    st.markdown('<div class="main-title">Deep IPL Insights</div>', unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 1.15rem; margin-bottom: 2rem;'>A structured, analytical deep dive into the numbers that define the Indian Premier League.</p>", unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # COMPUTATIONS
    # ---------------------------------------------------------
    deliveries['total_runs'] = deliveries['batsman_runs'] + deliveries['extras']
    
    # Batsmen
    top_run_scorers = deliveries.groupby('batsman')['batsman_runs'].sum().reset_index().sort_values(by='batsman_runs', ascending=False).head(10)
    sixes = deliveries[deliveries['batsman_runs'] == 6].groupby('batsman').size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
    fours = deliveries[deliveries['batsman_runs'] == 4].groupby('batsman').size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
    boundaries = deliveries[deliveries['batsman_runs'].isin([4, 6])].groupby('batsman').size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
    
    # Bowlers
    bowler_wickets_kinds = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']
    wickets_df = deliveries[deliveries['dismissal_kind'].isin(bowler_wickets_kinds)]
    top_wicket_takers = wickets_df.groupby('bowler')['dismissal_kind'].count().reset_index().rename(columns={'dismissal_kind':'wickets'}).sort_values(by='wickets', ascending=False).head(10)
    dismissals_count = wickets_df['dismissal_kind'].value_counts().reset_index()
    dismissals_count.columns = ['Dismissal Kind', 'Count']
    
    deliveries['isWide'] = deliveries['isWide'].fillna(0)
    deliveries['isNoBall'] = deliveries['isNoBall'].fillna(0)
    deliveries['bowler_runs'] = deliveries['batsman_runs'] + deliveries['isWide'] + deliveries['isNoBall']
    deliveries['isLegal'] = (deliveries['isWide'] == 0) & (deliveries['isNoBall'] == 0)
    
    overs = deliveries.groupby(['matchId', 'inning', 'over', 'bowler']).agg(
        bowler_runs=('bowler_runs', 'sum'),
        legal_balls=('isLegal', 'sum')
    ).reset_index()
    
    maidens = overs[(overs['bowler_runs'] == 0) & (overs['legal_balls'] == 6)]
    top_maidens = maidens['bowler'].value_counts().reset_index().head(10)
    top_maidens.columns = ['Bowler', 'Maiden Overs']
    
    # Team
    team_wins = matches['winner'].value_counts().reset_index()
    team_wins.columns = ['Team', 'Wins']
    
    matches_df = matches.copy()
    matches_df['date'] = pd.to_datetime(matches_df['date'], errors='coerce')
    finals = matches_df.loc[matches_df.groupby('season')['date'].idxmax()]
    trophies = finals['winner'].value_counts().reset_index()
    trophies.columns = ['Team', 'Trophies']
    
    team_total_runs = deliveries.groupby('batting_team')['total_runs'].sum().reset_index().sort_values(by='total_runs', ascending=False)
    team_wickets_df = deliveries[~deliveries['dismissal_kind'].isin(['retired hurt', 'retired out']) & deliveries['dismissal_kind'].notna()]
    team_total_wickets = team_wickets_df.groupby('bowling_team')['dismissal_kind'].count().reset_index().rename(columns={'dismissal_kind':'wickets'}).sort_values(by='wickets', ascending=False)
    
    over_runs = deliveries.groupby(['matchId', 'inning', 'over', 'batting_team'])['total_runs'].sum().reset_index()
    over_runs['over'] = over_runs['over'] + 1
    highest_over = over_runs.sort_values(by='total_runs', ascending=False).head(10)
    
    valid_matches = matches.dropna(subset=['winner'])
    toss_impact = (valid_matches['toss_winner'] == valid_matches['winner']).value_counts().reset_index()
    toss_impact.columns = ['Won Match after Winning Toss', 'Count']
    toss_impact['Won Match after Winning Toss'] = toss_impact['Won Match after Winning Toss'].map({True: 'Yes', False: 'No'})
    
    runs_per_season = deliveries.merge(matches[['matchId', 'season']], on='matchId', how='left').groupby(['season', 'matchId'])['total_runs'].sum().reset_index()
    avg_runs_season = runs_per_season.groupby('season')['total_runs'].mean().reset_index()
    
    over_totals = deliveries.groupby(['matchId', 'inning', 'over'])['total_runs'].sum().reset_index()
    runs_by_over = over_totals.groupby('over')['total_runs'].mean().reset_index()
    runs_by_over.columns = ['over', 'Expected Runs per Over']
    runs_by_over['over'] = runs_by_over['over'] + 1
    
    # General Records
    pom_count = matches['player_of_match'].value_counts().reset_index().head(10)
    pom_count.columns = ['Player', 'Awards']
    venues_count = matches['venue'].value_counts().reset_index().head(10)
    venues_count.columns = ['Venue', 'Matches Hosted']

    # ---------------------------------------------------------
    # BATSMEN INSIGHTS
    # ---------------------------------------------------------
    st.markdown('<h2 class="group-header">Batsmen Insights</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Top 10 Run-Scorers")
        fig1 = px.bar(top_run_scorers, x='batsman_runs', y='batsman', orientation='h', text='batsman_runs', template=CHART_THEME, color='batsman_runs', color_continuous_scale='Sunsetdark')
        fig1.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig1.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig1), use_container_width=True)
    with col2:
        st.markdown("### Most Boundaries (4s & 6s)")
        fig15 = px.bar(boundaries, x='count', y='batsman', orientation='h', text='count', template=CHART_THEME, color='count', color_continuous_scale='Purp')
        fig15.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig15.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig15), use_container_width=True)
        
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### Most 6s by a Player")
        fig13 = px.bar(sixes, x='count', y='batsman', orientation='h', text='count', template=CHART_THEME, color='count', color_continuous_scale='Magma')
        fig13.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig13.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig13), use_container_width=True)
    with col4:
        st.markdown("### Most 4s by a Player")
        fig14 = px.bar(fours, x='count', y='batsman', orientation='h', text='count', template=CHART_THEME, color='count', color_continuous_scale='Teal')
        fig14.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig14.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig14), use_container_width=True)

    # ---------------------------------------------------------
    # BOWLERS INSIGHTS
    # ---------------------------------------------------------
    st.markdown('<h2 class="group-header">Bowlers Insights</h2>', unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        st.markdown("### Top 10 Wicket-Takers")
        fig2 = px.bar(top_wicket_takers, x='wickets', y='bowler', orientation='h', text='wickets', template=CHART_THEME, color='wickets', color_continuous_scale='Blues')
        fig2.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig2.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig2), use_container_width=True)
    with col6:
        st.markdown("### Most Maiden Overs Bowled")
        fig17 = px.bar(top_maidens, x='Maiden Overs', y='Bowler', orientation='h', text='Maiden Overs', template=CHART_THEME, color='Maiden Overs', color_continuous_scale='Mint')
        fig17.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig17.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig17), use_container_width=True)

    st.markdown("### Common Dismissal Types")
    fig6 = px.pie(dismissals_count, values='Count', names='Dismissal Kind', hole=0.55, template=CHART_THEME, color_discrete_sequence=px.colors.sequential.Tealgrn)
    fig6.update_traces(textposition='outside', textinfo='percent+label', marker=dict(line=dict(color='#0F172A', width=3)), pull=[0.02]*len(dismissals_count))
    fig6.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False, margin=dict(t=20, b=20), height=400, font=dict(family="Inter, sans-serif", color="#F8FAFC", size=13))
    st.plotly_chart(fig6, use_container_width=True)

    # ---------------------------------------------------------
    # TEAM INSIGHTS
    # ---------------------------------------------------------
    st.markdown('<h2 class="group-header">Team Insights</h2>', unsafe_allow_html=True)
    col7, col8 = st.columns(2)
    with col7:
        st.markdown("### Most IPL Trophies Won")
        fig11 = px.bar(trophies, x='Trophies', y='Team', orientation='h', text='Trophies', template=CHART_THEME, color='Trophies', color_continuous_scale='Oryel')
        fig11.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig11.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig11), use_container_width=True)
    with col8:
        st.markdown("### Most Matches Won")
        fig3 = px.bar(team_wins.sort_values(by='Wins', ascending=True), x='Wins', y='Team', orientation='h', text='Wins', template=CHART_THEME, color='Wins', color_continuous_scale='Plasma')
        fig3.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig3.update_layout(coloraxis_showscale=False)
        st.plotly_chart(apply_premium_layout(fig3, height=450), use_container_width=True)
        
    col9, col10 = st.columns(2)
    with col9:
        st.markdown("### Total Runs Scored by Franchise")
        fig12 = px.bar(team_total_runs, x='total_runs', y='batting_team', orientation='h', text='total_runs', template=CHART_THEME, color='total_runs', color_continuous_scale='Sunsetdark')
        fig12.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig12.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig12, height=450), use_container_width=True)
    with col10:
        st.markdown("### Total Wickets Taken by Franchise")
        fig_tw = px.bar(team_total_wickets, x='wickets', y='bowling_team', orientation='h', text='wickets', template=CHART_THEME, color='wickets', color_continuous_scale='Teal')
        fig_tw.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig_tw.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig_tw, height=450), use_container_width=True)
        
    col11, col12 = st.columns(2)
    with col11:
        st.markdown("### Average Runs Per Match Across Seasons")
        fig5 = px.line(avg_runs_season, x='season', y='total_runs', markers=True, template=CHART_THEME)
        fig5.update_traces(line_color='#38BDF8', line_width=4, marker=dict(size=12, color='#818CF8', line=dict(width=3, color='#020617')))
        fig5.update_layout(xaxis_title="Season", yaxis_title="Average Runs per Match", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Inter, sans-serif", color="#94A3B8"), margin=dict(l=0, r=20, t=20, b=0))
        st.plotly_chart(fig5, use_container_width=True)
    with col12:
        st.markdown("### Toss Impact on Match Outcome")
        fig4 = px.pie(toss_impact, values='Count', names='Won Match after Winning Toss', hole=0.55, template=CHART_THEME, color_discrete_sequence=['#10B981', '#F43F5E'])
        fig4.update_traces(textposition='outside', textinfo='percent+label', marker=dict(line=dict(color='#0F172A', width=3)), pull=[0.02, 0.02])
        fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False, margin=dict(t=20, b=20), height=400, font=dict(family="Inter, sans-serif", color="#F8FAFC", size=13))
        st.plotly_chart(fig4, use_container_width=True)
        
    col13, col14 = st.columns(2)
    with col13:
        st.markdown("### Average Scoring Rate by Over (1 to 20)")
        fig8 = px.bar(runs_by_over, x='over', y='Expected Runs per Over', template=CHART_THEME, color='Expected Runs per Over', color_continuous_scale='Purp')
        fig8.update_traces(textposition='outside', texttemplate='%{y:.1f}', textfont=dict(color='#F8FAFC', size=11), marker_line_width=0)
        fig8.update_layout(coloraxis_showscale=False, xaxis_title="Over Number", yaxis_title="Avg Runs per Over", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=20, t=30, b=0), font=dict(family="Inter, sans-serif", color="#94A3B8"))
        fig8.update_xaxes(tickmode='linear', tick0=1, dtick=1, showgrid=False)
        fig8.update_yaxes(showgrid=False)
        st.plotly_chart(fig8, use_container_width=True)
    with col14:
        st.markdown("### Highest Run Score in a Single Over")
        fig16 = go.Figure(data=[go.Table(
            header=dict(values=['<b>Team</b>', '<b>Over No.</b>', '<b>Runs Scored</b>'], fill_color='rgba(30, 41, 59, 0.8)', align='left', font=dict(color='white', size=14, family='Outfit')),
            cells=dict(values=[highest_over.batting_team, highest_over.over, highest_over.total_runs], fill_color='rgba(15, 23, 42, 0.5)', align='left', font=dict(color='#E2E8F0', size=13, family='Inter'), height=35))
        ])
        fig16.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=380, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig16, use_container_width=True)

    # ---------------------------------------------------------
    # GENERAL RECORDS
    # ---------------------------------------------------------
    st.markdown('<h2 class="group-header">General Records</h2>', unsafe_allow_html=True)
    col15, col16 = st.columns(2)
    with col15:
        st.markdown("### Most 'Player of the Match' Awards")
        fig7 = px.bar(pom_count, x='Awards', y='Player', orientation='h', text='Awards', template=CHART_THEME, color='Awards', color_continuous_scale='Sunsetdark')
        fig7.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig7.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig7), use_container_width=True)
    with col16:
        st.markdown("### Venues Hosting Most Matches")
        fig10 = px.bar(venues_count, x='Matches Hosted', y='Venue', orientation='h', text='Matches Hosted', template=CHART_THEME, color='Matches Hosted', color_continuous_scale='Blues')
        fig10.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig10.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig10), use_container_width=True)

# --- Page: Player Comparison ---
elif page == "Player Comparison":
    st.title("Player Comparison")
    st.markdown("Select multiple players to compare their Head-to-Head statistics side-by-side.")
    
    tab1, tab2 = st.tabs(["🏏 Batsmen Comparison", "🎯 Bowlers Comparison"])
    
    with tab1:
        st.markdown("### Compare Batsmen")
        all_batsmen = sorted(deliveries['batsman'].dropna().unique())
        selected_batsmen = st.multiselect("Select Batsmen to Compare", all_batsmen, default=["Virat Kohli", "Mahendra Singh Dhoni", "Rohit Sharma"])
        
        if len(selected_batsmen) > 0:
            batsmen_stats = []
            for player in selected_batsmen:
                pdf = deliveries[deliveries['batsman'] == player]
                if pdf.empty: continue
                runs = int(pdf['batsman_runs'].sum())
                wides = pdf['isWide'].fillna(0)
                balls = len(pdf[wides == 0])
                sr = round((runs / balls) * 100, 2) if balls > 0 else 0
                
                dismissals = deliveries[deliveries['player_dismissed'] == player]
                outs = len(dismissals)
                avg = round(runs / outs, 2) if outs > 0 else runs
                
                matches = pdf['matchId'].nunique()
                
                highest = pdf.groupby('matchId')['batsman_runs'].sum().max()
                
                fours = len(pdf[pdf['batsman_runs'] == 4])
                sixes = len(pdf[pdf['batsman_runs'] == 6])
                
                batsmen_stats.append({
                    "Player": player,
                    "Innings": matches,
                    "Runs": runs,
                    "Average": avg,
                    "Strike Rate": sr,
                    "Highest Score": highest,
                    "4s": fours,
                    "6s": sixes
                })
            
            if batsmen_stats:
                comp_df = pd.DataFrame(batsmen_stats)
                st.dataframe(comp_df, use_container_width=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                chart_height = max(130, len(comp_df) * 22 + 80)
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### TOTAL RUNS COMPARISON")
                    fig_r = px.bar(comp_df, x="Runs", y="Player", orientation='h', text="Runs", color="Runs", template=CHART_THEME, color_continuous_scale='Sunsetdark')
                    fig_r.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
                    fig_r.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'}, bargap=0.15)
                    st.plotly_chart(apply_premium_layout(fig_r, height=chart_height), use_container_width=True)
                
                with col2:
                    st.markdown("### BATTING AVERAGE COMPARISON")
                    fig_a = px.bar(comp_df, x="Average", y="Player", orientation='h', text="Average", color="Average", template=CHART_THEME, color_continuous_scale='Purp')
                    fig_a.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
                    fig_a.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'}, bargap=0.15)
                    st.plotly_chart(apply_premium_layout(fig_a, height=chart_height), use_container_width=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                col3, col4 = st.columns(2)
                
                with col3:
                    st.markdown("### STRIKE RATE COMPARISON")
                    fig_sr = px.bar(comp_df, x="Strike Rate", y="Player", orientation='h', text="Strike Rate", color="Strike Rate", template=CHART_THEME, color_continuous_scale='Plasma')
                    fig_sr.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
                    fig_sr.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'}, bargap=0.15)
                    st.plotly_chart(apply_premium_layout(fig_sr, height=chart_height), use_container_width=True)

    with tab2:
        st.markdown("### Compare Bowlers")
        all_bowlers = sorted(deliveries['bowler'].dropna().unique())
        selected_bowlers = st.multiselect("Select Bowlers to Compare", all_bowlers, default=["Lasith Malinga", "Jasprit Bumrah", "Rashid Khan"])
        
        if len(selected_bowlers) > 0:
            bowlers_stats = []
            for player in selected_bowlers:
                pdf = deliveries[deliveries['bowler'] == player]
                if pdf.empty: continue
                
                wides = pdf['isWide'].fillna(0)
                noballs = pdf['isNoBall'].fillna(0)
                
                runs_conceded = int(pdf['batsman_runs'].sum() + wides.sum() + noballs.sum())
                
                valid_balls = len(pdf[(wides == 0) & (noballs == 0)])
                overs_bowled = round(valid_balls / 6.0, 1)
                exact_overs = valid_balls / 6.0
                
                economy = round(runs_conceded / exact_overs, 2) if exact_overs > 0 else 0
                
                bowler_wickets = pdf[pdf['dismissal_kind'].isin(['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket'])]
                wickets = len(bowler_wickets)
                
                match_stats = pdf.groupby('matchId').apply(
                    lambda x: pd.Series({
                        'w': x['dismissal_kind'].isin(['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']).sum(),
                        'r': (x['batsman_runs'] + x['isWide'].fillna(0) + x['isNoBall'].fillna(0)).sum()
                    })
                ).reset_index()
                best = match_stats.sort_values(by=['w', 'r'], ascending=[False, True]).iloc[0] if not match_stats.empty else pd.Series({'w': 0, 'r': 0})
                best_figure = f"{int(best['w'])}/{int(best['r'])}"
                best_w = int(best['w'])
                
                balls_per_wicket = round(valid_balls / wickets, 2) if wickets > 0 else 0
                
                bowlers_stats.append({
                    "Player": player,
                    "Overs Bowled": overs_bowled,
                    "Wickets": wickets,
                    "Economy": economy,
                    "Best": best_figure,
                    "Balls/Wicket": balls_per_wicket,
                    "Best Match Wickets": best_w
                })
                
            if bowlers_stats:
                comp_bdf = pd.DataFrame(bowlers_stats)
                st.dataframe(comp_bdf, use_container_width=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                chart_height = max(130, len(comp_bdf) * 22 + 80)
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### TOTAL WICKETS")
                    fig_w = px.bar(comp_bdf, x="Wickets", y="Player", orientation='h', text="Wickets", color="Wickets", template=CHART_THEME, color_continuous_scale='Sunsetdark')
                    fig_w.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
                    fig_w.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'}, bargap=0.15)
                    st.plotly_chart(apply_premium_layout(fig_w, height=chart_height), use_container_width=True)
                
                with col2:
                    st.markdown("### BEST BOWLING FIGURES")
                    fig_ba = px.bar(comp_bdf, x="Best Match Wickets", y="Player", orientation='h', text="Best", color="Best Match Wickets", template=CHART_THEME, color_continuous_scale='Purp')
                    fig_ba.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
                    fig_ba.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'}, bargap=0.15)
                    st.plotly_chart(apply_premium_layout(fig_ba, height=chart_height), use_container_width=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                col3, col4 = st.columns(2)
                
                with col3:
                    st.markdown("### ECONOMY RATE (LOWER IS BETTER)")
                    fig_ec = px.bar(comp_bdf, x="Economy", y="Player", orientation='h', text="Economy", color="Economy", template=CHART_THEME, color_continuous_scale='Teal')
                    fig_ec.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
                    fig_ec.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total descending'}, bargap=0.15)
                    st.plotly_chart(apply_premium_layout(fig_ec, height=chart_height), use_container_width=True)
