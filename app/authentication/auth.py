import bcrypt

class Authentication:
    def __init__(self):
        pass


    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password


    def check_password(self, hashed_password, input_password):
        return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)




#---------------------------------------------------------------------------------------------------



user = Authentication()


password = "password123"
hashed_password = user.hash_password(password)



input_password = "password000"
if user.check_password(hashed_password, input_password):
    print("Password is correct :)")
else:
    print("Password is incorrect ! :(")



