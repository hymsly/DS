# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 15:54:40 2018

@author: himan
"""

import pandas as pd
import numpy as np

def readAtributo(ruta):
    f = open(ruta,'r')
    f1 = f.readlines()
    atributos = []
    for atributo in f1:
        atributos.append(atributo.rstrip('\n'))
    return atributos

data = pd.read_csv('./TABLAS BCP/tc.txt',sep=',')

atributos = readAtributo('./TABLAS BCP/atributos.txt')

dataFiltrada = data[atributos]

#print(pd.isnull(dataFiltrada["tipo_cliente"]).values.ravel().sum())

categoricos = ["cat_zona1","tipo_cliente"]
meansInteger = ["numproductos_pas",
"numproductos_act",
"numproductos",
"meses_fmactivo_6_1000",
"meses_fmpasivo_6_0",
"meses_fmpasivo_12_100",
"meses_fmpasivo_6_100",
"meses_fmpasivo_12_1000",
"meses_fmpasivo_1_1000",
"meses_fmsavmf_12_0",
"meses_fmsavmf_12_100",
"meses_pmsavmf_12_0",
"meses_pmsavmf_12_100",
"meses_pasivo_activo_6_100",
"meses_pasivo_activo_12_1000",
"antiguedad_pas_tot",
"maxantiguedad_act_pas_vig",
"flg_cts_1_1000",
"flg_cts_6_1000",
"flg_cts_24_1000",
"flg_rev_12",
"flg_tc_12",
"num_tc_sum_24",
"lincre_tc_sum_24",
"flagpr_tc_sum_12",
"varied_prod_6_300",
"meses_fmsavmf_12_1000",
"meses_fmsavmf_6_100",
"meses_pmsavmf_6_100",
"meses_pmsavmf_6_1000",
"antiguedad_act_vig",
"cons_mtocns0",
"desde_ult_mtodisef",
"flg_07v_12_100",
"cnds_19e_count_12",
"cnds_21s_count_12",
"cndsmxmt13c_count_12",
"cndsmxmt17m_count_12",
"cndsmxmt06t_count_6",
"cnetigcl_d_count_12",
"cnetmtco_a_count_6"]
meansDouble = ["pmpasivo_med_6",
"ctdempreportadoclimed6",
"deudir12_deutot12",
"deudir6_deutot6",
"mtolintot_dmi0_pro6",
"bal_nhi_sum_12",
"linea_min_2",
"rt_mtpgos_sldfm_12",
"rt_pagos_balance",
"rt_cnetmtfac6m_c_sum_12_12",
"rt_cnetmtfac6m_d_sum_12_12",
"rt_cnetmtfac6m_e_sum_12_12",
"rt_cnetmtfac6m_f_sum_12_12",
"md_sum_12",
"prcnpsclet_med_12",
"prigclet_med_12",
"pr_02r_med_12",
"prcnpsclet_02r_med_12",
"mdigclet_02r_med_12",
"prcnpsclet_med_6",
"prigclet_med_6",
"prigclet_07v_med_6",
"mdigclet_11t_med_12",
"prcnpsclet_12m_med_12",
"cnop_16b_med_12",
"prcnpsclet_16b_med_12",
"prigclet_16b_med_12",
"mt_17m_sum_12",
"prmtcoet_17m_med_12",
"igcletmxmt50f_med_12",
"igcletmxmt100f_med_12",
"igcletmxcn100f_med_12",
"mtcoetmxcn_med_12",
"mtcoetmxcnfds_med_12",
"mtcoetmxcn06t_med_12",
"igcletmxmt_med_6",
"igcletmxcn_med_6",
"igcletmxmt05s_med_6",
"igcletmxmtop_med_12",
"ctgetigfijomxmtop_med_12",
"cnpscletmxmtop_med_12",
"ctgetmtcomxmtop_med_12",
"igcletmxmtop02r_med_12",
"ctgetmtcomxmtop02r_med_12",
"cnfecmxmt_med_6",
"sfent1_sfent24",
"utl_12_tc_v1",
"utl_6_tc",
"utl1_utl12_tc",
"utlcs_12_tc_v1",
"utlcs_6_tc_v1"]

def label_race(row,value,atr):
    for i in range(len(value)):
        if value[i]==row[atr]:
            return i
    return -1
def label_replace(row,value,atr):
    if(np.isnan(row[atr])):
        return value
    return row[atr]

def Discreto(df,atributo):
    values = df[atributo].unique().tolist()
    df[atributo] = df.apply(lambda row:label_race(row,values,atributo),axis = 1)
    return df

def MeanReplace(df,atributo,integer):
    X = df[atributo].values.tolist()
    cnt = 0
    suma = 0
    for x in X:
        if(np.isnan(x)):
            continue
        cnt = cnt+1
        suma += x
    value = cnt/suma
    if(integer):
        value = int(round(value))
    df[atributo] = df.apply(lambda row:label_replace(row,value,atributo),axis = 1)
    return df

for cat in categoricos:
    dataFiltrada = Discreto(dataFiltrada,cat)

for mean in meansInteger:
    dataFiltrada = MeanReplace(dataFiltrada,mean,1)

for mean in meansDouble:
    dataFiltrada = MeanReplace(dataFiltrada,mean,0)

#print(dataFiltrada["flg_tc_12"])
    
columns = dataFiltrada.columns.values.tolist()
####ANALIZANDO SI QUEDA ALGUN VALOR NULO
for col in columns:
    df = pd.isnull(dataFiltrada[col]).values.ravel().sum()
    if(df>0):
        print(df)

dataFiltrada.to_csv('./TABLAS BCP/tcFiltrada.txt',sep=',',index=False)