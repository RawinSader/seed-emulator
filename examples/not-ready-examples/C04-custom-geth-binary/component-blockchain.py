#!/usr/bin/env python3
# encoding: utf-8

from seedemu import *
import os

emu = Emulator()

# Create the Ethereum layer
# saveState=True: will set the blockchain folder using `volumes`,
# manual: requires you to trigger the /tmp/run.sh bash files in each container to lunch the ethereum nodes
# so the blockchain data will be preserved when containers are deleted.
# Note: right now we need to manually create the folder for each node (see README.md). 
eth = EthereumService(saveState = True, manual=False)

eth.setBaseConsensusMechanism(ConsensusMechanism.POA)

# Currently the minimum amount to have to be a validator in proof of stake
balance = 32 * pow(10, 18)

poa_1 = eth.install("eth1")
poa_2 = eth.install("eth2")
poa_3 = eth.install("eth3")
pow_1 = eth.install("eth4")
pow_2 = eth.install("eth5")
pow_3 = eth.install("eth6")

container_path = "~/volumes"
host_path = "{}/{}".format(os.getcwd(), "/volumes")
binary = "geth"


poa_1.createPrefundedAccounts(balance, 1).useLocalGethBinary(container_path, binary).unlockAccounts().startMiner()
poa_2.createPrefundedAccounts(balance, 1).unlockAccounts().startMiner()
poa_3.createPrefundedAccounts(balance, 1).unlockAccounts().startMiner()

emu.getVirtualNode('eth1').addSharedFolder(container_path, host_path).setDisplayName('Ethereum-1-poa')
emu.getVirtualNode('eth2').setDisplayName('Ethereum-2-poa')
emu.getVirtualNode('eth3').setDisplayName('Ethereum-3-poa')

pow_1.setConsensusMechanism(ConsensusMechanism.POW).useLocalGethBinary(container_path, binary).createPrefundedAccounts(balance, 1).unlockAccounts().startMiner()
pow_2.setConsensusMechanism(ConsensusMechanism.POW).createPrefundedAccounts(balance, 1).unlockAccounts().startMiner()
pow_3.setConsensusMechanism(ConsensusMechanism.POW).createPrefundedAccounts(balance, 1).unlockAccounts().startMiner()

emu.getVirtualNode("eth3").addSharedFolder(container_path, host_path).setDisplayName('Ethereum-1-pow')
emu.getVirtualNode("eth4").setDisplayName('Ethereum-2-pow')
emu.getVirtualNode("eth5").setDisplayName('Ethereum-3-pow')


# Add the layer and save the component to a file
emu.addLayer(eth)
emu.dump('component-blockchain.bin')
