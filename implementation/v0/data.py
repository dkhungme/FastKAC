import random
from charm.core.engine.util import objectToBytes,bytesToObject
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
import time, json, pickle, os, random, csv, copy
from kac import KAC
from sys import getsizeof
import subprocess
from charm.core.math.pairing import hashPair as sha1
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction,AuthenticatedCryptoAbstraction, MessageAuthenticator
import kac

# class KAC_test:
# 	def __init__(self, groupObj='SS512'):
# 		global group
# 		self.kac_test = KAC(groupObj)
# 		group=self.kac_test.group

def plain_generator(n):
		data=[]
		global datastring
		datastring=[]
		for i in xrange(n):
			# print "here"
			# x = random.randint(1,256)
			camera_id=random.getrandbits(8)
			time=random.getrandbits(16)
			location=random.getrandbits(8)
			value=random.getrandbits(8)
			data.append((camera_id,time,location,value))
			datastring.append(str(camera_id)+str(time)+str(location)+str(value))


		with open('data_generator.csv','w') as out:
			csv_out=csv.writer(out)
			csv_out.writerow(['id','time','location','value'])
			for row in data:
			    csv_out.writerow(row)


def generate_param(n):
	storage = {}
	global kac 
	kac = KAC()
	storage['n'] = n
	storage['param'] = kac.setup(n)
	storage['plain'] = [kac.group.random(GT)]
	storage['cipher'] = [kac.group.random(GT)]
	storage['e_g1_g2'] = kac.e_g1_g2
	storage['key'] = kac.keygen(storage['param'])
	global AESkey
	AESkey=[]

	for i in range(1,n+1): 
		plain = kac.group.random(GT)
		AESkey.append(SymmetricCryptoAbstraction(sha1(plain)))
		storage['plain'].append(plain)
		storage['cipher'].append(kac.encrypt(storage['key']['pk'], i, plain, storage['param']))
	
	print "I have done all parameters!"
	
	# outFile = open('GTparam.txt', 'w')
	# for i in range(1,n+1): 
	# 	storage['plain'] = [kac.group.random(GT)]
	# 	storage['cipher'] = [kac.group.random(GT)]
	# 	# with open('GTparam.txt', 'w') as outfile:
	# 	# json.dump(data,outfile)
	# 		# outfile.write(str(i)+':\n')
	# 	outFile.write('\nMy output GT element!\n')
	# 	plain = kac.group.random(GT)
	# 	storage['plain'].append(plain)
	# 	storage['cipher'].append(kac.encrypt(storage['key']['pk'], i, plain, storage['param']))
	# 	data=objectToBytes(storage['plain'], kac.group)
	# 	# with open('GTparam.txt', 'w') as outfile:
	# 	outFile.write(data)
	# 		# outfile.write(storage['plain'])
	# outFile.close()
	# p=subprocess.Popen("/home/grace/Desktop/KAC code/abc",stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
	# p.stdin.write(str(n)+'\n')
	# a = p.stdout.read()
	# print a
	# print "sent"
	# print storage
	return storage

def main():

	hour=0.1
	sampling=1
	n=int(hour*60*60*sampling)
	plain_generator(n)
    
	# if not os.path.isfile('Param.txt'):
	storage = generate_param(n)
	with open('Param.txt', 'w') as outfile:
	  	json.dump(serialize(storage), outfile)
	# else:
	with open('Param.txt', 'r') as infile:
  		storage = deserialize(json.load(infile))

  	# list_n = [2**i for i in xrange(16)]
  	list_n = [2**8]

  	# list_n = [i for i in xrange(1,n,50)]

  	AESEncryption(n)

  	extract_time, aggregate_size = kaccode.extraction_time(storage, list_n)
	with open('kac_extract_time.csv','w') as out:
	    csv_out=csv.writer(out)
	    csv_out.writerow(['n','time(s)'])
	    for row in extract_time:
	        csv_out.writerow(row)
  	
	NORMAL_DECRYPT = 1
	SET_DECRYPT = 2
	RANGE_DECRYPT = 3



	extract_time, aggregate_size, decrypt_time = kaccode.decryption_time(storage, list_n, RANGE_DECRYPT)
	# kac.group.EndBenchmark()


	# print("<=== General Benchmarks ===>")
	
	# # print("GT pairing   := ", msmtDict["Mul"][GT])
	# granDict = kac.group.GetGranularBenchmarks()
	# # print("<=== General Benchmarks ===>")
	# # print("Results  := ", msmtDict)
	# # print("<=== Granular Benchmarks ===>")
	# # print("GT pairing   := ", granDict["Pair"][GT])



	print "Range Decrypt Done!"

	with open('kac_aggregate_size.csv','w') as out:
	    csv_out=csv.writer(out)
	    csv_out.writerow(['n','bytes'])
	    for row in aggregate_size:
	        csv_out.writerow(row)

	with open('kac_range_decrypt_time.csv','w') as out:
	    csv_out=csv.writer(out)
	    csv_out.writerow(['n','time(s)'])
	    for row in decrypt_time:
	        csv_out.writerow(row)

	# extract_time, aggregate_size, decrypt_time = kaccode.decryption_time(storage, list_n, SET_DECRYPT)

	# print "Set Decrypt Done!"

	# with open('kac_set_decrypt_time.csv','w') as out:
	#     csv_out=csv.writer(out)
	#     csv_out.writerow(['n','time(s)'])
	#     for row in decrypt_time:
	#         csv_out.writerow(row)

	# aggregate_time, aggregate_size, decrypt_time = kaccode.decryption_time(storage, list_n, NORMAL_DECRYPT)

	# print "Normal Decrypt Done!"

	# with open('kac_normal_decrypt_time.csv','w') as out:
	#     csv_out=csv.writer(out)
	#     csv_out.writerow(['n','time(s)'])
	#     for row in decrypt_time:
	#         csv_out.writerow(row)

  	print "Test Done!"
  	# kac.encrypt_time_space(list_n)
  	# kac.decryption_time(storage, list_n, RANGE_DECRYPT)



	# return storage
	# p=subprocess.Popen("/home/grace/Desktop/KAC code/abc",stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
	# # p.stdin.write('3\n')
	# p.stdin.write(str(n)+'\n')
	# a = p.stdout.read() 
	# print a


def AESEncryption(n):
	for i in range(0,n):
		msg = datastring[i]
		ct = AESkey[i].encrypt(msg)
		dmsg = AESkey[i].decrypt(ct)
		assert msg == dmsg , 'o: =>%s\nm: =>%s' % (msg, dmsg)
	print "AES Encryption Done!"


def serialize(s):
	storage = {}
	storage['n'] = s['n']
	storage['param'] = objectToBytes(s['param'], kac.group)
	storage['e_g1_g2'] = objectToBytes(s['e_g1_g2'], kac.group)
	storage['key'] = objectToBytes(s['key'], kac.group)
	storage['plain'] = objectToBytes(s['plain'], kac.group)
	storage['cipher'] = objectToBytes(s['cipher'], kac.group)
	return storage

def deserialize(storage):
	kac = KAC()
	kac.n = storage['n']
	storage['param'] = bytesToObject(storage['param'], kac.group)
	storage['e_g1_g2'] = bytesToObject(storage['e_g1_g2'], kac.group)
	kac.e_g1_g2 = storage['e_g1_g2']
	storage['key'] = bytesToObject(storage['key'], kac.group)
	storage['plain'] = bytesToObject(storage['plain'], kac.group)
	storage['cipher'] = bytesToObject(storage['cipher'], kac.group)

	return storage



if __name__ == "__main__":
	main()
