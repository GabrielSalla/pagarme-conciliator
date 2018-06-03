import inquirer
import aiohttp
import logging
import json
import os

_logger = logging.getLogger("Pagar.me API")
PAGARME_API = "https://api.pagar.me/1"

AUTHENTICATION_METHOD = os.environ["AUTHENTICATION_METHOD"]
if AUTHENTICATION_METHOD == "api_key":
    API_KEY = os.environ["API_KEY"]
elif AUTHENTICATION_METHOD == "user":
    SESSION_ID = None
    ENVIRONMENT = os.environ["ENVIRONMENT"]
    if ENVIRONMENT not in ["test", "live"]:
        raise ValueError(f"Invalid ENVIRONMENT {ENVIRONMENT}")
else:
    raise ValueError(f"Invalid AUTHENTICATION_METHOD {AUTHENTICATION_METHOD}")


async def _request(method, endpoint, params=None, body=None):
    url = PAGARME_API + endpoint

    # Set the authentication variables
    headers = dict()
    request_params = dict()
    if AUTHENTICATION_METHOD == "api_key":
        request_params["api_key"] = API_KEY
    elif AUTHENTICATION_METHOD == "user":
        if SESSION_ID is not None:
            request_params["session_id"] = SESSION_ID
        headers["X-Live"] = "1" if ENVIRONMENT == "live" else "0"

    if params is not None:
        request_params.update(params)

    try:
        request = aiohttp.request(
            method, url, headers=headers, params=request_params, json=body)
        async with request as response:
            # If status is different from 200, something went wrong
            if response.status != 200:
                _logger.error(await response.text())
                return None
            data = await response.json()
            _logger.info(f"{url}  {params}  {body}")
            _logger.info(json.dumps(data))
            return data
    except aiohttp.ServerTimeoutError:
        _logger.error(f"ServerTimeoutError - {url} {json.dumps(body)}")
    except aiohttp.ClientConnectorError:
        _logger.error(f"ClientConnectorError - {url} {json.dumps(body)}")


async def post(endpoint, body=None):
    return await _request("POST", endpoint, body=body)


async def get(endpoint, params=None):
    return await _request("GET", endpoint, params=params)


def _save_session_id():
    with open(".session_id", "w") as session_file:
        session_file.write(SESSION_ID)


def _load_session_id():
    try:
        with open(".session_id", "r") as session_file:
            return session_file.read()
    except FileNotFoundError:
        return None


async def _get_user_info():
    endpoint = "/user"
    return await get(endpoint)


async def authenticate():
    global SESSION_ID

    if AUTHENTICATION_METHOD != "user":
        return True

    session_id = _load_session_id()
    if session_id is not None:
        SESSION_ID = session_id
        result = await _get_user_info()
        if result is not None:
            return True

    endpoint = "/sessions"

    questions = [
        inquirer.Text("email", message="Email"),
        inquirer.Password("password", message="Password")
    ]
    body = inquirer.prompt(questions)
    result = await post(endpoint, body=body)
    if result is not None:
        SESSION_ID = result["session_id"]
        _save_session_id()
        return True
    return False
