from flask import Blueprint, request, jsonify
import pandas as pd
from .data.search_data import USERS
from typing import Dict, List, Any

bp = Blueprint("search", __name__, url_prefix="/search")

@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200

def get_val_for_key(data : List[Dict], key : str) -> List:
    return [item[key] for item in data if key in item]


def filter_duplicates(data : List[Dict]) -> List:
    """ Filter duplicates from list of Dict

    Parameters:
        data: a list of dictionary containing the user data

    Returns:
        a list of dictionary of the same type with filtered out duplicates
    """
    tracked_ids = set()
    return_data = []

    for val in data:
        if val['id'] not in tracked_ids:
            tracked_ids.add(val['id'])
            return_data.append(val)
    
    return return_data

def search_users(args: Dict):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    # Implement search here!

    filtered_list = []
    if not args:
        filtered_list = USERS
    

    # Control statements are arranged in a way to match the criteria of bonus challenge
    # The seq. are:
    # id
    # name
    # age
    # occupation

    # Filter by Id
    if 'id' in args:
        if args['id'] in get_val_for_key(USERS, 'id'):
            for i, id in enumerate(get_val_for_key(USERS, 'id')):
                if args['id'] == id:
                    filtered_list.append(USERS[i])

    # Filter by Name        
    if 'name' in args:
        query_name = args['name'].lower()
        lower_name_list = [name.lower() for name in get_val_for_key(USERS, 'name')]
        for i, name in enumerate(lower_name_list):
            if  query_name in name:
                filtered_list.append(USERS[i])
            
    # Filter by Age
    if 'age' in args:
        query_age = int(args['age'])
        for i, age in enumerate(get_val_for_key(USERS, 'age')):
            if query_age in range(age - 1, age + 2):
                filtered_list.append(USERS[i])

    # Filter by Occupation       
    if 'occupation' in args:
        query_occ = args['occupation'].lower()
        lower_occ_list = [occ.lower() for occ in get_val_for_key(USERS, 'occupation')]
        for i, occupation in enumerate(lower_occ_list):
            if  query_occ in occupation:
                filtered_list.append(USERS[i])
            
    return filter_duplicates(filtered_list)