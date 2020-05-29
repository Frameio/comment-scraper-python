# This sample shows you how to scrape comments from a project.
# Pass the root_asset_id and a developer token in to get_all_project_comments
# to scrape the comments from a project. 

from frameioclient import FrameioClient
import requests, json, csv, itertools
import os

# Retrieve token and root_asset_id from a local .env file.
token = os.getenv('FRAME_IO_TOKEN')
root_asset_id = os.getenv('ROOT_ASSET_ID')

# Function for grabbing comments from assets. It's used by
# get_all_project_comments. It takes an initialized client,
# asset_id, and reference to an empty list. It returns
# all comments on all assets.

def all_comments(client, asset_id, comment_list):
    child_assets = client.get_asset_children(asset_id)

    for asset in child_assets:
        # Recurse through folders but skip empty ones
        if asset['type'] == "folder" and asset['item_count'] > 0:
            all_comments(client, asset['id'], comment_list)

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

# Takes a root asset ID for a project and a developer token.
# Returns a comment list with all assets.

def get_all_project_comments(root_asset_id, token):
    comment_list = []
    client = FrameioClient(token)

    all_comments(client, root_asset_id, comment_list)

    return comment_list

# Get all the comments on the project you choose by providing a root asset ID and a developer token.

responses = get_all_project_comments(root_asset_id, token)

# The response list comes back as a list of dicts.
# Flatten out responses so that there's only one item in each part of the list

flat_response_list = list(itertools.chain.from_iterable(responses))

# Now we can use list comprehension to grab what we want from each block in the list and make a new flat list.
# list_for_csv = [[o['text'], o['parent_id'], o['asset_id'], o['name'], o['owner_id'], o['owner']['email'], o['timestamp'], o['updated_at']] for o in flat_response_list]

# Let's write our new list out to a .csv file. We'll add a heading.
# with open("output.csv", 'w') as myfile:
#      wr = csv.writer(myfile, dialect='excel')
#      wr.writerow(['Comment', 'Parent ID', 'Asset ID', 'Asset Name', 'Owner ID', 'Email', 'Timestamp', 'Updated At'])
#      wr.writerows(list_for_csv)