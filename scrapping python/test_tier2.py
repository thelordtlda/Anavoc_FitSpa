from builders_watkins import build_hot_spring_yearly_specs, build_caldera_yearly_specs, build_endless_pools_yearly_specs
from builders_master_spas import build_master_spas_yearly_specs
from builders_hydropool import build_hydropool_yearly_specs

hs = build_hot_spring_yearly_specs()
cal = build_caldera_yearly_specs()
ep = build_endless_pools_yearly_specs()
ms = build_master_spas_yearly_specs()
hp = build_hydropool_yearly_specs()

print("Hot Spring records:", len(hs), "Swim:", sum(1 for x in hs if x["is_swim_spa"]))
print("Caldera records:", len(cal), "Swim:", sum(1 for x in cal if x["is_swim_spa"]))
print("Endless Pools records:", len(ep), "Swim:", sum(1 for x in ep if x["is_swim_spa"]))
print("Master Spas records:", len(ms), "Swim:", sum(1 for x in ms if x["is_swim_spa"]))
print("Hydropool records:", len(hp), "Swim:", sum(1 for x in hp if x["is_swim_spa"]))

total_new = len(hs) + len(cal) + len(ep) + len(ms) + len(hp)
total_swim = sum(1 for x in ep + ms + hp if x["is_swim_spa"])
print("Total new records:", total_new, "Total new swim spas:", total_swim)
