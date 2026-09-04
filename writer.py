import sys, base64, os
p=sys.argv[1]
os.makedirs(os.path.dirname(p), exist_ok=True)
open(p, chr(119)+chr(98)).write(base64.b64decode(sys.argv[2]))
print(chr(87)+chr(114)+chr(105)+chr(116)+chr(116)+chr(101)+chr(110)+chr(58), p)
