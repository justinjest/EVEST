# EVEST: EVE Station Trader

## So you wanna be space rich...

EVE Online is known for it's hard-working ~~victims~~ players. Folks that will gladly spend hundreds of hours hacking away on a spreadsheet that will make them .01 ISK more than the next capsuleer frantically refreshing buy orders.

It's no secret that mastering the market is the way to true pixel wealth in New Eden, but it's not easy.

Or at least it wasn't.

**Introducing EVEST: EVE Station Trader!**

EVEST monitors the market to let you know when an item in your chosen location is trading at a certain percentage below its usual price. When you're ready to make sweet ISK, you can generate a list of things currently trading lower than average. Log in, snap up the deals, and spin your pretty spaceships.

Meanwhile, EVEST is toiling away in the background, like your very own nullsec miner, trapped in a mixture of Stockholm syndrome and not knowing any better. When you're ready to cash out, run EVEST again, and it will let you know what's trading higher than usual--time to sell!

It's medium-term swing trading, the lazy way.

## Installing & Running EVEST

### In your terminal

After you have pulled the repo all you need to do is run `python3 ./src/main.py`.

### In docker

After you pull the repo you can instead run `docker compose run -rm evest` to keep your files in a docker container.

## Operation

### Preferences

When you run the file for the first time you will generate a preference file in ./data. This will enable you to set the range of items you want to look at, and limit your buy and sell orders to only items that are relevent to you.

### Menu Items

#### Update databases

Updates databases so you're always looking at the newest possible information. Running this command will update your historical information if it's older than 1 day old, and your live information if it's older than 15 minutes.

#### Produce order sheet

Returns a list of items to consider trading based on the criteria you set in your preferences.

#### Make Transactions

If you want to do some EVE-style paper trading, hit this button! An imaginary player will player will buy and sell the items that are on your current order sheet. Come back later to see if you've made a profit!

#### Update preferences

Allows you to update and fine-tune your preferences.

#### Quit

Quits the program. :'(
