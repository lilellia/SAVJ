import random
from collections import deque
import os
import argparse

# CLI arguments
# To encrypt: python main.py --e -file <filename> -nkeys <# of keys>
# To decrypt: python main.py
parser = argparse.ArgumentParser(description='SAVJ HackathonEncryption')
parser.add_argument('--encrypt', '--e', dest='mode', action='store_const', const='encrypt', default='decrypt')
parser.add_argument('-file', dest='file_to_encrypt')
parser.add_argument('-nkeys', dest='nkeys', type=int)

# ASCII characters 32, 33, ..., 125, 126
ALL_CHARS = [chr(i) for i in range(32, 127)]

def generate_key(message_):
	"""
	Return a list of random integers the length of the message.
	Even though `message_` is a list of individual lines, we return
	enough integers to fully encode the entire message.
	"""
	length = sum(len(line) for line in message_)
	return [random.randint(0, 93) for _ in range(length)]

def encrypt_string(to_encrypt, randoms):
	encrypted = ''

	for char, r in zip(to_encrypt, randoms):
		d = deque(ALL_CHARS)
		d.rotate(r)
		encrypted += d[ALL_CHARS.index(char)]

	return encrypted

def decrypt_string(to_decrypt, randoms):
	decrypted = ''

	for char, r in zip(to_decrypt, randoms):
		d = deque(ALL_CHARS)
		d.rotate(r)
		decrypted += ALL_CHARS[d.index(char)]

	return decrypted

def encrypt_message(message, randoms):
	encrypted = []
	i = 0
	for line in message:
		length = len(line)
		subrandom = randoms[i:i+length]
		encrypted.append(encrypt_string(line, subrandom))
		i += length

	return encrypted

def decrypt_message(message, randoms):
	decrypted = []
	i = 0
	for line in message:
		length = len(line)
		subrandom = randoms[i:i+length]
		decrypted.append(decrypt_string(line, subrandom))
		i += length

	return decrypted

def encrypt(nkeys, file_to_encrypt):
	# read in the message from file; each line is an element of `message`
	with open(file_to_encrypt, 'r') as ifile:
		message = [line.strip() for line in ifile.readlines()]

	# generate `nkeys` different keys, each of the length of the message
	keys = [generate_key(message) for _ in range(nkeys)]

	# the end result of the algorithm
	encrypted = []

	# make sure that all key files already in the folder are removed
	for keyfile in os.listdir('Keys'):
		os.remove(os.path.join('Keys', keyfile))

	# for each key...
	for i, key in enumerate(keys, 1):
		# write it to file
		with open(os.path.join('Keys', f'key{i}.txt'), 'w+') as kfile:
			kfile.write('\n'.join(map(str, key)))

		# ...and encrypt the message
		encrypted = encrypt_message(encrypted or message, key)

	# print encrypted to file/console
	with open('encrypted_file.txt', 'w+') as ofile:
		ofile.write('\n'.join(encrypted))

	print('Encrypted file output to /encrypted_file.txt')

def decrypt():
	# read keys from file
	keys = []
	for keyfile in os.listdir('Keys'):
		with open(os.path.join('Keys', keyfile), 'r') as kfile:
			keys.append(list(map(int, kfile.readlines())))

	# read the cipher text in from file; each line is an element of `cipher`
	with open('encrypted_file.txt', 'r') as ifile:
		cipher = [line.strip() for line in ifile.readlines()]

	# the end result of the algorithm
	decrypted = []

	# for each key...
	for key in keys:
		decrypted = decrypt_message(decrypted or cipher, key)

	# print decrypted to file/console
	with open('decrypted_file.txt', 'w+') as ofile:
		ofile.write('\n'.join(decrypted))

	print('Decrypted file output to /decrypted_file.txt')


if __name__ == '__main__':
	args = parser.parse_args()

	if args.mode == 'encrypt':
		encrypt(args.nkeys, args.file_to_encrypt)
	else:
		decrypt()
