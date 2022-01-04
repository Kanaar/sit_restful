# Installation:

clone the repo:
```bash
git@github.com:Kanaar/sit_restful.git
```

Install dependencies:
```bash
pip: -r requirements.txt
```

Setup database:
```bash
make dbreset
```

# Usage:

<ins>Preparing</ins><br>
The file `seeds.py` includes seeds with `groups_of_users` as per assignment description. A `group_of_users` was translated into instances of Order and `groups_of_users` as an OrderQueryset. Feel free to play around and change the size of orders, rows and seats (please note the Rank allocation based on row index). It is user tested and should all work well for different sets of data.<br>
<br>
Since the algorithm creates intances of tickets the database need to be flushed of those to re-run the algorithm. For simplicity you can flush and re-seed the database with the command `make dbrefresh`<br>
<br>
<ins>Execution</ins><br>
Ther are two algorithms available, the simple and advanced. These can be found in `api_seating.services`<br>
<br>
Simple: `SimpleSeatingService`
Improved: `GroupSeatingService`<br>
<br>
The algorithms can be executed with the command `make demo` and will print out the results of the rows as
a list of querysets. For the improved algorithm a verbose call option is available that prints the matrix at every change so the course of actions can be followed. <br>
<br>
The 'currently active' algorithm is the simple one, different algorithms can be set to active by commenting/uncommenting lines of code in the `demo.py` file. Don't forget to refresh the database between runs. <br>
<br>
The `GroupSeatingService(orders, n_front, n_back)` takes two extra arguments. These are parameters to define the number of attempts are made to keep a group together by moving them a row further (n_front). If that is not succesful, to define the max number of orders before the current order (n_back) can squeeze out. Please note that n_front moves forward in the iterations and n_back refers to backtracking interations. In reality n_front comes down to the order being placed further to the back of the section and n_back in reality moves the current order 'back' over the already filled seats to a row closer to the front of the section. <br>
If moving the order upward or backtracking downward will not place the group together at the current parameters, the group will be wrapped such as in the simple algorithm.
<br>

# API:

run a local server: `make s` <br>
<br>
Determine for what `order_id` the ticket information needs to be retrieved.<br>
Ticket wallet endpoint: `http://127.0.0.1:8000/orders/order_id`<br>


# Suggestions for refactoring:
- Not creating and deleting Ticket instances but collecting the information in a dict or dataframe first and creating all Tickets in the end when the final layout is clear could improve performance and reduce the risk of 'ghost' instances.
- Include simple logic to avoid an order be split among more than two rows (e.g. this risk exists when filling the final seats)
- Keen to discuss more :)

# Suggestions for further development:
- unit testing / set up a CD/CI pipeline
- validation methods
- model creation for Venue and Event to allow for scaling (current API contains 1-Venue 1-Event logic)
- Turn it into a multi-tenancy app to allow for organisations with multiple Venues
- I would have loved to build a consumer with a fancy UX but hopefully I get to work on the real thing.
- For frond-end `Section.curve = models.IntegerField()` that stores the curve degrees instead of a `Boolean` could open up some design features
- Include aisle preference in seating algorithm
