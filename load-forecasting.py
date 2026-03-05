import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
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
    from sklearn.linear_model import LinearRegression

    return (
        GradientBoostingRegressor,
        holidays,
        mean_absolute_percentage_error,
        mo,
        np,
        pd,
    )


@app.cell
def _(holidays):
    us_holidays = holidays.US()

    def get_season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Fall"

    return get_season, us_holidays


@app.cell
def _(pd):
    loads = pd.read_csv("./actual_load.csv")
    weathers = pd.read_csv("./actual_weather_all_ws.csv")

    loads["datetime"] = pd.to_datetime(loads["datetime"])
    loads["datetime"] = loads["datetime"].dt.tz_localize(
        "America/New_York", ambiguous=True, nonexistent="shift_forward"
    )

    weathers["datetime"] = pd.to_datetime(weathers["datetime"], utc=True)
    weathers["datetime"] = weathers["datetime"].dt.tz_convert("America/New_York")

    # Got the full date range
    # full_range = pd.date_range(start=loads['datetime'].min(), end=loads['datetime'].max(), freq="h", tz='UTC')

    # loads['datetime'] = pd.to_datetime(loads['datetime'], utc=True)

    # # Update datetime to fill gaps
    # loads = loads.set_index('datetime').reindex(full_range).reset_index()
    # loads.rename(columns={'index':'datetime'}, inplace=True)

    # # interpolated missing values by linear interpolation
    # loads['load_mw'] = loads['load_mw'].interpolate(method='linear')
    return loads, weathers


@app.cell
def _():
    # Average hour data
    # loads['hour'] = (loads['datetime'].dt.hour - 5) % 24
    # hourly_load = loads.groupby('hour').agg({'load_mw': 'mean'})
    # hourly_load.reset_index(inplace=True)
    return


@app.cell
def _():
    # px.line(hourly_load, x='hour', y='load_mw', title='Average Hourly Load')
    return


@app.cell
def _():
    # weathers['hour'] = (pd.to_datetime(weathers['datetime'], utc=True).dt.hour - 5) % 24
    # hourly_weather = weathers.groupby('hour').agg({'avg_all_ws_temp': 'mean'})
    # hourly_weather.reset_index(inplace=True)
    # print(hourly_weather.columns)
    # px.line(hourly_weather, x='hour', y='avg_all_ws_temp', title='Average Hourly Temperature')
    return


@app.cell
def _():
    # us_holidays = holidays.US()

    # loads['datetime'] = pd.to_datetime(loads['datetime'], utc=True)
    # loads['datetime'] = loads['datetime'].dt.tz_convert('America/New_York')
    # loads['day_of_week'] = loads['datetime'].dt.dayofweek
    # loads['month'] = loads['datetime'].dt.month
    # loads['is_weekend'] = loads['day_of_week'].isin([5, 6]).astype(int)
    # loads['prev_day_load'] = loads['load_mw'].shift(24)
    # loads['prev_week_load'] = loads['load_mw'].shift(24 * 7)
    # loads['is_night'] = ((loads['hour'] >= 0) & (loads['hour'] <= 6)).astype(int)
    # loads['is_morning'] = ((loads['hour'] >= 7) & (loads['hour'] <= 11)).astype(int)
    # loads['is_afternoon'] = ((loads['hour'] >= 12) & (loads['hour'] <= 17)).astype(int)
    # loads['is_evening'] = ((loads['hour'] >= 18) & (loads['hour'] <= 23)).astype(int)
    # loads['is_holiday'] = loads['datetime'].dt.date.apply(lambda x: x in us_holidays).astype(int)
    # loads['season'] = loads['month'].apply(get_season)
    # loads_fixed = pd.get_dummies(loads, columns=['season'], prefix='season')
    # load_features = ['datetime', 'hour', 'day_of_week', 'month', 'is_weekend', 'prev_day_load', 'prev_week_load', 'is_night', 'is_morning', 'is_afternoon', 'is_evening', 'is_holiday', 'season_Fall', 'season_Spring', 'season_Summer', 'season_Winter']
    return


@app.cell
def _():
    return


