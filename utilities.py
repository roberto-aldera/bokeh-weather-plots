import pandas as pd
import numpy as np


def prepare_weather_dataframe(weather_data: pd.DataFrame) -> pd.DataFrame:
    """
    Amend a dataframe that contains content required for plotting (like the datetime field)
    """
    # Make a datetime column to use as x-index
    weather_data = weather_data.rename(
        columns={"YYYY": "year", "MM": "month", "DD": "day"})
    weather_data["datetime"] = pd.to_datetime(
        weather_data[["day", "month", "year"]])

    weather_data["left"] = weather_data["datetime"] - \
        pd.DateOffset(days=0.5)
    weather_data["right"] = weather_data["datetime"] + \
        pd.DateOffset(days=0.5)

    return weather_data


def get_historical_data(start_year: int, num_years: int,
                        weather_data_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Find record high and low temperatures for every day of the year and store in a dataframe.
    This is not optimised - to deal with leap years and keep the timeline playing nicely,
    we recalculate these for every year that's in the query, effectively duplicating the
    records for each year (instead of being efficient and doing it once - big TODO here.)
    """
    days = []
    months = []
    years = []
    tmax_years = []
    tmax_vals = []
    tmin_years = []
    tmin_vals = []

    for _, the_year in np.ndenumerate(np.arange(start_year, start_year + num_years, 1)):

        for month in range(1, 13):
            weather_data_subset = weather_data_raw[weather_data_raw["MM"]
                                                   == month]

            for day in weather_data_subset[weather_data_subset["YYYY"] == the_year]["DD"]:
                idx_max_temp = weather_data_subset[weather_data_subset["DD"]
                                                   == day]["Tmax °C"].idxmax()
                idx_min_temp = weather_data_subset[weather_data_subset["DD"]
                                                   == day]["Tmin °C"].idxmin()
                days.append(day)
                months.append(month)
                years.append(the_year)
                tmax_years.append(
                    weather_data_subset.loc[idx_max_temp]["YYYY"])
                tmax_vals.append(
                    weather_data_subset.loc[idx_max_temp]["Tmax °C"])
                tmin_years.append(
                    weather_data_subset.loc[idx_min_temp]["YYYY"])
                tmin_vals.append(
                    weather_data_subset.loc[idx_min_temp]["Tmin °C"])

    historical_day_records = pd.DataFrame(
        {"day": days, "month": months, "year": years, "Tmax-year": tmax_years,
         "Tmax-degC": tmax_vals, "Tmin-year": tmin_years, "Tmin-degC": tmin_vals})
    historical_day_records["datetime"] = pd.to_datetime(
        historical_day_records[["day", "month", "year"]])
    historical_day_records["left"] = historical_day_records["datetime"] - \
        pd.DateOffset(days=0.5)
    historical_day_records["right"] = historical_day_records["datetime"] + \
        pd.DateOffset(days=0.5)

    return historical_day_records
