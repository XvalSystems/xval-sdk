import os
import json
from pathlib import Path
import requests
from .sdk.environment import switch_to_env

class Config:
	
	attributes = ['api_url', 'session_token', 'user_email']
	_attributes = ['config', 'config_dir', 'config_file']
	
	api_url = None
	session_token = None
	user_email = None
	
	def __setattr__(self, key, value):
		if key in self.attributes:
			super().__setattr__(key, value)
			self._save_config()
		elif (key in self._attributes):
			super().__setattr__(key, value)
		else:
			raise AttributeError(f"Config does not support arbitrary attributes. Use {self.attributes}.")
			  
	def __init__(self):
		self.config_dir = Path.home() / '.xval'
		self.config_file = self.config_dir / 'config.json'
		self._load_config()

	def _load_config(self):
		"""Load configuration from file or create default if not exists."""
		if not self.config_dir.exists():
			self.config_dir.mkdir(parents=True)
		
		if not self.config_file.exists():
			self._save_config()
		
		with open(self.config_file, 'r') as f:
			for key, value in json.load(f).items():
				setattr(self, key, value)
	
	@property
	def config(self):
		return {
			attr: getattr(self, attr) 
			for attr in self.attributes
		}
	
	@property
	def current_environment(self):
		user = self.current_user()
		if 'current_environment' in user:
			return user['current_environment']
		else:
			return None
		
	def switch_env(self, env_name: str) -> None:
		"""Switch to an environment."""
		user = self.current_user()
		for env in user['environments']:
			if env['name'] == env_name:
				switch_to_env(env['uuid'])
				return
		
		raise ValueError(f"Environment {env_name} not found or you don't have access to it.")



	def _save_config(self):
		"""Save current configuration to file."""
		with open(self.config_file, 'w') as f:
			json.dump(self.config, f, indent=4)

	def set_api_url(self, slug: str):
		"""Set the API URL based on the provided slug."""
		self.api_url = f'https://{slug}.api.xval.io'
	
	def current_user(self):
		"""Check authentication and return user metadata."""
		if not self.api_url or not self.session_token:
			return dict()

		url = f"{self.api_url}/auth/user/"
		if self.session_token:
			response = requests.get(url, headers={'Authorization': f'Token {self.session_token}'})
			response.raise_for_status()  # Raise an error for bad responses
			return response.json() # Return the JSON metadata
	
	def login(self, email: str|None, password: str):
		"""Login to the API and store session token."""

		email = self.user_email if email is None else email

		if email is None:
			return "Email is not set. Use the 'xval set --email <email>' command to set it or provide email."
		
		if self.user_email is None:
			self.user_email = email

		if not self.api_url:
			return "API URL is not set. Use the 'xval set --slug <slug>' command to set it." 

		try:
			response = requests.post(f"{self.api_url}/auth/login/", json={"email": email, "password": password}, timeout=10)
			response.raise_for_status()
		except requests.exceptions.Timeout:
			return "Request timed out. Please check your internet connection and try again."

		except requests.exceptions.RequestException as e:
			return f"An error occurred: {e}"

		if response.status_code == 200:
			token = response.json().get('key')
			if token:
				self.session_token = token
				self.user_email = email
				self._save_config()
				return "Login successful. Session token stored."
			else:
				return "Login failed: No token received."
		else:
			return f"Login failed: {response.status_code} {response.text}"

	def logout(self):
		"""Logout from the API."""
		if self.session_token:
			response = requests.post(f"{self.api_url}/auth/logout/", headers={'Authorization': f'Token {self.session_token}'})
			response.raise_for_status()
			self.session_token = None
			self._save_config()
			return "Logged out."
		else:
			return "Not logged in."
	
config = Config() 