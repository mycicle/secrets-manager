from Crypt import Crypt
from KeyGen import KeyGen

def main():

    key_generator = KeyGen(input("Please input your user password for initialization "))
    print(key_generator.hashed_password)
    print(key_generator.salt)
    print(key_generator.key)

    crypt = Crypt(key_generator.key)

    message_to_encrypt = "Message 1234$%^"
    print(message_to_encrypt)
    print(crypt.encrypt(message_to_encrypt))
    print(crypt.decrypt(crypt.encrypt(message_to_encrypt)))

if __name__ == "__main__":
    main()