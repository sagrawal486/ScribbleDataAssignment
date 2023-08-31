Project: ScribbleData - YouTube Video Analysis

Description:
A media company has a number of data scientists, PMs, and Analysts. They would like to prepare and analyze their event data in different ways. 

Table of Contents:
1. Introduction
2. Project Structure
3. Usage Instructions
4. Features

1. Introduction:
YouTube Video Analysis is a Python-based project that leverages data analysis techniques to uncover patterns and trends in YouTube video data. It provides insights that can be valuable for content creators, marketers, and other stakeholders.

2. Project Structure:
- BackgroundTasks: Contains scripts for data preprocessing and profile creation.
- Database: Includes scripts for database management i.e. getting and saving data into database.
- Outliers: Includes scripts to identify outlier videos based on views.
- Workflows: Contains scripts for different business use cases.
- Models: Schema of Tables

3. Instructions:
- Clone the repository.
`git clone `
- Create a virtual env
`python -m venv  & source  venv/bin/activate`
- Install the required dependencies (specified in requirements.txt).
`pip install -r requirements.txt`
- Configure the 'config.ini' file with your settings. (sample already provided)
- Run 'main.py' to save data into sqlite and get outliers.
`python main.py`
- Run the server
`uvicorn app:app --port 8000`
- API Docs: `http://localhost:8000/docs`

4. Features:
- Identify outlier videos with unusually high or low views using Interquartile Range (IQR).
- Analyze category popularity to discover trending categories.
- Find videos with the most trending days.
- Find out most favoured channels so that advertisers can choose to sign contract with these channels to 
  make profit .
