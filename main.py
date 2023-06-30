import tkinter as tk
import tkinter.font
import pandas as pd
import numpy as np
import tkinter.ttk as ttk
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import os

font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# dataFrame 영역 -------------------------------------------------------------
data = pd.read_csv('./data/데이터.csv', encoding='cp949')

station_JS = '정선한교'
station_TG = '태곡태양광발전소'
station_SC = '서천태양광발전소'
station_GW1 = '광양항 제1자전거도로 태양광발전소'
station_GW2 = '광양항 제2자전거도로 태양광발전소'
station_GW3 = '광양항 제3자전거도로 태양광발전소'
station_PG = '판교가압장 태양광발전소'
station_YS = '양산 태양광발전소'
station_BD1 = '분당지사 제1호 주차장 태양광발전소'
station_BD2 = '분당지사 제2호 주차장 태양광발전소'

global location_name
# tkinter 영역 -----------------------------------------------------------------
win = tk.Tk()
win.title("태양광 프로젝트")
win.configure(background="grey15")
win.resizable(False, False)
win.iconphoto(False, tk.PhotoImage(file='./image/icon.png'))

# Font ----------------------------------------------
font_title = tk.font.Font(family="페이북 Bold", size=12, weight="bold")
font_frametitle = tk.font.Font(family="페이북 Bold", size=15, weight="bold")
font_frameinfo = tk.font.Font(family="페이북 Bold", size=25, weight="bold")
font_showtime = tk.font.Font(family="페이북 Bold", size=35, weight="bold")

# report --
font_report_top = tk.font.Font(family="페이북 Bold", size=15, weight="bold")


# 함수영역 ------------------------------------------------

# 현재 출력 ---------------------------------------
def outtime():
    location_name = loc_get()
    realTime_value = year_value.get() + "-" + month_value.get() + "-" + day_value.get() + " " + hour_value.get() + ":"
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버팅후 금일발전량']]
    df_time = ddf[ddf['측정일시'].str.contains(realTime_value)]
    df_time = df_time.head(2)
    out_power = (df_time.iloc[1, 1] - df_time.iloc[0, 1]) / 1000  # 앞시간빼기
    out_power = format(out_power, ".2f")
    out_pwgen.configure(text=out_power)


# 시간 출력 ---------------------------------------
def nowtime():
    location_name = loc_get()
    realTime_value = year_value.get() + "-" + month_value.get() + "-" + day_value.get() + " " + str(
        int(hour_value.get()) - 1) + ":"
    realTime_plusvalue = year_value.get() + "-" + month_value.get() + "-" + day_value.get() + " " + hour_value.get() + ":"
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버팅후 금일발전량']]
    df_time = ddf[ddf['측정일시'].str.contains(realTime_value)]
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버팅후 금일발전량']]
    df_time_p = ddf[ddf['측정일시'].str.contains(realTime_plusvalue)]
    now_power = (df_time_p.iloc[0, 1] - df_time.iloc[0, 1]) / 1000  # 앞시간빼기
    now_power = format(now_power, ".2f")
    now_pwgen.configure(text=now_power)


# 0시~ 선택시간 ------------------------------------
def seltime():
    location_name = loc_get()
    realTime_value = year_value.get() + "-" + month_value.get() + "-" + day_value.get() + " " + hour_value.get() + ":"
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버팅후 금일발전량']]
    df_time = ddf[ddf['측정일시'].str.contains(realTime_value)]
    df_time = df_time.head(1)
    today_power = df_time.iloc[0, 1] / 1000  # W(와트) 단위라서 1000나누기
    sel_pwgen.configure(text=today_power)


# 경사 일사량 --------------------------------------
def slope_insol():
    location_name = loc_get()
    realTime_value = year_value.get() + "-" + month_value.get() + "-" + day_value.get() + " " + hour_value.get() + ":"
    df = data
    df = df.set_index('장소', drop=True)
    dfs = df.loc[location_name, ['측정일시', '경사면일사량(인버터단위)']]
    df_time = dfs[dfs['측정일시'].str.contains(realTime_value)]
    df_time = df_time.head(1)
    slope_data = round(df_time.iloc[0, 1], 2)
    slope_figure.configure(text=slope_data)


# 수평 일사량 --------------------------------------
def horizon_insol():
    location_name = loc_get()
    realTime_value = year_value.get() + "-" + month_value.get() + "-" + day_value.get() + " " + hour_value.get() + ":"
    df = data
    df = df.set_index('장소', drop=True)
    dfs = df.loc[location_name, ['측정일시', '수평면일사량(인버터단위)']]
    df_time = dfs[dfs['측정일시'].str.contains(realTime_value)]
    df_time = df_time.head(1)
    horizon_data = round(df_time.iloc[0, 1], 2)
    horizon_figure.configure(text=horizon_data)


# 모듈 온도 -----------------------------------------
def module_temp():
    location_name = loc_get()
    realTime_value = year_value.get() + "-" + month_value.get() + "-" + day_value.get() + " " + hour_value.get() + ":"
    df = data
    df = df.set_index('장소', drop=True)
    dfs = df.loc[location_name, ['측정일시', '모듈온도(인버터단위)']]
    df_time = dfs[dfs['측정일시'].str.contains(realTime_value)]
    df_time = df_time.head(1)
    module_data = round(df_time.iloc[0, 1], 2)
    module_figure.configure(text=module_data)


# 외부 온도 ------------------------------------------
def out_temp():
    location_name = loc_get()
    realTime_value = year_value.get() + "-" + month_value.get() + "-" + day_value.get() + " " + hour_value.get() + ":"
    df = data
    df = df.set_index('장소', drop=True)
    dfs = df.loc[location_name, ['측정일시', '외부온도(인버터단위)']]
    df_time = dfs[dfs['측정일시'].str.contains(realTime_value)]
    df_time = df_time.head(1)
    out_data = round(df_time.iloc[0, 1], 2)
    out_figure.configure(text=out_data)


