import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rcParams['font.sans-serif']=['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False  # 用来正常显示负号 用来正常显示中文标签

 #加载武汉地铁数据集
df1 = pd.read_csv("武汉地铁边.csv")
G1 = nx.from_pandas_edgelist(df1, 'source', 'target', create_using = nx.Graph())

# 加载武汉地铁添加共享单车数据集
df2 = pd.read_csv("武汉地铁边添加共享单车.csv")
G2 = nx.from_pandas_edgelist(df2, 'source', 'target', create_using = nx.Graph())

#print(len(G1.nodes()), "len(G2.nodes())")
n=len(G1.nodes())

#网络可视化
nx.draw(G1,node_size=100,with_labels=6666)
plt.show()
nx.draw(G2,node_size=100,with_labels=6666)
plt.show()

##度分布
# 定义求度分布的函数
def get_pdf(G):
    all_k = [G.degree(i) for i in G.nodes()]
    k = list(set(all_k))  # 获取所有可能的度值
    N = len(G.nodes())

    Pk = []
    for ki in sorted(k):
        c = 0
        for i in G.nodes():
            if G.degree(i) == ki:
                c += 1
        Pk.append(c / N)

    return sorted(k), Pk

k1, Pk1 = get_pdf(G1)
k2, Pk2 = get_pdf(G2)
#print(k1,Pk1)

#绘制度分布
plt.figure(figsize=(12,6))

plt.plot(k1, Pk1, 'ro-', label='武汉地铁')
plt.legend(loc=0)
plt.xlabel("$k$")
plt.ylabel("$p_k$")
plt.title('武汉地铁网络度分布')

plt.plot(k2, Pk2, color='g', label='武汉地铁加单车')
plt.legend(loc=0)
plt.xlabel("$k$")
plt.ylabel("$p_k$")
plt.title('武汉地铁网络度分布')
plt.show()


##蓄意攻击
# 计算原始网络的巨连通分支大小
largest_cc = max(nx.connected_components(G1), key=len)
initial_size = len(largest_cc) / n
# 静态攻击：始终在初始网络上攻击，按照节点度值大小将占比为f的节点移除，并计算剩余网络的巨连通分支相对大小
###不添加共享单车的网络
# 获取初始网络节点度值排序后的列表
degrees = dict(G1.degree())
sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)

nums =51
f_values = np.linspace(0, 1, num=nums)
relative_sizes = np.zeros(nums)
relative_sizes[0] = initial_size
for i in range(1, nums):
    # 计算要移除的节点列表
    num_removed = int(f_values[i] * n)
    removed_nodes = [x[0] for x in sorted_degrees[:num_removed]]

    # 移除节点并计算剩余网络的巨连通分支大小
    G_removed = G1.copy()
    G_removed.remove_nodes_from(removed_nodes)
    if len(G_removed)==0:
        break
    largest_cc_removed = max(nx.connected_components(G_removed), key=len)
    relative_sizes[i] = len(largest_cc_removed) / n

###添加共享单车的网络
# 获取初始网络节点度值排序后的列表
degrees = dict(G2.degree())
sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)

nums =51
f_values = np.linspace(0, 1, num=nums)
relative_sizes2 = np.zeros(nums)
relative_sizes2[0] = initial_size
for i in range(1, nums):
    # 计算要移除的节点列表
    num_removed = int(f_values[i] * n)
    removed_nodes = [x[0] for x in sorted_degrees[:num_removed]]

    # 移除节点并计算剩余网络的巨连通分支大小
    G_removed = G1.copy()
    G_removed.remove_nodes_from(removed_nodes)
    if len(G_removed)==0:
        break
    largest_cc2_removed = max(nx.connected_components(G_removed), key=len)
    relative_sizes2[i] = len(largest_cc2_removed) / n
# 绘制相对大小随着占比f的变化图
plt.figure(figsize=(12,6))
plt.plot(f_values, relative_sizes, label="武汉地铁",color="r", linewidth=2)
plt.plot(f_values, relative_sizes2,label="武汉地铁加单车", color='g', linewidth=2)
plt.xlabel('占比 f')
plt.ylabel('巨连通分支相对大小')
plt.title('蓄意攻击')
plt.show()

#随机攻击
###不添加共享单车的网络
# 计算不同占比f下剩余网络的巨连通分支相对大小
f_values = np.linspace(0, 1, num=101)
relative_sizes = np.zeros(101)
for i, f in enumerate(f_values):
    # 随机移除占比为f的节点
    removed_nodes = np.random.choice(G1.nodes(), size=int(f * len(G1)), replace=False)
    G_removed = G1.copy()
    G_removed.remove_nodes_from(removed_nodes)
    if len(G_removed)==0:
        break

 # 计算剩余网络的巨连通分支大小
    largest_cc_removed = max(nx.connected_components(G_removed), key=len)
    relative_sizes[i] = len(largest_cc_removed) / len(G1)

###添加共享单车的网络
# 计算不同占比f下剩余网络的巨连通分支相对大小
f_values = np.linspace(0, 1, num=101)
relative_sizes2 = np.zeros(101)
for i, f in enumerate(f_values):
    # 随机移除占比为f的节点
    removed_nodes = np.random.choice(G2.nodes(), size=int(f * len(G2)), replace=False)
    G_removed = G2.copy()
    G_removed.remove_nodes_from(removed_nodes)
    if len(G_removed)==0:
        break


    # 计算剩余网络的巨连通分支大小
    largest_cc2_removed = max(nx.connected_components(G_removed), key=len)
    relative_sizes2[i] = len(largest_cc2_removed) / len(G1)


# 绘制相对大小随着占比f的变化图
plt.figure(figsize=(12,6))
plt.plot(f_values, relative_sizes, color='r')
plt.plot(f_values, relative_sizes2, color='g')
plt.xlabel('占比 f')
plt.ylabel('巨连通分支相对大小')
plt.title('随机攻击')
plt.show()

