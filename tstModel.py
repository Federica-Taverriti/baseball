from model.model import Model

mymodel = Model()

mymodel.getTeamsOfYear(2012)
mymodel.creaGrafo(2012)
nodi, archi = mymodel.getGraphDetails()
print(f"Grafo creato! Il grafo ha {nodi} nodi e {archi} archi.")
v0 = mymodel.getRandomNode()
path, score = mymodel.getPathV2(v0)

print(f"Trovata soluzione lunga {len(path)} con somma pesi archi pari a {score}.")
for p in path:
    print(p)