# 인버터 상태------------------------------------------
def inverter_stat():
    # 인버터전압(R상) ------------------------------------
    df = data
    location_name = loc_get()
    realTime_value = year_value.get() + "-" + month_value.get() + "-" + day_value.get() + " " + hour_value.get() + ":"
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버터전압(R상)']]

    df_head = ddf[ddf['측정일시'].str.contains(realTime_value)]
    df_head = df_head.head(1)
    inverter_voltage_R = (float(df_head['인버터전압(R상)'].values))

    # 인버터전압(S상) ------------------------------------
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버터전압(S상)']]

    df_head = ddf[ddf['측정일시'].str.contains(realTime_value)]
    df_head = df_head.head(1)
    inverter_voltage_S = (float(df_head['인버터전압(S상)'].values))

    # 인버터전압(T상) ------------------------------------
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc['판교가압장 태양광발전소', ['측정일시', '인버터전압(T상)']]

    df_head = ddf[ddf['측정일시'].str.contains(realTime_value)]
    df_head = df_head.head(1)
    inverter_voltage_T = (float(df_head['인버터전압(T상)'].values))

    # 인버터전류(R상) ------------------------------------
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버터전류(R상)']]

    df_head = ddf[ddf['측정일시'].str.contains(realTime_value)]
    df_head = df_head.head(1)
    inverter_current_R = (float(df_head['인버터전류(R상)'].values))

    # 인버터전류(S상) ------------------------------------
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버터전류(S상)']]

    df_head = ddf[ddf['측정일시'].str.contains(realTime_value)]
    df_head = df_head.head(1)
    inverter_current_S = (float(df_head['인버터전류(S상)'].values))

    # 인버터전류(T상) ------------------------------------
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버터전류(T상)']]

    df_head = ddf[ddf['측정일시'].str.contains(realTime_value)]
    df_head = df_head.head(1)
    inverter_current_T = (float(df_head['인버터전류(T상)'].values))

    # 인버터 주파수 ------------------------------------
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버터주파수']]

    df_head = ddf[ddf['측정일시'].str.contains(realTime_value)]
    df_head = df_head.head(1)
    inverter_frequency = (float(df_head['인버터주파수'].values))

    # 인버터 주파수 ------------------------------------
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버팅후 금일발전량']]

    df_head = ddf[ddf['측정일시'].str.contains(realTime_value)]
    df_head = df_head.head(1)
    inverter_pwgen = (float(df_head['인버팅후 금일발전량'].values))

    circle = tkinter.font.Font(family="Malgun Gothic", size=20)
    if (inverter_pwgen > 0):
        r_label6.configure(text='●', fg='green', font=circle)
        t_label6.configure(text='●', fg='green', font=circle)
        s_label6.configure(text='●', fg='green', font=circle)
    else:
        r_label6.configure(text='●', fg='red', font=circle)
        t_label6.configure(text='●', fg='red', font=circle)
        s_label6.configure(text='●', fg='red', font=circle)

    inverter_stat = pd.DataFrame({'인버터전압': [inverter_voltage_R, inverter_voltage_T, inverter_voltage_S],
                                  '인버터전류': [inverter_current_R, inverter_current_T, inverter_current_S],
                                  '인버터주파수': [inverter_frequency, inverter_frequency, inverter_frequency],
                                  '인버팅후 금일발전량': [inverter_pwgen, inverter_pwgen, inverter_pwgen]},
                                 index=['R상', 'T상', 'S상'])

    r_label2.configure(text=inverter_voltage_R)
    r_label3.configure(text=inverter_current_R)
    r_label4.configure(text=inverter_frequency)
    r_label5.configure(text=inverter_pwgen)
    t_label2.configure(text=inverter_voltage_T)
    t_label3.configure(text=inverter_current_T)
    t_label4.configure(text=inverter_frequency)
    t_label5.configure(text=inverter_pwgen)
    s_label2.configure(text=inverter_voltage_S)
    s_label3.configure(text=inverter_current_S)
    s_label4.configure(text=inverter_frequency)
    s_label5.configure(text=inverter_pwgen)


# 현재 출력 프로그레스바 ----------------------------------------------
def now_progressbar():
    # 금일 발전량 값 ------------------------------------------------------
    location_name = loc_get()
    realTime_value = year_value.get() + "-" + month_value.get() + "-" + day_value.get()
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버팅후 금일발전량']]
    df_time = ddf[ddf['측정일시'].str.contains(realTime_value)]
    df_time = df_time.tail(1)
    none_power = df_time.iloc[0, 1] / 1000  # W(와트) 단위라서 1000나누기
    none_power = format(none_power, ".2f")
    none_progressbar.configure(value=none_power)
    none_progressbar.configure(maximum=none_power)

    # 0시~ 선택시간 값 __________________________________________________
    location_name = loc_get()
    realTime_value = year_value.get() + "-" + month_value.get() + "-" + day_value.get() + " " + hour_value.get() + ":"
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버팅후 금일발전량']]
    df_time = ddf[ddf['측정일시'].str.contains(realTime_value)]
    df_time = df_time.head(1)
    select_power = df_time.iloc[0, 1] / 1000  # W(와트) 단위라서 1000나누기
    select_progressbar.configure(value=select_power)
    select_progressbar.configure(maximum=none_power)


# 비교 그래프 ------------------------------------------------
# 금일 발전량 그래프 -------------------------------
def none_graph():
    realTime_value = year_value.get() + "-" + month_value.get() + "-" + day_value.get() + " "
    label1, value1 = graph_input(loc_get(), realTime_value)
    value1 = list(map(int, value1))
    label1 = list(map(int, label1))
    ax1.cla()
    ax1.tick_params(width=0)  # 눈금선 제거
    ax1.tick_params(colors='white')  # 눈금 색
    ax1.set_facecolor('#233446')
    ax1.bar(label1, value1, color='mediumspringgreen')
    ax1.set_title('금일발전량', color='white')
    canvas.draw()


# 전일금일비교 그래프 -------------------------------
def ejo_and_none_graph():
    realTime_value = year_value.get() + "-" + month_value.get() + "-" + day_value.get() + " "
    if int(day_value.get()) < 11:
        ejoTime_value = year_value.get() + "-" + month_value.get() + "-" + "0" + str(int(day_value.get()) - 1) + " "
    else:
        ejoTime_value = year_value.get() + "-" + month_value.get() + "-" + str(int(day_value.get()) - 1) + " "
    label1, value1 = graph_input(loc_get(), realTime_value)
    label2, value2 = graph_input(loc_get(), ejoTime_value)
    value1 = list(map(int, value1))
    label1 = list(map(int, label1))
    value2 = list(map(int, value2))
    label2 = list(map(int, label2))
    label1 = np.array(label1)
    label2 = np.array(label2)
    ax2.cla()
    bar_width = 0.2
    width = 0.4
    none = ax2.bar(label1 - bar_width, value1, width, color='mediumspringgreen')
    ejo = ax2.bar(label2 + bar_width, value2, width, color='lightskyblue')
    ax2.set_title('전일금일비교그래프', color='white')
    ax2.legend((none, ejo), ('금일', '전일'))
    ax2.set_xticks(label1)
    ax2.set_facecolor('#233446')
    ax2.tick_params(width=0)  # 눈금선 제거
    ax2.tick_params(colors='white')  # 눈금 색
    canvas.draw()


# 금일 발전량 ------------------------------------------------
def none_powergen():
    location_name = loc_get()
    realTime_value = year_value.get() + "-" + month_value.get() + "-" + day_value.get()
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버팅후 금일발전량']]
    df_time = ddf[ddf['측정일시'].str.contains(realTime_value)]
    df_time = df_time.tail(1)
    global none_powergen_figure    
    none_powergen_figure = df_time.iloc[0, 1] / 1000  # W(와트) 단위라서 1000나누기
    none_powergen_figure = format(none_powergen_figure, ".2f")
    none_pwgen.configure(text=none_powergen_figure)


# 전일 발전량 ------------------------------------------------
def ejo_powergen():
    location_name = loc_get()
    if int(day_value.get()) < 11:
        beforeTime_value = year_value.get() + "-" + month_value.get() + "-" + "0" + str(int(day_value.get()) - 1)
    else:
        beforeTime_value = year_value.get() + "-" + month_value.get() + "-" + str(int(day_value.get()) - 1)
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버팅후 금일발전량']]
    df_time = ddf[ddf['측정일시'].str.contains(beforeTime_value)]
    df_time = df_time.tail(1)
    global ejo_powergen_figure
    try:
        ejo_powergen_figure = df_time.iloc[0, 1] / 1000  # W(와트) 단위라서 1000나누기
    except IndexError:
        ejo_powergen_figure = 0
    ejo_powergen_figure = format(ejo_powergen_figure, ".2f")
    ejo_pwgen.configure(text=ejo_powergen_figure)


# 전일 대비 증가량
def increase_powergen():
    increase_powergen = round((float(none_powergen_figure) - float(ejo_powergen_figure)), 2)
    if (increase_powergen > 0):
        increase_powergen = '+' + str(round((float(none_powergen_figure) - float(ejo_powergen_figure)), 2))
    increase_pwgen.configure(text=increase_powergen)


