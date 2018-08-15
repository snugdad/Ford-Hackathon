"""
 Our client will feature the following specifications:
   0.) It will be the client in the client-server API model
   1.) It will connect with the fordappstore server Api and interface with this "parent" api
   2.) Each command that is run on the vehicle that interfaces with the internet and allows information to enter the system will be subject to validation via checksum of that information
   3.) All information passing into the system is parsed first at the server repository level
   4.) The client may not download information from any other source but 42king.fordappstore.com (This will be achieved via OAuth )
   5.) This API spec is a dumb client smart server model. All information about the vehicles systems and user credentials will be sent to the server and the server will decide the outcome of each request.
   6.) Due to 5, we will be able to store all client side information in plain-text caches(nothing needs to be secure on the vehicle)
   7.) On the subject of caches, this client API will have a plaintext cache of checksums representing every piece of information currently on the system.
   
   **Optional** 
   0.) all incoming packets are blocked (IPTABLES INPUT DROP?) unless the client requires internet access for download or stream. Otherwise, the client is a puppet of the server api, only able to authenticate it's request for information through the parent system.
"""

"""
Function schedule:
	All kirby_client functions start with the prefix kbc
	
	def kbc_getHmacCache(app_id):
		*   Gets every Sha256 HMAC for all source files related to the application specified by app_id
		from the server's cache of that applications valid Checksums (Since this is an HMAC there will be a session authentication that comes first to generate a valid key)
		* 	


"""
class Client:
	def __init__(self):
		pass

if __name__ == "__main__":
	'''
	loaded config = load config file
	client = Client(loaded config)
	while true:
		try client.connection:
			client.establish connection
		except Exception as err:
			handle(err)
		client.query(client started package={status, etc...})
		client.recieve({updated packages})
		install deps(client.packageList)
		prepare programs to launch
	'''
