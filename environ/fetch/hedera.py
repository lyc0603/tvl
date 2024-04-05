"""
Fetches data from Hedera Hashgraph.
"""

import json

import pandas as pd
import requests


def fetch_url(url: str, params: dict = {}) -> dict:
    """
    Fetch Hedera tokens from SaucerSwap API
    """
    response = requests.get(url, timeout=60, params=params)
    return response.json()


def post_url(url: str, json: dict = {}) -> dict:
    """
    Fetch Hedera tokens from SaucerSwap API
    """
    response = requests.post(url, timeout=60, json=json)
    return response.json()