# 금일 발전시간 ------------------------------------------------
def none_powergen_time():
    location_name = loc_get()
    realTime_value = year_value.get() + "-" + month_value.get() + "-" + day_value.get()
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버팅후 금일발전량']]
    df_time = ddf[ddf['측정일시'].str.contains(realTime_value)]
    for i in df_time['인버팅후 금일발전량']:
        if i != 0:
            start_pw = i
            break
    time_df = df_time.set_index('인버팅후 금일발전량', drop=True)

    start_time = time_df.loc[start_pw].values
    for a in start_time:
        start_time = a
    final_time = time_df.tail(1)
    final_time = final_time.index.values
    final_time = time_df.loc[final_time]
    final_time = final_time.head(1).values
    for b in final_time:
        final_time = b
    for c in final_time:
        final_time = c
    # start_time 문자열 분류
    a1 = start_time
    try:
        b1 = a1.split()
    except AttributeError:
        a1 = a1[0]
        b1 = a1.split()
    c1 = b1[1]
    d1 = c1.split(':')
    e1 = d1[0]
    start_time = e1

    # final_time 문자열 분류
    a2 = final_time
    b2 = a2.split()
    c2 = b2[1]
    d2 = c2.split(':')
    e2 = d2[0]
    final_time = e2

    time_figure = int(final_time) - int(start_time)
    none_pwgen_time.configure(text=time_figure)


# 전일 발전시간 ------------------------------------------------
def ejo_powergen_time():
    location_name = loc_get()
    if int(day_value.get()) < 11:
        beforeTime_value = year_value.get() + "-" + month_value.get() + "-" + "0" + str(int(day_value.get()) - 1)
    else:
        beforeTime_value = year_value.get() + "-" + month_value.get() + "-" + str(int(day_value.get()) - 1)
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버팅후 금일발전량']]
    df_time = ddf[ddf['측정일시'].str.contains(beforeTime_value)]
    global start_pw
    for i in df_time['인버팅후 금일발전량']:
        if i != 0:
            start_pw = i
            break

    try:
        start_pw = start_pw
        time_df = df_time.set_index('인버팅후 금일발전량', drop=True)
        start_time = time_df.loc[start_pw].values
        for a in start_time:
            start_time = a

        final_time = time_df.tail(1)
        final_time = final_time.index.values
        final_time = time_df.loc[final_time]
        final_time = final_time.head(1).values
        for b in final_time:
            final_time = b
        for c in final_time:
            final_time = c

        # start_time 문자열 분류
        a1 = start_time
        try:
            b1 = a1.split()
        except AttributeError:
            a1 = a1[0]
            b1 = a1.split()
        c1 = b1[1]
        d1 = c1.split(':')
        e1 = d1[0]
        start_time = e1

        # final_time 문자열 분류
        a2 = final_time
        b2 = a2.split()
        c2 = b2[1]
        d2 = c2.split(':')
        e2 = d2[0]
        final_time = e2

        time_figure = int(final_time) - int(start_time)
        ejo_pwgen_time.configure(text=time_figure)
    except NameError:
        ejo_pwgen_time.configure(text='0')




# 장소 변환 함수
def loc_get():
    location_ac = location_value.get()
    if location_ac == '정선한교':
        location_name = station_JS
    elif location_ac == '태곡발전소':
        location_name = station_TG
    elif location_ac == '서천발전소':
        location_name = station_SC
    elif location_ac == '제1광양항':
        location_name = station_GW1
    elif location_ac == '제2광양항':
        location_name = station_GW2
    elif location_ac == '제3광양항':
        location_name = station_GW3
    elif location_ac == '판교발전소':
        location_name = station_PG
    elif location_ac == '양산발전소':
        location_name = station_YS
    elif location_ac == '제1분당':
        location_name = station_BD1
    elif location_ac == '제2분당':
        location_name = station_BD2
    return location_name


def selectdate():
    startendhour.configure(text="0시 ~ " + hour_value.get() + "시")
    seldate_showtimeLabel.configure(
        text=year_value.get() + "년 " + month_value.get() + "월 " + day_value.get() + "일 " + hour_value.get() + "시 ")
    # 시간 get()
    realTime_value = year_value.get() + "-" + month_value.get() + "-" + day_value.get() + " " + hour_value.get() + ":"
    hourafterTime_value = year_value.get() + "-" + month_value.get() + "-" + day_value.get() + " " + str(
        int(hour_value.get()) + 1) + ":"
    # for i in range(1, 70):
    #     time.sleep(0.0001)
    #     inverter_gauge.set(i)
    #     inverter_progressbar.update()
    # for k in range(1, 80):
    #     time.sleep(0.0001)
    #     dc_gauge.set(k)
    #     dc_progressbar.update()
    # for j in range(1, 50):
    #     time.sleep(0.0001)
    #     ac_gauge.set(j)
    #     ac_progressbar.update()


def report_btn():
    # 보고서 액티비티 ------------------------------------------------------------------------------------------------
    report = tk.Tk()
    report.title("Report")
    report.configure(background="#233446")

    report.rowconfigure(0, weight=1)
    report.rowconfigure(1, weight=40)

    # Home버튼 함수

    def home_btn():
        report.destroy()

    # title(row =0) --------------------------
    title_Frame = tk.Frame(report)
    title_Frame.configure(background="grey15")

    # title Frame column 가중치
    title_Frame.columnconfigure(0, weight=1)

    # title f ont 설정
    # font 설정------------------------------------
    font_title = tk.font.Font(family="ArialBD", size=12, weight="bold")

    title = tk.Label(title_Frame, text="EO태양광", font=font_title, anchor='e', fg='white', bg='grey15')
    title.grid(row=0, column=0, sticky="w")
    title_Frame.grid(row=0, column=0, sticky="SNEW")

    # 보고서 프레임
    regraph_Frame = tk.Frame(report)
    regraph_Frame.configure(background="#233446")
    regraph_Frame.columnconfigure(0, weight=1)
    regraph_Frame.grid(row=1, column=0, sticky="NSEW")
    # 보고서 그래프 ----------------------------------------------------
    df = data
    ddf = df.loc[:, ['장소', '측정일시', '인버팅후 금일발전량']]
    ddf = ddf.astype({'측정일시': 'datetime64'})
    ddf_week = [g for n, g in ddf.set_index('측정일시').groupby(pd.Grouper(freq='W'))]
    week_1 = ddf_week[0]
    week_2 = ddf_week[1]
    week_3 = ddf_week[2]
    week_4 = ddf_week[3]
    week_5 = ddf_week[4]
    w1 = week_1.groupby(pd.Grouper(key='장소')).mean() / 1000
    w2 = week_2.groupby(pd.Grouper(key='장소')).mean() / 1000
    w3 = week_3.groupby(pd.Grouper(key='장소')).mean() / 1000
    w4 = week_4.groupby(pd.Grouper(key='장소')).mean() / 1000
    w5 = week_5.groupby(pd.Grouper(key='장소')).mean() / 1000

    max1 = w1['인버팅후 금일발전량'].max()
    min1 = w1['인버팅후 금일발전량'].min()
    mean1 = w1['인버팅후 금일발전량'].mean()

    max2 = w2['인버팅후 금일발전량'].max()
    min2 = w2['인버팅후 금일발전량'].min()
    mean2 = w2['인버팅후 금일발전량'].mean()

    max3 = w3['인버팅후 금일발전량'].max()
    min3 = w3['인버팅후 금일발전량'].min()
    mean3 = w3['인버팅후 금일발전량'].mean()

    max4 = w4['인버팅후 금일발전량'].max()
    min4 = w4['인버팅후 금일발전량'].min()
    mean4 = w4['인버팅후 금일발전량'].mean()

    max5 = w5['인버팅후 금일발전량'].max()
    min5 = w5['인버팅후 금일발전량'].min()
    mean5 = w5['인버팅후 금일발전량'].mean()

    weekk = ['8월 5주', '8월 4주', '8월 3주', '8월 2주', '8월 1주']
    maxx = [max1, max2, max3, max4, max5]
    minn = [min1, min2, min3, min4, min5]
    meann = [mean1, mean2, mean3, mean4, mean5]

    fig = plt.figure(figsize=(20, 8), facecolor="#233446")  # matplot 생성
    ax1 = plt.subplot(1, 2, 1)  # 서브플라트1 생성 2x1크기의 1번째부분 1행1열

    y = np.arange(len(weekk))

    ax1.barh(y + 0.15, maxx, label='최대 발전량', height=0.3, color='mediumspringgreen')  # 막대그래프그리기
    ax1.barh(y - 0.15, meann, label='평균 발전량', height=0.3, color='lightskyblue')
    ax1.set_yticks(y)
    ax1.set_yticklabels(weekk)
    ax1.set_title("EO 태양광 2021년 8월 주차별 발전량 보고서(최대)", fontsize=20, color="white")
    ax1.legend()
    ax1.set_ylabel('주차', fontsize=15, color="white")
    ax1.set_xlabel('발전량(kWh)', color="white")
    ax1.set_xlim(0, 7000)
    ax1.set_facecolor('#233446')
    ax1.tick_params(width=0)  # 눈금선 제거
    ax1.tick_params(colors='white')  # 눈금 색
    ax1.tick_params(labelsize=20)

    ax2 = plt.subplot(1, 2, 2)  # 서브플라트1 생성 2x1크기의 1번째부분 1행1열

    y = np.arange(len(weekk))
    ax2.barh(y, minn, label='최소 발전량', height=0.3, color='violet')  # 막대그래프그리기
    ax2.set_yticks(y)
    ax2.set_yticklabels(weekk)
    ax2.set_title("EO 태양광 2021년 8월 주차별 발전량 보고서(최소)", fontsize=20, color="white")
    ax2.legend()
    ax2.set_ylabel('주차', fontsize=15, color="white")
    ax2.set_xlabel('발전량(kWh)', color="white")
    ax2.set_xlim(0, 0.1)
    ax2.set_facecolor('#233446')
    ax2.tick_params(width=0)  # 눈금선 제거
    ax2.tick_params(colors='white')  # 눈금 색
    ax2.tick_params(labelsize=20)

    canvas = FigureCanvasTkAgg(fig, master=regraph_Frame)  # tkinter label 넣듯이 master에 부모 넣어주고 fig에 그래프넣어주면됨
    canvas.draw()  # matplot을 그려주는 함수
    canvas.get_tk_widget().grid(row=3, column=0, ipadx=40, ipady=20)  # matplot위치 라벨 grid랑 똑같음

    report.mainloop()


