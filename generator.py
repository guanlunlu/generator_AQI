#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
import operator

class pollution():
    def __init__(self, month, pollution, value) -> None:
        self.month = month
        self.pollution = pollution
        self.value = value
        self.aqi = -1

        # AQI standards
        self.aqi_O3 = [0, 51, 101, 151, 201, 301]
        self.O3_v = [0, 0.055, 0.071, 0.086, 0.106, 0.200]

        self.aqi_v = [0, 51, 101, 151, 201, 301, 401, 500]
        self.pm25_v = [0, 15.5, 35.5, 54.5, 150.5, 250.5, 350.5, 500.4]
        self.pm10_v = [0, 51, 101, 255, 355, 425, 505, 604]
        self.co_v = [0, 4.5, 9.5, 12.5, 15.5, 30.5, 40.5, 50.4]
        self.so2_v = [0, 21, 76, 186, 305, 605, 805, 1004]
        self.no2_v = [0, 31, 101, 361, 650, 1250, 1650, 2049]

        self.getAQI()
        pass

    def getAQI(self):
        if self.pollution == 'O3':
            self.value = self.value / 1000
            aqi = np.interp(self.value, self.O3_v, self.aqi_O3)
        elif self.pollution == 'PM2.5':
            self.value = self.value / 1000
            aqi = np.interp(self.value, self.pm25_v, self.aqi_v)
        elif self.pollution == 'PM10':
            aqi = np.interp(self.value, self.pm10_v, self.aqi_v)
        elif self.pollution == 'CO':
            aqi = np.interp(self.value, self.co_v, self.aqi_v)
        elif self.pollution == 'SO2':
            aqi = np.interp(self.value, self.so2_v, self.aqi_v)
        elif self.pollution == 'NO2':
            aqi = np.interp(self.value, self.no2_v, self.aqi_v)
        self.aqi = aqi
        # self.show()

    def show(self):
        print("Month", self.month, self.pollution, " = ", self.value, "aqi = ", self.aqi)

class month_avg():
    def __init__(self,row,row_idx):
        self.month = row['Month']
        self.o3 = pollution(self.month, 'O3', row['O3'])
        self.pm25 = pollution(self.month, 'PM2.5', row['PM2.5'])
        self.pm10= pollution(self.month, 'PM10', row['PM10'])
        self.co = pollution(self.month, 'CO', row['CO'])
        self.so2 = pollution(self.month, 'SO2', row['SO2'])
        self.no2 = pollution(self.month, 'NO2', row['NO2'])
        self.pollution_List = [self.o3, self.pm25, self.pm10, self.co, self.so2, self.no2]
        month_max_aqi = max(self.pollution_List, key=operator.attrgetter('aqi'))
        self.aqi = month_max_aqi.aqi
        # print("month aqi = ", self.aqi)

if __name__ == "__main__":
    sheetname_list = ['keelung', 'wanlee', 'fukuai', 'salu', 'fengyuan', 'twolin', 'tainan', 'annnan', 'chioutou']
    aqi_dict = {}
    for i in sheetname_list:
        # print("-----------------------------------------------------------")
        # print(i)
        data = pd.read_excel('generator.xls',sheet_name = i)
        df = pd.DataFrame(data, columns=['Month','O3','PM2.5','PM10','CO','SO2','NO2'])
        list_aqi = []
        for index, row in df.iterrows():
            r = month_avg(row, index)
            list_aqi.append(r.aqi)
        df.insert(df.shape[1], "aqi", list_aqi)
        aqi_dict[i] = list_aqi
        # aqi_df.insert(aqi_df.shape[1], i, list_aqi)
        # print (df)
    # print (aqi_dict)
    aqi_df = pd.DataFrame(data=aqi_dict)
    print(aqi_df)
    aqi_df.to_csv('aqi.csv')
    # print(aqi_df)