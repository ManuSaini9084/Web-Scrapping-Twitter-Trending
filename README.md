  #                                                                       Web Scrapping of Twitter Trending using Selenium

## Project Overview
A web application that scrapes and displays the top 5 trending topics on Twitter using Selenium, Flask, and MongoDB.

## Features
- Automated Twitter login
- Web scraping of trending topics
- Proxy-based IP rotation
- MongoDB data storage
- Simple web interface to trigger scraping
## Trending data stores in MongoDB 

![Screenshot 2025-01-01 230417](https://github.com/user-attachments/assets/9e5d0941-0ce2-4177-9998-0ab96fec2d8b)


## Trending data renders on UI

![Screenshot 2025-01-01 223002](https://github.com/user-attachments/assets/e3772995-f653-40f6-b426-df8bf3e7e0fe)


## Demo Video 

https://youtu.be/7Lnnc9IVIMg?si=USoFukdCd7EfO5zy


## Prerequisites
- Python 3.8+
- Chrome WebDriver
- ProxyMesh account
- MongoDB

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/twitter-trends-scraper.git
cd twitter-trends-scraper
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate 
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
- Update `config.py` with:
  - Twitter credentials
  - MongoDB URI
  - ProxyMesh API details

## Running the Application
```bash
python run.py
```

## Environment Setup
- Create `.env` file for sensitive configurations
- Install Chrome WebDriver compatible with your Chrome version

## Project Structure
- `config/`: Configuration files
- `src/`: Source code (scraper, routes)
- `templates/`: HTML templates
- `run.py`: Application entry point

## Key Dependencies
- Flask
- Selenium
- PyMongo
- ProxyMesh

## Troubleshooting
- Ensure Chrome WebDriver matches Chrome version
- Check network and proxy configurations
- Verify MongoDB connection

## Limitations
- Requires active Twitter login
- Dependent on Twitter's HTML structure