# 엑셀 열기
def excel_open():
    folder = os.getcwd()  # 현재 경로 얻어오기
    folder = folder + '\data\데이터.csv'  # 현재경로에서 데이터 파일 위치 추가해주기
    os.startfile(folder)  # 실행


def graph_input(loc, time_):
    # Graph Default Value
    location_name = loc
    realTime_value = time_
    # none power
    time_list1 = []
    for i in range(1, 23):
        time_list1.append((realTime_value) + str(i) + (':'))
    df = data
    df = df.set_index('장소', drop=True)
    ddf = df.loc[location_name, ['측정일시', '인버팅후 금일발전량']]
    df_time = ddf[ddf['측정일시'].str.contains(realTime_value)]

    pw1 = []
    values1 = []
    first_time = df_time['인버팅후 금일발전량'].head(1).values

    for j in first_time:
        first_time = j
    for k in time_list1:
        first_time = ddf[ddf['측정일시'].str.contains(k)]
        invert_pw1 = first_time['인버팅후 금일발전량'].head(1).values

        for j in invert_pw1:
            invert_pw1 = j
            pw1.append(invert_pw1)

    for p in range(0, len(pw1) - 1):
        values1.append((pw1[p + 1] - pw1[p]) / 1000)

    sel_pw = values1
    X = np.arange(len(sel_pw))
    x_ticks = [str(x) for x in range(1, len(sel_pw) + 1)]
    x = ['Col A', 'Col B', 'Col C']
    y = [50, 20, 80]
    x2 = ['Col A', 'Col B', 'Col C']
    y2 = [70, 40, 30]

    return x_ticks, values1


# win weight
win.columnconfigure(0, minsize=1500, weight=1)
win.rowconfigure(0, minsize=20, weight=1)
win.rowconfigure(1, minsize=20, weight=1)
win.rowconfigure(2, minsize=100, weight=2)
win.rowconfigure(3, minsize=300, weight=4)
win.rowconfigure(4, minsize=160, weight=3)
win.rowconfigure(5, minsize=100, weight=2)

# info-----------------------------------------------------
info = tk.Frame(win)
info.configure(background="grey15")

# CI
ci = tk.Label(text="(주)EO태양광", font=font_title, fg='white', bg='grey15')
ci.grid(row=0, column=0, sticky="w", padx=3, pady=3)

info.grid(row=0, column=1)

# topmenu (column =0 )---------------------------------------------------
topmenu = tk.Frame(win)
topmenu.configure(background="grey15", )

# topmenu row 가중치
topmenu.rowconfigure(0, weight=1)
# topmenu column 가중치
topmenu.columnconfigure(0, weight=0)
topmenu.columnconfigure(1, weight=1)
topmenu.columnconfigure(2, weight=1)
# topmenu.columnconfigure(3, weight=1)

# 홈버튼 ---------------------------------------------------
home_icon_link = tk.PhotoImage(file="./image/홈.png").subsample(8)
home_btn = tk.Button(topmenu, text="ㅁ", image=home_icon_link, width=40, background='#2A3747', bd=0, fg='turquoise1',
                     font=font_title)
home_btn.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)
# 보고서 ---------------------------------------------------
top1_btn = tk.Button(topmenu, text="보고서", background='#2A3747', bd=0, fg='turquoise1', font=font_title,
                     command=report_btn)
top1_btn.grid(row=0, column=1, sticky="nsew", padx=3, pady=3)
# 엑셀데이터 열기 ---------------------------------------------------
top2_btn = tk.Button(topmenu, text="엑셀데이터 열기", background='#2A3747', bd=0, fg='turquoise1', font=font_title,
                     command=excel_open)
top2_btn.grid(row=0, column=2, sticky="nsew", padx=3, pady=3)
# # 보고서 ---------------------------------------------------
# top3_btn = tk.Button(topmenu, text="보고서", background='#2A3747', bd=0, fg='turquoise1', font=font_title,
#                      command=report_btn)
# top3_btn.grid(row=0, column=3, sticky="nsew", padx=3, pady=3)

topmenu.grid(row=1, sticky="nsew")

# seldatemenu (column = 1)----------------------------------------------
seldatemenu = tk.Frame(win)
seldatemenu.configure(background="grey15")

# seldatemenu row 가중치
seldatemenu.rowconfigure(0, weight=1)
# seldatemenu column
seldatemenu.columnconfigure(0, weight=23)
seldatemenu.columnconfigure(1, weight=23)
seldatemenu.columnconfigure(2, weight=23)
seldatemenu.columnconfigure(3, weight=30)

# 현재출력 프레임-------------------------------------------
output_frame = tk.Frame(seldatemenu)
output_frame.configure(background="#233446")

# 현재출력 프레임 column 가중치
output_frame.columnconfigure(0, weight=3)
output_frame.columnconfigure(1, weight=6)
output_frame.columnconfigure(2, weight=1)

output_icon_link = tk.PhotoImage(file="./image/현재출력.png").subsample(2)
icon = tk.Label(output_frame, image=output_icon_link, bg="#233446")
icon.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
info_text = tk.Label(output_frame, text="현재 출력", font=font_frametitle, bg="#233446", fg="green yellow")
info_text.grid(row=0, column=1, sticky="w", padx=5, pady=5)
out_pwgen = tk.Label(output_frame, text="0", font=font_frameinfo, bg="#233446", fg="white")
out_pwgen.grid(row=1, column=1, sticky="e", padx=5, pady=5)
info_text = tk.Label(output_frame, text="kw", font=font_frametitle, bg="#233446", fg="green yellow")
info_text.grid(row=1, column=2, sticky="w", padx=5, pady=5)

output_frame.grid(column=0, row=0, sticky="nsew", padx=3, pady=3)

# 시간 출력 프레임 ---------------------------------------------------
showtime_frame = tk.Frame(seldatemenu)
showtime_frame.configure(background="#233446")

