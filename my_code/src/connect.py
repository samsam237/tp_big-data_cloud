from pyVim import connect
from pyVmomi import vim
import ssl

def simple_connect (host='vcsa', user='my_user', pwd='my_password', port=443):
    context = ssl._create_unverified_context() 
    si = connect.SmartConnect(
        host=host,
        user=user,
        pwd=pwd,
        port=port,
        sslContext=context
    ) # smartConnect will prevent failures and use ssl certificate
    return si

def disconnect(si):
    try:
        if si:
            connect.Disconnect(si)
            print("Deconnection avec succes")
    except Exception as e:
        print(f"Erreurr lors de la déconnection: {e}")