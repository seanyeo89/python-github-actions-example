import dash
from dash import dcc
from dash import html
from dash import dash_table as dt
from dash.dependencies import Input, Output, State
from stockstats import StockDataFrame as Sdf
import dash_bootstrap_components as dbc
import yahoo_fin.stock_info as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta
##import pickle
import random


# defining style color
## Redis key value stores
## Perform data cleaning and data validation on redis
## Use redis for 2 weeks. In memory database or persistent.
colors = {"background": "#000000", "text": "#ffFFFF"}

ticker_list = yf.tickers_sp500()
ticker_list = [item.replace(".", "-") for item in ticker_list]

external_stylesheets = [dbc.themes.SLATE]


# adding css
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.Div(
            [  # header Div
                dbc.Row(
                    [
                        dbc.Col(
                            html.Header(
                                [
                                    html.H1(
                                        "Stock Dashboard",
                                        style={
                                            "textAlign": "center",
                                            "color": colors["text"],
                                        },
                                    )
                                ]
                            )
                        )
                    ]
                )
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),

        html.Div(
            [  # Dropdown Div
                dbc.Row(
                    [
                        dbc.Col(  # Tickers
                            dcc.Dropdown(
                                id="stock_name",
                                options=[
                                    {
                                        "label": str(ticker_list[i]),
                                        "value": str(ticker_list[i]),
                                    }
                                    for i in range(len(ticker_list))
                                ],
                                searchable=True,
                                value=str(
                                    random.choice(
                                        [   "TSLA",
                                            "GM",
                                            "F",
                                            "FB",
                                            "AMZN",
                                            "AAPL",
                                            "NFLX",
                                            "GOOGL",
                                            "KO",
                                            "DIS",
                                            "MSFT",
                                            "NVDA",
                                            "AMD",
                                            "NKE",
                                        ]
                                    )
                                ),
                                placeholder="enter stock name",
                            ),
                            width={"size": 3, "offset": 3},
                        ),
                        dbc.Col(  # Graph type
                            dcc.Dropdown(
                                id="chart",
                                options=[
                                    {"label": "line", "value": "Line"},
                                    {"label": "candlestick",
                                        "value": "Candlestick"},
                                    {"label": "Simple moving average",
                                        "value": "SMA"},
                                    {
                                        "label": "Exponential moving average",
                                        "value": "EMA",
                                    },
                                    {"label": "MACD", "value": "MACD"},
                                    {"label": "RSI", "value": "RSI"},
                                    {"label": "OHLC", "value": "OHLC"},
                                    {"label": "BOLL", "value": "BOLL"}
                                ],
                                value="Line",
                                style={"color": "#000000"},
                            ),
                            width={"size": 3},
                        ),
                        dbc.Col(  # button
                            dbc.Button(
                                "Plot",
                                id="submit-button-state",
                                className="mr-1",
                                n_clicks=1,
                            ),
                            width={"size": 2},
                        ),
                    ]
                )
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id="live price",
                                config={
                                    "displaylogo": False,
                                    "modeBarButtonsToRemove": ["pan2d", "lasso2d"],
                                },
                            )
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id="graph",
                                config={
                                    "displaylogo": False,
                                    "modeBarButtonsToRemove": ["pan2d", "lasso2d"],
                                },
                            ),
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dt.DataTable(
                                id="info",
                                style_table={"height": "auto"},
                                style_cell={
                                    "white_space": "normal",
                                    "height": "auto",
                                    "backgroundColor": colors["background"],
                                    "color": "white",
                                    "font_size": "16px",
                                },
                                style_data={"border": "#4d4d4d"},
                                style_header={
                                    "backgroundColor": colors["background"],
                                    "fontWeight": "bold",
                                    "border": "#4d4d4d",
                                },
                                style_cell_conditional=[
                                    {"if": {"column_id": c}, "textAlign": "center"}
                                    for c in ["attribute", "value"]
                                ],
                            ),
                            width={"size": 6, "offset": 3},
                        )
                    ]
                ),
            ]
        ),
    ],
)

# Callback main graph