# 시간 출력 프레임 column 가중치
showtime_frame.columnconfigure(0, weight=3)
showtime_frame.columnconfigure(1, weight=6)
showtime_frame.columnconfigure(2, weight=1)

showtime_icon_link = tk.PhotoImage(file="./image/시간출력.png").subsample(2)
icon = tk.Label(showtime_frame, image=showtime_icon_link, bg="#233446")
icon.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
info_text = tk.Label(showtime_frame, text="시간 출력", font=font_frametitle, bg="#233446", fg="cyan3")
info_text.grid(row=0, column=1, sticky="w", padx=5, pady=5)
now_pwgen = tk.Label(showtime_frame, text="0", font=font_frameinfo, bg="#233446", fg="white")
now_pwgen.grid(row=1, column=1, sticky="e", padx=5, pady=5)
info_text = tk.Label(showtime_frame, text="kwh", font=font_frametitle, bg="#233446", fg="cyan3")
info_text.grid(row=1, column=2, sticky="w", padx=5, pady=5)

showtime_frame.grid(row=0, column=1, sticky="nsew", padx=3, pady=3)

# 0시~선택시간 프레임 ---------------------------------------------------
timestat_Frame = tk.Frame(seldatemenu)
timestat_Frame.configure(background="#233446")

# 시간 출력 프레임 column 가중치
timestat_Frame.columnconfigure(0, weight=4)
timestat_Frame.columnconfigure(1, weight=5)
timestat_Frame.columnconfigure(2, weight=1)

timestat_icon_link = tk.PhotoImage(file="./image/시간선택.png").subsample(2)
icon = tk.Label(timestat_Frame, image=timestat_icon_link, bg="#233446")
icon.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
startendhour = tk.Label(timestat_Frame, text="0시 ~ 선택시간", font=font_frametitle, bg="#233446", fg="cyan3")
startendhour.grid(row=0, column=1, sticky="w", padx=5, pady=5)
sel_pwgen = tk.Label(timestat_Frame, text="0", font=font_frameinfo, bg="#233446", fg="white")
sel_pwgen.grid(row=1, column=1, sticky="e", padx=5, pady=5)
info_text = tk.Label(timestat_Frame, text="kwh", font=font_frametitle, bg="#233446", fg="cyan3")
info_text.grid(row=1, column=2, sticky="w", padx=5, pady=5)

timestat_Frame.grid(row=0, column=2, sticky="nsew", padx=3, pady=3)

# 시간 선택 프레임 ---------------------------------------------------
seldate_Frame = tk.Frame(seldatemenu, bg="#233446")

seldate_Frame.columnconfigure(0, weight=1)
# 시간 콤보박스 프레임
seldate_select = tk.Frame(seldate_Frame, bg="#233446")

seldate_select.columnconfigure(0, weight=1)

# Combobox Value-------------------------
location_value = StringVar()
year_value = StringVar()
month_value = StringVar()
day_value = StringVar()
hour_value = StringVar()

# 시간보이기 프레임-----------------------------------------------

seldate_showtimeLabel = tk.Label(seldate_Frame, text="2020년 00월 00일 00시 ", bg="#233446", fg="white", font=font_showtime)
seldate_showtimeLabel.grid(row=0, sticky="e", padx=30)

seldate_combo_Frame = tk.Frame(seldate_select, bg="#233446")
year = ttk.Combobox(seldate_combo_Frame, width=4, textvariable=year_value, values=["2020", "2021"])
year.current(1)
year.grid(row=1, column=0)
year_text = tk.Label(seldate_combo_Frame, text="년", width=1, font=font_title, bg="#233446", fg="white")
year_text.grid(row=1, column=1)
month = ttk.Combobox(seldate_combo_Frame, width=2, textvariable=month_value,
                     values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
month.current(7)
month.grid(row=1, column=2)
year_text = tk.Label(seldate_combo_Frame, text="월", width=1, font=font_title, bg="#233446", fg="white")
year_text.grid(row=1, column=3)
day = ttk.Combobox(seldate_combo_Frame, width=2, textvariable=day_value,
                   values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15",
                           "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
                           "31"])
day.current(0)
day.grid(row=1, column=4)
year_text = tk.Label(seldate_combo_Frame, text="일", width=1, font=font_title, bg="#233446", fg="white")
year_text.grid(row=1, column=5)
hour = ttk.Combobox(seldate_combo_Frame, width=2, textvariable=hour_value,
                    values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17",
                            "18", "19", "20", "21", "22", "23", "24"])
hour.current(0)
hour.grid(row=1, column=6)
year_text = tk.Label(seldate_combo_Frame, text="시", width=1, font=font_title, bg="#233446", fg="white")
year_text.grid(row=1, column=7)
location = ttk.Combobox(seldate_combo_Frame, width=8, textvariable=location_value,
                        values=["정선한교", "태곡발전소", "서천발전소", "제1광양항", "제2광양항", "제3광양항", "판교발전소", "양산발전소", "제1분당", "제2분당"])
location.current(0)
location.grid(row=1, column=8)
button = tk.Button(seldate_combo_Frame, text="click",
                   command=lambda: [selectdate(), seltime(), nowtime(), outtime(), slope_insol(), horizon_insol(),
                                    module_temp(), out_temp(), none_powergen_time(), none_powergen(), ejo_powergen(),
                                    ejo_powergen_time(), increase_powergen(), ejo_and_none_graph(), none_graph(),
                                    now_progressbar(), inverter_stat()],
                   bg="#2f3640", fg="white", bd=1)
button.grid(row=1, column=9)
seldate_combo_Frame.grid(row=1, column=0, sticky="e")

seldate_select.grid(column=0, row=1, sticky="nsew")

seldate_Frame.grid(row=0, column=3, sticky="nsew", padx=3, pady=3)

seldatemenu.grid(row=2, sticky="nsew")

# detail_info (column = 2)---------------------------------------------
detail_info = tk.Frame(win)
detail_info.configure(background="grey15")

# detail_info row 가중치
detail_info.rowconfigure(0, weight=1)
# detail_info column 가중치
detail_info.columnconfigure(0, weight=5)
detail_info.columnconfigure(1, weight=95)

# info_btn_frame -> 버튼 프레임 부분 ---------------------------------------------
info_label_frame = tk.Frame(detail_info)
info_label_frame.configure(background="grey15")

# info_btn_frame column 가중치
info_label_frame.columnconfigure(0, weight=1)

# info_btn_frame row 가중치
info_label_frame.rowconfigure(0, weight=1)
info_label_frame.rowconfigure(1, weight=1)
info_label_frame.rowconfigure(2, weight=1)
info_label_frame.rowconfigure(3, weight=1)

# 경사일사량 프레임 ---------------------------------------------
slope_frame = tk.Frame(info_label_frame)
slope_frame.configure(background="#2A3747")

# 경사일사량 UI column 가중치
slope_frame.columnconfigure(0, weight=3)
slope_frame.columnconfigure(1, weight=6)
slope_frame.columnconfigure(2, weight=1)

slope_icon_link = tk.PhotoImage(file="./image/경사 일사량.png").subsample(2)
icon = tk.Label(slope_frame, image=slope_icon_link, bg="#2A3747")
icon.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
info_text = tk.Label(slope_frame, text="경사 일사량", font=font_frametitle, bg="#2A3747", fg="turquoise1")
info_text.grid(row=0, column=1, sticky="ws", padx=5, pady=5)
slope_figure = tk.Label(slope_frame, text="0.0", font=font_frameinfo, bg="#2A3747", fg="white")
slope_figure.grid(row=1, column=1, sticky="e", padx=5)
info_text = tk.Label(slope_frame, text="W/m", font=font_frametitle, bg="#2A3747", fg="turquoise1")
info_text.grid(row=1, column=2, sticky="w", padx=5, pady=5)

