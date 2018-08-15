#RESTful API

    There are 6 key CONSTRAINTS
        1.) Restful systems are client server and should be separate, allowed to evolve independently

        2.) REST API's are stateless, every call/transaction between the client and server contains all of the data it needs to complete the transaction

        3.) A cache, in our case the HMAC cache will be pertinent, but in any case can decrease the request overhead by handling large amounts of inbound and outbound calls

        4.) Uniform interface. In our case we will be perfecting the website, however our app's client gui would look just like its parent website, feeling and responding to a touch screen in an intuitive way that the user can be able to pick up and understand as well as a mouse and keyboard

        5.) These are layered systems: REST API's have architectural layers that work together to create a scalable, modular application(microservices approach)

        6.) The ability for code to be transmitted via the API for use within the application.

> RESTful systems are not constrained to a metadata format (XML) but can reture any format depending on CLIENT request. 

###API Library:

    Using python3 and the requests module, we can 
* Get a whole table
* Get information about a tuple in the table
* Add a tuple to the table
* Mark a tuple with indicative information (add a column) 
* Modify an existing tuple
