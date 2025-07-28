![EVEST: EVE Station Trader logo](/static/evest-logo.webp)

<!-- badges: start -->

[![GitHub License](https://badgen.net/github/license/justinjest/EVEST)](https://github.com/justinjest/EVEST/licence.md)
![Built for Boot.dev Hackathon](https://img.shields.io/badge/built%20for-Boot.dev%20Hackathon-blueviolet)

<!-- badges: end -->

## So you wanna be space rich...

EVE Online is known for it's hard-working ~~victims~~ players. Folks that will gladly spend hundreds of hours hacking away on a spreadsheet that will make them .01 ISK more than the next capsuleer frantically refreshing buy orders.

It's no secret that mastering the market is the way to true pixel wealth in New Eden, but it's not easy.

Or at least it wasn't.

## Introducing EVEST: EVE Station Trader

EVEST monitors the market to let you know when an item in your chosen location is trading at a certain percentage below its usual price. When you're ready to make sweet ISK, you can generate a list of things currently trading lower than average. Log in, snap up the deals, and spin your pretty spaceships.

Meanwhile, EVEST is toiling away in the background, like your very own nullsec miner, trapped in a mixture of Stockholm syndrome and not knowing any better. When you're ready to cash out, run EVEST again, and it will let you know what's trading higher than usual--time to sell!

It's medium-term swing trading, the lazy way.

## See it in action:

https://github.com/justinjest/EVEST/blob/main/static/evest-demo.mp4

## Installing EVEST

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/justinjest/EVEST
   ```

2. **Navigate to the Project**:

   ```bash
   cd EVEST
   ```

3. **Install Required Dependencies**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Using EVEST

To start the program, run:

```bash
python3 ./src/main.py
```

### Preferences

When you run the file for the first time you will generate a preference file in ./data. This will enable you to set the range of items you want to look at, and limit your buy and sell orders to only items that are relevent to you.

For a reasonable set of defaults you can use:

- Station: 1
- time = Quarter
- market_size = 1500000000
- market_volume = 1200
- tax = 3.5
- buy brokerage fee = 1.5
- sell brokerage fee = 1.5

### Menu Items

- **Update databases**

> Updates databases so you're always looking at the newest possible information. Running this command will update your historical information if it's older than 1 day old, and your live information if it's older than 15 minutes.

- Display market opportunities

> Returns a list of items to consider trading based on the criteria you set in your preferences. You can copy these and paste them straight into your in-game market quickbar!

- Make transactions

> If you want to do some EVE-style paper trading, hit this button! An imaginary player will player will buy and sell the items that are on your current order sheet. Come back later to see if you've made a profit!

- Update preferences

> Allows you to update and fine-tune your preferences.

- Quit

> ... do we need to explain?

## Contributing

- **Clone the repo**

- **Submit a pull request**

If you'd like to contribute, please fork the repository and open a pull request to the `main` branch. If you have a request please submit an issue report on github.
