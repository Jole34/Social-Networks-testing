import networkx as nx


def loadGraph():
    try:
        gr = nx.DiGraph()
        options = [1, 2, 3, 4]
        choice = int(input("Enter which Graph do you want do load:\n"
                           "\t1 ----  Epinions\n"
                           "\t2 ----  Wikipedia\n"
                           "\t3 ----  1Slashdot\n"
                           "\t4 ----  Bitcoin\n"))
        if choice in options:
            print("Loading....... ")
            if choice is 4:
                gr = loadBCoin()
                print("Graph is ready!")
            if choice is 1:
                gr = loadEpinionsandSlash(1)
                print("Graph is ready!")
            if choice is 3:
                gr = loadEpinionsandSlash(3)
                print("Graph is ready!")
            if choice is 2:
                gr = loadWikipedia()
                print("Graph is ready!")

        else:
            print("Please enter a valid number (1, 2, 3 or 4)")
            loadGraph()
        return gr
    except ValueError:
        print("Please enter valid number (1, 2, 3 or 4)")
        loadGraph()



def loadEpinionsandSlash(choice):
    gr = nx.DiGraph()
    txt1 = 'soc-sign-epinions.txt'
    txt2 = 'soc-sign-Slashdot090221.txt'
    final = ""
    if choice is 1:
        final = txt1
    else:
        final = txt2
    with open(final, 'r') as file:
        for _ in range(4):
            next(file)
        for line in file:
          data = line.split()
          af1 = data[2].strip()
          af = ""
          if af1 == "-1":
              af = "negative"
          else:
              af= "positive"
          gr.add_edge(data[0].strip(), data[1].strip(), affinity=af)
    return transformDirectedToUndirected(gr)


def loadWikipedia():
    gr = nx.DiGraph()
    src = None
    tr = None
    rs= None
    with open('wiki-RfA.txt', 'r', encoding="utf8") as file:

        for line in file:
            if line.strip().startswith('SRC'):
                src = line.strip()[4:]
            if line.strip().startswith('TGT'):
                tr = line.strip()[4:]
            if line.strip().startswith('RES'):
                if line.strip()[4:] == "-1":
                    rs = "negative"
                else:
                    rs = "positive"
            gr.add_edge(src, tr, affinity=rs)
    return transformDirectedToUndirected(gr)



def loadBCoin():
    gr = nx.DiGraph()
    import csv
    with open('soc-sign-bitcoinalpha.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            if int(line[2]) > 0:
                af = "positive"
            else:
                af = "negative"
            gr.add_edge(line[0], line[1], affinity=af)
            #no need for closing file object with operation will do that
    return transformDirectedToUndirected(gr)



def transformDirectedToUndirected(gr):
    undirected = nx.Graph()
    undirected.add_edges_from(gr.edges(), affinity="")
    for u, v, d in gr.edges(data=True):
        af =" "
        if (v, u) in gr.edges:
            af = gr[v][u]['affinity']
        if gr[u][v]['affinity'] == "negative" or af == "negative":
            undirected[u][v]['affinity'] = "negative"
        else:
            undirected[u][v]['affinity'] = "positive"
    return undirected

