# Crypto ARB
Cryptocurrency Spread Checker Telegram Bot

Сканирует Binance и Bestchange на наличие арбитражных ситуаций, согласно настройкам и отсылает результат в Telegram бот
```python
    ###################### ------ CONFIG --------- ##################
    threshold = 1               # threshold in percents (float)
    volume = 200                # trade volume. ex: 0.01 or 2000
    base_cur = 'USDT'           # base currency. ex: BTC USDT LTC ETH
    revs = 200                  # count of positive reviews. ex: 500
    bc_cache = 60               # bestchange cache in seconds
    chat_id = '<chatID>'        # ChatId TG
    #################################################################
    
    bot = telebot.TeleBot('<TELEGRAM_BOT_TOKEN>');
```
