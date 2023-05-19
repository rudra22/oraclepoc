import pandas as pd
import logging


class Transformer:
    def __init__(self, db_uri, logger: logging):
        self.db_uri = db_uri
        self.logger = logger

    def db_data_pull(self, sql) -> pd.DataFrame:
        try:
            self.logger.info("Pulling data from db ...")
            return pd.read_sql(sql, self.db_uri)
        except Exception as e:
            self.logger.error("Error in data pull. Error msg:{}".format(repr(e)))

    def joiner(self, left_df: pd.DataFrame, right_df: pd.DataFrame, join_type="inner",
               left_key_cols=None, right_key_cols=None) -> pd.DataFrame:
        try:
            if left_key_cols and right_key_cols:
                return left_df.merge(right_df, left_on=left_key_cols, right_on=right_key_cols, how=join_type)
            elif not left_key_cols and not right_key_cols:
                left_df.merge(right_df, how='cross')
            else:
                self.logger.error("Improper join condition. {}-{}".format(left_key_cols, right_key_cols))
                raise "Improper join condition. {}-{}".format(left_key_cols, right_key_cols)
        except Exception as e:
            self.logger.error("Error in joiner. Error msg:{}".format(repr(e)))

    def aggregator(self, df: pd.DataFrame, group_by_cols=None, agg_funcs=None) -> pd.DataFrame:
        if agg_funcs is None:
            agg_funcs = []
        if group_by_cols is None:
            group_by_cols = []

    def filter(self, df: pd.DataFrame, filter_cond=None) -> pd.DataFrame:
        pass

    def db_data_push(self, df: pd.DataFrame, table_name, write_mode="append"):
        try:
            self.logger.info("Writing data to db. Table name: {}".format(table_name))
            df.to_sql(table_name, self.db_uri, if_exists=write_mode)
        except Exception as e:
            self.logger.error("Error in db writing. Error msg:{}".format(repr(e)))
