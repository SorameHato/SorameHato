# coding: utf-8
import numpy, pandas

def vForceCalc(level:int,rank:int,score:int):
    # 랭크 보정값 계산    
    if rank == 5 or score == 10000000:
        rankAdjust = 1.1
    elif rank == 0:
        rankAdjust = 0.5
    elif rank == 1:
        rankAdjust = 1
    elif rank == 2:
        rankAdjust = 1.02
    elif rank == 3:
        rankAdjust = 1.04
    elif rank == 4:
        rankAdjust = 1.05
    else:
        print('그레이드가 잘못되었습니다. EF 랭크인 것으로 가정하고 계산합니다.')
        rankAdjust = 1
    # 스코어 보정값 계산
    if score >= 9900000:   # S
        scoreAdjust = 1.05
    elif score >= 9800000: # AAA+
        scoreAdjust = 1.02
    elif score >= 9700000: # AAA
        scoreAdjust = 1
    elif score >= 9500000: # AA+
        scoreAdjust = 0.97
    elif score >= 9300000: # AA
        scoreAdjust = 0.94
    elif score >= 9000000: # A+
        scoreAdjust = 0.91
    elif score >= 8700000: # A
        scoreAdjust = 0.88
    elif score >= 7500000: # B
        scoreAdjust = 0.85
    elif score >= 6500000: # C
        scoreAdjust = 0.82
    else:                  # D
        scoreAdjust = 0.8
    # 레벨 * 20 * 점수 / 1천만 * 랭크 보정값 * 스코어 보정값
    return level * 20 * score / 10000000 * rankAdjust * scoreAdjust

def makeDF(level:int) -> pandas.DataFrame:
    bottom = int(vForceCalc(level, 1, 8700000))
    top = int(vForceCalc(level, 5, 10000000))
    table = dict()
    for i in range(bottom, top+1, 1):
        table[i] = [numpy.nan, numpy.nan, numpy.nan, numpy.nan]

    for rank in [1, 2, 3, 4]:
        upper = 10000001
        #자동화하기 귀찮아서, 그냥 PUC위치에 EF든 EX든 MX든 UC든
        #PUC 볼포표롤 박아버리고 나중에 수작업으로 바꾸려고 upper을 10000001로 고정함
        target_vForce = 0
        for i in range(8700000,upper):
            vForce = vForceCalc(level,rank,i)
            if vForce >= target_vForce+1:
                target_vForce = int(vForce)
                table[target_vForce][rank-1] = i
    # 먼저 가로형으로 df를 생성 후, 세로형으로 변환
    df = pandas.DataFrame(data = table,index=[f'{level}_ef',f'{level}_ex',f'{level}_mx',f'{level}_uc']).transpose(copy=False)
    return df

# level = int(input('산출할 레벨 : '))
level = 19
df1 = makeDF(level) #그 레벨
df2 = makeDF(level+1) #그 레벨 +1
df = pandas.concat([df1, df2],axis=1) #둘을 가로로 합침
df = df.dropna(how='all') # 전부 값 없는 행 제거
print(df)

result_table = dict()

for col in df.index.tolist():
    col = int(col)
    if col >= 460:
        color = '<rowbgcolor=#500050,#500050><rowcolor=#ffffff,#ffffff>'
    elif col >= 440:
        color = '<rowbgcolor=#630063,#630063><rowcolor=#ffffff,#ffffff>'
    elif col >= 420:
        color = '<rowbgcolor=#760076,#760076><rowcolor=#ffffff,#ffffff>'
    elif col >= 400:
        color = '<rowbgcolor=#900090,#900090><rowcolor=#ffffff,#ffffff>'
    elif col >= 380:
        color = '<rowbgcolor=#dc143c,#dc143c><rowcolor=#ffffff,#ffffff>'
    elif col >= 360:
        color = '<rowbgcolor=#ffd700,#ffd700><rowcolor=#373a3c,#373a3c>'
    elif col >= 340:
        color = '<rowbgcolor=#c0c0c0,#c0c0c0><rowcolor=#373a3c,#373a3c>'
    elif col >= 320:
        color = '<rowbgcolor=#ffc0cb,#ffc0cb><rowcolor=#373a3c,#373a3c>'
    elif col >= 300:
        color = '<rowbgcolor=#ff2400,#ff2400><rowcolor=#ffffff,#ffffff>'
    elif col >= 280:
        color = '<rowbgcolor=#00ffff,#00ffff><rowcolor=#373a3c,#373a3c>'
    elif col >= 240:
        color = '<rowbgcolor=#ffff00,#ffff00><rowcolor=#373a3c,#373a3c>'
    else:
        color = '<rowbgcolor=#3399ff,#3399ff><rowcolor=#373a3c,#373a3c>'
    result_table[col] = f'||{color} {col}||'

def countNone(df:pandas.DataFrame)->None:
    none_count = 0 #nan이 연속된 행 갯수
    none_init = 0 #nan이 맨 처음 시작된 볼포 위치
    return_str = ''
    for idx, i in df.items():
        if numpy.isnan(i):
            if none_count == 0:
                none_init = idx
            none_count += 1
        elif none_count >= 1:
            return_str += f'{none_init} : NaN({none_count}), {idx} : {i}, '
            none_count = 0
        else:
            return_str += f'{idx} : {i}, '

    if none_count >= 1:
        return_str += f'{none_init} : NaN({none_count})'
        none_count = 0
    return return_str

def namuTableAdder(df:pandas.Series)->None:
    none_count = 0 #nan이 연속된 행 갯수
    none_init = 0 #nan이 맨 처음 시작된 볼포 위치
    for idx, i in df.items():
        if numpy.isnan(i):
            if none_count == 0:
                none_init = idx
            none_count += 1
        elif none_count >= 1:
            result_table[none_init] += f'<|{none_count}><bgcolor=#ffffff,#1c1d1f> ||'
            result_table[idx] += f' {int(i)}||'
            none_count = 0
        else:
            result_table[idx] += f' {int(i)}||'

    if none_count >= 1:
        result_table[none_init] += f'<|{none_count}><bgcolor=#ffffff,#1c1d1f> ||'
        none_count = 0

for i in range(df.shape[1]):
    namuTableAdder(df.iloc[:,i])

result_str = ''
for index in result_table.keys():
    result_str += result_table[index] + '\n'

import pyperclip
pyperclip.copy(result_str)
