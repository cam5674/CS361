# This program prints a text-based menu in the console for the user to interact with. All user information(favorite stocks/username) is saved in the storage.json file. A user can search stocks and save/add stocks to their profile.

This program includes three microservices: email confirmation, stock news, and stock deletion. Each microservice uses ZMQ as the communication pipeline.

 - **Email Confirmation Microservice**: This microservice processes a request containing the user’s email as a string and sends a confirmation email to the provided address.

 - **Stock News Microservice**: This microservice processes a list of stocks and returns links to relevant news articles for each stock. 

 - **Stock Deletion Microservice**: This microservice sends a request formatted as follows: {username: nameofuser, stock: stocktobedelete}. It then deletes the specified stock and updates the user profile.
 
WARNING: For the stocks program to work you need an api key from tiingo. The cred file contains my personal key. IF you would like to use this program, you will need to get a key from tiingo, create a module named cred and write your key in the program, like this: key = "7777777777". Then you can import it to this module.
