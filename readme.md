# EVEST: EVE Station Trader

## So you wanna be space rich...

EVE Online is known for it's hard-working ~~victims~~ players. Folks that will gladly spend hundreds of hours hacking away on a spreadsheet that will make them .01 ISK more than the next capsuleer frantically refreshing buy orders.

It's no secret that mastering the market is the way to true pixel wealth in New Eden, but it's not easy.

Or at least it wasn't.

**Introducing EVEST: EVE Station Trader!**

EVEST monitors the market to let you know when an item in your chosen location is trading at a certain percentage below its usual price. When you feel like it you can generate a buy and sell list, log in, take a peek at the item, and maybe set up an order for it.

Meanwhile, EVEST is toiling away in the background, like your very own nullsec miner, trapped in a mixture of Stockholm syndrome and not knowing any better. When you come back to check if your items is selling at a higher-than-average price, you get another sell list: Time to sell!

It's medium-term swing trading, the lazy way.

## Installing & Running EVEST

### In your terminal

After you have pulled the repo all you need to do is run ```python3 ./src/main.py```.

### In docker

After you pull the repo you can instead run ```docker compose run -rm evest``` to keep your files in a docker container.

## Operation

### Preferences

When you run the file for the first time you will generate a preference file in ./data. This will enable you to set the range of items you want to look at, and limit your buy and sell orders to only items that are relevent to you.

#### Station

EVEST currently supports the 3 largest markets in EVE, Jita, Dodixie, and Amarr VIII

#### Time period

This is the average of the historical database that you care about, all price comparisons will be over the average of this period. 

#### Market Size

This will limit the items to only items that have this volume of trading. Market size is price * items traded over the time period you select

#### Market Volume

The minimum number of items moved over the time period you selected

#### Taxes

These are the fees that our simulated agent will pay when they make a transaction. At max skills they are:
sales tax:       1.0
buy broker fee:  3.3 
sell broker fee: 3.3

### REPL functions 

#### Update databases

Updates databases if it has been at least 1 day for your historical database and at least 15 minutes for your live database

#### Produce order sheet

Returns a list of item names to consider buying with your preferences

#### Make Transactions

Your player will buy and sell the items that are on your current order sheet

#### Update preferences

Allows you to update your preferences

#### Quit

Quits the program
