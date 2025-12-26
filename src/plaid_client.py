import os
import time
from datetime import date

from plaid import ApiClient, Configuration
from plaid.api import plaid_api
from plaid.model.sandbox_public_token_create_request import (
    SandboxPublicTokenCreateRequest,
)
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,
)
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.products import Products
from plaid.exceptions import ApiException


def create_plaid_client():
    configuration = Configuration(
        host="https://sandbox.plaid.com",
        api_key={
            "clientId": os.environ["PLAID_CLIENT_ID"],
            "secret": os.environ["PLAID_SECRET"],
        },
    )
    return plaid_api.PlaidApi(ApiClient(configuration))


def get_sandbox_access_token(client):
    public_token_request = SandboxPublicTokenCreateRequest(
        institution_id="ins_109508",
        initial_products=[Products("transactions")], 
    )

    public_token_response = client.sandbox_public_token_create(
        public_token_request
    )
    public_token = public_token_response.public_token

    exchange_request = ItemPublicTokenExchangeRequest(
        public_token=public_token
    )
    exchange_response = client.item_public_token_exchange(exchange_request)

    return exchange_response.access_token


def fetch_transactions():
    client = create_plaid_client()
    access_token = get_sandbox_access_token(client)

    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=date(2024, 1, 1),
        end_date=date.today(),
    )

    for attempt in range(5):
        try:
            response = client.transactions_get(request)
            return response.transactions
        except ApiException as e:
            if "PRODUCT_NOT_READY" in str(e):
                print(f"Waiting for transactions… retry {attempt + 1}/5")
                time.sleep(2)
            else:
                raise e

    raise RuntimeError("Transactions not ready after retries")


