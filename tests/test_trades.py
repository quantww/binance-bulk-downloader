# import standard libraries
import os

# import third party libraries
import pytest

# import my libraries
from binance_bulk_downloader import BinanceBulkDownloader


def dynamic_trades_test_params():
    """
    Generate params for trades tests
    :return:
    """
    assets = list(BinanceBulkDownloader._FUTURES_ASSET + BinanceBulkDownloader._ASSET)
    for asset in assets:
        for data_type in ["trades"]:
            for timeperiod_per_file in ["daily", "monthly"]:
                yield pytest.param(
                    asset,
                    data_type,
                    timeperiod_per_file,
                    id=f"{asset}-{data_type}-{timeperiod_per_file}",
                )


@pytest.mark.parametrize(
    "asset, data_type, timeperiod_per_file",
    dynamic_trades_test_params(),
)
def test_trades(tmpdir, asset, data_type, timeperiod_per_file):
    """
    Test Trades
    :param tmpdir:
    :param asset: asset (spot, um, cm)
    :param data_type: data type (trades)
    :param timeperiod_per_file: time period per file (daily, monthly)
    :return:
    """
    downloader = BinanceBulkDownloader(
        destination_dir=tmpdir,
        asset=asset,
        data_type=data_type,
        timeperiod_per_file=timeperiod_per_file,
    )
    prefix = downloader._build_prefix()
    if timeperiod_per_file == "daily":
        if asset == "spot":
            single_download_prefix = prefix + "/BTCUSDT/BTCUSDT-trades-2021-01-01.zip"
        elif asset == "um":
            single_download_prefix = prefix + "/BTCUSDT/BTCUSDT-trades-2021-01-01.zip"
        elif asset == "cm":
            single_download_prefix = (
                prefix + "/BTCUSD_PERP/BTCUSD_PERP-trades-2021-01-01.zip"
            )
        else:
            raise ValueError(f"asset {asset} is not supported.")
        destination_path = tmpdir.join(single_download_prefix.replace(".zip", ".csv"))
        downloader._download(single_download_prefix)
        # If exists csv file on destination dir, test is passed.
        assert os.path.exists(destination_path)
    elif timeperiod_per_file == "monthly":
        # BTCUSDT monthly data is too large, so use BTCBUSD instead.
        if asset == "spot":
            single_download_prefix = prefix + "/BTCBUSD/BTCBUSD-trades-2021-01.zip"
        elif asset == "um":
            single_download_prefix = prefix + "/BTCBUSD/BTCBUSD-trades-2021-01.zip"
        elif asset == "cm":
            single_download_prefix = (
                prefix + "/BTCUSD_PERP/BTCUSD_PERP-trades-2021-01.zip"
            )
        else:
            raise ValueError(f"asset {asset} is not supported.")
        destination_path = tmpdir.join(single_download_prefix.replace(".zip", ".csv"))
        downloader._download(single_download_prefix)
        # If exists csv file on destination dir, test is passed.
        assert os.path.exists(destination_path)
