import pytest
import plot_temperature_one_year


def test_the_main(tmp_path):
    """
    Some very basic tests that just run the main with different inputs.
    Just here to catch obvious errors.
    """
    args = ["--output_dir", tmp_path,
            "--year", 2020]
    args = [str(i) for i in args]  # we need all arguments as strings
    plot_temperature_one_year.main(args)

    # Must catch cases where year is out of bounds
    with pytest.raises(ValueError):
        args = ["--output_dir", tmp_path,
                "--year", 2021]
        # we need all arguments as strings
        plot_temperature_one_year.main([str(i) for i in args])

    with pytest.raises(ValueError):
        args = ["--output_dir", tmp_path,
                "--year", 1800]
        # we need all arguments as strings
        plot_temperature_one_year.main([str(i) for i in args])
