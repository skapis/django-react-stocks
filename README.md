# Django-React Stock Tracker App
In this directory is a web application for stock tracking in React and Django Framework. For the backend is used Django Rest Framework and for the frontend ReactJS. For the authorization is used JWT Tokens. This application is similar to Stock Tracker App in this [directory](https://github.com/skapis/django_stockapp). Users can create one portfolio and add stocks, transactions and dividends records. Each user has to sign up then he can create one or more portfolios and add companies, transactions and dividends.


## Dashboard
The main page is a dashboard where users can see widgets with the current value of the portfolio, total portfolio value, and gain/loss number of companies in the portfolio. Under these widgets are two charts. The first chart shows the total portfolio value in time the second shows portfolio holdings.
At the bottom of the page is a table with aggregated holdings data. Here user can add a new company to his portfolio. In the selector in the navigation bar user can switch between his portfolios.

![Dashboard](https://github.com/skapis/appscreenshots/blob/main/Django_React_stocks/dashboard.png)

## Transactions
Another page is the transactions page. There is only a table with all transactions in the portfolio. Users can add a new transaction, edit or delete it.

![Transactions](https://github.com/skapis/appscreenshots/blob/main/Django_React_stocks/transactions.png)

## Dividends
On the dividends page are also widgets and charts. Users can see total expected dividends, received dividends and dividend yields. Users can also add, edit or delete dividend records.

![Dividends](https://github.com/skapis/appscreenshots/blob/main/Django_React_stocks/dividends.png)

## User Profile
On the user profile page, the user can edit the name, create a new portfolio or delete an existing one.

![Account](https://github.com/skapis/appscreenshots/blob/main/Django_React_stocks/profile.png)

