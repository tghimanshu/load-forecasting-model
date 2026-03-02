import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import plotly.express as px
    import plotly.graph_objects as go
    import matplotlib.pyplot as plt
    import seaborn as sns
    import holidays
    import os

    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.metrics import mean_absolute_percentage_error

    return (
        GradientBoostingRegressor,
        holidays,
        mean_absolute_percentage_error,
        np,
        pd,
        px,
    )


@app.function
def get_season(month):
    if month in [12,1,2]:
        return 'Winter'
    elif month in [3,4,5]:
        return 'Spring'
    elif month in [6,7,8]:
        return 'Summer'
    else:
        return 'Fall'


@app.cell
def _(pd):
    loads = pd.read_csv("./actual_load.csv")
    weathers = pd.read_csv("./actual_weather_all_ws.csv")

    # Got the full date range
    full_range = pd.date_range(start=loads['datetime'].min(), end=loads['datetime'].max(), freq="h", tz='UTC')

    loads['datetime'] = pd.to_datetime(loads['datetime'], utc=True)

    # Update datetime to fill gaps
    loads = loads.set_index('datetime').reindex(full_range).reset_index()
    loads.rename(columns={'index':'datetime'}, inplace=True)

    # interpolated missing values by linear interpolation
    loads['load_mw'] = loads['load_mw'].interpolate(method='linear')
    return loads, weathers


@app.cell
def _(loads):
    # Average hour data
    loads['hour'] = (loads['datetime'].dt.hour - 5) % 24
    hourly_load = loads.groupby('hour').agg({'load_mw': 'mean'})
    hourly_load.reset_index(inplace=True)
    return (hourly_load,)


@app.cell
def _(hourly_load, px):
    px.line(hourly_load, x='hour', y='load_mw', title='Average Hourly Load')
    return


@app.cell
def _(pd, px, weathers):
    weathers['hour'] = (pd.to_datetime(weathers['datetime'], utc=True).dt.hour - 5) % 24
    hourly_weather = weathers.groupby('hour').agg({'avg_all_ws_temp': 'mean'})
    hourly_weather.reset_index(inplace=True)
    print(hourly_weather.columns)
    px.line(hourly_weather, x='hour', y='avg_all_ws_temp', title='Average Hourly Temperature')
    return


@app.cell
def _(holidays, loads, pd):
    us_holidays = holidays.US()

    loads['datetime'] = pd.to_datetime(loads['datetime'], utc=True)
    loads['datetime'] = loads['datetime'].dt.tz_convert('America/New_York')
    loads['day_of_week'] = loads['datetime'].dt.dayofweek
    loads['month'] = loads['datetime'].dt.month
    loads['is_weekend'] = loads['day_of_week'].isin([5, 6]).astype(int)
    loads['prev_day_load'] = loads['load_mw'].shift(24)
    loads['prev_week_load'] = loads['load_mw'].shift(24 * 7)
    loads['is_night'] = ((loads['hour'] >= 0) & (loads['hour'] <= 6)).astype(int)
    loads['is_morning'] = ((loads['hour'] >= 7) & (loads['hour'] <= 11)).astype(int)
    loads['is_afternoon'] = ((loads['hour'] >= 12) & (loads['hour'] <= 17)).astype(int)
    loads['is_evening'] = ((loads['hour'] >= 18) & (loads['hour'] <= 23)).astype(int)
    loads['is_holiday'] = loads['datetime'].dt.date.apply(lambda x: x in us_holidays).astype(int)
    loads['season'] = loads['month'].apply(get_season)
    loads_fixed = pd.get_dummies(loads, columns=['season'], prefix='season')
    load_features = ['datetime', 'hour', 'day_of_week', 'month', 'is_weekend', 'prev_day_load', 'prev_week_load', 'is_night', 'is_morning', 'is_afternoon', 'is_evening', 'is_holiday', 'season_Fall', 'season_Spring', 'season_Summer', 'season_Winter']
    return load_features, loads_fixed, us_holidays


@app.cell
def _():
    return


@app.cell
def _(pd, weathers):
    weathers_trimmed = weathers[['datetime', 'avg_all_ws_temp', 'hour']]
    weathers_trimmed['datetime'] = pd.to_datetime(weathers_trimmed['datetime'], utc=True)
    weathers_trimmed['datetime'] = weathers_trimmed['datetime'].dt.tz_convert('America/New_York')
    weathers_trimmed.rename(columns={'avg_all_ws_temp': 'avg_temp'}, inplace=True)
    weathers_trimmed['prev_day_avg_temp'] = weathers_trimmed['avg_temp'].shift(24)
    weathers_trimmed['prev_week_avg_temp'] = weathers_trimmed['avg_temp'].shift(24 * 7)

    weathers_trimmed['rolling_avg_temp_6h'] = weathers_trimmed['avg_temp'].rolling(window=6).mean()
    weathers_trimmed['rolling_avg_temp_24h'] = weathers_trimmed['avg_temp'].rolling(window=24).mean()

    weathers_trimmed['rolling_avg_temp_6h'] = weathers_trimmed['rolling_avg_temp_6h'].bfill()
    weathers_trimmed['rolling_avg_temp_24h'] = weathers_trimmed['rolling_avg_temp_24h'].bfill()

    weathers_trimmed['cdd'] = weathers_trimmed['avg_temp'].apply(lambda x: max(0, x - 18))
    weathers_trimmed['hdd'] = weathers_trimmed['avg_temp'].apply(lambda x: max(0, 18 - x))

    weathers_features = ['datetime', 'avg_temp', 'prev_day_avg_temp', 'prev_week_avg_temp', 'rolling_avg_temp_6h', 'rolling_avg_temp_24h']
    weathers_trimmed = weathers_trimmed[weathers_features]
    return weathers_features, weathers_trimmed


