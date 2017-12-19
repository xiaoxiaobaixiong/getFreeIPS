from getFreeIPS.model import session, IP


'''
num is the ip's count that you want
'''
def getfreeip(num):
    return session.query(IP).all()[1:num]