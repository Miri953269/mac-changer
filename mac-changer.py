import random,subprocess,optparse

from sympy import false

print("""
███╗   ███╗ █████╗  ██████╗     ██████╗██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███████╗██████╗ 
████╗ ████║██╔══██╗██╔════╝    ██╔════╝██║  ██║██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔══██╗
██╔████╔██║███████║██║         ██║     ███████║███████║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝
██║╚██╔╝██║██╔══██║██║         ██║     ██╔══██║██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗
██║ ╚═╝ ██║██║  ██║╚██████╗    ╚██████╗██║  ██║██║  ██║██║ ╚████║╚██████╔╝███████╗██║  ██║
╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                    ~by Agazade Mirabbas
""")

period=0

def inputs():
    t=optparse.OptionParser()
    t.add_option("-I","--interface",dest="interface",help="Add your interface")
    t.add_option("-T","--time",dest="time",help="Choose how often the Mac address will change. In hours, minutes or seconds, for example: 1h, 3m, 10s (Optional)")
    t.add_option("-M","--mac",dest="mac",help="Enter the mac address you want to obtain. If you are going to use the time option, or if you want to change the mac address randomly, just add r in front of the mac option")
    return t.parse_args()

def random_mac_generator():
    mac_address_random=""
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, "a", "b", "c", "d", "e", "f"]
    b = [1, 2, 3, 4, 5, 6, 7, 8, 9, "a", "b", "c", "d", "e", "f"]
    for i in range(0,6):
        if i==0:
            c=[]
            for j in range(1,15,2):
                 k=b[j]
                 c.append(k)
            else:
                b=c
        else:
            b=a
        num = str(random.choice(a)) + str(random.choice(b))
        mac_address_random+=num
        if i==5:
            break
        else:
            mac_address_random+=":"
    return mac_address_random

def check_mac(mac):
    check = subprocess.check_output("ifconfig | grep ether | awk '{print $2}'", shell=True).decode().strip()
    if mac==check:
        print("Your Mac address has been successfully changed.")
        print(f"Mac address - {mac}")

def control(interface,time,mac):
    if not interface:
        interface=input("Please add your interface: ")
    if not time:
        time="0s"
    if not mac:
        if time!="0s":
            mac="r"
        else:
            mac = input("Please add the mac address, or you can type r and the mac address will be chosen randomly: ")
    return interface,time,mac
(user_input,args)=inputs()
i,t,m=control(user_input.interface,user_input.time,user_input.mac)
try:
    if t[-1] not in ['s','S','m','M','h','H']:
        print("This is not a valid time value!")
        exit()
    else:
        if t[1]=='h' or t[1]=='H':
            t=int(t[0:-1])*3600
        elif t[1]=='m' or t[1]=='M':
            t=int(t[0:-1])*60
        else:
            t=int(t[0:-1])
except ValueError:
    print("This is not a valid time value!")
    exit()
def change_mac(selected_interface,mac_address):
    subprocess.call(["ifconfig", selected_interface, "down"])
    subprocess.call(["ifconfig", selected_interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", selected_interface, "up"])
q=false
if t==0:
    if m=="r" or m=="R":
        n=random_mac_generator()
        change_mac(i,n)
        check_mac(n)
    else:
        change_mac(i,m)
        check_mac(m)
else:
    if m not in {"r","R"}:
        query=input("If the time option is used, the mac should be selected randomly, do you agree?(Y/n): ")
        if query=="Y" or query=="y":
            m="r"
        elif query=="N" or query=="n":
            exit()
        else:
            print("Invalid input!")
            exit()
    print("Press Ctrl+C to exit")
    try:
        while q == false:
            n = random_mac_generator()
            change_mac(i, n)
            check_mac(n)
            t = str(t)
            subprocess.call(["sleep", t])
    except KeyboardInterrupt:
        print("\nScript manually stopped")
        exit()
