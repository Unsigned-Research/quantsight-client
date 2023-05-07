[![Publish to PyPI](https://github.com/Unsigned-Research/quantsight-client/actions/workflows/publish-to-pypi.yml/badge.svg?branch=master)](https://github.com/Unsigned-Research/quantsight-client/actions/workflows/publish-to-pypi.yml)
[![PyPI version](https://badge.fury.io/py/quantsight.svg)](https://badge.fury.io/py/quantsight)
[![PyPI version](https://img.shields.io/badge/Quantsight-Visit%20Website-blue.svg)](https://www.quantsight.dev/)
<br />
<br />

<img height="60" src="https://www.quantsight.dev/static/media/trades.2cd0b7149637f5303dd5.png"/>

This is a Python client for the Quantsight Data API, which allows you to fetch historical funding rates, candle data, and perform custom queries from supported exchanges. The client is easy to use and supports fetching data into a Pandas DataFrame for further analysis.

### Key features:


#### ✅ Pull data from API directly as a pandas DataFrame
#### ✅ Automatically cached data for faster retrieval and saved credits
#### ✅ Integrated OpenAI for querying data using natural language prompts


## Installation

To install the Quantsight Data API Python client, use `pip`:

```bash
pip install quantsight
```

## Usage

First, import the `QuantsightDataAPI` class and create an instance with your API key:

```python
import quantsight as qs

api_key = "your_api_key"
qs = qs.Quantsight(api_key)
```

Then, you can use the following methods to fetch data from the Quantsight Data API:

### Get funding rate

To fetch historical funding rates from a supported exchange, use the `get_funding_rate` method:

```python
funding_rate_df = qs.get_funding_rate(
    exchange="okx",
    limit=1e6,
)
```

### Get OHLCV data

To fetch candle data from a supported exchange, use the `get_ohlcv` method:

```python
ohlcv_df = qs.get_ohlcv(
    period="1d",
    exchange="okx",
    limit=1e6,
)
```

### Get OHLCV data around time

To fetch candle data around a specific point in time, use the `get_ohlcv_around_time` method:

```python
ohlcv_around_time_df = qs.get_ohlcv_around_time(
    period="1d",
    exchange="okx",
    target_time=time(9,0,0),
    sample_count=10,
    limit=1e6,
)
```

> Endpoint is useful for execution optimisation or seasonality analysis

### Custom query (BETA)

To perform a custom query, use the `custom_query` method:

```python
custom_query_df = qs.custom_query(
    "SELECT close FROM {{okx.ohlcv.swap.1d}} LIMIT 10", 
    dry_run=True, 
    use_legacy_sql=False
)
```

Each method returns a Pandas DataFrame containing the fetched data.

### Caching

Queries are cached both in BigQuery and on the client side in order to maximise your data allowance.

By default the local cache location is stored next to the clien.py file but you may change it when initialising the 
client:

```python
qs = qs.Quantsight(
    api_key=api_key,
    cache_path=Path("root/your/custom/cache/location")
)
```

You can retrieve cache metadata like so:
```python
qs.read_cache_metadata()
```

You can delete all cache like so:
```python
qs.clear_cache()
```

> Pandas cache is handled by the [data-cache](https://pypi.org/project/data-cache/) library.

## Documentation

The documentation for each endpoints can be found here: https://api.quantsight.dev/docs

## License

This project is licensed under the MIT License. See the [GNU GENERAL PUBLIC LICENSE](LICENSE) file for details.
