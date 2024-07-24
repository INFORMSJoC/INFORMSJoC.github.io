import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools
import scipy as sp
import numpy as np
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
     #对随机生成的连通图上的每个点进行赋权
    for node in G.nodes() :
        G.nodes[node]['weight'] = random.randint(1, 10000)
        print(f"Node {node} weight: {G.nodes[node]['weight']}")

    return G

#生成white点集并建立起逆映射
def terminal_nodes(graph):
    terminals = set()
    mapping = {}
    for node in graph.nodes():
        new_node = f"{node}_1"
        terminals.add(new_node)  # 添加新节点
        mapping[node] = new_node  # 记录节点映射关系
    # 生成逆映射
    inverse_mapping = {v: k for k, v in mapping.items()}
    return terminals, inverse_mapping

#更新图black点集和terminal点集
def generate_new_graph_1(ori_graph, black_nodes, terminals, vertices):
    graph = ori_graph.copy()

    vertices_1 = vertices.intersection(ori_graph.nodes())
    random_node = random.choice(list(vertices_1))
    vertices_1.remove(random_node)
 
    for node in vertices_1:
        for neighbor in ori_graph.neighbors(node):
            graph.add_edge(random_node, neighbor)
    graph.remove_nodes_from(vertices_1)
    terminals = terminals - vertices
    terminals.add(random_node)
    black_nodes = black_nodes - vertices
    black_nodes.add(random_node)
    graph.nodes[random_node]['weight'] = 0

    return graph, black_nodes, terminals

#图中部分节点集合的权重之和
def sum_weight(graph, nodes):
    weight_sum = 0
    for node in nodes:
        if node in graph.nodes():
            # 获取节点的权重属性，并累加到权重之和中
            weight_sum += graph.nodes[node]['weight']
    return weight_sum

#计算点加权的最短路，不包括起始点,输出的路是全集
def point_weighted_shortest_path(ori_graph, source, target, inverse_mapping):
    graph = ori_graph.copy()

    if not graph.has_node(target):# 检查节点是否已经存在于图中
        node1 = inverse_mapping[target]
        graph.add_node(target)
        graph.nodes[target]['weight'] = 0
        for neighbor in set(graph.neighbors(node1)) | {node1}:
            graph.add_edge(target, neighbor)
    
    distances = {node: float('inf') for node in graph.nodes()}
    distances[source] = 0  #不包括起点权重

    predecessors = {}
    unvisited = set(graph.nodes())
    predecessors[target] = source
    while unvisited:
        current_node = min(unvisited, key=lambda node: distances[node])
        if current_node == target:
            break
        if target in graph.neighbors(current_node):
            weight = graph.nodes[target]['weight'] 
            distances[target] = distances[current_node] + weight 
            predecessors[target] = current_node
            break
        unvisited.remove(current_node)
        for neighbor in graph.neighbors(current_node):
            if neighbor in unvisited:
                weight = G.nodes[neighbor]['weight']  
                new_distance = distances[current_node] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_node
    shortest_path = [target]
    while target != source:
        target = predecessors[target]
        shortest_path.append(target)
    shortest_path.reverse()
    if len(shortest_path) > 1:
        shortest_distance = distances[shortest_path[-2]] # 最短路计算到倒数第2个点
    else :
        shortest_distance = distances[shortest_path[-1]]
    path_nodes = set(shortest_path) 
    return path_nodes, shortest_distance

#计算图中包含点x,y,v三个点的最小Steinertree的点权之和,不包括点vertices
def min_steiner_tree(graph, vertices, vertice, inverse_mapping):
    shortest_distance = float('inf')
    shortest_tree = set()
    if len(vertices) == 3:

        for node in graph.nodes() :
            shortest_tree_node = set()
            for node_1 in vertices:
                path_nodes, shortest_distance_1 = point_weighted_shortest_path(graph, node, node_1, inverse_mapping)
                #print("边到路的映射0:", node, node_1, path_nodes, shortest_distance)
                shortest_tree_node.update(path_nodes)
            
            tree_weight = sum_weight(graph, shortest_tree_node) - graph.nodes[vertice]['weight']#不属于graph的点默认赋值为0
            #print("边到路的映射00:", shortest_tree_node, tree_weight, shortest_distance)
            if tree_weight < shortest_distance:
                shortest_tree = shortest_tree_node
                shortest_distance = tree_weight
                #print("边到路的映射000:", shortest_tree, shortest_tree_node)
            
    else :
        if len(vertices) == 2:
            for node in vertices:
                if node != vertice:
                    shortest_tree, shortest_distance = point_weighted_shortest_path(graph, vertice, node, inverse_mapping)
            
            shortest_distance = shortest_distance - graph.nodes[vertice]['weight'] 


        else:
            shortest_tree = vertices
            shortest_distance = 0

    #print("边到路的映射1:", vertices, vertice, shortest_tree, shortest_distance)

    return shortest_tree, shortest_distance


