import importlib.metadata
dists = sorted([d.metadata['Name'] for d in importlib.metadata.distributions()])
for p in dists:
    print(p)
