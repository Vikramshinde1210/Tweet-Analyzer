#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing required libraries
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import dash
import dash_core_components as dcc
import dash_html_components as html
from tweepy import OAuthHandler
import plotly.graph_objs as go
from dash.dependencies import Input, Output,State
from PIL import Image
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import seaborn as sns
import dash_bootstrap_components as dbc


# In[2]:

#Replace keys generated here
# Put this keys here by creating twitter developer account
ACESS_TOKEN = 
ACESS_TOKEN_SECRET = 
CONSUMER_KEY = 
CONSUMER_SECRET = 


# In[3]:


# authenticate the keys by creating authentication object
auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)

# set access token and access token secret
auth.set_access_token(ACESS_TOKEN,ACESS_TOKEN_SECRET)


# In[4]:


# create the API object
api = tweepy.API(auth, wait_on_rate_limit=True)


# In[ ]:






app = dash.Dash(__name__,external_stylesheets=[dbc.themes.CYBORG])
server = app.server

# style={'display':'inline-block', 'verticalAlign':'top', 'width':'30%'}


# In[ ]:


app.layout = html.Div(children=[
    html.Title("Tweet Analyzer"),
    html.Img(src="https://help.twitter.com/content/dam/help-twitter/twitter-logo.png",style={'display':'inline-block', 'verticalAlign':'middle','height':'10%', 'width':'10%','margin-left': '45%'}),
    html.H1("Tweet Analyzer 🔥",
           style={
            'textAlign': 'center',
            'color': '#7FDBFF'
        }),
    html.H3("Analyze Tweets Of Specific Account on Twitter",
           style={
            'textAlign': 'center',
            'color': '#7FDBFF'
        }),
    dcc.Input(id='id1',placeholder='Enter the exact twitter handle of the User (without @)',type='text', style={'display':'inline-block','verticalAlign':'middle', 'width':'50%','margin-left': '25%'}),
    html.Br(),
    html.Br(),
    html.H6("Select Action To Perform",
           style={
            'textAlign': 'center',
            'color': '#7FDBFF'
        }),
    dcc.Dropdown(id='id2',
                options=[
                    {'label':"Show Recent Tweets",'value':"tweets"},
                    {'label':"Generate Word Cloud",'value':"cloud"},
                    {'label':"Visualize The Sentiment Analysis",'value':"sentiment"}
                    
                ],
                 style={'display':'inline-block', 'verticalAlign':'middle', 'width':'50%','margin-left': '25%'}),
     html.Br(),
    html.Br(),
    html.H6("Select No Of Tweets To Fetch",
           style={
            'textAlign': 'center',
            'color': '#7FDBFF'
        }),
    dcc.Dropdown(id='id6',
                   options=[{'label':'5  ',
                          'value':5},
                         {'label':'10  ',
                          'value':10},
                           {'label':'50  ',
                          'value':50},
                           {'label':'100  ',
                          'value':100}],
                  value=5,style={'display':'inline-block', 'verticalAlign':'middle', 'width':'50%','margin-left': '25%'}),
    html.Br(),
    html.Br(),
    
    dbc.Button("Submit",id="submit",color="success",className="mr-1",style={'verticalAlign':'middle', 'width':'50%','margin-left': '25%'}),
    html.Br(),
    html.Br(),
    html.Div(id="id3", style={'textAlign': 'center'}),
    html.H6("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------",
           style={
            'textAlign': 'center',
            'color': '#7FDBFF'
        }),
    html.Br(),
    html.Br(),
    html.H3("Analyze General Tweets Using Keyword Search",
           style={
            'textAlign': 'center',
            'color': '#7FDBFF'
        }),
    
    dcc.Input(id='id7',placeholder='Enter Any Keyword or hashtag to search',type='text', style={'display':'inline-block','verticalAlign':'middle', 'width':'50%','margin-left': '25%'}),
    html.Br(),
    html.Br(),
    dcc.Dropdown(id='id8',
                   options=[{'label':'With Retweets',
                          'value':"with"},
                         {'label':'Without Retweets',
                          'value':"without"},
                           ],
                  value="with",style={'display':'inline-block', 'verticalAlign':'middle', 'width':'50%','margin-left': '25%'}),
    html.Br(),
    html.Br(),
    dbc.Button("Submit",id="submit1",color="success",className="mr-1",style={'verticalAlign':'middle', 'width':'50%','margin-left': '25%'}),
    html.Br(),
    html.Br(),
    html.Div(id="id9",style={'textAlign': 'center'})

    
    

    
    
    
    
],style={"verticalAlign":"center"})


