import sys

with open("frontend/src/views/DashboardView.vue", "r") as f:
    lines = f.readlines()

# Find the start of the services tab
start = -1
for i, line in enumerate(lines):
    if '<div v-if="citizenCurrentTab === \'services\'"' in line:
        start = i
        break

if start == -1:
    print("Could not find start of services tab")
    sys.exit(1)

# Find the exact end tag
div_count = 0
end = -1
for i in range(start, len(lines)):
    line = lines[i]
    div_count += line.count('<div')
    div_count -= line.count('</div')
    if div_count == 0:
        end = i
        break

if end == -1:
    print("Could not find end of services tab")
    sys.exit(1)

catalogue_block = lines[start:end+1]

# Modify the copied block for the modal context
# (It had `v-if="citizenCurrentTab === 'services'"`, we will remove that attribute so it works regardless)
catalogue_block[0] = catalogue_block[0].replace('v-if="citizenCurrentTab === \'services\'"', '')

modal_html = [
    '      <!-- Staff Catalogue Modal -->\n',
    '      <BaseModal v-model:show="showStaffCatalogueModal" @close="showStaffCatalogueModal = false" :title="\'Unified Service Catalogue\'">\n',
    '        <div class="u-p-6" style="max-height: 80vh; overflow-y: auto; background: var(--color-background); border-radius: 0.5rem;">\n'
] + catalogue_block + [
    '        </div>\n',
    '      </BaseModal>\n\n'
]

# Find where to insert the modal (Before `<!-- SYSTEM ADMINISTRATION VIEW -->`)
admin_start = -1
for i, line in enumerate(lines):
    if '<!-- SYSTEM ADMINISTRATION VIEW -->' in line:
        admin_start = i
        break

filtered_lines = lines[:admin_start] + modal_html + lines[admin_start:]

# Find where to inject the button in the STAFF portal header
staff_start = -1
for i, line in enumerate(filtered_lines):
    if '<!-- STAFF OPERATIONS VIEW -->' in line:
        staff_start = i
        break

btn_index = -1
for i in range(staff_start, len(filtered_lines)):
    if '<div class="toolbar__filters">' in filtered_lines[i]:
        btn_index = i
        break

btn_html = [
    '                  <button @click="showStaffCatalogueModal = true" class="button button--secondary button--small mr-4">\n',
    '                    <i class="bi bi-grid-3x3-gap-fill u-mr-1"></i> Open Service Catalogue\n',
    '                  </button>\n'
]
filtered_lines = filtered_lines[:btn_index+1] + btn_html + filtered_lines[btn_index+1:]

# Add showStaffCatalogueModal var definition
setup_start = -1
for i, line in enumerate(filtered_lines):
    if 'const showCompleteStepModal = ref(false);' in line:
        setup_start = i
        break

if setup_start != -1:
    filtered_lines.insert(setup_start + 1, '  const showStaffCatalogueModal = ref(false);\n')
else:
    for i, line in enumerate(filtered_lines):
        if 'const closeCompleteStepModal =' in line:
            filtered_lines.insert(i, '  const showStaffCatalogueModal = ref(false);\n')
            break

with open("frontend/src/views/DashboardView.vue", "w") as f:
    f.writelines(filtered_lines)

print(f"Patched successfully. Captured {start} to {end}.")
