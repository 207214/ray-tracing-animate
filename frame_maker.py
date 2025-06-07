from frame_config import (
    frame_dict,
    main_after_frame_body,
    main_before_frame_body
)

objects_common_options = ["material", "ior", "ka", "ks", "kd", "p", "native_color"]
main_cpp_pre_file = "main_without_main.txt"
main_cpp_file = "main.cpp"

def form_frame_body(new_frame_dict = None):

    frame_info = frame_dict
    if new_frame_dict is not None:
        frame_info = new_frame_dict

    frame_body = ""
    frame_body += "\n".join(["""    """ + option + " = " + str(frame_dict["scene"][option]) + ";" for option in frame_info["scene"]])

    frame_body += '''
    std::vector<uint32_t> image(height*width);
    
    for (auto& pixel : image)
        pixel = background_color;

    std::vector<Object*> objects;
    std::vector<Light*> lights;

'''
    objects_push_back_commands_list = []

    for obj_group_name in frame_info["objects"]:
        obj_number = 0
        eyes_flag = obj_group_name == "Eyes"
        for obj_dict in frame_info["objects"][obj_group_name]:
            obj_number += 1
            obj_name = obj_group_name.lower()
            if not eyes_flag:
                obj_name += "_" + str(obj_number)
            if obj_group_name == "Light":
                objects_push_back_commands_list.append("""    """ + "lights.push_back(" + obj_name + ");\n")
            else:
                if not eyes_flag:
                    objects_push_back_commands_list.append("""    """ + "objects.push_back(" + obj_name + ");\n")
            inherit_options = [option for option in obj_dict if option in objects_common_options]
            own_options     = [option for option in obj_dict if option not in objects_common_options]


            obj_creation = """    """ + obj_group_name + " " + (not eyes_flag)*"*" + obj_name + (not eyes_flag)*(" = new " + obj_group_name) + "("
            obj_creation += "".join([str(obj_dict[option]) + ", "
                                 for option in own_options])
            obj_creation = obj_creation[:-2] + ");\n"
            obj_creation += "\n".join(["""    """ + obj_name + "->" + option + " = " + str(obj_dict[option]) + ";"
                                 for option in inherit_options])
            frame_body += obj_creation + "\n\n"

    for add_command in objects_push_back_commands_list:
        frame_body += add_command

    return frame_body

def form_main_function():
    return main_before_frame_body + form_frame_body() + main_after_frame_body

def form_main_cpp(prefix):
    with open(main_cpp_pre_file, 'r') as f:
        file_content = f.read()
        file_content += form_main_function()
    f.close()
    with open(prefix + "_" + main_cpp_file, 'w') as f:
        f.write(file_content)
    f.close()

for f in range(0,380):
    sph_x = -1.8 + f*0.01
    frame_dict["objects"]["Sphere"][0]["c"] = "vec(" + str(sph_x) + ", 0, -1.2)"
    form_main_cpp(str(f))



