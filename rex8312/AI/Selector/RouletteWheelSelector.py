# -*- coding: utf-8 -*-



__author__ = 'rex8312'

from Selector import BaseSelector
import numpy as np
import pylab as pl

from pprint import pprint


class RouletteWheelSelector(BaseSelector):
    """
    Genetic Algorithm 과 같은 알고리즘의 사용하기 위한 룰렛휠 선택
    gene 에 해당하는 params 와 fitness 에 해당하는 values 를 입력 받아
    새로운 population 을 출력함
    """
    norm_values = None
    roulette = None

    def set_params(self, params, values):
        """
        roulette 생성,
        특정 index 의 param 은 동일한 index 를 가지는 value 와 연관되어 있음
        :param params: 2차원 실수 배열 GA의 gene 에 해당
        :param values: 1차원 실수 배열, GA의 fitness 에 해당
        :return: None
        """
        BaseSelector.set_params(self, params, values)
        total_value = sum(self.values)
        self.norm_values = self.values / total_value
        self.roulette = []
        for idx, nv in enumerate(self.norm_values):
            self.roulette.append(sum(self.norm_values[0:idx]))
        self.roulette = self.roulette[1:]

    def select(self, n=1):
        """
        set_params 에서 생성한 roulette 을 이용해 크기 n을 가지는 새로운 parameter 집합을 생성
        GA의 다음 세대 population 에 해당함
        :param n: 자연수, 새로운 parameter 집합의 크기
        :return:
            new_params: 새로운 parameter 집합
            new_value: values 를 새로운 parameter 집합에 맞춰 재배열
            idx_list: new_parameter 를 구성하는 parameter 의 원래 위치
        """
        random_numbers = np.random.random(n)
        idx_list = np.digitize(random_numbers, self.roulette)
        new_params = []
        new_values = []
        for idx in idx_list:
            new_params.append(self.params[idx])
            new_values.append(self.values[idx])
        return new_params, new_values, idx_list


if __name__ == '__main__':
    params = [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
    ]
    values = [0.1, 0.55, 1.0, 0.80, 0.1]

    selector = RouletteWheelSelector()

    # 룰렛 생성
    selector.set_params(params, values)

    # 몇 개의 데이터를 샘플링 할 것인지 입력
    new_params, new_values, idx_list = selector.select(1000)

    # 재 선택된 파라미터: new_params
    # 선택된 파라미터와 연관된 값: new_values
    # 테스트 목적으로 히스토 그램을 그리기 위한 데이터: idx_list
    pl.hist(idx_list)
    pl.show()

    pprint(zip(new_params, new_values))