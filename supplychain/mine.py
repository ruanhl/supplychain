# -*- coding: utf-8 -*-
import random
import json
import math
import time
import numpy as np

# 字典数据读取
file = open('../data.txt', 'r')
js = file.read()
dic = json.loads(js)
# print(dic)
file.close()

r = dic['r']
rm = dic['r_m']
s = dic['s']
sm = dic['s_m']
m = dic['m']
rr = dic['rr']
w = dic['w']
t = dic['t']
tm = dic['t_m']
c = dic['c']
d = dic['d']
cd = dic['cd']
cr = dic['cr']
cwn = dic['cwn']

num_arr = [[20, 50, 3, 6, 30, 20, 30], [20, 50, 3, 6, 60, 20, 60], [20, 50, 3, 6, 100, 20, 100],
           [30, 90, 6, 12, 30, 30, 30], [30, 90, 6, 12, 60, 30, 60], [30, 90, 6, 12, 100, 30, 100],
           [50, 140, 9, 20, 30, 40, 30], [50, 140, 9, 20, 60, 40, 60], [50, 140, 9, 20, 100, 40, 100]]

# 依次为成本，碳排放，废气，废水，固体废物的最大值
max_value = [[5545020.997467856, 9094958.991537316, 1.8289262, 1610.6010999999999, 59.25509300000001],
             [7971417.4608233, 13093518.373952521, 2.6345772, 2320.0486, 85.355658],
             [9215973.252384385, 15140771.148889793, 3.0467966000000004, 2683.0578, 98.710874],
             [15247045.810097592, 27235230.46176002, 3.1850608000000005, 2805.8563999999997, 103.24881200000002],
             [22031560.559122473, 39413922.76294044, 4.6114738, 4062.4828999999995, 149.490507],
             [25442928.8108584, 45510524.786803134, 5.3248436, 4690.8823, 172.61322900000002],
             [29796755.939102244, 55962949.222346865, 4.2035504, 3705.0621999999994, 136.375806],
             [43569936.1473109, 81899066.3292498, 6.153859199999999, 5424.1226, 199.65133800000004],
             [50281055.05964345, 94478024.42140886, 7.0978832, 6256.208599999999, 230.278798]]


# 子代生成
def initial_population(x):
    # 原料商0 供应商1 制造商2 仓储3 分销商4 回收再制造商5 客户6
    arr = num_arr[x]
    population = []
    for i in range(20):
        pop = []
        for _ in range(int(arr[1] / 10 * 3)):
            pop.append(random.randint(0, arr[0] - 1))
        for _ in range(int(arr[1] / 10)):
            a = [_ for _ in range(10)]
            result = random.sample(a, 3)
            pop += result
        for _ in range(arr[4]):
            pop.append(random.randint(0, arr[3] - 1))
        for _ in range(arr[4]):
            pop.append(random.randint(0, arr[5] - 1))
        population.append(pop)
    return population


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * 1000


def get_func(population, x):
    # 原料商0 供应商1 制造商2 仓储3 分销商4 回收再制造商5 客户6
    arr = num_arr[x]
    num_s = int(arr[1] / 10)

    # WI
    def func1(pop):
        w_ = pop[num_s * 6: num_s * 6 + arr[4]]
        standard = 0

        w_num = [[0 for _ in range(arr[3])] for i in range(arr[2])]
        for i in range(arr[2]):
            for _ in range(arr[4]):
                w_num[i][w_[_]] += cwn[i][_]
        for i in range(arr[2]):
            avg = sum(w_num[i]) / len(w_num[i])
            standard += (sum((_ - avg) ** 2 for _ in w_num[i]) / len(w_num[i])) ** 0.5
        standard = standard / arr[2]
        return standard

    # 目标函数
    def func2(pop):
        r_ = pop[:num_s * 3]
        s_ = pop[num_s * 3: num_s * 6]
        w_ = pop[num_s * 6: num_s * 6 + arr[4]]
        t_ = pop[num_s * 6 + arr[4]:]

        cost_w_built = arr[3] * 200

        cost_produce_rsm = cost_produce_t = 0
        tan_produce_rsm = tan_produce_t = 0
        gas_produce_rsm = gas_produce_t = 0
        water_produce_rsm = water_produce_t = 0
        solid_produce_rsm = solid_produce_t = 0

        for i in range(arr[2]):
            num = sum(cr[i][:arr[6]])
            num_rr = sum(cr[i][:arr[6]]) * rr[i]

            p = (rm[i] + rm[i + 1] + rm[i + 2]) / num
            p1 = (sm[i] + sm[i + 1] + sm[i + 2]) / num
            p2 = (tm[i] + tm[i + 1] + tm[i + 2]) / num_rr

            while i < num_s * 3:
                if p <= 1:
                    cost_produce_rsm += num * 2 * 0.6
                    tan_produce_rsm += num / 100 * 0.35
                    gas_produce_rsm += num / 100 * 0.0025
                    water_produce_rsm += num / 100 * 2
                    solid_produce_rsm += num / 100 * 0.07
                else:
                    cost_produce_rsm += num * 2 * 0.6 * p
                    tan_produce_rsm += num / 100 * 0.35 * p
                    gas_produce_rsm += num / 100 * 0.0025 * p
                    water_produce_rsm += num / 100 * 2 * p
                    solid_produce_rsm += num / 100 * 0.07 * p
            while i < num_s * 6:
                if p <= 1:
                    cost_produce_rsm += num * 0.6
                    tan_produce_rsm = num / 100 * 0.1
                    gas_produce_rsm += num / 100 * 0.001
                    water_produce_rsm += num / 100 * 1.2
                    solid_produce_rsm += num / 100 * 0.05
                else:
                    cost_produce_rsm += num * 0.6 * p1
                    tan_produce_rsm = num / 100 * 0.1 * p1
                    gas_produce_rsm += num / 100 * 0.001 * p1
                    water_produce_rsm += num / 100 * 1.2 * p1
                    solid_produce_rsm += num / 100 * 0.05 * p1
            while (i > num_s * 6 + arr[4]) and i < num_s * 6 + arr[4]:
                if p <= 1:
                    cost_produce_rsm += num_rr * 0.15 + int(num_rr * 0.4) * 0.5
                    tan_produce_t += num_rr / 100 * 0.38 + int(num_rr * 0.4) / 100 * 0.31
                    gas_produce_t += num_rr / 100 * 0.002 + int(num_rr * 0.4) / 100 * 0.0025
                    water_produce_t += num_rr / 100 + int(num_rr * 0.4) / 100 * 2
                    solid_produce_t += num_rr / 100 * 0.03 + int(num_rr * 0.4) / 100 * 0.05
                else:
                    cost_produce_rsm += (num_rr * 0.15 + int(num_rr * 0.4) * 0.5) * p2
                    tan_produce_t += (num_rr / 100 * 0.38 + int(num_rr * 0.4) / 100 * 0.31) * p2
                    gas_produce_t += (num_rr / 100 * 0.002 + int(num_rr * 0.4) / 100 * 0.0025) * p2
                    water_produce_t += (num_rr / 100 + int(num_rr * 0.4) / 100 * 2) * p2
                    solid_produce_t += (num_rr / 100 * 0.03 + int(num_rr * 0.4) / 100 * 0.05) * p2

            i += 3

        cost_trans_c_1 = cost_trans_c_2 = cost_trans_r = 0
        for i1 in range(arr[2]):
            for i2 in range(num_s * 3):
                num = sum(cr[i1][:arr[6]])
                group = int(i2 / 3)
                cost_trans_c_1 += 5.15 * distance(r[r_[i2]][0], r[r_[i2]][1], s[group][s_[i2]][0], s[group][s_[i2]][1]
                                                  ) / 3 * num * 2 + 10.25 * distance(m[i1][0], m[i1][1],
                                                                                     s[group][s_[i2]][0],
                                                                                     s[group][s_[i2]][1]) / 3 * num
        for i1 in range(arr[2]):
            for i2 in range(arr[4]):
                num_d = cr[i1][i2] - cwn[i1][i2]
                cost_trans_c_2 += 40.5 * (distance(m[i1][0], m[i1][1], d[i2][0], d[i2][1]) * num_d +
                                          cd[i2] * 100 * num_d +
                                          distance(d[i2][0], d[i2][1], w[w_[i2]][0], w[w_[i2]][1]) * cwn[i1][i2] +
                                          distance(m[i1][0], m[i1][1], w[w_[i2]][0], w[w_[i2]][1]) * cwn[i1][i2])
        for i in range(arr[2]):
            for i1 in range(arr[6]):
                cost_trans_r += 40.5 * cr[i][i1] * rr[i] * (cd[i1] * 100 +
                                                            distance(c[i1][0], c[i1][1], t[t_[i1]][0], t[t_[i1]][1]))

        tan_w_built = arr[3] * 0.7

        tan_trans_c_1 = tan_trans_c_2 = tan_trans_r = 0
        for i1 in range(arr[2]):
            for i2 in range(num_s * 3):
                num = sum(cr[i1][:arr[6]])
                group = int(i2 / 3)
                tan_trans_c_1 += 0.12 * distance(r[r_[i2]][0], r[r_[i2]][1], s[group][s_[i2]][0],
                                                 s[group][s_[i2]][1]) / 300 * \
                                 num * 2 + 0.16 * distance(m[i1][0], m[i1][1], s[group][s_[i2]][0], s[group][s_[i2]][1]
                                                           ) / 300 * num
        for i1 in range(arr[2]):
            for i2 in range(arr[4]):
                num_d = cr[i1][i2] - cwn[i1][i2]
                tan_trans_c_2 += 0.21 * distance(m[i1][0], m[i1][1], d[i2][0], d[i2][1]) * num_d / 100 + \
                                 0.21 * cd[i2] * num_d + \
                                 0.21 * distance(d[i2][0], d[i2][1], w[w_[i2]][0], w[w_[i2]][1]) * cwn[i1][i2] / 100 + \
                                 0.21 * distance(m[i1][0], m[i1][1], w[w_[i2]][0], w[w_[i2]][1]) * cwn[i1][i2] / 100
        for i in range(arr[2]):
            for i1 in range(arr[6]):
                tan_trans_r += 0.21 * cr[i][i1] * rr[i] * (
                        cd[i1] + distance(c[i1][0], c[i1][1], t[t_[i1]][0], t[t_[i1]][1]) / 100)

        fun_ps = (0.39 * (cost_produce_rsm + cost_trans_c_1 / 10000) / max_value[x][0]
                    + 0.28 * (0.27 * (tan_produce_rsm + tan_trans_c_1) / max_value[x][1]
                              + 0.27 * gas_produce_rsm / max_value[x][2] +
                  0.23 * water_produce_rsm / max_value[x][3] + 0.23 * solid_produce_rsm / max_value[x][4]))

        fun_ss = (0.39 * (cost_w_built + cost_trans_c_2 / 10000) / max_value[x][0]
                    + 0.28 * (0.27 * (tan_w_built + tan_trans_c_2) / max_value[x][1]))

        fun_rs = (0.39 * (cost_produce_t + cost_trans_r / 10000) / max_value[x][0]
                    + 0.28 * (0.27 * (tan_produce_t + tan_trans_r) / max_value[x][1]
                              + 0.27 * gas_produce_t / max_value[x][2] +
                  0.23 * water_produce_t / max_value[x][3] + 0.23 * solid_produce_t / max_value[x][4]))

        return fun_ps, fun_ss, fun_rs

    functions = []
    for _ in range(len(population)):
        a, b, o = func2(population[_])
        func_ = [a, b, o, func1(population[_])]
        functions.append(func_)

    return functions


