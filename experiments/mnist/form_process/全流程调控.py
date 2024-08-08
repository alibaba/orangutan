from consts.nerve_props import TYPE
from ..regions import REGION
from ...util import get_soma_inds, save_axon_end_inds_with_new_nerves
from ...form_nerve.form_nerve import form_nerve
import numpy as np
import math
import itertools

axon_end_inds = {}
make_new_nerve_packs = form_nerve.make_new_nerve_packs


def 计算相邻点差值(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '信号输入')
    father_inds = get_soma_inds('全流程调控',  
                                '计算相邻点差值')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励边缘点(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '计算相邻点差值')
    father_inds = get_soma_inds('全流程调控',  
                                '激励边缘点')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励轮廓方位(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '激励边缘点')
    father_inds = get_soma_inds('全流程调控',  
                                '激励轮廓方位')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励轮廓直线(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '激励轮廓方位')
    father_inds = get_soma_inds('全流程调控',  
                                '激励轮廓直线')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励射线(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '激励轮廓方位')
    father_inds = get_soma_inds('全流程调控',  
                                '激励射线')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 汇总轮廓直线(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '激励轮廓直线')
    father_inds = get_soma_inds('全流程调控',  
                                '汇总轮廓直线')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 汇总射线(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '激励射线')
    father_inds = get_soma_inds('全流程调控',  
                                '汇总射线')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励轮廓中心(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '汇总轮廓直线')
    father_inds = get_soma_inds('全流程调控',  
                                '激励轮廓中心')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励角(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '汇总射线')
    father_inds = get_soma_inds('全流程调控',  
                                '激励角')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 反馈激励轮廓方位(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '反馈激励轮廓直线')
    father_inds = get_soma_inds('全流程调控',  
                                '反馈激励轮廓方位')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 反馈激励边缘点(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '反馈激励轮廓方位')
    father_inds = get_soma_inds('全流程调控',  
                                '反馈激励边缘点')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励像素独占轮廓方位(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '反馈激励边缘点')
    father_inds = get_soma_inds('全流程调控',  
                                '激励像素独占轮廓方位')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励像素独占轮廓直线(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '激励像素独占轮廓方位')
    father_inds = get_soma_inds('全流程调控',  
                                '激励像素独占轮廓直线')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 汇总像素独占轮廓直线(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '激励像素独占轮廓直线')
    father_inds = get_soma_inds('全流程调控',  
                                '汇总像素独占轮廓直线')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励像素独占轮廓中心(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '汇总像素独占轮廓直线')
    father_inds = get_soma_inds('全流程调控',  
                                '激励像素独占轮廓中心')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 激励数字(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '激励轮廓中心')
    father_inds = get_soma_inds('全流程调控',  
                                '激励数字')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 反馈预测角(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '激励数字')
    father_inds = get_soma_inds('全流程调控',  
                                '反馈预测角')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 反馈预测轮廓中心(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '激励数字')
    father_inds = get_soma_inds('全流程调控',  
                                '反馈预测轮廓中心')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 计算预测偏差或意外(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '反馈预测轮廓中心')
    father_inds = get_soma_inds('全流程调控',  
                                '计算预测偏差或意外')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def 建立或调整预测回路(cortex_obj):
    mother_inds = get_soma_inds('全流程调控',  
                                '计算预测偏差或意外')
    father_inds = get_soma_inds('全流程调控',  
                                '建立或调整预测回路')
    return make_new_nerve_packs(mother_inds, father_inds, cortex_obj)


def form_init_nerve():
    return [
        计算相邻点差值,
        激励边缘点,
        激励轮廓方位,
        *[激励轮廓直线, 激励射线],
        *[汇总轮廓直线, 汇总射线],
        *[激励轮廓中心, 激励角],
        反馈激励轮廓方位,
        反馈激励边缘点,
        激励像素独占轮廓方位,
        激励像素独占轮廓直线,
        汇总像素独占轮廓直线,
        激励像素独占轮廓中心,
        激励数字,
        *[反馈预测角, 反馈预测轮廓中心],
        计算预测偏差或意外,
        建立或调整预测回路,
    ]
