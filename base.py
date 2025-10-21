
import pandas as pd
card = pd.read_excel('刷卡数据.xlsx')        
weather = pd.read_csv('攀枝花2023-2024年历史天气.csv')
card.columns = card.columns.str.strip()          
card['deal_time'] = pd.to_datetime(card['消费时间'])
card['date'] = card['deal_time'].dt.date
card['hour']  = card['deal_time'].dt.hour
card['minute'] = card['deal_time'].dt.minute
card['weekday'] = card['deal_time'].dt.weekday         
weather['date'] = pd.to_datetime(weather['日期']).dt.date
morning_peak = card[
    (card['weekday'] < 5) &
    (
        ((card['hour'] == 7) & (card['minute'] >= 30)) |
        (card['hour'] == 8) |
        ((card['hour'] == 9) & (card['minute'] == 0))
    )
].copy()
top20 = (
    morning_peak.groupby('线路')['卡号']
    .count()
    .sort_values(ascending=False)
    .head(20)
    .reset_index(name='boardings')
)
top20.to_csv('top20_am_peak.csv', index=False, encoding='utf-8-sig')
peak_day_line = (
    morning_peak.groupby(['date', '线路'])['卡号']
    .count()
    .reset_index(name='boardings')
)
weather_peak = peak_day_line.merge(
    weather[['date', '天气状态', '最低温（℃）', '最高温（℃）']],
    on='date', how='left'
)
weather_peak.to_csv('target.csv', index=False, encoding='utf-8-sig')

