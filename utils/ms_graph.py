import msal
import requests
from flask import current_app, url_for, session

class MicrosoftGraph:
    def __init__(self):
        self._app = None

    def _build_msal_app(self):
        return msal.ConfidentialClientApplication(
            current_app.config['CLIENT_ID'],
            authority=current_app.config['AUTHORITY'],
            client_credential=current_app.config['CLIENT_SECRET'],
            token_cache=self._load_cache()
        )

    def _load_cache(self):
        cache = msal.SerializableTokenCache()
        if session.get('token_cache'):
            cache.deserialize(session.get('token_cache'))
        return cache

    def _save_cache(self, cache):
        if cache.has_state_changed:
            session['token_cache'] = cache.serialize()

    def get_auth_url(self, scopes=None):
        if scopes is None:
            scopes = current_app.config['SCOPE']
        msal_app = self._build_msal_app()
        return msal_app.get_authorization_request_url(
            scopes,
            redirect_uri=url_for('graph_auth.callback', _external=True)
        )

    def acquire_token_by_code(self, code, scopes=None):
        if scopes is None:
            scopes = current_app.config['SCOPE']
        msal_app = self._build_msal_app()
        cache = self._load_cache()
        result = msal_app.acquire_token_by_authorization_code(
            code,
            scopes=scopes,
            redirect_uri=url_for('graph_auth.callback', _external=True)
        )
        self._save_cache(cache)
        return result

    def get_token_from_cache(self, scopes=None):
        if scopes is None:
            scopes = current_app.config['SCOPE']
        msal_app = self._build_msal_app()
        cache = self._load_cache()
        accounts = msal_app.get_accounts()
        if accounts:
            result = msal_app.acquire_token_silent(scopes, account=accounts[0])
            self._save_cache(cache)
            return result
        return None

    def call_graph(self, endpoint, method='GET', data=None, json=None):
        token_result = self.get_token_from_cache()
        if not token_result:
            return None
        
        headers = {'Authorization': f"Bearer {token_result['access_token']}"}
        url = f"https://graph.microsoft.com/v1.0{endpoint}"
        
        response = requests.request(method, url, headers=headers, data=data, json=json)
        return response.json()
