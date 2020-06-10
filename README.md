# comment-scraper-python

<img width="1644" alt="artboard_small" src="https://user-images.githubusercontent.com/19295862/66240171-ba8dd280-e6b0-11e9-9ccf-573a4fc5961f.png">

# Frame.io 
Frame.io is a cloud-based video review and collaboration platform.  Our API enables developers to automate workflows, build custom actions and UI components, and integrate to the tools and software of their choice.

# Comment Scraper 
The comment scraper takes a root asset ID (`ROOT_ASSET_ID`) for a project and a developer token. It walks through your project and does the following: 

1. Inspect all the assets in the project that have comments. 
2. Fetches the comments via the Frame.io API and stores them in dicts.
3. Flattens the data and outputs to a .csv file. 

# Try it Now
You can see a Flask app using the comment scraper on Glitch here: https://glitch.com/~frameio-comment-scraper. You will need a developer token and you will need to retrieve the root asset ID to try it out. 

# Pre-requisites

* Developer account with Frame.io - [https://developer.frame.io](https://developer.frame.io)

# Configure Your Developer Token
You must configure a developer token for authentication. You can do that using the instructions in the [Create Developer Tokens](https://docs.frame.io/docs/authentication#section-create-developer-tokens) section of Frame.io's developer docs. 

# Setup
The code can be run in Python 2.7 or 3.x. 

Before running the code, source TOKEN (your authenticated API token) and ROOT_ASSET_ID, which is the root ID for the project to scrape comments from.  

# Run the code

1. `$ python -i comment_scraper.py`

2.  `comments.csv` is written to the project directory.  Open the file and bask in the glory of your comments data!