@app.callback(
    # output
    [Output("graph", "figure"), Output("live price", "figure")],
    # input
    [Input("submit-button-state", "n_clicks")],
    # state
    [State("stock_name", "value"), State("chart", "value")],
)
def graph_genrator(n_clicks, ticker, chart_name):

    if n_clicks >= 1:  # Checking for user to click submit button
        #edit time horizon to 10 years max
        # loading data
        start_date = datetime.now().date() - timedelta(days=5 * 365)
        end_data = datetime.now().date()
        df = yf.get_data(
            ticker, start_date=start_date, end_date=end_data, interval="1d"
        )
        stock = Sdf(df)

        # selecting graph type

        # line plot
        if chart_name == "Line":
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=list(df.index), y=list(df.close), fill="tozeroy", name="close"
                    )
                ],
                layout={
                    "height": 1000,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )
            #Correct error in code label of 10d
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    activecolor="blue",
                    bgcolor=colors["background"],
                    buttons=list(
                        [
                            dict(count=10, label="10D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            ##dict(step="all"),
                        ]
                    ),
                ),
            )

        # Candlestick
        if chart_name == "Candlestick":
            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=list(df.index),
                        open=list(df.open),
                        high=list(df.high),
                        low=list(df.low),
                        close=list(df.close),
                        name="Candlestick",
                    )
                ],
                layout={
                    "height": 1000,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    activecolor="blue",
                    bgcolor=colors["background"],
                    buttons=list(
                        [
                            dict(count=10, label="10D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            ##dict(step="all"),
                        ]
                    ),
                ),
            )

        # simple moving average
        if chart_name == "SMA":
            close_ma_10 = df.close.rolling(10).mean()
            close_ma_15 = df.close.rolling(15).mean()
            close_ma_30 = df.close.rolling(30).mean()
            close_ma_100 = df.close.rolling(100).mean()
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=list(close_ma_10.index), y=list(close_ma_10), name="10 Days"
                    ),
                    go.Scatter(
                        x=list(close_ma_15.index), y=list(close_ma_15), name="15 Days"
                    ),
                    go.Scatter(
                        x=list(close_ma_30.index), y=list(close_ma_15), name="30 Days"
                    ),
                    go.Scatter(
                        x=list(close_ma_100.index), y=list(close_ma_15), name="100 Days"
                    ),
                ],
                layout={
                    "height": 1000,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    activecolor="blue",
                    bgcolor=colors["background"],
                    buttons=list(
                        [
                            dict(count=10, label="10D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            ##dict(step="all"),
                        ]
                    ),
                ),
            )

        # Open_high_low_close
        if chart_name == "OHLC":
            fig = go.Figure(
                data=[
                    go.Ohlc(
                        x=df.index,
                        open=df.open,
                        high=df.high,
                        low=df.low,
                        close=df.close,
                    )
                ],
                layout={
                    "height": 1000,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    activecolor="blue",
                    bgcolor=colors["background"],
                    buttons=list(
                        [
                            dict(count=10, label="10D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            ##dict(step="all"),
                        ]
                    ),
                ),
            )


         # Bollinger

         # Define the parameters for the Bollinger Band calculation
        
        if chart_name == "BOLL":

            # Define the parameters for the Bollinger Band calculation
            ma_size = 20
            bol_size = 2
            df.insert(0, 'moving_average', df['close'].rolling(ma_size).mean())

            # Calculate the upper and lower Bollinger Bands
            df.insert(0, 'bol_upper', df['moving_average'] + df['close'].rolling(ma_size).std() * bol_size)
            df.insert(0, 'bol_lower', df['moving_average'] - df['close'].rolling(ma_size).std() * bol_size)
            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=df.index,
                        open=df.open,
                        high=df.high,
                        low=df.low,
                        close=df.close,
                    )
                ],
            layout={
                    "height": 1000,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                }
            )
            trace1 = go.Scatter(
             x=df.index, y=df['bol_upper'], mode="lines", showlegend=False, name="BB_upper"
            )

            trace2 = go.Scatter(
            x=df.index, y=df['moving_average'], mode="lines", showlegend=False, name="BB_mean"
            )

            trace3 = go.Scatter(
            x=df.index, y=df['bol_lower'], mode="lines", showlegend=False, name="BB_lower"
            )

            fig.add_trace(trace1)  # plot in first row
            fig.add_trace(trace2)  # plot in first row
            fig.add_trace(trace3)  # plot in first row

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    activecolor="blue",
                    bgcolor=colors["background"],
                    buttons=list(
                        [
                            dict(count=10, label="10D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            ##dict(step="all"),
                        ]
                    ),
                ),
            )
        # Exponential moving average
        if chart_name == "EMA":
            close_ema_10 = df.close.ewm(span=10).mean()
            close_ema_15 = df.close.ewm(span=15).mean()
            close_ema_30 = df.close.ewm(span=30).mean()
            close_ema_100 = df.close.ewm(span=100).mean()
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=list(close_ema_10.index), y=list(close_ema_10), name="10 Days"
                    ),
                    go.Scatter(
                        x=list(close_ema_15.index), y=list(close_ema_15), name="15 Days"
                    ),
                    go.Scatter(
                        x=list(close_ema_30.index), y=list(close_ema_30), name="30 Days"
                    ),
                    go.Scatter(
                        x=list(close_ema_100.index),
                        y=list(close_ema_100),
                        name="100 Days",
                    ),
                ],
                layout={
                    "height": 1000,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    activecolor="blue",
                    bgcolor=colors["background"],
                    buttons=list(
                        [
                            dict(count=10, label="10D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            ##dict(step="all"),
                        ]
                    ),
                ),
            )

        # Moving average convergence divergence
        ##MACD is often displayed with a histogram (see the chart below) which graphs the distance between the MACD and its signal line. If the MACD is above the signal line, the histogram will be above the MACD’s baseline. If the MACD is below its signal line, the histogram will be below the MACD’s baseline. Traders use the MACD’s histogram to identify when bullish or bearish momentum is high.
        if chart_name == "MACD":
            df["MACD"], df["signal"], df["hist"] = (
                stock["macd"],
                stock["macds"],
                stock["macdh"],
            )
            fig = go.Figure(
                data=[
                    go.Scatter(x=list(df.index), y=list(df.MACD), name="MACD"),
                    go.Scatter(x=list(df.index), y=list(
                        df.signal), name="Signal"),
                    go.Scatter(
                        x=list(df.index),
                        y=list(df["hist"]),
                        line=dict(color="royalblue", width=2, dash="dot"),
                        name="Histogram",
                    ),
                ],
                layout={
                    "height": 1000,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    activecolor="blue",
                    bgcolor=colors["background"],
                    buttons=list(
                        [
                            dict(count=10, label="10D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            ##dict(step="all"),
                        ]
                    ),
                ),
            )

            # Relative strength index
            #Some traders will consider it a “buy signal” if a security’s RSI reading moves below 30, based on the idea that the security has been oversold and is therefore poised for a rebound. 
        if chart_name == "RSI":
            rsi_6 = stock["rsi_6"]
            rsi_14 = stock["rsi_14"]
            rsi_30=stock["rsi_30"]
            fig = go.Figure(
                data=[
                    go.Scatter(x=list(df.index), y=list(
                        rsi_6), name="RSI 6 Day"),
                    go.Scatter(x=list(df.index), y=list(
                        rsi_14), name="RSI 14 Day"),
                    go.Scatter(x=list(df.index), y=list(
                        rsi_30), name="RSI 30 Day"),
                ],
                layout={
                    "height": 1000,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    activecolor="blue",
                    bgcolor=colors["background"],
                    buttons=list(
                        [
                            dict(count=10, label="10D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            ##dict(step="all"),
                        ]
                    ),
                ),
            )
    #edited time delta to reflect price changes in last 7 days mainly instead of original 1 month.
    #Rationale of choice is to show cross week change although weekend will result in 4 days interval in the worse case scenario.
    end_data = datetime.now().date()
    start_date = datetime.now().date() - timedelta(days=7)
    res_df = yf.get_data(
        ticker, start_date=start_date, end_date=end_data, interval="1d"
    )
    price = yf.get_live_price(ticker)
    prev_close = res_df.close.iloc[0]
    #edit price indicator to show percentage change
    live_price = go.Figure(
        data=[
            go.Indicator(
                domain={"x": [0, 1], "y": [0, 1]},
                value=round(price,3),
                mode="number+delta",
                title={"text": "Price and 7d change in price"},
                delta={"reference": prev_close,'relative': True},
            )
        ],
        layout={
            "height": 300,
            "showlegend": True,
            "plot_bgcolor": colors["background"],
            "paper_bgcolor": colors["background"],
            "font": {"color": colors["text"]},
        },
    )

    return fig, live_price


@app.callback(
    # output
    [Output("info", "columns"), Output("info", "data")],
    # input
    [Input("submit-button-state", "n_clicks")],
    # state
    [State("stock_name", "value")],
)
def quotes_genrator(n_clicks, ticker):
    # info table
    current_stock = yf.get_quote_table(ticker, dict_result=False)
    columns = [{"name": i, "id": i} for i in current_stock.columns]
    t_data = current_stock.to_dict("records")

    # price

    return columns, t_data


if __name__ == "__main__":
    app.run_server(debug=True)