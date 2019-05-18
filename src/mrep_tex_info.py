import sys

from src.group_stats import GroupStats

example_input_line = "3072x6144 (18432 KB, ?), 3072x6144 (18432 KB), PF_DXT5, TEXTUREGROUP_World, /Game/BeeSimulator/UI/Bestiary/Textures/T_Page_anim.T_Page_anim, NO, 0"


def is_pot(num):
    return num != 0 and ((num & (num - 1)) == 0)


def get_tex_size(line):
    fields = line.split(', ')
    cur_field = fields[2]
    size_str = cur_field.split(' ')[0]
    size_fields = size_str.split('x')

    x = int(size_fields[0])
    y = int(size_fields[1])

    return x, y


def is_tex_pot(line):
    x, y = get_tex_size(line)
    return is_pot(x) and is_pot(y)


def get_tex_memory(line):
    fields = line.split(', ')
    cur_field = fields[2]

    memory = cur_field[cur_field.find('(') + 1:cur_field.find(')')]
    memory_kb = int(memory.split(' ')[0])

    return memory_kb


def get_group(line, all_tokens, all_stats):
    for token in all_tokens:
        if token in line:
            return all_stats[token]

    return all_stats['other']


tokens = [
    '/Game/BeeSimulator/UI/LoadingScreen',
    '/Game/BeeSimulator/UI/MainMenu/MenuAssets/Achievements_Icons/',
    '/Game/BeeSimulator/UI/MainMenu/Glossary/GlossaryAssets/Textures',
    '/Game/BeeSimulator/UI/MainMenu/',
    '/Game/BeeSimulator/UI/Bestiary',
    '/Game/BeeSimulator/UI',
    '/Game/BeeSimulator/Textures/Architecture-Props/Hive/',
    '/Game/BeeSimulator/Textures/Foliage',
    '/Game/BeeSimulator/Textures/Architecture-Props', '/Game/BeeSimulator/Animations',
    '/Game/BeeSimulator/VisualEffects', '/Game/BeeSimulator/Textures/Rocks-Trunks',
    '/Game/BeeSimulator/Maps/CentralPark_WC', '/Game/BeeSimulator/Textures/Other',
    '/Game/StarterContent', '/Game/BeeSimulator/Weather']

group_stats = {}
for token in tokens:
    group_stats[token] = GroupStats(token)

group_stats['other'] = GroupStats('other')

texture_block_reached = False
pass_next_line = False

print('Running mrep_text_info on file: ', sys.argv[1])

with open(sys.argv[1], 'r') as file:
    lines = file.readlines()

    for l in lines:

        if not l.startswith('Listing all textures') and not texture_block_reached:
            continue

        if l.startswith('Listing all textures'):
            texture_block_reached = True
            pass_next_line = True
            continue

        if pass_next_line:
            pass_next_line = False
            continue

        if texture_block_reached and l.startswith('Total'):
            break

        if not texture_block_reached:
            continue

        kb = get_tex_memory(l)

        group_stat = get_group(l, tokens, group_stats)
        group_stat.total_count += 1
        group_stat.total_kbs += kb

        if not is_tex_pot(l):
            group_stat.non_pot_count += 1
            group_stat.non_pot_kbs += kb

all_groups_stats = GroupStats('AllGroupStats')

for token in tokens:
    print(str(group_stats[token]))
    all_groups_stats.add(group_stats[token])

print(str(group_stats['other']))
all_groups_stats.add(group_stats['other'])

print(str(all_groups_stats))
