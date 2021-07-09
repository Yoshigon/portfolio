import matplotlib.pyplot as plt
import pandas_datareader
import pandas_datareader.stooq as stooq
import datetime
import pandas as pd


def plot_performance(start, end, stocklist, weights):
    _df = pd.DataFrame()
    for i in range(len(stocklist)):
        w = weights[i]
        stockcode = stocklist[i] + ".jp"
        df = pandas_datareader.stooq.StooqDailyReader(stockcode, start, end).read()
        df = df.sort_values(by='Date', ascending=True)
        df = pd.DataFrame(df['Close'])
        df = df.apply(lambda x: (x - x[0]) / x[0])
        df = df.rename(columns={'Close': f'Close{stocklist[i]}'})
        df *= w
        _df = pd.concat([_df, df], axis=1)
    _df["sum"] = _df.sum(axis="columns")
    return _df


def main():
    print('組み入れる銘柄の数を入力してください')
    num_stocks = int(input())
    stocks = []
    weights = []

    for i in range(num_stocks):
        print(f'{i+1}個目の銘柄コードを入力してください')
        stock = input()
        print(f'{stock}のウェイトを入力してください(負でもOK)')
        weight = float(input())
        stocks.append(stock)
        weights.append(weight)
    print(f'入力された総ウェイトは{sum(weights)}です (和が1.0でない場合は、全体が1.0になるように修正します)')
    leverage = sum(weights)
    for i in range(num_stocks):
        weights[i] /= leverage

    title = "stock-weight: "
    for i in range(num_stocks):
        title += f'{stocks[i]}-{weights[i] * 100}% '

    print('運用開始日を入力してください(YYYY MM DD)')
    year, month, date = input().split()
    year = int(year)
    if month[0] == '0':
        month = int(month[1])
    else:
        month = int(month)
    if date[0] == '0':
        date = int(date[1])
    else:
        date = int(date)
    start = datetime.datetime(year, month, date)

    print('運用終了日を入力してください(YYYY/MM/DD)')
    year, month, date = input().split()
    year = int(year)
    if month[0] == '0':
        month = int(month[1])
    else:
        month = int(month)
    if date[0] == '0':
        date = int(date[1])
    else:
        date = int(date)
    end = datetime.datetime(year, month, date)

    df = plot_performance(start, end, stocks, weights)
    topix = plot_performance(start, end, ['1348'], [1])

    df_plot = pd.DataFrame()
    df_plot['your_portfolio'] = df['sum']
    df_plot['topix'] = topix['sum']

    df_plot.to_csv('df_plot.csv')
    plt.figure(figsize=(24, 16))
    df_plot.plot()
    plt.title(title, loc='center')
    plt.savefig('./portfolio.png')
    plt.close('all')


if __name__ == "__main__":
    main()
