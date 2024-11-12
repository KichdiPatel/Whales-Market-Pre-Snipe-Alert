import time
import requests
import multiprocessing

# from EventLogDecoder import EventLogDecoder
# from web3 import Web3, EthereumTesterProvider

"""
- Query block data for contract
- Wait for create method, copy down id 
- Send mobile alert
- Once create method is executed, watch following offer creations until first one for id is found
- Send mobile alert
"""
API_KEY = "API-KEY"


# Use the pushover api to send a mobile notification of any alerts
def alert(msg):
    import http.client, urllib

    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request(
        "POST",
        "/1/messages.json",
        urllib.parse.urlencode(
            {
                "token": "TOKEN",
                "user": "USER",
                "message": msg,
            }
        ),
        {"Content-type": "application/x-www-form-urlencoded"},
    )
    conn.getresponse()


# returns the current block
def getCurrentBlock():
    api_url = f"https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={int(time.time())}&closest=before&apikey={API_KEY}"
    res = requests.get(api_url)
    return res.json()["result"]


# Using the etherscan api, checks the whales market smart contract transactions for the createToken function
def getCreateTokenLogs(fromBlock, toBlock):
    api_url = f"https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock={fromBlock}&toBlock={toBlock}&address=0x1eCdB32e59e948C010a189a0798C674a2d0c6603&topic0=0x1da02fe9181848bf1b401dde762d155f0da084c24db69129a3c7479f970ddbcc&page=1&offset=1000&apikey={API_KEY}"
    res = requests.get(api_url)
    val = res.json()["result"]
    tokens = []
    for tx in val:
        token = tx["data"][2:66]
        tokens.append(token)

    return tokens


# Using the etherscan api, checks the whales market smart contract transactions for the newOffer function
def getNewOffer(fromBlock, toBlock, token):
    api_url = f"https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock={fromBlock}&toBlock={toBlock}&address=0x1eCdB32e59e948C010a189a0798C674a2d0c6603&topic0=0x8f8f88015929d8eeb82fcc5c324b9713dc52572eae5cf9e6e80f7e2d81ae0898&page=1&offset=1000&apikey={API_KEY}"
    response = requests.get(api_url)
    txs = response.json()["result"]

    result = []

    for tx in txs:
        data = tx["data"]
        if token in data:
            result.append(tx)
    return result


# continuously check for tokens until a opportunity is found
def newOfferLoop(from_block, token):
    to_block = from_block
    while True:
        from_block = to_block
        to_block = getCurrentBlock()
        print(f"checking tokens from {from_block} to {to_block}")
        val = getNewOffer(from_block, to_block, token)
        if len(val) > 0:
            alert(f"New offer found: {token}")
            break

        time.sleep(600)  # TUNE THIS DELAY


# constantly check for tokens
def constantly_running_process():
    to_block = getCurrentBlock()
    while True:
        # print("Constantly running process is running...")
        from_block = to_block
        to_block = getCurrentBlock()
        tokens = getCreateTokenLogs(from_block, to_block)

        print(f"checking tokens from {from_block} to {to_block}")

        # process_list = []
        if len(tokens) > 0:
            alert(f"New tokens found: {tokens}")
        #     # Start new processes for getNewOffer
        #     for token in tokens:
        #         process = multiprocessing.Process(
        #             target=newOfferLoop, args=(from_block, to_block, token)
        #         )
        #         process.start()
        #         process_list.append(process)

        # for process in process_list:
        #     process.join()  # This will wait for all processes to finish

        time.sleep(600)  # TUNE THIS DELAY


if __name__ == "__main__":
    print("Starting new deployment!")
    try:
        # constantly_running = multiprocessing.Process(target=constantly_running_process)
        # constantly_running.start()
        # constantly_running_process()
        newOfferLoop(
            getCurrentBlock(),
            "0x3932353800000000000000000000000000000000000000000000000000000000",
        )
    except:
        alert("Error: Review code")
    # newOfferLoop(100, "12345")
