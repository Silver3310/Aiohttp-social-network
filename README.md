## Social network with Asynchronous Python  

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a200186cdb0e423a9118e62fea44c53b)](https://www.codacy.com/manual/Silver3310/Aiohttp-social-network?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Silver3310/Aiohttp-social-network&amp;utm_campaign=Badge_Grade)
  
The social network that was made while watching the ITVDN course  
  
The project was mainly built using aiohttp as an asynchronous server, motor as an asynchronous driver for MongoDB, and Jinja2 for working with templates

### How to run the project

Make sure, you have python 3.7, python3.7-venv, git, and MongoBD being installed, then do the following:

1.  ```git clone https://github.com/Silver3310/Aiohttp-social-network```
2.  ```cd Aiohttp-social-network```
3.  ```python3.7 -m venv venv```
4.  ```source venv/bin/activate```
5.  ```pip install -r requirements.txt```
6.  ```sudo service mongod start```
7.  ```python -c "from cryptography import fernet; print('SECRET_KEY =', fernet.Fernet.generate_key())" > config/secret.py```
8.  ```md static```
9.  ```python main.py```
