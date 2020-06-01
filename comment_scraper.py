###################################
# This scraper shows you how to gather comments from
# a Frame.io project and write to a tidy CSV.
# Comments are gathered recursively from the 
# Folders, files and version stacks within your project.
###################################


import csv
from os import getenv
from itertools import chain

from frameioclient import FrameioClient

def build_comments_list(client, asset_id, comment_list):
    """
    Takes an initialized client, recursively builds a list of comments
    and returns the list. (Technically, it's a list of dicts)
    """
    assets = client.get_asset_children(asset_id)

    for asset in assets:
        # Recurse through folders but skip the empty ones
        if asset['type'] == "folder" and asset['item_count'] > 0:
            build_comments_list(client, asset['id'], comment_list)

        if asset['type'] == "file" and asset['comment_count'] > 0:
            comments = client.get_comments(asset['id'])
            for comment in comments:
                # The 'get_comments" call won't return the asset name or parent ID
                # So we'll add them to the dictionary now. 
                comment['parent_id'] = asset['parent_id']
                comment['name'] = asset['name']
                comment_list.append(comment)

        if asset['type'] == "version_stack":
            # Read about version stacks: https://docs.frame.io/docs/managing-version-stacks
            versions = client.get_asset_children(asset['id'])
            for v_asset in versions:
                comments = client.get_comments(v_asset['id'])
                for comment in comments:
                    comment['parent_id'] = v_asset['parent_id']
                    comment['name'] = v_asset['name']
                    comment_list.append(comment)

    return comment_list


def flatten_dict(d):
    # The get_comments API response is verbose and contains nested objects.
    # Use this helper functon to flatten the dict holding the API response data
    # and namespace the attributes.

    def expand(key, val):
            if isinstance(val, dict):
                return [ (key + '.' + k, v) for k, v in flatten_dict(val).items() ]
            else:
                return [ (key, val) ]
    
    items = [ item for k, v in d.items() for item in expand(k, v)]

    return dict(items)


def write_comments_csv(c_list):
    # Writes comments to comments.csv
    # Any attributes you add to the headers list will automatically be written to the CSV
    # The API returns many attributes so familiarize with the response data!
    headers = ['text', 'name', 'inserted_at', 'timestamp', 'has_replies', 'parent_id', 'owner.name', 'owner.email', 'owner_id', 'owner.account_id']

    # Flattening the comments dicts is not at all necessary, but the namespacing
    # makes the CSV headers much more readable.
    flat_comments_list = []
    for c in c_list:
        flat_comments_list.append(flatten_dict(c))

    with open('comments.csv', 'w') as file:
        f_csv = csv.DictWriter(file, headers, extrasaction='ignore')
        f_csv.writeheader()
        f_csv.writerows(flat_comments_list)


if __name__ = __main__:

    # Retrieve token and root_asset_id from a local .env file.
    # If you don't know what Root Asset ID is, read this guide: https://docs.frame.io/docs/root-asset-ids 
    TOKEN = getenv('FRAME_IO_TOKEN')
    ROOT_ASSET_ID = getenv('ROOT_ASSET_ID')

    # Initialize the client library
    client = FrameioClient(TOKEN)

    # Build the comments list
    comments = []
    comments_list = build_comments_list(client, ROOT_ASSET_ID, comments)

    # Write the comments to comments.csv
    write_comments_csv(comments_list)