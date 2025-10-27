# SonosRPC
A simple program written in python for enabling Discord's Rich Presence in Sonos S1 based systems.
[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence) 
## Dependencies
##### Pypresence
~~~
pip install pypresence
~~~
##### Node.js 20+
For https://github.com/jishi/node-sonos-http-api/
## Installation	
1) Clone this repository
~~~
git clone https://github.com/mikuhere/SonosRPC
~~~
2) Get a developer application ID from discord
3) Edit config.ini and add the application ID
~~~
[General]
urlToSonosAPI = http://localhost:5005/state
discordAppID = 12345678900121
#enter discord app ID from discord developer page to discordAppID
~~~
4) Get the Sonos API running
Change directory to node-sonos-http-api
5) Run the following commands
~~~
npm install
npm start
~~~
6) node-sonos-http-api should now be running
7) run main.py
~~~
python main.py
~~~