@app.cell
def _(load_features, loads_fixed, pd, weathers_features, weathers_trimmed):
    final_data = pd.merge(loads_fixed, weathers_trimmed, on='datetime', how='left')
    final_data = final_data.dropna(subset='prev_week_load')

    final_data['winter_temp'] = final_data['season_Winter'] * final_data['avg_temp']
    final_data['spring_temp'] = final_data['season_Spring'] * final_data['avg_temp']
    final_data['summer_temp'] = final_data['season_Summer'] * final_data['avg_temp']
    final_data['fall_temp'] = final_data['season_Fall'] * final_data['avg_temp']

    final_data_features = list(set(load_features + weathers_features + ['winter_temp', 'spring_temp', 'summer_temp', 'fall_temp']))

    final_data.head(5)
    return final_data, final_data_features


@app.cell
def _(final_data_features):
    final_data_features
    return


@app.cell
def _():
    return


@app.cell
def _(final_data):
    cutoff_period = '2024-01-01'
    train_set = final_data[final_data['datetime'] < cutoff_period]
    test_set = final_data[final_data['datetime'] >= cutoff_period]

    print("Training Set: ", len(train_set))
    print("Testing Set: ", len(test_set))
    return test_set, train_set


@app.cell
def _(
    GradientBoostingRegressor,
    final_data_features,
    mean_absolute_percentage_error,
    test_set,
    train_set,
):
    target = 'load_mw'
    model_features = [col for col in final_data_features if col != "datetime"]

    model = GradientBoostingRegressor(n_estimators=500, learning_rate=0.1, max_depth=5, random_state=52)
    model.fit(train_set[model_features], train_set[target])

    test_preds = model.predict(test_set[model_features])

    mape = mean_absolute_percentage_error(test_set[target], test_preds)
    print(f"Validation Mape (2024): {mape}")
    return model, model_features


@app.cell
def _(model_features, test_set):
    # train_set[target].shape
    test_set[model_features].shape
    return


@app.cell
def _(pd, us_holidays, weathers):
    dataset_2025 = weathers[weathers['datetime']>= '2025-01-01']
    dataset_2025['datetime'] = pd.to_datetime(dataset_2025['datetime']).dt.tz_convert('America/New_York')
    range_2025 = pd.date_range(start='2025-01-01', end='2026-01-01', freq='h', tz='America/New_York')
    dataset_2025 = dataset_2025[dataset_2025['datetime'] >= '2025-01-01']
    dataset_2025 = dataset_2025[['datetime', 'avg_all_ws_temp']]
    dataset_2025 = dataset_2025.set_index('datetime').reindex(range_2025).reset_index()
    dataset_2025 = dataset_2025.iloc[:-1]

    # dataset_2025['avg_all_ws_temp'] = dataset_2025['avg_all_ws_temp'].interpolate(method="linear")
    dataset_2025['avg_all_ws_temp'] = dataset_2025['avg_all_ws_temp'].interpolate(method='linear')
    dataset_2025.rename(columns={'index': 'datetime', 'avg_all_ws_temp':'avg_temp'}, inplace=True)
    dataset_2025

    dataset_2025['hour'] = dataset_2025['datetime'].dt.hour
    dataset_2025['day_of_week'] = dataset_2025['datetime'].dt.dayofweek
    dataset_2025['month'] = dataset_2025['datetime'].dt.month
    dataset_2025['is_weekend'] = dataset_2025['day_of_week'].isin([5, 6]).astype(int)
    dataset_2025['is_night'] = ((dataset_2025['hour'] >= 0) & (dataset_2025['hour'] <= 6)).astype(int)
    dataset_2025['is_morning'] = ((dataset_2025['hour'] >= 7) & (dataset_2025['hour'] <= 11)).astype(int)
    dataset_2025['is_afternoon'] = ((dataset_2025['hour'] >= 12) & (dataset_2025['hour'] <= 17)).astype(int)
    dataset_2025['is_evening'] = ((dataset_2025['hour'] >= 18) & (dataset_2025['hour'] <= 23)).astype(int)
    dataset_2025['is_holiday'] = dataset_2025['datetime'].dt.date.apply(lambda x: x in us_holidays).astype(int)
    dataset_2025['season'] = dataset_2025['month'].apply(get_season)
    dataset_2025 = pd.get_dummies(dataset_2025, columns=['season'], prefix='season')

    dataset_2025['prev_day_avg_temp'] = dataset_2025['avg_temp'].shift(24)
    dataset_2025['prev_week_avg_temp'] = dataset_2025['avg_temp'].shift(24 * 7)

    dataset_2025['rolling_avg_temp_6h'] = dataset_2025['avg_temp'].rolling(window=6).mean()
    dataset_2025['rolling_avg_temp_24h'] = dataset_2025['avg_temp'].rolling(window=24).mean()

    dataset_2025['rolling_avg_temp_6h'] = dataset_2025['rolling_avg_temp_6h'].bfill()
    dataset_2025['rolling_avg_temp_24h'] = dataset_2025['rolling_avg_temp_24h'].bfill()

    dataset_2025['cdd'] = dataset_2025['avg_temp'].apply(lambda x: max(0, x - 18))
    dataset_2025['hdd'] = dataset_2025['avg_temp'].apply(lambda x: max(0, 18 - x))

    dataset_2025['winter_temp'] = dataset_2025['season_Winter'] * dataset_2025['avg_temp']
    dataset_2025['spring_temp'] = dataset_2025['season_Spring'] * dataset_2025['avg_temp']
    dataset_2025['summer_temp'] = dataset_2025['season_Summer'] * dataset_2025['avg_temp']
    dataset_2025['fall_temp'] = dataset_2025['season_Fall'] * dataset_2025['avg_temp']

    return (dataset_2025,)


