from bestchange_api import BestChange
from binance.spot import Spot
import json
import telebot;

currs = {
    "USDT" : 208,    # SOL 180, ERC20 36, TRC20 10, BEP20 208
    "BTC" : 43,
    "ETH" : 139,
    "ETC" : 160,
    "LTC" : 99,
    "LUNA": 2,
    "OMG" : 48,
    "BAT" : 61,
    "NEAR": 76,
    "SOL" : 82,
    "DOGE": 115,
    "XVG" : 124,
    "KMD" : 134,
    "ONT" : 135,
    "MATIC":138,
    "DASH": 140,
    "XMR" : 149,
    "XRP" : 161,
    "ZEC" : 162,
    "ZRX" : 168,
    "BCH" : 172,
    "XEM" : 173,
    "XTZ" : 175,
    "NEO" : 177,
    "EOS" : 178,
    "IOTA": 179,
    "ADA" : 181,
    "XLM" : 182,
    "BTG" : 184,
    "TRX" : 185,
    "VET" : 8,
    "QTUM": 26,
    "BTT" : 27,
    "LINK": 197,
    "ATOM": 198,
    "DOT" : 201,
    "UNI" : 202,
    "RVN" : 205,
    "MKR" : 213,
    "ALGO": 216,
    "AVAX": 217,
    "YFI" : 220,
    "MANA": 227
}

def bin(in_curr,out_curr,depth=1000):
    client = Spot()
    pair = out_curr+in_curr
    resp = client.depth(pair,limit=10)
    data = json.loads(json.dumps(resp))
    full_d = 0
    for i in data['asks']:
        d = float(i[1])*float(i[0])
        full_d = full_d + d
        if full_d > depth:
            return i[0]
            break

def bc(in_curr,out_curr,depth=100, reviews=500, bccache=300):
    api = BestChange(exchangers_reviews=True, split_reviews=True, cache_seconds=bccache)
    exchangers = api.exchangers().get()
    iin_curr = currs[in_curr]
    iout_curr = currs[out_curr]
    dir_from = iin_curr
    dir_to = iout_curr
    rows = api.rates().filter(dir_from, dir_to)
    res_ex = {}
    for val in rows:
        get = float(val['get']) / float(val['give'])
        res_d = float(val['reserve'])
        max_d = float(val['max_sum'])*get
        min_d = float(val['min_sum'])*get
        if (res_d > depth) and (max_d > depth) and (depth > min_d) and (int(val['reviews'][1]) > reviews) and (int(val['reviews'][0]) < 1):
            exname = exchangers[val['exchange_id']]['name']
            res_ex[exname] = { 'rate' : get, 'reserve' : res_d, 'max': max_d, 'exid' : val['exchange_id']}
    max_rate = 0
    max_ex = {}
    for i in res_ex:
        curr_rate = float(res_ex[i]['rate'])
        if curr_rate > max_rate:
            max_ex = res_ex[i]
            max_ex['name'] = i
            max_rate = curr_rate
    return max_ex


def tst(p1, p2):
    api = BestChange(exchangers_reviews=True, split_reviews=True, cache_seconds=300)
    exchangers = api.exchangers().get()
    dir_from = currs[p1]
    dir_to = currs[p2]
    rows = api.rates().filter(dir_from, dir_to)
    for val in rows[:1]:
        print('{} : {} {} {} {}'.format(api.currencies().get_by_id(dir_from), api.currencies().get_by_id(dir_to), val['reviews'][1], exchangers[val['exchange_id']]['name'], val))

if __name__ == '__main__':

    ###################### ------ CONFIG --------- ##################
    threshold = 1               # threshold in percents (float)
    volume = 200                # trade volume. ex: 0.01 or 2000
    base_cur = 'USDT'           # base currency. ex: BTC USDT LTC ETH
    revs = 200                  # count of positive reviews. ex: 500
    bc_cache = 60               # bestchange cache in seconds
    chat_id = '<ChanID>'       # ChatId TG
    #################################################################

    bot = telebot.TeleBot('<TELEGRAM_BOT_TOKEN>');


#    @bot.message_handler(content_types=['text'])
#    def get_text_messages(message):
#        bot.send_message(message.from_user.id, "Привет, текущие настройки: Базовая валюта "+base_cur+", объём торгов "+str(volume)+" "+base_cur+", кэш "+ str(bc_cache)+" сек., необходимо положительных отзывов "+str(revs)+", пороговое значение прибыли "+ str(threshold)+"%")


#    bot.polling(none_stop=True, interval=0)


    dd = float(volume)
    bot.send_message(chat_id, "Бот стартанул")
    while True:
        for i in currs:
            if not(i == base_cur):
                p1 = i
                p2 = base_cur
    #            tst(p1, p2)
                try:
                    bc_dict = bc(p1,p2, depth=dd, reviews=revs, bccache=bc_cache)
                    bin_rate = bin(p2,p1,depth=dd)
                    bc_rate = float(bc_dict['rate'])
                    bc_name = bc_dict['name']
                    perc = round(float((float(dd)/float(bin_rate) * float(bc_rate))/float(dd)*100 - 100 ),2)
                    perc_str = str(perc)+'%'
                    print(perc_str)
                    if (perc > threshold):
                        instructions='PAIR: '+p1+p2+'  BINANCE: '+str(bin_rate)+'  BESTCHANGE: '+str(bc_rate)+' by '+str(bc_name)+'  PROFIT FROM '+str(dd)+' '+p2+': '+perc_str+'\nBUY '+str(float(dd/float(bin_rate)))+' '+str(p1)+', you will receive '+str(float(dd/float(bin_rate)*bc_rate))+' '+str(p2)
                        print('--------------------------------------')
                        #print('PAIR: '+p1+p2+'  BINANCE: '+str(bin_rate)+'  BESTCHANGE: '+str(bc_rate)+' by '+str(bc_name)+'  PROFIT FROM '+str(dd)+' '+p2+': '+perc_str)
                        #print('BUY '+str(float(dd/float(bin_rate)))+' '+str(p1)+', you will receive '+str(float(dd/float(bin_rate)*bc_rate))+' '+str(p2))
                        print(instructions)
                        bot.send_message(chat_id,instructions)
                except:
                    pass
