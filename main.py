import sys
import argparse


def main():
    input_args = argparse.ArgumentParser()
    input_args.add_argument('-f', default='object.obj', metavar='filename', nargs=1,
                            help='input file name (default: object.obj)')
    input_args.add_argument('-m', default='object.mtl', metavar='material_filename', nargs=1,
                            help='input file name for colors (default: object.mtl)')

    args = input_args.parse_args()
    input_file_name = args.f
    material_file_name = args.m
    destination_triangles_file_name = 'triangle_vertecies.txt'
    destination_textures_file_name = 'texture_vertecies.txt'
    destination_colors_file_name = 'colors_vertecies.txt'

    try:
        input_file = open(input_file_name, 'r')
    except IOError:
        print('File ', input_file_name, ' couldn\'t be opened')
        sys.exit(1)
    try:
        material_file = open(material_file_name, 'r')
    except IOError:
        print('File ', material_file_name, ' couldn\'t be opened')
        sys.exit(1)

    hashes = '####################'

    result_names = []
    result_trv = []
    trv_count = []
    result_txv = []

    materials_obj = []
    materials_mtl = []
    colors_mtl = []

    for line in input_file.readlines():
        line = line.rstrip()
        splited_string = line.split(' ')
        if line.startswith('#'):
            continue

        if line.startswith('vt'):
            for i in range(1, len(splited_string)):
                result_txv[len(result_txv) - 1] += splited_string[i]
                result_txv[len(result_txv) - 1] += ', '
            result_txv[len(result_txv) - 1] += '\n'

        if line.startswith('vt'):
            continue

        if line.startswith('vn'):
            continue

        if line.startswith('usemtl'):
            materials_obj.append(splited_string[1])

        if line.startswith('o'):
            result_names.append('\n' + hashes + ' ' + splited_string[1] + ' ' + hashes + '\n \n')
            trv_count.append(0)
            result_trv.append('')
            result_txv.append('')

        if line.startswith('v'):
            if len(splited_string) != 4:
                print("Not triangle only .obj file")
                sys.exit(2)
            result_trv[len(result_trv) - 1] += splited_string[1] + ', '
            result_trv[len(result_trv) - 1] += splited_string[2] + ', '
            result_trv[len(result_trv) - 1] += splited_string[3] + ', \n'
            trv_count[len(result_trv) - 1] += 1

    for line in material_file.readlines():
        line = line.rstrip()
        splited_string = line.split(' ')
        if line.startswith('#'):
            continue

        if line.startswith('newmtl'):
            materials_mtl.append(splited_string[1])

        if line.startswith('Kd'):
            colors_mtl.append(splited_string[1] + ', ' + splited_string[2] + ', ' + splited_string[3] + ',\n')

    try:
        output_triangle_file = open(destination_triangles_file_name, 'w')
    except IOError:
        print('File ', destination_triangles_file_name, ' couldn\'t be opened')
        sys.exit(1)
    try:
        output_textures_file = open(destination_textures_file_name, 'w')
    except IOError:
        print('File ', destination_textures_file_name, ' couldn\'t be opened')
        sys.exit(1)
    try:
        output_colors_file = open(destination_colors_file_name, 'w')
    except IOError:
        print('File ', destination_colors_file_name, ' couldn\'t be opened')
        sys.exit(1)

    for i in range(0, len(result_names)):
        output_triangle_file.write(result_names[i] + result_trv[i])

    for i in range(0, len(result_names)):
        output_textures_file.write(result_names[i] + result_txv[i])

    for i in range(0, len(materials_obj)):
        for j in range(len(materials_mtl)):
            if materials_obj[i] == materials_mtl[j]:
                output_colors_file.write(result_names[j])
                for k in range(0, trv_count[j]):
                    output_colors_file.write(colors_mtl[j])

    output_triangle_file.close()
    output_textures_file.close()
    output_colors_file.close()
    input_file.close()
    material_file.close()


if __name__ == "__main__":
    main()
