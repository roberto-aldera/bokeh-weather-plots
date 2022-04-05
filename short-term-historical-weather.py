import pandas as pd
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import pdb


def get_historical_data(args, weather_data_raw: pd.DataFrame):
    # Find record temperatures
    # Example: find hottest ever Nth of April, then record the temp and also the year in a new table.
    days = []
    months = []
    years = []
    tmax_years = []
    tmax_vals = []
    tmin_years = []
    tmin_vals = []
    selected_year = args.year
    # pdb.set_trace()
    for month in range(1, 13):
        weather_data_subset = weather_data_raw[weather_data_raw["MM"]
                                               == month]

        for day in weather_data_subset[weather_data_subset["YYYY"] == selected_year]["DD"]:
            idx_max_temp = weather_data_subset[weather_data_subset["DD"]
                                               == day]["Tmax °C"].idxmax()
            idx_min_temp = weather_data_subset[weather_data_subset["DD"]
                                               == day]["Tmin °C"].idxmin()
            days.append(day)
            months.append(month)
            years.append(selected_year)
            tmax_years.append(weather_data_subset.loc[idx_max_temp]["YYYY"])
            tmax_vals.append(weather_data_subset.loc[idx_max_temp]["Tmax °C"])
            tmin_years.append(weather_data_subset.loc[idx_min_temp]["YYYY"])
            tmin_vals.append(weather_data_subset.loc[idx_min_temp]["Tmin °C"])

    historical_day_records = pd.DataFrame(
        {"day": days, "month": months, "year": years, "Tmax-year": tmax_years, "Tmax-degC": tmax_vals,
         "Tmin-year": tmin_years, "Tmin-degC": tmin_vals})
    historical_day_records["datetime"] = pd.to_datetime(
        historical_day_records[["day", "month", "year"]])

    return historical_day_records


def prepare_weather_dataframe(args, weather_data_raw: pd.DataFrame):
    # Possible alteration: make this index relevant for current month (perhaps 15 days either side of today?)
    # Crop dataset to cover selected years
    weather_data_subset = weather_data_raw[(
        (weather_data_raw["YYYY"] == args.year))]

    weather_data = weather_data_subset.reset_index(drop=True)

    # Make a datetime column to use as x-index
    weather_data = weather_data.rename(
        columns={"YYYY": "year", "MM": "month", "DD": "day"})
    weather_data["datetime"] = pd.to_datetime(
        weather_data[["day", "month", "year"]])
    # weather_data["datetime"] = weather_data["datetime"].dt.dayofyear # out of use for now

    weather_data["left"] = weather_data["datetime"] - pd.DateOffset(days=0.5)
    weather_data["right"] = weather_data["datetime"] + pd.DateOffset(days=0.5)

    return weather_data


def make_plots(weather_data, historical_day_records, args):
    output_file = "/tmp/weather-data.pdf"
    _, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))
    ax.plot(weather_data["datetime"], weather_data["Daily Tmean °C"], '*-',
            color="tab:blue", label="Mean temp")
    ax.bar(x=historical_day_records["datetime"],
           height=historical_day_records["Tmax-degC"] -
           historical_day_records["Tmin-degC"],
           bottom=historical_day_records["Tmin-degC"],
           width=1.0,
           linewidth=1.0,
           edgecolor="tab:blue",
           facecolor="tab:blue",
           alpha=0.25,
           label="Record temperature")

    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()

    plt.savefig(output_file)
    plt.close()

    print("Plots generated and written to:", output_file)


def main(args):
    print("Running...")

    # Data from https://www.geog.ox.ac.uk/research/climate/rms/daily-data.html
    weather_data_raw = pd.read_csv("daily-data-to-dec-2020.csv")
    # handle non-numeric instances like where data is missing
    weather_data_raw = weather_data_raw.apply(pd.to_numeric, errors="coerce")

    weather_data = prepare_weather_dataframe(args,
                                             weather_data_raw)
    historical_day_records = get_historical_data(args, weather_data_raw)

    make_plots(weather_data, historical_day_records, args)


if __name__ == "__main__":
    parser = ArgumentParser(add_help=False)
    parser.add_argument("--output_dir", type=str, default="",
                        help="Path to folder where outputs will be saved")
    parser.add_argument("--year", type=int, default=2019,
                        help="Year for which to run analysis")
    args = parser.parse_args()

    if args.year < 1815 or args.year > 2020:
        raise ValueError(
            f"Invalid start year: {args.year} - this must be between 1815 and 2020.")

    main(args)
