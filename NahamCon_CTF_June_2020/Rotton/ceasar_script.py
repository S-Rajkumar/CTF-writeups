from pwn import *
#nc jh2i.com 50034
sh = remote('jh2i.com',50034)
flag = {}
alb = "abcdefghijklmnopqrstuvwxyz"

def find_shift(i,j):
	a = int(ord(i))
	b = int(ord(j))
	c = a - b
	return c

def decode(st):
	s = st.strip().decode('utf-8')
	i = 's'
	j = s[0]
	shift = find_shift(i,j)
	cipherText = ""
	for ch in s :
		if ch in alb :
			cipherText += chr((ord(ch) + shift - 97) % 26 + 97)
		else :
			cipherText += ch
	cipherText += "\n"
	return cipherText.encode()

try :
	while True:
		st = sh.recvline()
		print(st.strip())
		res = decode(st)
		print(res.strip())
		txt = res.strip().decode('utf-8')
		x = re.findall("[0-9]+", txt)
		if len(x) > 0 :
			if len(x[0]) == 2 :
				flag[x[0]] = txt[58]
			if len(x[0]) == 1 :
				flag[x[0]] = txt[57]
		if len(list(flag.keys())) == 31:
			break
		sh.sendline(res)
except :
	sh.close()
print("*******************Flag*****************************")
print("Flag is : ",end="")
for i in range(31) :
	print(flag[str(i)],end="")
print()
