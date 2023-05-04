import os

import requests
import pandas as pd
import json
from typing import Optional
from datetime import datetime, timezone
from data_cache import pandas_cache
from pathlib import Path
import os


class QuantsightClient:
    def __init__(
            self,
            api_key: str,
            openai_api_key: str = None,
            cache_path: Path = None
    ):
        self.base_url = "https://api.quantsight.dev"
        self.headers = {"Authorization": f"Bearer {api_key}"}

        file_location = Path(__file__).resolve().parent

        if cache_path is None:
            cache_path = file_location

        os.environ["CACHE_PATH"] = str(cache_path)

    def _request(
            self,
            endpoint: str,
            payload: dict
    ) -> pd.DataFrame:
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}: \n {response.json()}")

        data = json.loads(response.text)
        df = pd.DataFrame(data)

        if "ts" in df.columns:
            df['ts'] = pd.to_datetime(df['ts'])

        return df

    @pandas_cache
    def get_funding_rate(
            self,
            from_ts: datetime = datetime(2010, 1, 1, tzinfo=timezone.utc),
            to_ts: datetime = datetime.now(tz=timezone.utc),
            exchange: str = "okx",
            limit: int = 100,
            ticker: Optional[str] = None
    ) -> pd.DataFrame:
        payload = {
            "from_ts": from_ts.isoformat(),
            "to_ts": to_ts.isoformat(),
            "exchange": exchange,
            "limit": limit,
            "ticker": ticker,
        }
        return self._request("/get_funding_rate", payload)

    @pandas_cache
    def get_ohlcv(
            self,
            from_ts: datetime = datetime(2010, 1, 1, tzinfo=timezone.utc),
            to_ts: datetime = datetime.now(tz=timezone.utc),
            exchange: str = "okx",
            period: str = "1d",
            instrument: str = "swap",
            limit: int = 100,
            ticker: Optional[str] = None
    ) -> pd.DataFrame:
        payload = {
            "from_ts": from_ts.isoformat(),
            "to_ts": to_ts.isoformat(),
            "exchange": exchange,
            "period": period,
            "instrument": instrument,
            "limit": limit,
            "ticker": ticker,
        }
        return self._request("/get_ohlcv", payload)

    @pandas_cache
    def get_ohlcv_around_time(
            self,
            from_ts: datetime,
            to_ts: datetime,
            exchange: str,
            period: str,
            instrument: str,
            target_time: str,
            sample_count: int,
            limit: int = 100,
            ticker: Optional[str] = None
    ) -> pd.DataFrame:
        payload = {
            "from_ts": from_ts.isoformat(),
            "to_ts": to_ts.isoformat(),
            "exchange": exchange,
            "period": period,
            "instrument": instrument,
            "target_time": target_time,
            "sample_count": sample_count,
            "limit": limit,
            "ticker": ticker,
        }
        return self._request("/get_ohlcv_around_time", payload)

    @pandas_cache
    def custom_query(
            self,
            query: str,
            dry_run: bool = True,
            use_legacy_sql: bool = False
    ) -> pd.DataFrame:
        payload = {
            "query": query,
            "dry_run": dry_run,
            "use_legacy_sql": use_legacy_sql,
        }
        return self._request("/custom_query", payload)
