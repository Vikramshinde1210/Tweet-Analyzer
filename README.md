# Tweet-Analyzer

Web App Link : https://tweet-analyzer-web-app.herokuapp.com/

This is a cool web app integrated with twitter which takes the twitter handel as as input and does :

1.Analyze the tweets of your favourite Personalities

	This tool performs the following tasks :
	1. Fetches the 5/10/50/100 most recent tweets from the given twitter handel
	2. Generates a Word Cloud
	3. Performs Sentiment Analysis a displays it in form of a Count plot 
		Sentiment analysis is done by performing following operation on the text
		1. Analyzes Subjectivity of tweets and adds an additional column for it
		2. Analyzes Polarity of tweets and adds an additional column for it
		3. Analyzes Sentiments of tweets and adds an additional column for it

2. Perform general keyword on twitter and display the fetched tweets related to keyword


This respository contains all the files for end to end model building and deployment of tweet analyzer web app

Procfile : To generate command to run the app

Requirements.txt: Requirement file

app1.py : main file which contain all code which runs on server

Presentation : Presentation of the project 

Final_Demo.gif : Demostration of Input and Output flow

<h1 align="center">Demonstration</h1>
<img src="Final_demo.gif"  />

Steps to run this project on localhost:
1. Create twitter developer account and generate api keys
2. Clone this Repo
3. Replace that keys values in app1.py file
4. Open CMD type pip install requirements.txt
5. In CMD type python app1.py




