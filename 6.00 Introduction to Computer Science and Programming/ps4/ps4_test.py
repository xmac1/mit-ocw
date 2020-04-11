from ps4 import *

text = 'Androids'
cipher_text = apply_shift(text, 18)
print cipher_text


text = find_best_shift(wordlist, cipher_text)
print text


print apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])

s = '01234567'
print s[:]
