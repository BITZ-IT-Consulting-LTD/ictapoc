import re

with open('frontend/src/views/DashboardView.vue', 'r') as f:
    lines = f.readlines()

# find modal start
for i, line in enumerate(lines):
    if '<!-- Staff Catalogue Modal -->' in line:
        modal_idx = i
        break

start_catalogue = -1
end_catalogue = -1

for i, line in enumerate(lines):
    if '<div class="toolbar u-w-full">' in line:
        start_catalogue = i
        break

for i in range(start_catalogue, len(lines)):
    if '<!-- STAFF OPERATIONS VIEW -->' in line:
        end_catalogue = i - 6 # roughly before the </section>
        break

catalogue_block = lines[start_catalogue:end_catalogue]

modal_repl = [
    '      <!-- Staff Catalogue Modal -->\n',
    '      <BaseModal v-model:show="showStaffCatalogueModal" @close="showStaffCatalogueModal = false" :title="\'Unified Service Catalogue\'">\n',
    '        <div class="u-p-6" style="max-height: 70vh; overflow-y: auto; background: var(--color-background); border-radius: 0.5rem;">\n',
] + catalogue_block + [
    '        </div>\n',
    '      </BaseModal>\n'
]

# replace modal
start_modal = modal_idx
end_modal = -1
for i in range(modal_idx + 1, len(lines)):
    if '</BaseModal>' in lines[i]:
        end_modal = i
        break

lines = lines[:start_modal] + modal_repl + lines[end_modal+1:]

with open('frontend/src/views/DashboardView.vue', 'w') as f:
    f.writelines(lines)
print("Patched DashboardView.vue with actual catalogue")
