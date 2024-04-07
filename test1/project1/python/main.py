import time
import numpy as np


############################################################################
# Add any modules you want to use here~
############################################################################
# define class stack for DFS
class Stack():
    def __init__(self):
        self.item = []

    def isEmpty(self):
        return len(self.item)==0
    
    def push(self, data):
        self.item.append(data)

    def pop(self):
        if (self.isEmpty()):
            return None
        else:
            return self.item.pop()
        
    def size(self):
        return len(self.item)



class DFS():
    def __init__(self, G, root) -> None:
        """
        G: UndirectedGraph
        root: node slove for structure diversity
        """
        self.graph = G
        self.root = root
        self.vertex_list = G.adj_list[G.vertex_dict[root]]


    def partialSearch(self):
        # initialization
        stack = Stack()
        record_dict = {}
        visited_num = 0
        vertex_num = len(self.vertex_list)

        for v in self.vertex_list:
            record_dict[v] = [False,False]   # ifvisited, ifmarked#
        
        # partial dfs
        for vertex in self.vertex_list:
            stack.push((vertex,True))

        while not stack.isEmpty():
            visit_vertex, is_parent_root = stack.pop()
            visit_vertex_id = self.graph.vertex_dict[visit_vertex]
            if not record_dict[visit_vertex][0]:
                record_dict[visit_vertex][0] = True
                visited_num += 1
                if is_parent_root:
                    record_dict[visit_vertex][1] = True

            # stop when all vertices have been visited
            if visited_num == vertex_num:
                break       

            for adj in self.graph.adj_list[visit_vertex_id]:
                if adj in self.vertex_list:
                    if not record_dict[adj][0]:
                        stack.push((adj,False))

        structure_div = 0
        for _, value in record_dict.items():
            if value[1]:
                structure_div += 1

        return structure_div


class DisjointSet():
    def __init__(self, G, node):
        self.graph = G
        self.node = node
        self.vertex_list = G.adj_list[G.vertex_dict[node]]
        self.edge_set = set()
        for vertex in self.vertex_list:
            for adj_ver in G.adj_list[G.vertex_dict[vertex]]:
                if adj_ver in self.vertex_list:
                    self.edge_set.add((min(vertex,adj_ver),max(vertex,adj_ver)))
        self.djs_dict = {}
        for vertex in self.vertex_list:
            self.djs_dict[vertex] = [-1,1]  #parent, setsize#

    def union(self, v1, v2):
        v1 = self.find(v1)
        v2 = self.find(v2)
        if v1!=v2: 
            if self.djs_dict[v1][1] < self.djs_dict[v2][1]:
                self.djs_dict[v2][1] += self.djs_dict[v1][1]
                self.djs_dict[v1][0] = v2
            else :
                self.djs_dict[v1][1] += self.djs_dict[v2][1]
                self.djs_dict[v2][0] = v1

    def find(self, v):
        if self.djs_dict[v][0] == -1:
            return v
        else:
            self.djs_dict[v][0] = self.find(self.djs_dict[v][0])
            return self.djs_dict[v][0]

    def createDJS(self):
        for edge in self.edge_set:
            self.union(edge[0],edge[1])
        djs_num = 0
        for _, value in self.djs_dict.items():
            if value[0] == -1:
                djs_num += 1
        return djs_num




############################################################################
# You can define any auxiliary functions~
############################################################################


def StructureDiversity(G):
    # intialization of the result
    result = [0] * (G.vertex_num)

    ############################################################################
    # TODO: Your code here~
    # Input: G
    # Output: the structure diversity of all vertices
    # analyze the time complexity of StructureDiversity(G)
    ############################################################################
    for vertex, id in list(G.vertex_dict.items()):
        dfs = DFS(G,vertex)
        result[id] = dfs.partialSearch()
    return result


def StructureDiversityWithDJSet(G):
    # initialization
    result = [0] * (G.vertex_num)

    # slove structure diversity of each vertex in graph
    for vertex, id in list(G.vertex_dict.items()):
        djs = DisjointSet(G,vertex)
        result[id] = djs.createDJS()

    return result

############################################################################
# Do not edit this code cell.
############################################################################

class UndirectedGraph(object):
    def __init__(self, edge_list):
        self.vertex_dict = {}  # 存储各点的名称和id值
        self.adj_list = []   # 存储各点邻居的名称而非id
        self.vertex_num = 0
        for [src, dst, _] in edge_list:
            self.add_edge(src, dst)

    def add_vertex(self, name):
        id = self.vertex_num
        self.vertex_dict[name] = id
        self.vertex_num += 1
        self.adj_list.append(list())

    def add_edge(self, vertex1, vertex2):
        if vertex1 not in self.vertex_dict.keys():
            self.add_vertex(vertex1)
        if vertex2 not in self.vertex_dict.keys():
            self.add_vertex(vertex2)
        self.adj_list[self.vertex_dict[vertex1]].append(vertex2)
        self.adj_list[self.vertex_dict[vertex2]].append(vertex1)

def check_result(prediction, ground_truth):
    return np.array_equal(prediction, ground_truth)

if __name__ == "__main__":

    print('\n##### Loading the dataset...')
    edge_list = np.loadtxt('cora.graph', dtype=int)
    sd_list = np.loadtxt('cora.sd', dtype=int)
    G = UndirectedGraph(edge_list)

    print('\n##### Test ...')
    start = time.time()
    structure_div = StructureDiversity(G)
    end = time.time()
    print("Processing time: {}".format(end-start))
    print("Correct result" if check_result(structure_div, sd_list) else "Incorrect result")