slope_frame.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)
# 수평일사량 프레임 ---------------------------------------------
horizon_frame = tk.Frame(info_label_frame)
horizon_frame.configure(background="#2A3747")

# 수평일사량 UI column 가중치
horizon_frame.columnconfigure(0, weight=3)
horizon_frame.columnconfigure(1, weight=6)
horizon_frame.columnconfigure(2, weight=1)

horizon_icon_link = tk.PhotoImage(file="./image/수평 일사량.png").subsample(2)
icon = tk.Label(horizon_frame, image=horizon_icon_link, bg="#2A3747")
icon.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
info_text = tk.Label(horizon_frame, text="수평 일사량", font=font_frametitle, bg="#2A3747", fg="turquoise1")
info_text.grid(row=0, column=1, sticky="ws", padx=5, pady=5)
horizon_figure = tk.Label(horizon_frame, text="0.0", font=font_frameinfo, bg="#2A3747", fg="white")
horizon_figure.grid(row=1, column=1, sticky="e", padx=5)
info_text = tk.Label(horizon_frame, text="W/m", font=font_frametitle, bg="#2A3747", fg="turquoise1")
info_text.grid(row=1, column=2, sticky="w", padx=5, pady=5)

horizon_frame.grid(row=1, column=0, sticky="nsew", padx=3, pady=3)

# 모듈 온도 프레임 ---------------------------------------------
module_frame = tk.Frame(info_label_frame)
module_frame.configure(background="#2A3747")

# 모듈 온도 UI column 가중치
module_frame.columnconfigure(0, weight=3)
module_frame.columnconfigure(1, weight=6)
module_frame.columnconfigure(2, weight=1)

module_icon_link = tk.PhotoImage(file="./image/모듈 온도.png").subsample(2)
icon = tk.Label(module_frame, image=module_icon_link, bg="#2A3747")
icon.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
info_text = tk.Label(module_frame, text="모듈 온도", font=font_frametitle, bg="#2A3747", fg="Seagreen1")
info_text.grid(row=0, column=1, sticky="ws", padx=5, pady=5)
module_figure = tk.Label(module_frame, text="0.0", font=font_frameinfo, bg="#2A3747", fg="white")
module_figure.grid(row=1, column=1, sticky="e", padx=5)
info_text = tk.Label(module_frame, text="℃", font=font_frametitle, bg="#2A3747", fg="Seagreen1")
info_text.grid(row=1, column=2, sticky="w", padx=5, pady=5)

module_frame.grid(row=2, column=0, sticky="nsew", padx=3, pady=3)

# 외부 온도 프레임 ---------------------------------------------
out_frame = tk.Frame(info_label_frame)
out_frame.configure(background="#2A3747")

# 외부 온도 UI column 가중치
out_frame.columnconfigure(0, weight=3)
out_frame.columnconfigure(1, weight=6)
out_frame.columnconfigure(2, weight=1)

out_icon_link = tk.PhotoImage(file="./image/외부 온도.png").subsample(2)
icon = tk.Label(out_frame, image=out_icon_link, bg="#2A3747")
icon.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
info_text = tk.Label(out_frame, text="외부 온도", font=font_frametitle, bg="#2A3747", fg="Seagreen1")
info_text.grid(row=0, column=1, sticky="ws", padx=5, pady=5)
out_figure = tk.Label(out_frame, text="0.0", font=font_frameinfo, bg="#2A3747", fg="white")
out_figure.grid(row=1, column=1, sticky="e", padx=5)
info_text = tk.Label(out_frame, text="℃", font=font_frametitle, bg="#2A3747", fg="Seagreen1")
info_text.grid(row=1, column=2, sticky="w", padx=5, pady=5)

out_frame.grid(row=3, column=0, sticky="nsew", padx=3, pady=3)

info_label_frame.grid(row=0, column=0, sticky="nsew")

# 그래프프레임 ---------------------------------------------
info_graph_label = tk.Frame(detail_info)
info_graph_label.configure(background="grey15")

# info_graph_label column 가중치
info_graph_label.columnconfigure(0, weight=8)
info_graph_label.columnconfigure(1, weight=2)
# info_graph_label row 가중치
info_graph_label.rowconfigure(0, weight=5)
info_graph_label.rowconfigure(1, weight=95)

# 파워상태 타이틀 라벨 ---------------------------------------------
show_inverter_title = tk.Label(info_graph_label, text="Power Status (현재발전기준 : INV)", bg="#2f3640", bd=1, fg='white',
                               font=font_title)
show_inverter_title.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

# 인버터/DC/AC/변환효율 프레임 ---------------------------------------------

# 인버터 효율 프레임
show_efficiency = tk.Frame(info_graph_label, background="#233446")
show_efficiency.columnconfigure(0, weight=1)
show_efficiency.rowconfigure(0, weight=1)
show_efficiency.rowconfigure(1, weight=1)
show_efficiency.rowconfigure(2, weight=1)
show_efficiency.rowconfigure(3, weight=1)
# title 프레임
title = tk.Frame(show_efficiency, background="#233446")
title.columnconfigure(0, weight=1)
title.columnconfigure(1, weight=1)
title.columnconfigure(2, weight=1)
title.columnconfigure(3, weight=1)
title.columnconfigure(4, weight=1)
title.columnconfigure(5, weight=1)
title.rowconfigure(0, weight=1)
label1 = tk.Label(title, borderwidth=1, relief="sunken", text='\t', background="#233446", fg='white', font=font_title)
label1.grid(row=0, column=0, sticky="nsew")
label2 = tk.Label(title, borderwidth=1, relief="sunken", text='인버터\n전압', background="#2f3640", fg='white',
                  font=font_title)
label2.grid(row=0, column=1, sticky="nsew")
label3 = tk.Label(title, borderwidth=1, relief="sunken", text='인버터\n전류', background="#2f3640", fg='white',
                  font=font_title)
label3.grid(row=0, column=2, sticky="nsew")
label4 = tk.Label(title, borderwidth=1, relief="sunken", text='인버터\n주파수', background="#2f3640", fg='white',
                  font=font_title)
label4.grid(row=0, column=3, sticky="nsew")
label5 = tk.Label(title, borderwidth=1, relief="sunken", text='인버팅\n후 금일\n발전량', background="#2f3640", fg='white',
                  font=font_title)
label5.grid(row=0, column=4, sticky="nsew")
label6 = tk.Label(title, borderwidth=1, relief="sunken", text='인버터\n상태', background="#2f3640", fg='white',
                  font=font_title)
label6.grid(row=0, column=5, sticky="nsew")
title.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)
# R상 프레임
inverter_R = tk.Frame(show_efficiency, background="#233446")
inverter_R.columnconfigure(0, weight=1)
inverter_R.columnconfigure(1, weight=1)
inverter_R.columnconfigure(2, weight=1)
inverter_R.columnconfigure(3, weight=1)
inverter_R.columnconfigure(4, weight=1)
inverter_R.columnconfigure(5, weight=1)
inverter_R.rowconfigure(0, weight=1)
r_label1 = tk.Label(inverter_R, borderwidth=1, relief="sunken", text='R상', background="#2f3640", fg='white',
                    font=font_title)
r_label1.grid(row=0, column=0, sticky="nsew")
r_label2 = tk.Label(inverter_R, borderwidth=1, relief="sunken", text='0', background="#233446", fg='white',
                    font=font_title)
r_label2.grid(row=0, column=1, sticky="nsew")
r_label3 = tk.Label(inverter_R, borderwidth=1, relief="sunken", text='0', background="#233446", fg='white',
                    font=font_title)
r_label3.grid(row=0, column=2, sticky="nsew")
r_label4 = tk.Label(inverter_R, borderwidth=1, relief="sunken", text='0', background="#233446", fg='white',
                    font=font_title)
r_label4.grid(row=0, column=3, sticky="nsew")
r_label5 = tk.Label(inverter_R, borderwidth=1, relief="sunken", text='0', background="#233446", fg='white',
                    font=font_title)
