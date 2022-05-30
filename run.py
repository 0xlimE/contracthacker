from flask import *
from flask_socketio import *
from threading import *
import json
import pickle
import string
import random
import uuid
import os
import time

################ Flask Startup ################ 
app = Flask(__name__)
random.seed(time.time())
app.config['SECRET_KEY'] = os.urandom(30).hex()
eventcode = os.environ['eventcode']
socketio = SocketIO(app, logger=True)
maxContracts = 200
deployedContracts = 0


################ Load the JSON ################
contractPort = int(os.environ['port'])
contractNameDirty = os.environ['contractname']
contractName = ''.join(filter(str.isalnum, contractNameDirty))
with open("contracts.json","r") as f:
    contracts = json.loads(f.read())
contractSourceLocation = contracts.get(contractName).get("source")
if contractSourceLocation != "redacted":
    with open("projects/"+contractSourceLocation,"r") as f:
        contractSource = f.read()
else:
    contractSource = "redacted"
contractObjective = contracts.get(contractName).get("objective")
contractFunding = contracts.get(contractName).get("funding")
contractFlag = contracts.get(contractName).get("flag")

errorMessages=["The challenge has not been solved","Nope, not solved yet","The challenge still remains to be solved","Not yet, keep going though","The challenge is still unsolved, you can do it though","Not quite solved yet"]


################ ETH PART ################
from brownie import *
p = project.load("projects/"+contractName, name=contractName)
p.load_config()
#from brownie.project.StealFromMe import *
exec("from brownie.project.{} import *".format(contractName))
exec("contractRef = "+contractName)
network.connect('ropsten-custom') #Prefaces this command: "brownie networks add Ethereum ropsten-own-node host=http://YOUR NDODE IP:8545 chainid=100 explorer=https://api-ropsten.etherscan.io/api"
network.accounts.from_mnemonic("MNEMONIC HERE?")
mainaccount = accounts[0]
### 

global thread 
global result 
result = {}
info = None
contract = None

def deploy(tuplein):
    result,uuid = tuplein
    deployed = contractRef.deploy({'from': accounts[0],'value':contractFunding,'required_confs':0})
    result[uuid] = deployed


@app.route('/')
def root():
    global thread
    global result
    global info
    global contract

    if session.get("id") is None: #Everyone needs a session id.
        session["id"] = uuid.uuid1(random.randint(1000,100000000000000)).hex

    if session.get('authorized') is None:
        return render_template('auth.html')

    if session.get('deployed'):
        contract = Contract.from_abi(contractName,session.get("contractAddress"),contractRef.abi)
        deployedContracts = deployedContracts+1
        return render_template('index.html',title=contractName,objective=contractObjective.get("long"),sourcecode=contractSource,abi=json.dumps(contract.abi,indent=2),address=contract.address)

    elif(not session.get('started')):
        session['started'] = True
        thread = Thread(target=deploy, args=((result,session.get("id")),))
        thread.start()
        print("starting")
        return render_template('deploying.html')

    elif(not session.get('deployed')):
        if(deployedContracts > maxContracts):
            return render_template_string("Too many contracts have been deployed for this event")
        if not thread.is_alive() or info is not None:
            info = result.get(session.get("id"))
            if(info.status == 1):
                session['deployed'] = True
                session['contractAddress'] = info.contract_address
                contract = Contract.from_abi(contractName,info.contract_address,contractRef.abi)
                return render_template('index.html',title=contractName,objective=contractObjective.get("long"),sourcecode=contractSource,abi=json.dumps(contract.abi,indent=2),address=contract.address)
        return render_template('deploying.html')
    return render_template('deploying.html')


@app.route('/auth',methods = ['GET', 'POST'])
def auth():
    if request.method == 'POST':
        if request.form.get('eventcode') == eventcode:
            session['authorized'] = True



    return redirect(url_for('root'))

def get_abi():
    return contract.abi

def check_solved():
    if contractObjective.get("short") == "emptycontract":
        if contract.balance() <= 0:
            return contractFlag
        else:
            return None
    return None



@socketio.on('check_solved')   
def message_recieved():
    flag = check_solved()
    print(flag)
    if flag is not None:
        emit('flag_check', {'text':flag})
    else:
        emit('flag_check', {'text':random.choice(errorMessages)})



#Actually Start the App
if __name__ == '__main__':
    """ Run the app. """    
    socketio.run(app,host="0.0.0.0", port=contractPort, debug=True,use_reloader=False)
