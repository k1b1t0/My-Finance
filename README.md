# MY FINANCE
#### Video Demo: https://youtu.be/9cNht7hs34Q?si=bxLFWBxNAbx740nw
#### Description:
This is a web application using Python, SQL, Flask... to manage money.
In the past, i had priblems managin my spending, I wanted to separated my money into many funds but there weren't many apps help me doing it and I was not good enough in Excel to solve that problem. So after a read about final project, I came up with this idea of a web app helps me solve that problem.
There are 5 main parts in this project corresponding to 5 pages: "Login/register", "Homepage", "Add fund", "Update", "History"
#### What is in the files:
- Folder "flask_session" to store sessions from Flask
- Folder "static" store some CSS
- Folder "templates" store html files which I used to run the pages
    - addfund.html, history.html, index.html, login.html, register.html, update.html just like the names
    - apology.html is the page where show the apology (or error)
    - layout.html is the layout of every pages (the name of the web, the navigator...)
- app.py are the main python code of the web app, with some functions form the helpers.py
- finance.db is the database of the app, where we store every information we need and to queue it using SQL
#### Ideas:
##### Login/register
- The login page will (logout and) input username and password and checking information if the account is existed
- The register page input username, password and confirmation to create new account
- It will have to check
    1. if the username is already taken
    2. if the confirmation is wrong
- After register, it will direct the user to login page again, to login their account
- Finance is a sensitive issue so information security is very important
##### Add fund
- This is where I used to create more funds to split my money
- I will input a name and a initial amount for this new fund, but I have to check if the name is already taken
- If there are no fund with the same name I can create this new fund by adding it to the database
##### Update
- This is where I record my daily transactions
- You cannot spend more than you can afford, so the money spent can't exceed the money in the fund, which I have to check
- I would like to record the amount, reason, category, time and the fund which I used to purchase
##### Homepage
- Homepage is the first page I see when coming to the web
- It will shows all my funds and the money in there, which gave me an overview of my money
##### History
- History is where I can see all the history of my purchasing
- Where I re-thinking of my purchases, so I need time and category

#### How i did:
##### Login/register
- I used a table in finance.db names "users" with id | username | hash to store users's datas (hash not password)
- To check if the login information is correct, I iterate the table and check if there is an user with the same name and same hashed password
- When getting a new registration, I iterate the table to see if there are any user with same name before, then I check the confirmation
- login.html used layout.html for layout, then it input username and password in method "POST"
- register.html also used layout.html, it input username, password and confirmation
##### Add fund
- addfund.html will input a text for name and a number for initial positive amount in method "POST"
- I used table "funds" (id | ID_user | name | amount) to store funds
- I will check if there is an existed fund that has same name and ID_user. If not, I can add the new fund to the tables where the ID_user is the session["user_id"]
##### Update
- update.html used layout.html for layout
- I created "purchases" table, which will store every valid transactions
- It includes id | ID_user | amount | ID_ctg | detail | ID_fund | time
- I used "update.html" to get inputs (amount, category, detail, fund), then check if the transaction is valid or not.
- If the transaction is valid, i will add it into the table where ID_user is the session["user_id"]
- I also used a "categories" table (id | name) to store category
- After added the transaction I will update the amount of the fund with ID_fund
##### Homepage
- homepage.html used layout.html for layout
- I queue in funds and find all the funds by ID_user
- Then I showed it to the page using table funds | amount
##### History
- history.html used layout.html for layout
- I queue in purchases, find all the transactions by ID_user
- Then I showed it to the page using table time | amount | category | detail | fund