def crossover_mutation(parent1, parent2):
    crossover = []
    for _ in range(len(parent1)):
        if random.uniform(0, 1) < 0.5:
            crossover.append(parent1[_])
        else:
            crossover.append(parent2[_])
    return crossover


def breading(population_0, population_1):
    count_0 = count_1 = count = 0
    offspring = []

    while count_0 < 5:
        i, j = random.randint(0, 9), random.randint(0, 9)
        parent1 = i if i < j else j

        i, j = random.randint(0, 9), random.randint(0, 9)
        parent2 = i if i < j else j

        while parent1 == parent2:  # 如果选择到的两个父代完全一样，则重选另一个
            i, j = random.randint(0, 9), random.randint(0, 9)
            parent2 = i if i < j else j

        offspring_ = crossover_mutation(population_0[parent1], population_0[parent2])
        offspring.append(offspring_)
        count_0 += 1

    while count_1 < 5:
        i, j = random.randint(0, 9), random.randint(0, 9)
        parent1 = i if i < j else j

        i, j = random.randint(0, 9), random.randint(0, 9)
        parent2 = i if i < j else j

        while parent1 == parent2:  # 如果选择到的两个父代完全一样，则重选另一个
            i, j = random.randint(0, 9), random.randint(0, 9)
            parent2 = i if i < j else j

        offspring_ = crossover_mutation(population_1[parent1], population_1[parent2])
        offspring.append(offspring_)
        count_1 += 1

    while count < 10:
        i, j = random.randint(0, 9), random.randint(0, 9)
        parent1 = i if i < j else j

        i, j = random.randint(0, 9), random.randint(0, 9)
        parent2 = i if i < j else j

        offspring_ = crossover_mutation(population_0[parent1], population_1[parent2])
        offspring.append(offspring_)
        count += 1

    return offspring


def breed1(population, count_offspring):
    count = 0
    offspring = []
    pop_len = len(population)
    while count < count_offspring:
        i, j = random.randint(0, pop_len), random.randint(0, pop_len)
        while i == j:
            i = random.randint(0, pop_len)

        offspring_ = crossover_mutation(population[i], population[j])
        offspring.append(offspring_)
        count += 1
    return offspring