r_label5.grid(row=0, column=4, sticky="nsew")
r_label6 = tk.Label(inverter_R, borderwidth=1, relief="sunken", text='0', background="#233446", fg='white',
                    font=font_title)
r_label6.grid(row=0, column=5, sticky="nsew")
inverter_R.grid(row=1, column=0, sticky="nsew", padx=3, pady=3)
# T상 프레임
inverter_T = tk.Frame(show_efficiency, background="#233446")
inverter_T.columnconfigure(0, weight=1)
inverter_T.columnconfigure(1, weight=1)
inverter_T.columnconfigure(2, weight=1)
inverter_T.columnconfigure(3, weight=1)
inverter_T.columnconfigure(4, weight=1)
inverter_T.columnconfigure(5, weight=1)
inverter_T.rowconfigure(0, weight=1)
t_label1 = tk.Label(inverter_T, borderwidth=1, relief="sunken", text='T상', background="#2f3640", fg='white',
                    font=font_title)
t_label1.grid(row=0, column=0, sticky="nsew")
t_label2 = tk.Label(inverter_T, borderwidth=1, relief="sunken", text='0', background="#233446", fg='white',
                    font=font_title)
t_label2.grid(row=0, column=1, sticky="nsew")
t_label3 = tk.Label(inverter_T, borderwidth=1, relief="sunken", text='0', background="#233446", fg='white',
                    font=font_title)
t_label3.grid(row=0, column=2, sticky="nsew")
t_label4 = tk.Label(inverter_T, borderwidth=1, relief="sunken", text='0', background="#233446", fg='white',
                    font=font_title)
t_label4.grid(row=0, column=3, sticky="nsew")
t_label5 = tk.Label(inverter_T, borderwidth=1, relief="sunken", text='0', background="#233446", fg='white',
                    font=font_title)
t_label5.grid(row=0, column=4, sticky="nsew")
t_label6 = tk.Label(inverter_T, borderwidth=1, relief="sunken", text='0', background="#233446", fg='white',
                    font=font_title)
t_label6.grid(row=0, column=5, sticky="nsew")
inverter_T.grid(row=2, column=0, sticky="nsew", padx=3, pady=3)
# S상 프레임
inverter_S = tk.Frame(show_efficiency, background="#233446")
inverter_S.columnconfigure(0, weight=1)
inverter_S.columnconfigure(1, weight=1)
inverter_S.columnconfigure(2, weight=1)
inverter_S.columnconfigure(3, weight=1)
inverter_S.columnconfigure(4, weight=1)
inverter_S.columnconfigure(5, weight=1)
inverter_S.rowconfigure(0, weight=1)
s_label1 = tk.Label(inverter_S, borderwidth=1, relief="sunken", text='S상', background="#2f3640", fg='white',
                    font=font_title)
s_label1.grid(row=0, column=0, sticky="nsew")
s_label2 = tk.Label(inverter_S, borderwidth=1, relief="sunken", text='0', background="#233446", fg='white',
                    font=font_title)
s_label2.grid(row=0, column=1, sticky="nsew")
s_label3 = tk.Label(inverter_S, borderwidth=1, relief="sunken", text='0', background="#233446", fg='white',
                    font=font_title)
s_label3.grid(row=0, column=2, sticky="nsew")
s_label4 = tk.Label(inverter_S, borderwidth=1, relief="sunken", text='0', background="#233446", fg='white',
                    font=font_title)
s_label4.grid(row=0, column=3, sticky="nsew")
s_label5 = tk.Label(inverter_S, borderwidth=1, relief="sunken", text='0', background="#233446", fg='white',
                    font=font_title)
s_label5.grid(row=0, column=4, sticky="nsew")
s_label6 = tk.Label(inverter_S, borderwidth=1, relief="sunken", text='0', background="#233446", fg='white')
s_label6.grid(row=0, column=5, sticky="nsew")
inverter_S.grid(row=3, column=0, sticky="nsew", padx=3, pady=3)

show_efficiency.grid(row=1, column=0, sticky="nsew", padx=3, pady=3)

# 현시간출력 프레임 -------------------------------------------------

show_nowoutput_frame = tk.Frame(info_graph_label, bg="#233446")
show_nowoutput_frame.columnconfigure(0, weight=1)
show_nowoutput_frame.rowconfigure(0, weight=10)
show_nowoutput_frame.rowconfigure(1, weight=15)
show_nowoutput_frame.rowconfigure(2, weight=30)
show_nowoutput_frame.rowconfigure(3, weight=15)
show_nowoutput_frame.rowconfigure(4, weight=30)
show_nowoutput = tk.Label(show_nowoutput_frame, text="현시간 출력", bg="#2f3640", bd=1, fg='khaki2', font=font_title,
                          anchor='n')

select_today = tk.Label(show_nowoutput_frame, text="0시 ~ 선택시간 ", bg="#233446", bd=1, fg='white', font=font_title)
select_today.grid(row=1, column=0, pady=1)

select_progressbar = ttk.Progressbar(show_nowoutput_frame, maximum=15000, length=300, value=0)
select_progressbar.grid(row=2, column=0, pady=1, ipady=10)

none_today = tk.Label(show_nowoutput_frame, text="금일발전량", bg="#233446", bd=1, fg='white', font=font_title)
none_today.grid(row=3, column=0, pady=1)

none_progressbar = ttk.Progressbar(show_nowoutput_frame, maximum=15000, length=300, value=0)
none_progressbar.grid(row=4, column=0, pady=1, ipady=10)

show_nowoutput.grid(row=0, column=0, sticky="nsew")
show_nowoutput_frame.grid(row=1, column=1, sticky="nsew", padx=3, pady=3)

info_graph_label.grid(row=0, column=1, sticky="nsew")

detail_info.grid(row=3, sticky="nsew")

# powergen 프레임 (column = 3)----------------------------------------------
powergen = tk.Frame(win)
powergen.configure(background="grey15")

# powergen column 가중치
powergen.columnconfigure(0, weight=1)
# powergen row 가중치
powergen.rowconfigure(0, weight=1)

# Graph Default Value--------------------------------------
fig = plt.figure(figsize=(21, 2))
fig.patch.set_facecolor('#233446')
# none graph---------------------------------------------
label1, value1 = graph_input('정선한교', '2021-08-01 ')
value1 = list(map(int, value1))
label1 = list(map(int, label1))
ax1 = plt.subplot(1, 2, 1)
ax1.bar(label1, value1, color='#20E5DE')
ax1.tick_params(width=0)  # 눈금선 제거
ax1.tick_params(colors='white')  # 눈금 색
ax1.set_facecolor('#233446')
ax1.set_title('금일발전량추이', color='white')
ax1.set_xticks(label1)
# ejo graph----------------------------------------------
label2, value2 = graph_input('정선한교', '2021-08-02 ')
value2 = list(map(int, value2))
label2 = list(map(int, label2))
label2 = np.array(label2)
label1 = np.array(label1)
ax2 = plt.subplot(1, 2, 2)
bar_width = 0.2
width = 0.4
none = ax2.bar(label1 - bar_width, value1, width, color='#233446')
ejo = ax2.bar(label2 + bar_width, value2, width, color='lightskyblue')
ax2.set_facecolor('#233446')
ax2.tick_params(width=0)  # 눈금선 제거
ax2.tick_params(colors='white')  # 눈금 색
ax2.set_title('전일금일비교그래프', color='white')
ax2.legend((none[0], ejo[0]), ('금일', '전일'))
ax2.set_xticks(label1)
canvas = FigureCanvasTkAgg(fig, master=powergen)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=3, pady=3)

powergen.grid(row=4)

# bottommenu(column =4)----------------------------------------------
bottommenu = tk.Frame(win)
bottommenu.configure(background="grey15")

