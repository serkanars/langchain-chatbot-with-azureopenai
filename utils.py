from transformers import pipeline
import pyodbc
import pandas as pd
import urllib
from sqlalchemy import create_engine
import tiktoken


def classification(sentence):
    classifier = pipeline("zero-shot-classification",model="facebook/bart-large-mnli")
    candidate_labels = ['yazılım', 'diğer']
    result = classifier(sentence, candidate_labels)
    return result["labels"][0], result["scores"][0]



def sqlInsert(df: pd.DataFrame,table_name: str):

    quoted = urllib.parse.quote_plus("""Driver={SQL Server};
            Server=RPTSERVER;
            Database=DATA_ANALYTICS;
            Trusted_Connection=yes;""")
    
    engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))
    
    df.to_sql(table_name, schema='dbo', con = engine, if_exists = "append",index=False)

    print("INSERT İŞLEMİ BAŞARILI BİR ŞEKİLDE TAMAMLANMIŞTIR.")


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
