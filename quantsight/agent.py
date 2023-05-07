import pandas as pd
from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
import logging

logger = logging.getLogger(__name__)


class QueryAgent:

    def __init__(self, openai_api_key: str, gpt_model_name: str = "gpt-3.5-turbo", **kwargs):
        if openai_api_key is not None:
            self.open_api = ChatOpenAI(openai_api_key=openai_api_key, temperature=0, model_name=gpt_model_name)

    def preprocess_df(self, input_df: pd.DataFrame) -> pd.DataFrame:
        logger.info(f"Pre-processing the DataFrame, column names are likely to change.")

        df = input_df.rename(columns={
            'ts': "timestamp",
            'open': "open_price",
            'high': "high_price",
            'low': "low_price",
            'close': "close_price",
        })

        if "timestamp" in df.columns and "ticker" in df.columns:
            df = df[~df.duplicated(subset=["ticker", "timestamp"])]

        if "timestamp" in df.columns:
            df['day_of_week'] = df['timestamp'].dt.day_name()
            df['month'] = df['timestamp'].dt.month_name()
            df['day'] = df['timestamp'].dt.day
            df['year'] = df['timestamp'].dt.year
            df = df.set_index('timestamp').sort_index()
            df['timestamp'] = df.index

        return df

    def llm_query(self, df: pd.DataFrame, query: str, pre_process_df: bool = True):
        if pre_process_df is True:
            df = self.preprocess_df(df.copy())

        agent = create_pandas_dataframe_agent(
            llm=self.open_api,
            df=df,
            verbose=True,
        )

        agent.run(query)
