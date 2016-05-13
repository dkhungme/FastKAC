from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.core.engine.util import objectToBytes,bytesToObject

import time, json, pickle, os, random, csv, copy
from sys import getsizeof
groupObj='SS512'
global group
group = PairingGroup(groupObj)


r = group.random(ZR)
i=0
for i in xrange(1,10):
	r_i = group.hash(str(r) + str(i), ZR)
	print r_i
