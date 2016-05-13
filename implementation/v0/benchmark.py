from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair

trials = 10
group = PairingGroup("SS1024")
g = group.random(G1)
h = group.random(G1)
i = group.random(G2)

assert group.InitBenchmark(), "failed to initialize benchmark"
group.StartBenchmark(["Mul", "Exp", "Pair", "Granular"])
for a in range(trials):
    j = g * h
    k = i ** group.random(ZR)
    t = (j ** group.random(ZR)) / h
    n = pair(h, i)
group.EndBenchmark()

msmtDict = group.GetGeneralBenchmarks()
granDict = group.GetGranularBenchmarks()
print("<=== General Benchmarks ===>")
print("Results  := ", msmtDict)
# print("G3 pair   := ", msmtDict["Pair"][G2])
print("<=== Granular Benchmarks ===>")
print("G1 mul   := ", granDict["Mul"][G1])
print("G2 exp   := ", granDict["Exp"][G2])
# print("G3 pair   := ", granDict["Pair"][G])