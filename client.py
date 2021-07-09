from seal import *
import os
import numpy as np
import server

def initSeal():
    #Inizializzazione dei paremetri per SEAL
	parms= EncryptionParameters(scheme_type.CKKS) #SCHEMA USATO
	
	poly_modulus_degree = 8192
	parms.set_poly_modulus_degree(poly_modulus_degree)
	parms.set_coeff_modulus(CoeffModulus.Create(poly_modulus_degree, [60, 40, 40, 60]))
	
	#Generazione contensto
	context = SEALContext.Create(parms)
	print("SEAL context created")

	return context

def getKeys(context):

	public_key = PublicKey()
	private_key = SecretKey()

	if ((os.path.isfile("keys/public.key")) and (os.path.isfile("keys/private.key"))):
		public_key.load(context, "keys/public.key")
		private_key.load(context, "keys/private.key")
		print("Loaded local keys")
	else:
		try:
			os.mkdir("keys")
		except OSError:
			pass
		keygen = KeyGenerator(context)
		public_key = keygen.public_key()
		private_key = keygen.secret_key()
		print("Keys generated")
		public_key.save("keys/public.key")
		private_key.save("keys/private.key")
		print("Keys stored")

	return public_key, private_key

def encryptData(data, context, key, dst):

	data_shape = np.shape(data)

	#Scale
	scale = pow(2.0, 60)

	ls = [] #lista contenente i numeri criptati
	res = np.zeros((data_shape))
	
	#Creazione oggetto per l'encrypting
	encryptor = Encryptor(context, key)
	
	#Creazione oggetto encodere per inserire valori numerici (double o vettori di double) all'interno di un oggetto Plaintext
	encoder = CKKSEncoder(context)
	
	#Oggetto Plaintext
	plaintext = Plaintext()
	
	#Oggetto Ciphertext
	ciphertext = Ciphertext()
	
	#Encoding del vettore di numeri nel plaintext
	encoder.encode(data, scale, plaintext)

	#Encrypting (l'oggetto ciphertext viene "riempito" con i numeri criptati)
	encryptor.encrypt(plaintext, ciphertext)

	ciphertext.save(dst)

	print("Saved ciphertext")

if __name__ == "__main__":
    
	data = age, he, al, gen = [24, 4, 6, 1]

	try:
		os.mkdir("data")
	except OSError:
		pass

	context = initSeal()
	public_key, private_key = getKeys(context)
	for i in range (len(data)):
		encryptData(data[i], context, public_key, "data/ciphertext_" + str(i))
	
	print("Esecuzione server")
	server.main(context)

	result = Ciphertext()
	result.load(context, "data/result")
	print("Loaded result")
	
	decr = Decryptor(context, private_key)
	enc = CKKSEncoder(context)

	plain_answer = Plaintext()
	plain_answer = decr.decrypt(result)
	dec_answer = enc.decode(plain_answer)
	
	print("Result: " + str(dec_answer[0]))
	
	for filename in os.listdir("data"):
		os.remove(os.path.join("data", filename))
	print("Ciphertexts and result files deleted")
