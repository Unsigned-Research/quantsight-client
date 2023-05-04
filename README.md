[![Publish to PyPI](https://github.com/Unsigned-Research/quantsight-client/actions/workflows/publish-to-pypi.yml/badge.svg?branch=master)](https://github.com/Unsigned-Research/quantsight-client/actions/workflows/publish-to-pypi.yml)
[![PyPI version](https://badge.fury.io/py/quantsight.svg)](https://badge.fury.io/py/quantsight)
[![PyPI version](https://img.shields.io/badge/Quantsight-Visit%20Website-blue.svg)](https://www.quantsight.dev/)

<img height="60" src="https://www.quantsight.dev/static/media/trades.2cd0b7149637f5303dd5.png"/>

This is a Python client for the Quantsight Data API, which allows you to fetch historical funding rates, candle data, and perform custom queries from supported exchanges. The client is easy to use and supports fetching data into a Pandas DataFrame for further analysis.

### Key features:


#### ✅ Pull data from API directly as a pandas DataFrame
#### ✅ Automatically cached data for faster retrieval and saved credits
#### ✅ Integrated OpenAI for querying data in natural language prompts


## Installation

To install the Quantsight Data API Python client, use `pip`:

```bash
pip install quantsight
```

## Usage

First, import the `QuantsightDataAPI` class and create an instance with your API key:

```python
from quantsight import Quantsight

api_key = "your_api_key"
qs = Quantsight(api_key)
```

Then, you can use the following methods to fetch data from the Quantsight Data API:

### Get funding rate

To fetch historical funding rates from a supported exchange, use the `get_funding_rate` method:

```python
funding_rate_df = qs.get_funding_rate("2010-01-01T00:00:00", "2023-05-04T11:47:20.958631", "okx", 100, "BTC-USD-SWAP")
```

### Get OHLCV data

To fetch candle data from a supported exchange, use the `get_ohlcv` method:

```python
ohlcv_df = qs.get_ohlcv("2010-01-01T00:00:00", "2023-05-04T11:47:20.958631", "okx", "1d", "spot", 100, "BTC-USD-SWAP")
```

### Get OHLCV data around time

To fetch candle data around a specific point in time, use the `get_ohlcv_around_time` method:

```python
ohlcv_around_time_df = qs.get_ohlcv_around_time("2010-01-01T00:00:00+00:00", "2023-05-04T10:47:20.956633+00:00", "okx", "1d", "spot", "00:00:00", 10, 100, "BTC-USD-SWAP")
```

### Custom query (BETA)

To perform a custom query, use the `custom_query` method:

```python
custom_query_df = qs.custom_query("SELECT close FROM {{okx.ohlcv.swap.1d}} LIMIT 10", dry_run=True, use_legacy_sql=False)
```

Each method returns a Pandas DataFrame containing the fetched data.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
