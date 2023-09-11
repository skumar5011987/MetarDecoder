# MetarDecoder
This is a METAR code decoder project that decodes METAR weather reports based on the provided state code. It provides two API endpoints. This README.md file will guide you through setting up and running the project.

# Prerequisites
Before you start, make sure you have the following prerequisites installed on your macOS:

1: Python 3.9
2: git
3: virtualenv
4: pip (Python package manager)

# Installation
1: Clone this repository to your local machine.
    git clone https://github.com/skumar5011987/MetarDecoder.git
or
2: extract the source code
    metar.gz

3: change directory
    cd /MetarDecoder

4: Create a virtual environment to isolate project dependencies.
    virtualenv venv

5: Activate the virtual environment.
    source venv/bin/activate

6: Install project dependencies from the requirements.txt file.
    pip install -r requirements.txt

7: Make sure you are in the project directory and the virtual environment is activated.

8: move to the project directoty containing file 'manage.py'

9: start the server(at specific port 8080)
    python manage.py runserver 8080

# API Endpoints
1. Ping
    URL: http://localhost:8000/metar/ping
    Method: GET
    Description: Check if the API server is running.
    Open browser and paste the URL.
    ex: http://localhost:8000/metar/ping

2. METAR Info
    URL: http://localhost:8000/metar/info
    Method: GET
    Query Parameters:
    scode (required): The state code for which you want to retrieve METAR information (e.g., CYLL).
    nocache (optional): Set to 1 to bypass caching and fetch the latest METAR data.
    ex: http://localhost:8000/metar/info?scode=CYLL&nocache=1

# Contact
    Name: Sailesh Kumar
    Email: sailesh.18738@knit.ac.in
    GitHub: https://github.com/skumar5011987