# comment-scraper-python

<img width="1644" alt="artboard_small" src="https://user-images.githubusercontent.com/19295862/66240171-ba8dd280-e6b0-11e9-9ccf-573a4fc5961f.png">

# Frame.io 
Frame.io is a cloud-based collaboration hub that allows video professionals to share files, comment on clips real-time, and compare different versions and edits of a clip. 

# Comment Scraper 
The comment scraper takes a root asset ID (`root_asset_id`) for a project and a developer token. It walks through your project and does the following: 

1. Grabs all the assets in the project that have comments. 
2. Puts these assets into a list.
3. Flattens the list and outputs it into a .csv file. 

The comment scraper does not handle version stacks. 

# Try it Now
You can see a Flask app using the comment scraper on Glitch here: https://glitch.com/~frameio-comment-scraper. You will need a developer token and you will need to retrieve the root asset ID to try it out. 

# Pre-requisites

* Developer account with Frame.io - [https://developer.frame.io](https://developer.frame.io)

# Configure Your Developer Token
You must configure a developer token for authentication. You can do that using the instructions in the [Create Developer Tokens](https://docs.frame.io/docs/authentication#section-create-developer-tokens) section of Frame.io's developer docs. 

# Setup
The sample is written in Python 3. You run it by doing the following:

1. Open **comment_scrape.py**.

2. Put the root asset ID you want to retrieve info for in for the ROOT_ASSET_ID value at the top. 

3. Put your developer token in for TOKEN at the top. 

# Usage

1. Run the sample with `$ python comment_scrape.py`

2. Retrieve the .csv file. It will appear in the same folder that you run comment_scrape.py from and be named **output.csv**.


