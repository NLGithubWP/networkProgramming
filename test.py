

slots = []
slotsNum = 32
for _ in range(32):
    slots.append([])


def put(slots, key, value):
    i = hash(key) % slotsNum
    pos = -1
    for pos, (k, v) in enumerate(slots[i]):
        if key == k:
            break
    else:
        slots[i].append((key, value))
    if pos >= 0 and pos < len(slots[i]):
        slots[i][pos] = (key, value)


def get(slots, key):
    i = hash(key) % slotsNum
    for k, v in slots[i]:
        if key == k:
            return v
    else:
        raise KeyError(key)		# 不存在时抛出异常


put(slots, 'a', 1)
print(get(slots, 'a'))
put(slots, 'b' ,2)
print(get(slots, 'b'))
put(slots, 'a', 3)
print(get(slots, 'a'))
