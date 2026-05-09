n=input("Enter Password")
copy=n
def password(n,q):
    k=input("Enter Password")
    if k==n:
        print("Login Successfully")
    else:
        print("\n Password try again")
        q=q+1
        if q<3:
            password(n,q)
        elif q==3:
            print("You have entered password to max limit... Please again")
        else:
            print("Invalide input please check entered password")
password(n,0)