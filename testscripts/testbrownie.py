from brownie import *
from threading import Thread
import json
p = project.load('projects/Charity', name="Charity")
p.load_config()
from brownie.project.Charity import *
network.connect('ropsten-own-node')
network.accounts.from_mnemonic("mnemonic")
mainaccount = accounts[0]
print(mainaccount.balance())
info = Charity.deploy({'from': accounts[0],'value':'0.1 ether'})
# def run(inf):
#     info = Token.deploy("Test Token", "TST", 18, 1e21, {'from': accounts[0]})
#     inf.append(info)

# result = []
# t = Thread(target=run, args=(result,))
# t.start()
