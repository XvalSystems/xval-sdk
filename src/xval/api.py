import requests
from .config import config as _config

endpoints = {
	"env": {
		"list": "/users/environment/", 
		"create": "/users/environment/",
		"retrieve": "/users/environment/{uuid}/"
	},
	"data": {
		"list": "/data/", 
		"create": "/data/", 
		"delete": "/data/{uuid}/",
		"retrieve": "/data/{uuid}/"
	},
	"run": {
		"list": "/run/", 
		"create": "/run/", 
		"delete": "/run/{uuid}/", 
		"clone": "/run/{uuid}/clone/",
		"retrieve": "/run/{uuid}/",
		"audits": "/run/{uuid}/audits/",
	},
	"run_element": {
		"update": "/run-element/{uuid}/",
		"retrieve": "/run-element/{uuid}/"
	},
}

def post(url: str, data: dict|None = None):
	"""Post a request to the API."""
	if data is None:
		data = {}
	response = requests.post(f"{_config.api_url}{url}", json=data, headers={'Authorization': f'Token {_config.session_token}'})
	response.raise_for_status()
	return response.json()


def get(url: str):
	"""Get a request from the API."""
	response = requests.get(f"{_config.api_url}{url}", headers={'Authorization': f'Token {_config.session_token}'})
	response.raise_for_status()
	return response.json()


def delete(url: str):
	"""Delete a request from the API."""
	response = requests.delete(f"{_config.api_url}{url}", headers={'Authorization': f'Token {_config.session_token}'})
	response.raise_for_status()
	return response

def patch(url: str, data: dict):
	"""Patch a request to the API."""
	response = requests.patch(f"{_config.api_url}{url}", json=data, headers={'Authorization': f'Token {_config.session_token}'})
	response.raise_for_status()
	return response.json()

