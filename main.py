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
    result_txv = []
    faces_tab = []
    offset_value = 0
    triangle_vertecies_with_faces = []
    color_counter = []

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

        if line.startswith('f'):
            faces_tab[len(result_trv) - 1].append(splited_string[1] + ', ' + splited_string[2] + ', ' + splited_string[3] + ', \n')

        if line.startswith('usemtl'):
            materials_obj.append(splited_string[1])

        if line.startswith('o'):
            result_names.append('\n' + hashes + ' ' + splited_string[1] + ' ' + hashes + '\n \n')
            triangle_vertecies_with_faces.append('')
            result_trv.append([])
            result_txv.append('')
            faces_tab.append([])
            color_counter.append(0)

        if line.startswith('v'):
            if len(splited_string) != 4:
                print("Not triangle only .obj file")
                sys.exit(2)
            result_trv[len(result_trv) - 1].append(splited_string[1] + ', ' + splited_string[2] + ', ' + splited_string[3] + ', \n')

    for i in range(0, len(faces_tab)):
        for j in range(0, len(faces_tab[i])):
            line = faces_tab[i][j].rstrip(',')
            splited_string = line.split(' ')
            splited_vertex_id_1 = splited_string[0].split('/')
            splited_vertex_id_2 = splited_string[1].split('/')
            splited_vertex_id_3 = splited_string[2].split('/')
            splited_vertex_id_1 = int(splited_vertex_id_1[0]) - offset_value
            splited_vertex_id_2 = int(splited_vertex_id_2[0]) - offset_value
            splited_vertex_id_3 = int(splited_vertex_id_3[0]) - offset_value
            triangle_vertecies_with_faces[i] += (result_trv[i][splited_vertex_id_1 - 1]
                                                 + result_trv[i][splited_vertex_id_2 - 1]
                                                 + result_trv[i][splited_vertex_id_3 - 1])
            color_counter[i] += 3
        offset_value += len(result_trv[i])



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
        output_triangle_file.write(result_names[i] + triangle_vertecies_with_faces[i])

    for i in range(0, len(result_names)):
        output_textures_file.write(result_names[i] + result_txv[i])

    for i in range(0, len(materials_obj)):
        for j in range(len(materials_mtl)):
            if materials_obj[i] == materials_mtl[j]:
                output_colors_file.write(result_names[j])
                for k in range(0, color_counter[j]):
                    output_colors_file.write(colors_mtl[j])

    output_triangle_file.close()
    output_textures_file.close()
    output_colors_file.close()
    input_file.close()
    material_file.close()


if __name__ == "__main__":
    main()
