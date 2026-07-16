import random
comp = random.choice(["qogoz","qaychi","tosh"])
user = input("(tosh/qaychi/qogoz: )")
if comp == user:
    print("durrang")
elif    (comp == "qogoz" and user =="qaychi") or (comp =="qaychi" and user =="tosh") or (comp =="tosh" and user =="qogoz"):
            print("yutdingiz...")
            print(f"kompeyuter {comp} ni tanlagan edi")
else:
    print("yutqazding...")
    print(f"kompeyuter {comp} ni tanlagan edi")