from decouple import config

import pihole as ph
import telegram

from datetime import datetime
import pandas as pd
import pytz
import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def epocToDateTime(epoch):
    return datetime.fromtimestamp(int(epoch), tz=pytz.timezone(config('pihole_timezone')))


def xlabel(x, pos, df):
    date_time = df.index[pos]
    return date_time.strftime('%H:%M') if pos % 8 == 0 else ''


def createGraph(pihole_data):

    pihole_domains_queried = pihole_data['domains']
    pihole_ads_blocked = pihole_data['ads']

    # Domains Queried

    domains_queried_cnt = list(pihole_domains_queried.values())
    domains_queried_index = list(
        map(epocToDateTime, pihole_domains_queried.keys()))

    df_domains_queried = pd.DataFrame(domains_queried_cnt, columns=[
        "Queried"], index=domains_queried_index)

    # ADs Blocked

    ads_blocked_cnt = list(pihole_ads_blocked.values())
    ads_blocked_index = list(map(epocToDateTime, pihole_ads_blocked.keys()))

    df_ads_blocked = pd.DataFrame(ads_blocked_cnt, columns=[
        "Blocked"], index=ads_blocked_index)

    # Final DataFrame

    df_queried = df_domains_queried.join(df_ads_blocked)

    # Plot The Graph

    last_date_time = df_queried.index[len(
        df_queried.index) - 1].strftime('%Y-%m-%d %H:%M')
    title = f'Pihole Statistics For {last_date_time}'
    ax = df_queried.plot.bar(figsize=(20, 6), title=title, stacked=True, color={
                             "Blocked": "#ee6002", "Queried": "#5c00d2"})

    formatter = ticker.FuncFormatter(
        lambda x, pos: xlabel(x, pos, df_queried))
    ax.xaxis.set_major_formatter(formatter)

    plt.xticks(rotation='45')
    plt.gcf().autofmt_xdate()
    plt.savefig(config('pihole_graph_file'))


# Connect To PiHole
pihole = ph.PiHole(config('pihole_ip'))
pihole.authenticate(config('pihole_pass'))
pihole.refresh()

# Get PiHole Metrics
pihole_data = pihole.getGraphData()
pihole_status = pihole.status
pihole_queries = pihole.queries
pihole_blocked = pihole.blocked
pihole_ads_percentage = pihole.ads_percentage
pihole_top_devices = pihole.top_devices

# Create ADs Blocking Graph
createGraph(pihole_data)

# Setup Telegram Bot
bot = telegram.Bot(token=config('telegram_token'))

# Send Telegram Message
current_date = datetime.now().strftime('%Y-%m-%d')
pihole_stats = f'''
<b>PiHole Metrics</b> on {current_date}

• <b>Total Queries</b> {pihole_queries}
• <b>ADs Blocked</b> {pihole_blocked}
• <b>Percentage Blocked</b> {pihole_ads_percentage}%

'''

bot.send_message(text=pihole_stats, chat_id=config('telegram_chatid'),
                 parse_mode=telegram.ParseMode.HTML)
bot.send_photo(photo=open(config('pihole_graph_file'), 'rb'),
               chat_id=config('telegram_chatid'))

# Remove the Generated Image
os.remove(config('pihole_graph_file'))

