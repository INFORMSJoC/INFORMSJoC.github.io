import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools
import scipy as sp
import time

#随机生成一个连通图
def generate_random_connected_graph(n_nodes, min_degree_m, max_degree_m):
    G = nx.Graph()
    G.add_node(0)

    for i in range(1, n_nodes):
        node_to_connect = random.choice(list(G.nodes))
        G.add_edge(i, node_to_connect)
    
    for node in G.nodes():
        connections = random.randint(min_degree_m, max_degree_m)
        #print("点度:", node, connections)
        neighbors_nodes = set(G.neighbors(node))
        connections = connections - len(neighbors_nodes)
        potential_nodes = set(range(n_nodes)) - {node} - set(G[node])
        if connections > 0:
            for _ in range(connections):
                if not potential_nodes:
                    break
                new_node = random.choice(list(potential_nodes))
                G.add_edge(node, new_node)
                potential_nodes.remove(new_node)
    return G



#计算图graph的点导出子图的连通分支个数
def number_c1(G, vertices):
    sub_graph = G.subgraph(vertices)
    return nx.number_connected_components(sub_graph)

#计算点还需要的覆盖次数
def need_cover(G, vertice, vertices, rand_m):
    neighbors = set(G.neighbors(vertice))
    cover_need = rand_m - len(neighbors & vertices)
    if cover_need < 0:
        cover_need = 0 
    return cover_need

#计算选择点集后还需要的总的覆盖次数
def need_cover_all(G, vertices, rand_m):
    total_need = 0
    for node in G.nodes:
        if node not in vertices:
            neighbors = set(G.neighbors(node))
            vertices = set(vertices)
            cover_need = rand_m - len(neighbors & vertices)
            if cover_need > 0:
                total_need += cover_need
    return total_need

#定义potential_function
def potential_function(G, vertices, rand_m):
    number_f = number_c1(G, vertices) + need_cover_all(G, vertices, rand_m)
    return number_f

#定义点vertex满足引理条件的邻集
def condition_neighbors(graph, vertex, vertices):
    neighbors_1 = set()
    neighbors_2 = set(graph.neighbors(vertex)) - vertices
    for u in neighbors_2 :
        S_1 = vertices.copy()
        S_1.add(u)
        cover_need = need_cover_all(G, vertices, rand_m) - need_cover_all(G, S_1, rand_m)
        number_c =  number_c1(graph, vertices) - number_c1(graph, S_1)
        if cover_need == 0 and number_c == 0:
            neighbors_1.add(u)
    return neighbors_1  

#输出集合中权重最小的点
def min_weight_node(G, vertices):
    weight_1 = float('inf')
    for node in vertices:
        if G.nodes[node]['weight'] < weight_1:
            min_vertex = node
            weight_1 = G.nodes[node]['weight']
    return min_vertex

#定义算法2，找出效率最高的星状结构
def algorithm_2(G, vertices, rand_m):
    max_benefit_star = set()
    max_benefit_rate = 0
    for vertex in G.nodes() - vertices:
        potential_Star = {vertex}
        tem_set =vertices.copy()
        tem_set.add(vertex)
        weight_v1 = G.nodes[vertex]['weight']
        marginal_benefit = - potential_function(G, tem_set, rand_m) + potential_function(G, vertices, rand_m)
        marginal_benefit_rate = marginal_benefit/weight_v1
        if need_cover(G, vertex, vertices, rand_m) == 0: #如果点vertex没有覆盖需求，就继续选合适的邻点，否则直接输出S_2[vertex]
            neighbor_set2 = condition_neighbors(G, vertex, vertices) #计算出满足引理条件的vertex的邻集
            #lenth_set = len(neighbor_set2)
            #if lenth_set > 0:
                #print("符合引理条件的邻集:", neighbor_set2)
            while len(neighbor_set2) != 0:
                u = min_weight_node(G, neighbor_set2)
                neighbor_set2.remove(u)
                weight_v2 = G.nodes[u]['weight']
                tem_set2 = tem_set.copy()
                tem_set2.add(u)
                if number_c1(G, tem_set) - number_c1(G, tem_set2) == 1 and 1/weight_v2 > marginal_benefit_rate:
                    potential_Star.add(u)
                    tem_set.add(u)
                    weight_v1 += weight_v2
                    marginal_benefit += 1  
                    marginal_benefit_rate = marginal_benefit/weight_v1 
        if marginal_benefit_rate > max_benefit_rate:
            max_benefit_star = potential_Star
            max_benefit_rate = marginal_benefit_rate
    return max_benefit_star

