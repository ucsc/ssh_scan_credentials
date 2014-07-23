ssh\_scan\_credentials
====================

used to test ssh access, using credentials provided from input, and reading from a file.

This script is used to scan through a given list of hosts.  The assumption is that the hosts have FQDN.

It will test to make sure that systems on the list have the user 'secscan1' authorized.  It will do this by using the third-party paraminko ssh library.  Depending on the error that it recieves after it attempts to get the time on the remote system, the script will determine whether it has access, or what went wrong.

The library uses threads to expediate the process.  Make sure your machine can handle the load given the size of the list.

The output of the script is up_servers.txt

