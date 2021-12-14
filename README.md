# python-github-actions-example

![](https://github.com/nikhilkumarsingh/python-github-actions-example/workflows/Python%20application/badge.svg)

Example for creating a simple CI/CD pipeline for a Python Project using Github Actions.

## What is CI/CD?
With the continuous method of software development, developers often continuously build, test, and deploy iterative code changes. This iterative process reduces the chance that new code created is  buggy . With this method, there is less human intervention or even no intervention at all, from the development of new code until its deployment.

## Continuous integration
Each change submitted to an application, even to development branches, is built and tested automatically and continuously. These tests ensure the changes pass all tests, guidelines, and code compliance standards you established for your application.

## Continuous deployment
Continuous deployment checks the code automatically, and does not requires human intervention to manually and strategically trigger the deployment of the changes. Through this, developer can reduce the routine manual labour and focus on higher value output.

## Motivation of the project
-Develop a GITLAB workflow for CI/CD of python based web app with 2 examples of Flask and Dash.
-Enable easy deployment by just adjusting the src folder app.py.
-Continually evolving data with new metrics of focus or analysis methods.
-Covid 19 data and S&P 500 data

## Outcome
Dash dashboard that returns a random stock ticker from a list of selected companies namely FAANG, Tesla, GM , Ford and others like Microsoft.


## Steps
### Iteration 1:
Develop workflow that can render Hello World Flask App and successfully link to Heroku.
### Iteration 2:
Try out with task master app to observe if Flask CRUD functions can work.
### Iteration 3: 
Edit to do with COVID 19 dataset. Did locally but failed on heroku.
### Iteration 4:
Focus on End goal of stock market understanding and customisation of parameters such as Bollinger Bands and RSI to desired intervals instead of industry standard.
### Iteration 5:
Add on perhaps news feed via API to focus on articles on Dashboard at side.
### If possible
Compare with S&P500 returns as well.
## Challenges
### 1) Setting up environment variables and compatability of software version. Complete requirements.txt

### 2) Procfile difference between Flask app and Dash. Flask app uses command app:app while Dash involves app:server.
### 3) Heroku inability to find local files. (Trying to find a go around). Current solution involves utilising data from yahoo finance stock info.
![image]screenshots/AAPL_Boll_bands_pre_update.JPG
### 4) Problem with yahoo finance stock info due to stock splits as compared to google. E.g of AAPL which will result in difficulty in visualising.



## Initialisation process





## Types of test
-Logic test for number of cases of covid-19
-Warning test