#定义近似算法1，计算出一个（1，m）CDS
def algorithm_1(G, rand_m):
    i = 1
    cd_set = set()  #点集connected_dominating_set初始化为空集
    weight_set = 0
    while number_c1(G, cd_set) + need_cover_all(G, cd_set, rand_m) > 1 :
        eff_star = algorithm_2(G, cd_set, rand_m)
        weight_set = sum(G.nodes[node]['weight'] for node in eff_star)
        lenth_set_1 = len(eff_star)
        if lenth_set_1 > 1:
            print("最", i, "个最优的星状结构:", eff_star, weight_set)
        cd_set.update(eff_star)
        i += 1
    return cd_set

#定义最优解算法1，计算出一个（1，m）CDS
def optimal_algorithm_1(G, rand_m):
    cd_set = set()  #点集connected_dominating_set初始化为空集
    min_weight = float('inf')
    for i in range(2, n_nodes):
        node_pairs = list(itertools.combinations(G.nodes, i))
        # 遍历所有包含i个点的子集
        for pair in node_pairs:
            number_f = potential_function(G, pair, rand_m)
            if number_f == 1:
                weight_1 = sum(G.nodes[node]['weight'] for node in pair)
                if weight_1 < min_weight:
                    min_weight = weight_1
                    pair = set(pair)
                    cd_set = pair
                    print("连通控制集:", cd_set, min_weight)
    return cd_set


#循环次数
repeat_time = 10
number_weight_1 = 0
number_weight_2 = 0
for i in range(repeat_time) :
    # 生成连通图
    n_nodes = 30
    min_degree_m = 2
    max_degree_m = 4
    G = generate_random_connected_graph(n_nodes, min_degree_m, max_degree_m)

    #计算最大最小度
    degrees = dict(G.degree())
    max_degree = max(degrees.values())
    min_degree = min(degrees.values())

    #对随机生成的连通图上的每个点进行赋权
    for node in G.nodes() :
        G.nodes[node]['weight'] = random.randint(1, 10000)
        #print(f"Node {node} weight: {G.nodes[node]['weight']}")

    rand_m = 2
    start_time = time.time()
    #运行算法1，计算图G的连通控制集
    CD_set = algorithm_1(G, rand_m)

    end_time = time.time()

    run_time = end_time - start_time

    print("近似算法运行时间1:", run_time) 

    numbor_2 = potential_function(G, CD_set, rand_m)
    min_weight_CDS = sum(G.nodes[node]['weight'] for node in CD_set)
    number_weight_1 += min_weight_CDS
    # 输出连通控制集
    print("近似连通控制集:", CD_set, min_weight_CDS)     
    print("函数值是否为1:", numbor_2) 


    start_time = time.time()
     
    #运行最优算法1，计算图G的连通控制集
    optimal_set = optimal_algorithm_1(G, rand_m)

    end_time = time.time()
    run_time = end_time - start_time
    print("最优算法运行时间2:", run_time) 
    numbor_3 = potential_function(G, optimal_set, rand_m)
    min_weight_OPT = sum(G.nodes[node]['weight'] for node in optimal_set)

    number_weight_2 += min_weight_OPT
    # 输出连通控制集
    print("最小连通控制集:", optimal_set, min_weight_OPT)     
    print("函数值是否为1:", numbor_3) 

     # 输出最大最小度
    print("最大度:", max_degree)
    print("最小度:", min_degree)
    # 计算并输出近似比
    approximation_rate = min_weight_CDS/min_weight_OPT
    print("近似算法近似比为:", approximation_rate)

print("近似算法pingjun近似比为:", number_weight_1 / repeat_time, number_weight_2 / repeat_time, number_weight_1 / number_weight_2)

