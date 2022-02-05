import pandas as pd
from sqlalchemy import create_engine

disk_engine = create_engine('sqlite:///webserver/subtitles.db')

chunksize = 10 ** 4
for chunk in pd.read_csv('data/subtitles_all.txt', sep='\t', error_bad_lines=False, chunksize=chunksize):
    try:
        chunk.to_sql(name='OpenSubtitles', if_exists='append', con = disk_engine, index=False)
    except Exception as e:
        print(e)