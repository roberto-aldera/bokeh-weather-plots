import pytest
import make_weather_plots
import plot_temperature_one_year


def test_make_weather_plots_main(tmp_path):
    """
    Some very basic tests for the bokeh script that just run the
    main with different inputs. Just here to catch obvious errors.
    """
    args = ["--output_dir", tmp_path,
            "--start_year", 2019,
            "--num_years", 2]
    # we need all arguments as strings
    make_weather_plots.main([str(i) for i in args])

    # Should still work even if number of years takes us out of range
    args = ["--output_dir", tmp_path,
            "--start_year", 2019,
            "--num_years", 5]
    make_weather_plots.main([str(i) for i in args])

    # Must catch cases where start year is out of bounds
    with pytest.raises(ValueError):
        args = ["--output_dir", tmp_path,
                "--start_year", 2021]
        make_weather_plots.main([str(i) for i in args])

    with pytest.raises(ValueError):
        args = ["--output_dir", tmp_path,
                "--start_year", 1800]
        make_weather_plots.main([str(i) for i in args])


def test_plot_temperature_one_year_main(tmp_path):
    """
    Some very basic tests for the single-year script that just run the
    main with different inputs. Just here to catch obvious errors.
    """
    args = ["--output_dir", tmp_path,
            "--year", 2020]
    # we need all arguments as strings
    plot_temperature_one_year.main([str(i) for i in args])

    # Must catch cases where year is out of bounds
    with pytest.raises(ValueError):
        args = ["--output_dir", tmp_path,
                "--year", 2021]
        plot_temperature_one_year.main([str(i) for i in args])

    with pytest.raises(ValueError):
        args = ["--output_dir", tmp_path,
                "--year", 1800]
        plot_temperature_one_year.main([str(i) for i in args])