@app.cell
def _():
    # weathers_trimmed = weathers[['datetime', 'avg_all_ws_temp', 'hour']]
    # weathers_trimmed['datetime'] = pd.to_datetime(weathers_trimmed['datetime'], utc=True)
    # weathers_trimmed['datetime'] = weathers_trimmed['datetime'].dt.tz_convert('America/New_York')
    # weathers_trimmed.rename(columns={'avg_all_ws_temp': 'avg_temp'}, inplace=True)
    # weathers_trimmed['prev_day_avg_temp'] = weathers_trimmed['avg_temp'].shift(24)
    # weathers_trimmed['prev_week_avg_temp'] = weathers_trimmed['avg_temp'].shift(24 * 7)

    # weathers_trimmed['rolling_avg_temp_6h'] = weathers_trimmed['avg_temp'].rolling(window=6).mean()
    # weathers_trimmed['rolling_avg_temp_24h'] = weathers_trimmed['avg_temp'].rolling(window=24).mean()

    # weathers_trimmed['rolling_avg_temp_6h'] = weathers_trimmed['rolling_avg_temp_6h'].bfill()
    # weathers_trimmed['rolling_avg_temp_24h'] = weathers_trimmed['rolling_avg_temp_24h'].bfill()

    # weathers_trimmed['cdd'] = weathers_trimmed['avg_temp'].apply(lambda x: max(0, x - 18))
    # weathers_trimmed['hdd'] = weathers_trimmed['avg_temp'].apply(lambda x: max(0, 18 - x))

    # weathers_features = ['datetime', 'avg_temp', 'prev_day_avg_temp', 'prev_week_avg_temp', 'rolling_avg_temp_6h', 'rolling_avg_temp_24h']
    # weathers_trimmed = weathers_trimmed[weathers_features]
    return


@app.cell
def _():
    # final_data = pd.merge(loads_fixed, weathers_trimmed, on='datetime', how='left')
    # final_data = final_data.dropna(subset='prev_week_load')

    # final_data['winter_temp'] = final_data['season_Winter'] * final_data['avg_temp']
    # final_data['spring_temp'] = final_data['season_Spring'] * final_data['avg_temp']
    # final_data['summer_temp'] = final_data['season_Summer'] * final_data['avg_temp']
    # final_data['fall_temp'] = final_data['season_Fall'] * final_data['avg_temp']

    # final_data_features = list(set(load_features + weathers_features + ['winter_temp', 'spring_temp', 'summer_temp', 'fall_temp']))

    # final_data.head(5)
    return


@app.cell
def _():
    # final_data_features
    return


@app.cell
def _():
    return


@app.cell
def _():
    # cutoff_period = '2024-01-01'
    # train_set = final_data[final_data['datetime'] < cutoff_period]
    # test_set = final_data[final_data['datetime'] >= cutoff_period]

    # print("Training Set: ", len(train_set))
    # print("Testing Set: ", len(test_set))
    return


@app.cell
def _():
    # target = 'load_mw'
    # model_features = [col for col in final_data_features if col != "datetime"]

    # model = GradientBoostingRegressor(n_estimators=500, learning_rate=0.1, max_depth=5, random_state=52)
    # model.fit(train_set[model_features], train_set[target])

    # test_preds = model.predict(test_set[model_features])

    # mape = mean_absolute_percentage_error(test_set[target], test_preds)
    # print(f"Validation Mape (2024): {mape}")
    return


@app.cell
def _():
    # # train_set[target].shape
    # test_set[model_features].shape
    return


