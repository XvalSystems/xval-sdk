import xval.api as api
import pandas as pd
import json


def data(uuid: str):
	df_data = json.loads(api.get(f"/data/{uuid}/table"))
	df = pd.DataFrame(**{
		'data': df_data['data'],
		'columns': df_data['columns'],
		'index': df_data['index'],
	})
	print(df)


handlers = {
    'data': data,
}