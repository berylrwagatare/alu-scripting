#!/usr/bin/python3
"""Recursively query the Reddit API for the titles of all hot posts."""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """Return a list of all hot post titles, or None if no results."""
    if hot_list is None:
        hot_list = []
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu-scripting:v1.0 (by /u/alu_student)"}
    try:
        response = requests.get(url, headers=headers,
                                params={"limit": 100, "after": after},
                                allow_redirects=False)
        if response.status_code != 200:
            return None
        data = response.json().get("data", {})
    except Exception:
        return None

    for post in data.get("children", []):
        hot_list.append(post.get("data", {}).get("title"))

    after = data.get("after")
    if after is not None:
        return recurse(subreddit, hot_list, after)
    return hot_list if hot_list else None