@app.cell
def _():
    # dataset_2025 = weathers[weathers['datetime']>= '2025-01-01']
    # dataset_2025['datetime'] = pd.to_datetime(dataset_2025['datetime']).dt.tz_convert('America/New_York')
    # range_2025 = pd.date_range(start='2025-01-01', end='2026-01-01', freq='h', tz='America/New_York')
    # dataset_2025 = dataset_2025[dataset_2025['datetime'] >= '2025-01-01']
    # dataset_2025 = dataset_2025[['datetime', 'avg_all_ws_temp']]
    # dataset_2025 = dataset_2025.set_index('datetime').reindex(range_2025).reset_index()
    # dataset_2025 = dataset_2025.iloc[:-1]

    # # dataset_2025['avg_all_ws_temp'] = dataset_2025['avg_all_ws_temp'].interpolate(method="linear")
    # dataset_2025['avg_all_ws_temp'] = dataset_2025['avg_all_ws_temp'].interpolate(method='linear')
    # dataset_2025.rename(columns={'index': 'datetime', 'avg_all_ws_temp':'avg_temp'}, inplace=True)
    # dataset_2025

    # dataset_2025['hour'] = dataset_2025['datetime'].dt.hour
    # dataset_2025['day_of_week'] = dataset_2025['datetime'].dt.dayofweek
    # dataset_2025['month'] = dataset_2025['datetime'].dt.month
    # dataset_2025['is_weekend'] = dataset_2025['day_of_week'].isin([5, 6]).astype(int)
    # dataset_2025['is_night'] = ((dataset_2025['hour'] >= 0) & (dataset_2025['hour'] <= 6)).astype(int)
    # dataset_2025['is_morning'] = ((dataset_2025['hour'] >= 7) & (dataset_2025['hour'] <= 11)).astype(int)
    # dataset_2025['is_afternoon'] = ((dataset_2025['hour'] >= 12) & (dataset_2025['hour'] <= 17)).astype(int)
    # dataset_2025['is_evening'] = ((dataset_2025['hour'] >= 18) & (dataset_2025['hour'] <= 23)).astype(int)
    # dataset_2025['is_holiday'] = dataset_2025['datetime'].dt.date.apply(lambda x: x in us_holidays).astype(int)
    # dataset_2025['season'] = dataset_2025['month'].apply(get_season)
    # dataset_2025 = pd.get_dummies(dataset_2025, columns=['season'], prefix='season')

    # dataset_2025['prev_day_avg_temp'] = dataset_2025['avg_temp'].shift(24)
    # dataset_2025['prev_week_avg_temp'] = dataset_2025['avg_temp'].shift(24 * 7)

    # dataset_2025['rolling_avg_temp_6h'] = dataset_2025['avg_temp'].rolling(window=6).mean()
    # dataset_2025['rolling_avg_temp_24h'] = dataset_2025['avg_temp'].rolling(window=24).mean()

    # dataset_2025['rolling_avg_temp_6h'] = dataset_2025['rolling_avg_temp_6h'].bfill()
    # dataset_2025['rolling_avg_temp_24h'] = dataset_2025['rolling_avg_temp_24h'].bfill()

    # dataset_2025['cdd'] = dataset_2025['avg_temp'].apply(lambda x: max(0, x - 18))
    # dataset_2025['hdd'] = dataset_2025['avg_temp'].apply(lambda x: max(0, 18 - x))

    # dataset_2025['winter_temp'] = dataset_2025['season_Winter'] * dataset_2025['avg_temp']
    # dataset_2025['spring_temp'] = dataset_2025['season_Spring'] * dataset_2025['avg_temp']
    # dataset_2025['summer_temp'] = dataset_2025['season_Summer'] * dataset_2025['avg_temp']
    # dataset_2025['fall_temp'] = dataset_2025['season_Fall'] * dataset_2025['avg_temp']
    return


@app.cell
def _():
    # dataset_2025['load_mw'] = np.nan
    # forecast_df = pd.concat([final_data, dataset_2025]).reset_index()

    # forecast_df['prev_day_load'] = forecast_df['load_mw'].shift(24)
    # forecast_df['prev_week_load'] = forecast_df['load_mw'].shift(24 * 7)

    # forecast_df['prev_day_avg_temp'] = forecast_df['avg_temp'].shift(24)
    # forecast_df['prev_week_avg_temp'] = forecast_df['avg_temp'].shift(24 * 7)

    # forecast_df['rolling_avg_temp_6h'] = forecast_df['avg_temp'].rolling(window=6).mean()
    # forecast_df['rolling_avg_temp_24h'] = forecast_df['avg_temp'].rolling(window=24).mean()

    # forecast_df['rolling_avg_temp_6h'] = forecast_df['rolling_avg_temp_6h'].bfill()
    # forecast_df['rolling_avg_temp_24h'] = forecast_df['rolling_avg_temp_24h'].bfill()

    # forecast_indices = forecast_df[forecast_df['datetime'].dt.year == 2025].index

    # for idx in forecast_indices:
    #     forecast_df.at[idx, 'prev_day_load'] = forecast_df.at[idx - 24, 'load_mw']
    #     forecast_df.at[idx, 'prev_week_load'] = forecast_df.at[idx - (24 * 7), 'load_mw']

    #     current_features = forecast_df.loc[[idx], model_features]

    #     prediction = model.predict(current_features)[0]

    #     forecast_df.at[idx, 'load_mw'] = prediction

    # final_2025_results = forecast_df[forecast_df['datetime'].dt.year == 2025][['datetime', 'load_mw']]
    return


@app.cell
def _():
    # forecast_indices
    # forecast_df.shape
    # current_features.columns
    return