#构造一个新的完全图，节点是剩余所有的terminal点，边权是两个terminal点之间的最短路的权重(不包括node点的权重)
def generate_matching_graph(original_graph, vertices, node, inverse_mapping):
    new_graph = nx.complete_graph(vertices)
    edge_shortest_path = {}

    for (u, v) in new_graph.edges():
        vertices_1 = set()
        vertices_1.add(node)
        vertices_1.add(u)
        vertices_1.add(v)
        shortest_tree, shortest_distance = min_steiner_tree(original_graph, vertices_1, node, inverse_mapping)
        edge_shortest_path[(u, v)] = shortest_tree
        edge_shortest_path[(v, u)] = shortest_tree
        new_graph[u][v]['weight'] = shortest_distance

    return new_graph, edge_shortest_path

#构造一个新图，根据需要的匹配数
def generate_graph_l(graph, number_1):
    new_graph = graph.copy()
    dummy_nodes = ['dummy_' + str(i) for i in range(number_1)]
    new_graph.add_nodes_from(dummy_nodes)
    for dummy_node in dummy_nodes:
        for node in graph.nodes():
            new_graph.add_edge(dummy_node, node)
            new_graph[dummy_node][node]['weight'] = 0
    for (u, v) in new_graph.edges():
        if 'weight' not in new_graph[u][v]:
            print("没有权重的边:", (u, v))
            
    return new_graph, dummy_nodes

# 输出与点集 dummy_nodes 没有交集的边集对应路的点集
def nodes_without_dummy(matching, dummy_nodes, edge_shortest_path):
    #print("匹配1：", matching)
    new_matching = set(matching)
    path_nodes = set()
    for edge in matching:
        u, v = edge
        if u in dummy_nodes or v in dummy_nodes:
            new_matching.remove(edge)
    #print("匹配2：", new_matching)
    for edge in new_matching:
        path_nodes_1 = edge_shortest_path[edge]
        path_nodes.update(path_nodes_1)

    
    return path_nodes

#计算边加权最小完美匹配
def min_weight_matching(graph):
    new_graph = graph.copy()
    sum_weight = 0
    weights_1 = 0
    for (u, v) in new_graph.edges():
        if new_graph[u][v]['weight'] > weights_1:
            weights_1 = new_graph[u][v]['weight']

    weights_1 += 1

    for (u, v) in new_graph.edges():
        # 重新设置边的权重
        new_graph[u][v]['weight'] = weights_1 - new_graph[u][v]['weight']
    
    min_matching = nx.max_weight_matching(new_graph, weight='weight', maxcardinality=True)
    for  (u, v) in min_matching:
        sum_weight += graph[u][v]['weight']

    return min_matching, sum_weight



#计算图中以node为中心，包含number_1个terminal点最小3+branch-spider
def min_matching(graph, new_complete_graph, node, number_1, inverse_mapping, edge_shortest_path):
    total_weight =  float('inf')
    shortest_spider_3 = set()
    if number_1 % 2 != 0:
        for node_1 in new_complete_graph.nodes():
            shortest_path, shortest_distance = point_weighted_shortest_path(graph, node, node_1, inverse_mapping)
            path_nodes = set(shortest_path)
            G1 = new_complete_graph.copy()  # 首先复制图 G，以保留原始图 G 的结构
            G1.remove_node(node_1)
            num_nodes = G1.number_of_nodes()
            number_2 = num_nodes - number_1 + 1
            G1, dummy_nodes = generate_graph_l(G1, number_2)
            min_matching, matching_weight= min_weight_matching(G1)
            if total_weight > matching_weight + graph.nodes[node]['weight'] + shortest_distance:
                total_weight = matching_weight + graph.nodes[node]['weight'] + shortest_distance
                path_nodes_1 = nodes_without_dummy(min_matching, dummy_nodes, edge_shortest_path)
                path_nodes.update(path_nodes_1)
                shortest_spider_3 = path_nodes         

    else :
        G1 = new_complete_graph.copy()
        #print("测试图G1：", G1.nodes())
        num_nodes = G1.number_of_nodes()
        number_2 = num_nodes - number_1
        G1, dummy_nodes = generate_graph_l(G1, number_2)
        min_matching, matching_weight = min_weight_matching(G1)
        if total_weight > matching_weight + graph.nodes[node]['weight']:
            total_weight = matching_weight + graph.nodes[node]['weight']
            shortest_spider_3 = nodes_without_dummy(min_matching, dummy_nodes, edge_shortest_path)
    
    return shortest_spider_3, total_weight

