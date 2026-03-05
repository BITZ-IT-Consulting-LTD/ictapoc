with open("frontend/src/views/DashboardView.vue") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<div v-if="citizenCurrentTab === \'services\'"' in line:
        start = i
        break

# find the matching closing div for start
div_count = 0
end = -1
for i in range(start, len(lines)):
    line = lines[i]
    div_count += line.count('<div')
    div_count -= line.count('</div')
    if div_count == 0:
        end = i
        break

print(f"Start: {start}, End: {end}")
