# This sample shows you how scrape comments from a project.
# Pass the root_asset_id and a developer token in to get_all_project_comments
# to scrape the comments from a project. This sample does not include
# version stacks.

from frameioclient import FrameioClient
from flask import Flask, jsonify, request
import requests, json, csv, itertools

ROOT_ASSET_ID = "Put your root asset ID here."
TOKEN = "Put your developer token here."
# Function for grabbing comments from assets. It's used by
# get_all_project_comments. It takes an initialized client,
# asset_id, and reference to an empty list. It returns
# all comments on all assets. This sample does not include
# version stacks.

def all_comments(client, asset_id, comment_list):
    files = client.get_asset_children(asset_id)

    for item in files:
        if item['type'] == "file":
            if item['comment_count'] > 0:
                comments = client.get_comments(item['id'])
                comment_list.append(comments)

        if item['type'] == "folder" :
            if item['item_count'] > 0:
                all_comments(client, item['id'], comment_list)
        if item['type'] == "version_stack":
            vfiles = client.get_asset_children(item['id'])
            for item in vfiles.results:
                if item['type'] == "file":
                    if item['comment_count'] > 0:
                        comments = client.get_comments(item['id'])
                        comment_list.append(comments)


# Takes a root asset ID for a project and a developer token.
# Returns a comment list with all assets
def get_all_project_comments(root_asset_id, token):
    comment_list = []
    client = FrameioClient(token)

    all_comments(client, root_asset_id, comment_list)

    return comment_list

# Get all the comments on the project you choose by providing a root asset ID and a developer token.
responses = get_all_project_comments(ROOT_ASSET_ID, TOKEN)

# The responses list comes back as a list of Paginated Objects.
# This makes them separate out into lists of lists.

response_lists = [r.results for r in responses]

# Flatten out response_lists so that there's only one item in each part of the list
flat_response_list = list(itertools.chain.from_iterable(response_lists))

# Retrieve the asset name and add it to the end of each list so we can associate it with the asset ID later.
client = FrameioClient(TOKEN)
for item in flat_response_list:
    asset = client.get_asset(item['asset_id'])
    item['name'] = asset['name']

# Now we can use list comprehension to grab what we want from each block in the list and make a new flat list.
list_for_csv = [[o['text'], o['parent_id'], o['asset_id'], o['name'], o['owner_id'], o['owner']['email'], o['timestamp'], o['updated_at']] for o in flat_response_list]

# Let's write our new list out to a .csv file. We'll add a heading.
with open("output.csv", 'w') as myfile:
     wr = csv.writer(myfile, dialect='excel')
     wr.writerow(['Comment', 'Parent ID', 'Asset ID', 'Asset Name', 'Owner ID', 'Email', 'Timestamp', 'Updated At'])
     wr.writerows(list_for_csv)
