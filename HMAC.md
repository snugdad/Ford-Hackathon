#HMAC

	Key Reading Python 3.7 hashlib, secrets
	https://docs.python.org/3/library/hmac.html


>A message authentication code (MAC) is produced from a message and a secret key by a MAC algorithm. An important property of a MAC is that it is impossible¹ to produce the MAC of a message and a secret key without knowing the secret key. A MAC of the same message produced by a different key looks unrelated. Even knowing the MAC of other messages does not help in computing the MAC of a new message.

>An HMAC is a MAC which is based on a hash function. The basic idea is to concatenate the key and the message, and hash them together. Since it is impossible, given a cryptographic hash, to find out what it is the hash of, knowing the hash (or even a collection of such hashes) does not make it possible to find the key. The basic idea doesn't quite work out, in part because of length extension attacks, so the actual HMAC construction is a little more complicated. For more information, browse the hmac tag on Cryptography Stack Exchange, especially Why is H(k||x) not a secure MAC construction?, Is H(k||length||x) a secure MAC construction? and HMAC vs MAC functions. There are other ways to define a MAC, for example MAC algorithms based on block ciphers such as CMAC.

>A MAC authenticates a message. If Alice sees a message and a MAC and knows the associated secret key, she can verify that the MAC was produced by a principal that knows the key by doing the MAC computation herself. Therefore, if a message comes with a correct MAC attached, it means this message was seen by a holder of the secret key at some point. A MAC is a signature based on a secret key, providing similar assurances to a signature scheme based on public-key cryptography such as RSA-based schemes where the signature must have been produced by a principal in possession of the private key.

>For example, suppose Alice keeps her secret key to herself and only ever uses it to compute MACs of messages that she stores on a cloud server or other unreliable storage media. If she later reads back a message and sees a correct MAC attached to it, she knows that this is one of the messages that she stored in the past.

>An HMAC by itself does not provide message integrity. It can be one of the components in a protocol that provides integrity. For example, suppose that Alice stores successive versions of multiple files on an unreliable media, together with their MACs. (Again we assume that only Alice knows the secret key.) If she reads back a file with a correct MAC, she knows that what she read back is some previous version of some file she stored. An attacker in control of the storage media could still return older versions of the file, or a different file. One possible way to provide storage integrity in this scenario would be to include the file name and a version number as part of the data whose MAC is computed; Alice would need to remember the latest version number of each file so as to verify that she is not given stale data. Another way to ensure integrity would be for Alice to remember the MAC of each file (but then a hash would do just as well in this particular scenario).

	Our HMAC will be generated as follows:
		All data will be appended with the following:
	For simplicity we are limiting the number of digits to two: 2 digit device Id, 2 digit OS Id, 2 digit kirby_client version, followed by 2 digit app_id 2 digit app_version 2 digit user_id, 2 digit user_secret for a total of 14 numeric characters separated by . for a total of a 20 character string appended to each file's data when it is sent for hmac verification

>For each app version that is installed:
*	The 

