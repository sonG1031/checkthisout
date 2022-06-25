import random
import string


lower = string.ascii_lowercase
upper = string.ascii_uppercase
num = string.digits
symbols = string.punctuation

all = lower + upper + num + symbols

tmp = random.sample(all, 15)
code = r"".join(tmp)


print(code)