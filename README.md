# contracthacker
A platform for ethereum smart contract hacking CTF challenges.
Test

## Set up
Add your node set up in the `setup.sh`.

Add your wallets mnemonic in the `run.py` file on line 49.

Then run `docker-compose up`. 
This will start the 3 challenges; `StealFromMe`, `Bank` and `Charity`. 


## Adding a new challenge
To add a new challenge, decide on a challenge name, it can only be alphanumeric characters (no spaces). In this example I will use the name `coolchallenge`.

Make a new folder under `projects` named your challenge name, and then make a folder under this named `contracts` and add your solidity contract file here, in this example `coolchallenge.sol`.
```projects/coolchallenge/contracts/coolchallenge.sol```

Open the `contracts.json` file and add an entry for the contract, in this example:
```
    "coolchallenge":{
        "name":"coolchallenge",
        "source":"coolchallenge/contracts/coolchallenge.sol",
        "objective":{"short":"emptycontract","long":"Empty the contract for funds."},
        "funding":"0.1 ether",
        "flag":"CTF{this_is_cool_challenge}"
    }
```
For now only the objective `emptycontract` is supported, if you wish to add more, please open a pull request.

Add the challenge to the `docker-compose.yml` file, for this example with port 8005, eventcode 1234 and name:
```
  coolchallenge:
    build: .
    ports:
    - "8005:8005"
    environment:
      - port=8005
      - eventcode=1234
      - contractname=coolchallenge
```
and perform the commands `docker-compose down` and then `docker-compose up`, then the challenge should be deployed on the specified port.