@app.cell
def _():
    # train_set[model_features].columns
    return


@app.cell
def _():
    # px.line(data_frame=forecast_df, x='datetime', y='load_mw')
    return


@app.cell
def _():
    # results = final_2025_results.copy()
    # results['datetime'] = results['datetime'].dt.strftime('%Y-%m-%d %H:00:00')
    # results.to_csv("JackOfAllTrades.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Trying Linear Regression
    """)
    return


@app.cell
def _(get_season, pd, us_holidays, weathers):
    date_range = pd.date_range(
        start="2021-01-01", end="2025-12-31 23:00", freq="h", tz="America/New_York"
    )
    main_dataset = pd.DataFrame({"datetime": date_range})

    main_dataset["hour"] = main_dataset["datetime"].dt.hour
    main_dataset["day_of_week"] = main_dataset["datetime"].dt.dayofweek
    main_dataset["month"] = main_dataset["datetime"].dt.month
    main_dataset["is_weekend"] = main_dataset["day_of_week"].isin([5, 6]).astype(int)
    main_dataset["is_night"] = (
        (main_dataset["hour"] >= 0) & (main_dataset["hour"] <= 6)
    ).astype(int)
    main_dataset["is_morning"] = (
        (main_dataset["hour"] >= 7) & (main_dataset["hour"] <= 11)
    ).astype(int)
    main_dataset["is_afternoon"] = (
        (main_dataset["hour"] >= 12) & (main_dataset["hour"] <= 17)
    ).astype(int)
    main_dataset["is_evening"] = (
        (main_dataset["hour"] >= 18) & (main_dataset["hour"] <= 23)
    ).astype(int)
    main_dataset["is_holiday"] = (
        main_dataset["datetime"].dt.date.apply(lambda x: x in us_holidays).astype(int)
    )
    main_dataset["season"] = main_dataset["month"].apply(get_season)

    main_dataset = pd.get_dummies(
        main_dataset,
        columns=["season", "day_of_week", "hour", "month"],
        prefix=["season", "day_of_week", "hour", "month"],
    )

    main_dataset = main_dataset.merge(weathers, on="datetime", how="left")

    main_dataset.rename(columns={"avg_all_ws_temp": "avg_temp"}, inplace=True)

    # ffill for any mid-series weather gaps (no future data leakage)
    main_dataset["avg_temp"] = main_dataset["avg_temp"].ffill()

    main_dataset["prev_day_avg_temp"] = main_dataset["avg_temp"].shift(24)
    main_dataset["prev_week_avg_temp"] = main_dataset["avg_temp"].shift(24 * 7)

    main_dataset["rolling_avg_temp_6h"] = (
        main_dataset["avg_temp"].rolling(window=6).mean()
    )
    main_dataset["rolling_avg_temp_24h"] = (
        main_dataset["avg_temp"].rolling(window=24).mean()
    )

    main_dataset["cdd"] = main_dataset["avg_temp"].apply(lambda x: max(0, x - 18))
    main_dataset["hdd"] = main_dataset["avg_temp"].apply(lambda x: max(0, 18 - x))

    main_dataset["winter_temp"] = (
        main_dataset["season_Winter"] * main_dataset["avg_temp"]
    )
    main_dataset["spring_temp"] = (
        main_dataset["season_Spring"] * main_dataset["avg_temp"]
    )
    main_dataset["summer_temp"] = (
        main_dataset["season_Summer"] * main_dataset["avg_temp"]
    )
    main_dataset["fall_temp"] = main_dataset["season_Fall"] * main_dataset["avg_temp"]

    cols = [
        "season_Fall",
        "season_Spring",
        "season_Summer",
        "season_Winter",
        "day_of_week_0",
        "day_of_week_1",
        "day_of_week_2",
        "day_of_week_3",
        "day_of_week_4",
        "day_of_week_5",
        "day_of_week_6",
        "hour_0",
        "hour_1",
        "hour_2",
        "hour_3",
        "hour_4",
        "hour_5",
        "hour_6",
        "hour_7",
        "hour_8",
        "hour_9",
        "hour_10",
        "hour_11",
        "hour_12",
        "hour_13",
        "hour_14",
        "hour_15",
        "hour_16",
        "hour_17",
        "hour_18",
        "hour_19",
        "hour_20",
        "hour_21",
        "hour_22",
        "hour_23",
        "month_1",
        "month_2",
        "month_3",
        "month_4",
        "month_5",
        "month_6",
        "month_7",
        "month_8",
        "month_9",
        "month_10",
        "month_11",
        "month_12",
    ]

    for col in cols:
        main_dataset[f"{col}_temp"] = main_dataset[col] * main_dataset["avg_temp"]

    # Drop rows with NaNs from lag/rolling features (avoids leaking future data via bfill)
    # main_dataset.dropna(inplace=True)
    main_dataset.reset_index(drop=True, inplace=True)

    # main_dataset.head(5)
    main_dataset.columns
    return (main_dataset,)


@app.cell
def _():
    return


@app.cell
def _(loads, main_dataset):
    # 2021-2024 dataset
    training_dataset = main_dataset[main_dataset["datetime"].dt.year < 2025].copy()
    training_dataset = training_dataset.merge(loads, on="datetime", how="left")
    training_dataset["load_mw"] = training_dataset["load_mw"].interpolate(
        method="linear"
    )
    training_dataset.iloc[0].T
    return (training_dataset,)


@app.cell
def _(training_dataset):
    training_dataset['prev_day_avg_temp'] = training_dataset['prev_day_avg_temp'].ffill()
    training_dataset['prev_week_avg_temp'] = training_dataset['prev_week_avg_temp'].ffill()
    training_dataset['rolling_avg_temp_6h'] = training_dataset['rolling_avg_temp_6h'].ffill()
    training_dataset['rolling_avg_temp_24h'] = training_dataset['rolling_avg_temp_24h'].ffill()
    training_dataset.isna().any()
    return


@app.cell
def _(
    GradientBoostingRegressor,
    mean_absolute_percentage_error,
    training_dataset,
):
    model_features = [
        feat for feat in training_dataset.columns if feat not in ["datetime", "load_mw", "ws1_temp", "ws2_temp", "ws3_temp", "ws4_temp", "ws5_temp", "ws6_temp", "ws7_temp", "ws8_temp", "ws9_temp", "ws10_temp", "ws11_temp", "ws12_temp", "ws13_temp", "ws14_temp", "ws15_temp", "ws16_temp", "ws17_temp", "ws18_temp", "ws19_temp", "ws20_temp"]
    ]
    target = "load_mw"
    cutoff_period = 2024
    train_set = training_dataset[training_dataset["datetime"].dt.year < cutoff_period]
    test_set = training_dataset[training_dataset["datetime"].dt.year >= cutoff_period]

    print("Training Set: ", len(train_set))
    print("Testing Set: ", len(test_set))

    model = GradientBoostingRegressor(
        n_estimators=500, learning_rate=0.1, max_depth=7, random_state=25
    )
    model.fit(train_set[model_features], train_set[target])
    # model = LinearRegression()
    # model.fit(train_set[model_features], train_set[target])

    test_preds = model.predict(test_set[model_features])

    mape = mean_absolute_percentage_error(test_set[target], test_preds)
    print(f"Validation Mape (2024): {mape}")
    return model, model_features


@app.cell
def _(main_dataset, model, model_features, np):
    # 2025 Dataset

    dataset_2025 = main_dataset[main_dataset["datetime"].dt.year == 2025].copy()
    dataset_2025['prev_day_avg_temp'] = dataset_2025['prev_day_avg_temp'].ffill()
    dataset_2025['prev_week_avg_temp'] = dataset_2025['prev_week_avg_temp'].ffill()
    dataset_2025['rolling_avg_temp_6h'] = dataset_2025['rolling_avg_temp_6h'].ffill()
    dataset_2025['rolling_avg_temp_24h'] = dataset_2025['rolling_avg_temp_24h'].ffill()
    dataset_2025["load_mw"] = np.nan
    dataset_2025.reset_index(drop=True, inplace=True)

    preds = model.predict(dataset_2025[model_features])
    dataset_2025.isna().any()
    return dataset_2025, preds


@app.cell
def _(dataset_2025, preds):
    dataset_2025.max()
    preds
    dataset_2025["load_mw"] = preds
    final_2025_results = dataset_2025[["datetime", "load_mw"]]
    final_2025_results['datetime'] = final_2025_results['datetime'].dt.strftime('%Y-%m-%d %H:00:00')
    final_2025_results.rename(columns={'load_mw': 'forecast_load'}, inplace=True)
    final_2025_results.to_csv("JackOfAllTrades.csv", index=False)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
