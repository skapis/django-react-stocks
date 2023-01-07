# Django-React Stock Tracker App
In this directory is web application for stock tracking in React and Django Framework. For the backend is used Django Rest Framework and for the frontend is used ReactJS. For the authorization of user are used JWT Tokens. This application is similar to Stock Tracker App in this [directory](https://github.com/skapis/django_stockapp) In app user can create one portfolio, add stocks, transactions and dividends records. Each user has to sign up then he can create one or more portfolios and add companies, transactions and dividends.


## Dashboard
Main page is dashboard, where user can see widgets with current value of portfolio, total portfolio value, gain/loss and how many companies are in portfolio. Under the widgets are two charts. First chart shows total portfolio value in time and the second shows portfolio holdings.
At the bottom of the page is table with holdings with aggregated data of holdings. Here user can add new company to his portfolio. In the selector in navigation bar user can swith between his portfolios.

![Dashboard](https://github.com/skapis/appscreenshots/blob/main/Django_React_stocks/dashboard.png)

## Transactions
Another page is transactions page, where is only table with all transactions in portfolio. User can add new transaction, get detail, edit transaction or delete it.

![Transactions](https://github.com/skapis/appscreenshots/blob/main/Django_React_stocks/transactions.png)

## Dividends
On the dividends page is also widgets and charts. User can see how much dividends will he receive, how much he received yet and dividend yields. User can also add, edit or delete dividend records.

![Dividends](https://github.com/skapis/appscreenshots/blob/main/Django_React_stocks/dividends.png)

## User Profile
In user profile page, user can edit name of portfolio, create new portfolio or delete existing.

![Account](https://github.com/skapis/appscreenshots/blob/main/Django_React_stocks/profile.png)