def breed2(population, count_offspring):
    count = 0
    offspring = []
    while count < count_offspring:
        i, j = random.randint(0, 9), random.randint(0, 9)
        offspring_ = crossover_mutation(population[i], population[j])
        offspring.append(offspring_)
        count += 1
    return offspring


def mutation1(offspring, x, mutation_rate=0.1):
    arr = num_arr[x]
    num_s = int(arr[1] / 10)
    count = num_s * 4 + arr[4] * 2
    for i in range(len(offspring)):
        for j in range(count):
            if j in range(num_s * 3):
                probability = random.uniform(0, 1)
                if probability < mutation_rate:
                    offspring[i][j] = random.randint(0, arr[0] - 1)
            elif j in range(num_s * 3, num_s * 4):
                j = num_s * 3 + (j - num_s * 3) * 3
                probability = random.uniform(0, 1)
                if probability < mutation_rate:
                    a = [_ for _ in range(10)]
                    result = random.sample(a, 3)
                    offspring[i][j] = result[0]
                    offspring[i][j + 1] = result[1]
                    offspring[i][j + 2] = result[2]
            elif j in range(num_s * 4, num_s * 4 + arr[4]):
                j = j + num_s * 2
                probability = random.uniform(0, 1)
                if probability < mutation_rate:
                    offspring[i][j] = random.randint(0, arr[3] - 1)
            elif j in range(num_s * 4 + arr[4], count):
                j = j + num_s * 2
                probability = random.uniform(0, 1)
                if probability < mutation_rate:
                    offspring[i][j] = random.randint(0, arr[5] - 1)
    return offspring


def mutation2(offspring, x, mutation_rate=0.1):
    arr = num_arr[x]
    for _ in range(len(offspring)):
        for i in range(len(offspring[_])):
            probability = random.uniform(0, 1)
            if probability < mutation_rate:
                offspring[_][i] = random.randint(0, arr[3] - 1)
    return offspring


def new(population, function, x):
    arr = num_arr[x]
    num_s = int(arr[1] / 10)
    pop_ps = []
    pop_ss_wi = []
    pop_ss = []
    pop_rs = []
    func = np.array(function)

    sorted_indices = np.argsort(func[:, 0])[:20]
    for _ in sorted_indices:
        pop_ps.append(population[_][num_s * 6])
    pop_ps += breed1(pop_ps, 20)

    sorted_indices1 = np.argsort(func[:, 1])[:10]
    for _ in sorted_indices1:
        pop_ss.append(population[_][num_s * 6: num_s * 6 + arr[4]])

    sorted_indices3 = np.argsort(func[:, 3])[:10]
    for _ in sorted_indices3:
        pop_ss_wi.append(population[_][num_s * 6: num_s * 6 + arr[4]])

    pop_ss += pop_ss_wi
    pop_ss += breed1(pop_ss, 5)
    pop_ss += breed1(pop_ss_wi, 5)
    pop_ss += breed2(pop_ss_wi, 10)

    sorted_indices2 = np.argsort(func[:, 2])[:20]
    for _ in sorted_indices2:
        pop_rs.append(population[_][num_s * 6 + arr[4]:])
    pop_rs += breed1(pop_ps, 20)

    pop = []
    for _ in range(40):
        pop.append(pop_ps[_]+pop_ss[_]+pop_rs[_])
    mutation1(pop, x)

    return pop


def best(population, function, x):
    arr = num_arr[x]
    num_s = int(arr[1] / 10)
    pop_ps = []
    pop_ss = []
    pop_rs = []
    func = np.array(function)

    sorted_indices = np.argsort(func[:, 0])[:1]
    for _ in sorted_indices:
        pop_ps.append(population[_][num_s * 6])

    sorted_indices1 = np.argsort(func[:, 1])[:1]
    for _ in sorted_indices1:
        pop_ss.append(population[_][num_s * 6: num_s * 6 + arr[4]])

    sorted_indices2 = np.argsort(func[:, 2])[:1]
    for _ in sorted_indices2:
        pop_rs.append(population[_][num_s * 6 + arr[4]:])

    pop = pop_ps[0] + pop_ss[0] + pop_rs[0]

    return pop


if __name__ == '__main__':
    L = 0  # 算例
    num = 1
    while num < 11:
        t = 1
        start_time = time.time()
        population = initial_population(L)
        population += initial_population(L)
        while t <= 300:  # 迭代
            func = get_func(population, L)
            population = new(population, func, L)
            t = t + 1
        end_time = time.time()
        runtime = end_time - start_time
        population = best(population, get_func(population, L), L)
        num += 1