# botoommenu column 가중치
bottommenu.columnconfigure(0, weight=2)
bottommenu.columnconfigure(1, weight=2)
bottommenu.columnconfigure(2, weight=2)
bottommenu.columnconfigure(3, weight=2)
bottommenu.columnconfigure(4, weight=2)
# botoommenu row 가중치
bottommenu.rowconfigure(0, weight=1)

# 금일 발전량 프레임 ----------------------------------------------
today_powergen_frame = tk.Frame(bottommenu)
today_powergen_frame.configure(background="#233446")

# 금일 발전량 가중치
today_powergen_frame.columnconfigure(0, weight=3)
today_powergen_frame.columnconfigure(0, weight=6)
today_powergen_frame.columnconfigure(0, weight=1)
today_powergen_frame.columnconfigure(1, weight=3)
today_powergen_frame.columnconfigure(2, weight=7)

today_powergen_icon_link = tk.PhotoImage(file="./image/금일 발전량.png").subsample(2)
icon = tk.Label(today_powergen_frame, image=today_powergen_icon_link, bg="#233446")
icon.grid(row=0, column=0, rowspan=2, padx=5, pady=3)
info_text = tk.Label(today_powergen_frame, text="금일 발전량", font=font_frametitle, bg="#233446", fg='mediumspringgreen')
info_text.grid(row=0, column=1, sticky="ws", padx=5, pady=5)
none_pwgen = tk.Label(today_powergen_frame, text="0.0", font=font_frameinfo, bg="#233446", fg="white")
none_pwgen.grid(row=1, column=1, sticky="e", padx=5)
info_text = tk.Label(today_powergen_frame, text="kWh", font=font_frametitle, bg="#233446", fg="Seagreen1")
info_text.grid(row=1, column=2, sticky="w", padx=5, pady=5)

today_powergen_frame.grid(row=2, column=0, sticky="nsew", padx=3, pady=3)

# 금일 발전시간 프레임 ----------------------------------------------
today_powergen_time_frame = tk.Frame(bottommenu)
today_powergen_time_frame.configure(background="#233446")

# 금일 발전시간 가중치
today_powergen_time_frame.columnconfigure(0, weight=3)
today_powergen_time_frame.columnconfigure(0, weight=6)
today_powergen_time_frame.columnconfigure(0, weight=1)
today_powergen_time_frame.columnconfigure(1, weight=3)
today_powergen_time_frame.columnconfigure(2, weight=7)

today_powergen_time_icon_link = tk.PhotoImage(file="./image/금일 발전시간.png").subsample(2)
icon = tk.Label(today_powergen_time_frame, image=today_powergen_time_icon_link, bg="#233446")
icon.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
info_text = tk.Label(today_powergen_time_frame, text="금일 발전시간", font=font_frametitle, bg="#233446",
                     fg='mediumspringgreen')
info_text.grid(row=0, column=1, sticky="ws", padx=5, pady=3)
none_pwgen_time = tk.Label(today_powergen_time_frame, text="0.0", font=font_frameinfo, bg="#233446", fg="white")
none_pwgen_time.grid(row=1, column=1, sticky="e", padx=5)
info_text = tk.Label(today_powergen_time_frame, text="Hour", font=font_frametitle, bg="#233446", fg="Seagreen1")
info_text.grid(row=1, column=2, sticky="w", padx=5, pady=5)

today_powergen_time_frame.grid(row=2, column=1, sticky="nsew", padx=3, pady=3)

# 전일 발전량 프레임 ----------------------------------------------
yesterday_powergen_frame = tk.Frame(bottommenu)
yesterday_powergen_frame.configure(background="#233446")

# 전일 발전량 가중치
yesterday_powergen_frame.columnconfigure(0, weight=3)
yesterday_powergen_frame.columnconfigure(0, weight=6)
yesterday_powergen_frame.columnconfigure(0, weight=1)
yesterday_powergen_frame.columnconfigure(1, weight=3)
yesterday_powergen_frame.columnconfigure(2, weight=7)

yesterday_powergen_icon_link = tk.PhotoImage(file="./image/전일 발전량.png").subsample(2)
icon = tk.Label(yesterday_powergen_frame, image=yesterday_powergen_icon_link, bg="#233446")
icon.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
info_text = tk.Label(yesterday_powergen_frame, text="전일 발전량", font=font_frametitle, bg="#233446", fg='lightskyblue')
info_text.grid(row=0, column=1, sticky="ws", padx=5, pady=3)
ejo_pwgen = tk.Label(yesterday_powergen_frame, text="0.0", font=font_frameinfo, bg="#233446", fg="white")
ejo_pwgen.grid(row=1, column=1, sticky="e", padx=5)
info_text = tk.Label(yesterday_powergen_frame, text="kWh", font=font_frametitle, bg="#233446", fg="lightskyblue")
info_text.grid(row=1, column=2, sticky="w", padx=5, pady=5)

yesterday_powergen_frame.grid(row=2, column=2, sticky="nsew", padx=3, pady=3)

# 전일 발전시간 프레임 --------------------------------------
yesterday_powergen_time_frame = tk.Frame(bottommenu)
yesterday_powergen_time_frame.configure(background="#233446")

# 전일 발전시간 가중치
yesterday_powergen_time_frame.columnconfigure(0, weight=3)
yesterday_powergen_time_frame.columnconfigure(0, weight=6)
yesterday_powergen_time_frame.columnconfigure(0, weight=1)
yesterday_powergen_time_frame.columnconfigure(1, weight=3)
yesterday_powergen_time_frame.columnconfigure(2, weight=7)

yesterday_powergen_time_icon_link = tk.PhotoImage(file="./image/전일 발전시간.png").subsample(2)
icon = tk.Label(yesterday_powergen_time_frame, image=yesterday_powergen_time_icon_link, bg="#233446")
icon.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
info_text = tk.Label(yesterday_powergen_time_frame, text="전일 발전시간", font=font_frametitle, bg="#233446",
                     fg='lightskyblue')
info_text.grid(row=0, column=1, sticky="ws", padx=5, pady=3)
ejo_pwgen_time = tk.Label(yesterday_powergen_time_frame, text="0.0", font=font_frameinfo, bg="#233446", fg="white")
ejo_pwgen_time.grid(row=1, column=1, sticky="e", padx=5)
info_text = tk.Label(yesterday_powergen_time_frame, text="Hour", font=font_frametitle, bg="#233446", fg="lightskyblue")
info_text.grid(row=1, column=2, sticky="w", padx=5, pady=5)

yesterday_powergen_time_frame.grid(row=2, column=3, sticky="nsew", padx=3, pady=3)

# 전일 대비 증가량 프레임 --------------------------------------
increase_powergen_frame = tk.Frame(bottommenu)
increase_powergen_frame.configure(background="#233446")

# 전일 대비 증가량 가중치
increase_powergen_frame.columnconfigure(0, weight=3)
increase_powergen_frame.columnconfigure(0, weight=6)
increase_powergen_frame.columnconfigure(0, weight=1)
increase_powergen_frame.columnconfigure(1, weight=3)
increase_powergen_frame.columnconfigure(2, weight=7)

increase_powergen_frame_icon_link = tk.PhotoImage(file="./image/전일 대비 증가량.png").subsample(2)
icon = tk.Label(increase_powergen_frame, image=increase_powergen_frame_icon_link, bg="#233446")
icon.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
info_text = tk.Label(increase_powergen_frame, text="전일 대비 증가량", font=font_frametitle, bg="#233446", fg='lightskyblue')
info_text.grid(row=0, column=1, sticky="ws", padx=5, pady=5)
increase_pwgen = tk.Label(increase_powergen_frame, text="+ 0.0", font=font_frameinfo, bg="#233446", fg="white")
increase_pwgen.grid(row=1, column=1, sticky="e", padx=5)

increase_powergen_frame.grid(row=2, column=4, sticky="nsew", padx=3, pady=3)

bottommenu.grid(row=5, sticky="nwe")

win.mainloop()