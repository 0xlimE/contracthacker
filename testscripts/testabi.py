from brownie import *
from threading import Thread
p = project.load('testabi', name="testabi")
p.load_config()
from brownie.project.testabi import *
network.connect('ropsten-own-node')
network.accounts.from_mnemonic("mnemonic")
mainaccount = accounts[0]
print(mainaccount.balance())

#from brownie.network import gas_price
#from brownie.network.gas.strategies import GasNowStrategy#use gas strategy to deploy fast https://eth-brownie.readthedocs.io/en/stable/core-gas.html
#gas_strategy = GasNowStrategy("fast")
#gas_price(gas_strategy)

info = CaptureTheEther.deploy({'from': accounts[0]})