@app.cell
def _(dataset_2025, final_data, model, model_features, np, pd):
    dataset_2025['load_mw'] = np.nan
    forecast_df = pd.concat([final_data, dataset_2025]).reset_index()

    forecast_df['prev_day_load'] = forecast_df['load_mw'].shift(24)
    forecast_df['prev_week_load'] = forecast_df['load_mw'].shift(24 * 7)

    forecast_df['prev_day_avg_temp'] = forecast_df['avg_temp'].shift(24)
    forecast_df['prev_week_avg_temp'] = forecast_df['avg_temp'].shift(24 * 7)

    forecast_df['rolling_avg_temp_6h'] = forecast_df['avg_temp'].rolling(window=6).mean()
    forecast_df['rolling_avg_temp_24h'] = forecast_df['avg_temp'].rolling(window=24).mean()

    forecast_df['rolling_avg_temp_6h'] = forecast_df['rolling_avg_temp_6h'].bfill()
    forecast_df['rolling_avg_temp_24h'] = forecast_df['rolling_avg_temp_24h'].bfill()

    forecast_indices = forecast_df[forecast_df['datetime'].dt.year == 2025].index

    backtest_df = forecast_df.copy()
    backtest_df.loc[backtest_df['datetime'].dt.year == 2024, 'load_mw'] = np.nan
    backtest_indices = backtest_df[backtest_df['datetime'].dt.year == 2024].index

    for idx, idx2 in zip(forecast_indices, backtest_indices):
        # Look back at the load_mw column (which contains 2023 actuals or 2024 predictions)
        backtest_df.at[idx2, 'prev_day_load'] = backtest_df.at[idx2 - 24, 'load_mw']
        backtest_df.at[idx2, 'prev_week_load'] = backtest_df.at[idx2 - (24 * 7), 'load_mw']

        # Predict using your improved feature list
        current_features = backtest_df.loc[[idx2], model_features]
        prediction = model.predict(current_features)[0]

        # Fill the 'load_mw' column so the next hour can use this prediction as a lag
        backtest_df.at[idx2, 'load_mw'] = prediction


        forecast_df.at[idx, 'prev_day_load'] = forecast_df.at[idx - 24, 'load_mw']
        forecast_df.at[idx, 'prev_week_load'] = forecast_df.at[idx - (24 * 7), 'load_mw']

        current_features = forecast_df.loc[[idx], model_features]

        prediction = model.predict(current_features)[0]

        forecast_df.at[idx, 'load_mw'] = prediction

    final_2025_results = forecast_df[forecast_df['datetime'].dt.year == 2025][['datetime', 'load_mw']]
    backtest_2024_results = forecast_df[forecast_df['datetime'].dt.year == 2024][['datetime', 'load_mw']]
    return current_features, final_2025_results, forecast_df, forecast_indices


@app.cell
def _(current_features, forecast_df, forecast_indices):
    forecast_indices
    forecast_df.shape
    current_features.columns
    return


@app.cell
def _(model_features, train_set):
    train_set[model_features].columns
    return


@app.cell
def _(forecast_df, px):
    px.line(data_frame=forecast_df, x='datetime', y='load_mw')
    return


@app.cell
def _(final_2025_results):
    results = final_2025_results.copy()
    results['datetime'] = results['datetime'].dt.strftime('%Y-%m-%d %H:00:00')
    results.to_csv("JackOfAllTrades.csv")
    return


if __name__ == "__main__":
    app.run()
