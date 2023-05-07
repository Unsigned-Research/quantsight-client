import requests
import pandas as pd
import json
from typing import Optional
from datetime import datetime, timezone, time
from data_cache import pandas_cache, read_metadata
from pathlib import Path
import os
import shutil
from .agent import QueryAgent


class QuantsightClient(QueryAgent):
    def __init__(self, api_key: str, openai_api_key: str = None, cache_path: Path = None, **kwargs):
        super().__init__(openai_api_key, **kwargs)
        self.base_url = "https://api.quantsight.dev"
        self.headers = {"Authorization": f"Bearer {api_key}"}

        file_location = Path(__file__).resolve().parent

        self.cache_path = cache_path
        if self.cache_path is None:
            self.cache_path = file_location
        self.cache_path = self.cache_path / "temp"

        self.cache_path.mkdir(parents=True, exist_ok=True)

        os.environ["CACHE_PATH"] = str(self.cache_path)

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

    def clear_cache(self):
        os.remove(self.cache_path / "data.h5")

    def read_cache_metadata(self):
        return read_metadata(str(self.cache_path / "data.h5"))

    @pandas_cache
    def get_funding_rate(
            self,
            from_ts: datetime = datetime(2010, 1, 1, tzinfo=timezone.utc),
            to_ts: datetime = datetime(2023, 5, 1, tzinfo=timezone.utc),
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
            to_ts: datetime = datetime(2023, 5, 1, tzinfo=timezone.utc),
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

    @pandas_cache
    def get_ohlcv_around_time(
            self,
            from_ts: datetime = datetime(2010, 1, 1, tzinfo=timezone.utc),
            to_ts: datetime = datetime(2023, 5, 1, tzinfo=timezone.utc),
            exchange: str = "okx",
            period: str = "1h",
            instrument: str = "swap",
            target_time: str = time(10, 0, 0),
            sample_count: int = 10,
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
