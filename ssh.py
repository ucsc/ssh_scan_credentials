## Totally stole all of this: 
# http://stackoverflow.com/questions/20472288/python-ssh-password-auth-no-external-libraries-or-public-private-keys
#!/usr/bin/python

import sys, pdb, getpass
from socket import gaierror, error, timeout
import threading
import os.path
import exceptions
sys.path.append('./paramiko/lib-12.04/sites-packages/')
import paramiko
import ecdsa

COMMAND='hostname; uptime'
USER='secscan1'
PASSWORD = getpass.getpass("Enter password for SSH systems:")
up = open("up_servers.txt",'w')

def scan_ssh(HOST):
  try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #print('*** Connecting to: %s ***' % HOST)
    client.connect(hostname=HOST, port=22, username=USER, password=PASSWORD,timeout=5)
    up.write("HOST: %s UP\n" % HOST)
    #chan = client.invoke_shell()
    #stdout = client.exec_command(COMMAND)
    #chan.close()
    client.close()

  except gaierror as e:
    #print('%s: Caught exception: %s: %s *** ' % (HOST,e.__class__, e))
    if (e[0] == 8):
      up.write("HOST: %s DNSINACTIVE\n" % HOST)
    else:
      up.write("HOST: %s :UNCAUGHT EXCEPT: %s\n" % (HOST,e))
  
  except paramiko.AuthenticationException as e:
    #print('%s: Caught exception: %s: %s *** ' % (HOST,e.__class__, e))
    up.write("HOST: %s AUTHFAIL\n" % HOST)

  except timeout as e:
    #print('%s: Caught exception: %s: %s *** ' % (HOST,e.__class__, e))
    up.write("HOST: %s PORTBLOCKED\n" % HOST)

  except error as e:
    #print('%s: Caught exception: %s: %s *** ' % (HOST,e.__class__, e))
    if (e[0] == 60):
      up.write("HOST: %s PORTBLOCKED\n" % HOST)
    else:
      up.write("HOST: %s :UNCAUGHT EXCEPT: %s\n" % (HOST,e))
  
  except exceptions.NotImplementedError:
      up.write("HOST: %s URANDMISSING\n" % HOST)
    

  except Exception as e:
    print('%s: Caught exception: %s: %s *** ' % (HOST,e.__class__, e))
    up.write("HOST: %s :UNCAUGHT EXCEPT: %s\n" % (HOST,e))
    try:
      client.close()
    except:
      pass
  return


def main():
  thread_list = []
  if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
    ssh_servers = open(sys.argv[1])
  else:
    print "File needs to be entered with command. File needs to be valid."
    exit(1)
  try:
    for line in ssh_servers:
      HOST = line.strip()
      t = threading.Thread(target=scan_ssh, args=(HOST,))
      t.start()
      thread_list.append(t)
  
    for t in thread_list:
      t.join()

  except Exception as e:
    print "File failed to open."

  up.close()
  ssh_servers.close()

main()
