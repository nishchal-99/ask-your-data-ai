def dataframe_to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")


def sql_to_text_bytes(sql_query):
    return sql_query.encode("utf-8")