#定义算法2，找出效率最3+branch-spider
def algorithm_branch_spider_3(graph, terminals, inverse_mapping):
    benefit_branch_spider_3 = set()
    benefit_rate = float('inf')
    number_2 = len(terminals) + 1
    for node in graph.nodes():
        new_complete_graph, edge_shortest_path = generate_matching_graph(graph, terminals, node, inverse_mapping)
        for number_1 in range(3, number_2):
            shortest_spider_3, total_weight = min_matching(graph, new_complete_graph, node, number_1, inverse_mapping, edge_shortest_path)#尽量合并成一个
            #print("测试4：", shortest_spider_3)
            spider_rat = total_weight / number_1
            if spider_rat < benefit_rate:
                benefit_rate = spider_rat
                benefit_branch_spider_3 = shortest_spider_3
    return benefit_branch_spider_3

#定义算法1，计算出一个CDS
def algorithm_3(new_graph):
    graph = new_graph.copy()
    i = 1
    cd_set = set()  #点集connected_dominating_set初始化为空集
    black_nodes = set()
    terminals, inverse_mapping = terminal_nodes(graph)
    #print("测试3：", terminals, inverse_mapping)
    while len(terminals) > 2 :
        benefit_branch_spider_3 = algorithm_branch_spider_3(graph, terminals, inverse_mapping)
        print("最X个branch_spider_3:", i, benefit_branch_spider_3)
        i += 1
        spider_nodes = benefit_branch_spider_3.intersection(graph.nodes())
        cd_set.update(spider_nodes)
        graph, black_nodes, terminals = generate_new_graph_1(graph, black_nodes, terminals, benefit_branch_spider_3)
        #print("测试4：", graph.nodes(), black_nodes, terminals, inverse_mapping)
    if len(terminals) == 2 :
        source = random.choice(list(terminals.intersection(black_nodes)))
        terminals.remove(source)
        for target in terminals :
            shortest_path, shortest_distance = point_weighted_shortest_path(graph, source, target, inverse_mapping)
            spider_nodes = shortest_path.intersection(graph.nodes())
        cd_set.update(spider_nodes)

    return cd_set


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




#循环次数
repeat_time = 3

for i in range(repeat_time) :
    # 生成连通图
    n_nodes = 20
    min_degree_m = 2
    max_degree_m = 10
    G = generate_random_connected_graph(n_nodes, min_degree_m, max_degree_m)

    #计算最大最小度
    degrees = dict(G.degree())
    max_degree = max(degrees.values())
    min_degree = min(degrees.values())


    rand_m = 1
    start_time = time.time()
    #运行算法1，计算图G的连通控制集
    CD_set = algorithm_1(G, rand_m)

    end_time = time.time()

     # 计算算法运行时间（以秒为单位）
    run_time = end_time - start_time

    print("程序1运行时间:", run_time)   

    numbor_2 = potential_function(G, CD_set, rand_m)
    min_weight_CDS = sum(G.nodes[node]['weight'] for node in CD_set)
    # 输出连通控制集
    print("近似连通控制集:", CD_set, min_weight_CDS)     
    print("函数值是否为1:", numbor_2) 
     
    #运行最优算法1，计算图G的连通控制集
    start_time = time.time()

    optimal_set = algorithm_3(G)
    
    end_time = time.time()

    # 计算算法运行时间（以秒为单位）
    run_time = end_time - start_time

    print("程序2运行时间:", run_time)    

    numbor_3 = potential_function(G, optimal_set, rand_m)
    min_weight_OPT = sum(G.nodes[node]['weight'] for node in optimal_set)
    # 输出连通控制集
    print("连通控制集2:", optimal_set, min_weight_OPT)     
    print("函数值是否为1:", numbor_3) 

     # 输出最大最小度
    print("最大度:", max_degree)
    print("最小度:", min_degree)
    # 计算并输出近似比
    approximation_rate = min_weight_CDS/min_weight_OPT
    print("近似算法近似比为:", approximation_rate)

