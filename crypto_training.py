import pandas as pd

FUTURE_PERIOD_PREDICT = 3  # how far into the future are we trying to predict?
RATIO_TO_PREDICT = "LTC-USD"

# classification function that we'll use to map in a moment
def classify(current, future):
    if float(future) > float(current):
        return 1
    else:
        return 0

# import initialize dataset
df = pd.read_csv("data/LTC-USD.csv", names=['time', 'low', 'high', 'open', 'close', 'volume'])

# begin empty
main_df = pd.DataFrame() 

# the 4 ratios we want to consider
ratios = ["BTC-USD", "LTC-USD", "BCH-USD", "ETH-USD"]  
for ratio in ratios:  # begin iteration
    print(ratio)
    dataset = f'data/{ratio}.csv'  # get the full path to the file.
    df = pd.read_csv(dataset, names=['time', 'low', 'high', 'open', 'close', 'volume'])  # read in specific file

    # rename volume and close to include the ticker so we can still which close/volume is which:
    df.rename(columns={"close": f"{ratio}_close", "volume": f"{ratio}_volume"}, inplace=True)

    df.set_index("time", inplace=True)  # set time as index so we can join them on this shared time
    df = df[[f"{ratio}_close", f"{ratio}_volume"]]  # ignore the other columns besides price and volume

    if len(main_df)==0:  # if the dataframe is empty
        main_df = df  # then it's just the current df
    else:  # otherwise, join this data to the main one
        main_df = main_df.join(df)

main_df.fillna(method="ffill", inplace=True)  # if there are gaps in data, use previously known values
main_df.dropna(inplace=True)

# If the "future" column is higher, great, it's a 1 (buy). Otherwise it's a 0 (sell)
main_df['future'] = main_df[f'{RATIO_TO_PREDICT}_close'].shift(-FUTURE_PERIOD_PREDICT)

# will just shift the columns for us, a negative shift will shift them "up."
main_df['target'] = list(map(classify, main_df[f'{RATIO_TO_PREDICT}_close'], main_df['future']))

print(main_df.head())
