import requests
import pandas as pd
import json
from typing import Optional
from datetime import datetime


class Quantsight:
    def __init__(self, api_key: str):
        self.base_url = "https://api.quantsight.dev"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def _request(
            self,
            endpoint: str,
            payload: dict
    ) -> pd.DataFrame:
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}")

        data = json.loads(response.text)
        return pd.DataFrame(data)

    def get_funding_rate(
            self,
            from_ts: datetime,
            to_ts: datetime,
            exchange: str,
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

    def get_ohlcv(
            self,
            from_ts: datetime,
            to_ts: datetime,
            exchange: str,
            period: str,
            instrument: str,
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
