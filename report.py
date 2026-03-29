def rep():
    name=input("Enter the name:")
    voteid=input("Enter the voteid:")
    consti=input("Enter the Constituency:")
    data={"Name":name,
          "voteid":voteid,
          "Constituency":consti}
    print("Name:",data["Name"]+"\n"+"voteid:",data["voteid"]+"\n"+"Constituency:",data["Constituency"])
    return()
