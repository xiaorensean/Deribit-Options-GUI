from PyQt5.QtWidgets import QApplication
import matplotlib.pyplot as plt
import numpy as np
import math
import time
import seaborn as sns
import smtplib
import copy
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
#pkg_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
from influxdb_client.influxdb_client_host_1 import InfluxClientHost1
from influxdb_client.influxdb_client_host_2 import InfluxClientHost2
from qt.qt_tables import TableView

def roundup10(x):
    return int(math.ceil(x / 10.0)) * 10


host_1 = InfluxClientHost1()
host_2 = InfluxClientHost2()


data = host_1.query_tables("deribit_optionsTicker",["symbol,open_interest","where time > now() - 1d"])



latest_data_df = data.drop_duplicates(subset = ['symbol'],keep="last").sort_values("symbol")
last_data = data.drop_duplicates(subset = ['symbol'],keep="first").sort_values("symbol")
report = latest_data_df.copy()
report["open_interest_prev_day"] = last_data.open_interest.tolist()
report["open_interest_delta"] = report.open_interest - report.open_interest_prev_day
oi_unit = [i[:3] for i in report.symbol.tolist()]
report['open_interest_unit'] = oi_unit
report = report.sort_values("symbol")
report = report[report.columns.tolist()[1:]]
#%%
symbols = "ETH"
# add filter
btc_data = report[report.open_interest_unit==symbols]
data_points = btc_data.shape[0]
data_points_10 = roundup10(data_points)
x_dim = 10
y_dim = int(data_points_10/x_dim)
symbol_hm = np.asarray(btc_data.symbol.tolist()+["No Data"]*(data_points_10-data_points)).reshape(y_dim,x_dim)
opd_hm = np.asarray(btc_data.open_interest_delta.tolist()+[0]*(data_points_10-data_points)).reshape(y_dim,x_dim)
print(symbol_hm)
print(opd_hm)
hm_data = pd.DataFrame(btc_data.open_interest_delta.tolist()+[0]*(data_points_10-data_points),columns=['open_interest_delta'])
y_rows = []
x_cols = []
for i in range(1,y_dim+1):
    for j in range(1,x_dim+1):
        y_rows.append(i)
        x_cols.append(j)
hm_data['Yrows'] = y_rows
hm_data['Xcols'] = x_cols
hm_data_pivot = hm_data.pivot_table(index="Yrows",columns="Xcols",values="open_interest_delta")

labels = (np.asarray(["{0} \n {1:.2f}".format(symb,value) for symb, value \
                      in zip(symbol_hm.flatten(),opd_hm.flatten())])).reshape(y_dim,x_dim)
fig, ax = plt.subplots(figsize=(32,27))
title = symbols + " Options OI Changes Heatmap"
plt.title(title,fontsize=18)
ttl = ax.title
ttl.set_position([0.5,1.05])
ax.set_xticks([])
ax.set_yticks([])
ax.axis('off')
sns.heatmap(hm_data_pivot,annot=labels,fmt="",cmap="RdYlGn",linewidths=0.30,ax=ax)
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)
#latest_data_array = latest_data_df[["open_interest","volume"]].to_numpy()
#sns.heatmap(btc_hm,annot=True, annot_kws={"size": 11},cmap='PuBu')

#%%
data_gui = {}
for idx in range(labels.shape[1]):
    data_gui.update({str(idx):[str(i) for i in list(labels[:,idx])]})

if __name__ == "__main__":
    app = QApplication(sys.argv)
    table = TableView("BTC Options Table",data_gui, labels.shape[0], labels.shape[1])
    sys.exit(app.exec_())




