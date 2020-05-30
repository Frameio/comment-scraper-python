# This sample shows you how to scrape comments from a project.
# Pass the root_asset_id and a developer token in to get_all_project_comments
# generate_csv will create a CSV containing your comments.

from frameioclient import FrameioClient
import requests, json, csv
from os import getenv
from itertools import chain

# Retrieve token and root_asset_id from a local .env file.
# If you haven't worked with root_asset_id read this guide: https://docs.frame.io/docs/root-asset-ids 
token = getenv('FRAME_IO_TOKEN')
root_asset_id = getenv('ROOT_ASSET_ID')


def build_comments_list(client, asset_id, comment_list):
# Function for grabbing comments from assets. It's used by
# get_all_project_comments. It takes an initialized client,
# asset_id, and reference to an empty list. It returns
# comments on all assets.
    assets = client.get_asset_children(asset_id)

    for asset in assets:
        # Recurse through folders but skip empty ones
        if asset['type'] == "folder" and asset['item_count'] > 0:
            build_comments_list(client, asset['id'], comment_list)

# You can't get the asset name or parent ID from the `get_comments` call, so we'll add
# them to the comment dictionary now.

        if asset['type'] == "file" and asset['comment_count'] > 0:
            comments = client.get_comments(asset['id'])
            for comment in comments:
                comment['parent_id'] = asset['parent_id']
                comment['name'] = asset['name']
                comment_list.append(comment)

        if asset['type'] == "version_stack":

# Note about version stacks

            versions = client.get_asset_children(asset['id'])
            for v_asset in versions:
                comments = client.get_comments(v_asset['id'])
                for comment in comments:
                    comment['parent_id'] = v_asset['parent_id']
                    comment['name'] = v_asset['name']
                    comment_list.append(comment)

    return comment_list

# Takes a root asset ID for a project and a developer token.
# Returns a comment list with all assets.

def flatten_dict(d):
# Neeed to flatten dictionary because of data structure of API.  Owner has nested attributes with same name as base level.

    def expand(key, val):
            if isinstance(val, dict):
                return [ (key + '.' + k, v) for k, v in flatten_dict(val).items() ]
            else:
                return [ (key, val) ]
    
    items = [ item for k, v in d.items() for item in expand(k, v)]

    return dict(items)

def get_all_project_comments(root_asset_id, token):
    comment_list = []
    client = FrameioClient(token)

    build_comments_list(client, root_asset_id, comment_list)

    return comment_list

# Declare a client
client = FrameioClient(token)

# Collect all comments, still formatted like API data which we will need to flatten
comment_list = []
comments = build_comments_list(client, root_asset_id, comment_list)


# Get all the comments on the project you choose by providing a root asset ID and a developer token.

# responses = get_all_project_comments(root_asset_id, token)

# Now we can use list comprehension to grab what we want from each block in the list and make a new flat list.
# list_for_csv = [[o['text'], o['parent_id'], o['asset_id'], o['name'], o['owner_id'], o['owner']['email'], o['timestamp'], o['updated_at']] for o in flat_response_list]




# Flatten
# This is not strictly necessary, but the API returns an owners dict of objects and some attributes have the same name
# as the comment attributes.  This way all the attribute names are clearly namespaced.
flattened_comments = []
for c in comment_list:
    flattened_comments.append(flatten_dict(c))

headers = ['text', 'name', 'inserted_at', 'timestamp', 'has_replies', 'parent_id', 'owner.name', 'owner.email', 'owner_id', 'owner.account_id']

# Let's write our new list out to a .csv file. We'll add a heading.
with open('comments.csv', 'w') as file:
    f_csv = csv.DictWriter(file, headers, extrasaction='ignore')
    f_csv.writeheader()
    f_csv.writerows(flattened_comments)