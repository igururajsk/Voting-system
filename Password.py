'''
import random 
import array
from password_generator import PasswordGenerator

# maximum length of password needed 
# this can be changed to suit your password length 
def passw():
      

      pwo = PasswordGenerator()
      passw=pwo.generate()
      print(passw)
      return passw
'''
import string
from random import *
def passw():
      characters = string.ascii_letters + string.punctuation  + string.digits
      passw =  "".join(choice(characters) for x in range(randint(8, 16)))
      print (passw)
      return passw