# In[ ]:


def cleanTxt(text):
    text = re.sub(r'@[A-Za-z0-9]+',"",text) # removes @mentions
    text = re.sub(r'#',"",text) # removing # symbol
    text = re.sub(r"RT[\s]+","",text) # remove re-tweets
    text = re.sub(r"https?:\/\/\S+","",text) # remove the hyperlink
    text = re.sub(r'[!*@#%&$_?.:^]+',"",text) # removing all the special characters
    
    return text

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
    return TextBlob(text).sentiment.polarity

def getAnalysis(score):
    if score < 0:
        return "Negative"
    elif score == 0:
        return "Neutral"
    else:
        return "Positive"


# In[ ]:


@app.callback(Output('id3','children'),
              [Input('submit','n_clicks')],
              [State('id1','value'),State('id2','value'),State('id6','value')])
def output(n_clicks,number1,number2,number3):
    if str(number1)=="":
        return [html.H1("Please Enter username",
           style={
            'textAlign': 'center',
            'color': '#7FDBFF'
        })]
    posts = api.user_timeline(screen_name=number1, count = number3, lang ="en", tweet_mode="extended")
    
    if len(posts)==0:
        return [html.Ul(id='my-list')]
    
    if str(number2)=="tweets":
        return [html.Ul(id='my-list', children=[html.Li(i.full_text) for i in posts])]
    if str(number2)=='cloud':
        df = pd.DataFrame([tweet.full_text for tweet in posts], columns= ['Tweets'])
        df['Tweets'] = df['Tweets'].apply(cleanTxt)
        df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
        df['Polarity'] = df['Tweets'].apply(getPolarity)
        allWords = " ".join([twts for twts in df['Tweets']])
        wordCloud = WordCloud(width=500,height=300,random_state=21,max_font_size=119).generate(allWords)
        plt.imshow(wordCloud,interpolation="bilinear")
        plt.axis("off")
        plt.savefig('WC.jpg')
        img = base64.b64encode(open("WC.jpg", 'rb').read())
        return [html.Img(src='data:image/png;base64,{}'.format(img.decode()))]
    if str(number2)=="sentiment":
        df = pd.DataFrame([tweet.full_text for tweet in posts], columns= ['Tweets'])
        df['Tweets'] = df['Tweets'].apply(cleanTxt)
        df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
        df['Polarity'] = df['Tweets'].apply(getPolarity)
        df['Analysis'] = df['Polarity'].apply(getAnalysis)
        plt.figure()
        sns.countplot(x=df["Analysis"],data=df)
        plt.savefig("W1.jpg")
        img = base64.b64encode(open("W1.jpg", 'rb').read())
        return [html.Img(src='data:image/png;base64,{}'.format(img.decode()), style={
                'height': '50%',
                'width': '50%'
            })]
        
        
        
        


# In[ ]:


@app.callback(Output('id9','children'),
              [Input('submit1','n_clicks')],
              [State('id7','value'),State('id8','value')])
def op(n_clicks,number1,number2):
    if number2=="without":
        number1 = number1 + " -filter:retweets"
    tweets = tweepy.Cursor(api.search,
              q=number1,
              lang="en").items(10)
    return [html.Ul(id='my-list', children=[html.Li(i.text) for i in tweets])]
    

    
    
        


# In[ ]:


if __name__=="__main__":
    app.run_server()


# In[ ]:





# In[ ]:




