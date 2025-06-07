'''

I) Параметры объектов
  Общие параметры:
    1) material          - число; 0 - reflection, 1 - diffuse, 2 - reflection&refr
    2) ior               - число; показатель преломления
    3) ka                - число; "тон света, рассеиваемого объектом в случае, когда на него не попадают прямые лучи источников освещения"
    4) ks                - число; вес бликовой компоненты
    5) kd                - число; вес диффузной компоненты
    6) p -               - число; коэффициент гладкости
    7) native_color      - число до 2^32 (можно в формате 0x (0x0000FF00) ), либо строка с комбинациями RED, GREEN, BLUE ("RED", "RED|GREEN", "BLUE", т.д.)

  Параметры AABB:
    8) min_xyz           - строка вида "vec(1,2.4,-3)"; минимальные значения каждой из координат
    9) max_xyz           - строка вида "vec(1,2.4,-3)"; максимальные значения каждой из координат

  Параметры Plane:
    8) const_coord       - строка, содержащая константную координату плоскости; например "'y'"; плоскость параллельна плоскости двух других координат
    9) const_coord_value - число; значение константной координаты

  Параметры Sphere:
    8) c                 - строка вида "vec(1,2.4,-3)"; вектор, соответствующий центру сферы;
    9) rad               - число; радиус сферы

II) Параметры Eye
    1) angle_y           - число; (??) под каким углом к y смотрим ?
    2) watching_from     - строка вида "vec(1,2.4,-3)"; вектор точки наблюдения; кажется, неиспользуемый параметр

III) Параметры Light
    1) position          - строка вида "vec(1,2.4,-3)"; вектор, соответствующий точке, откуда исходит луч света
    2) color             - число до 2^32 (можно в формате 0x (0x0000FF00) ), либо строка с комбинациями RED, GREEN, BLUE ("RED", "RED|GREEN", "BLUE", т.д.)
'''

frame_dict = {

    "objects": {
        "AABB": [
            # left wall
            #{"material": 0, "ior": 1.333, "ka": 0.4, "ks": 1, "kd": 0.5, "p": 5.0, "native_color": 0x00FF0000, "min_xyz": "vec(-1,-1,-2)", "max_xyz": "vec(-1,1,1)"},
            # right wall
            #{"material": 1, "ior": 1.333, "ka": 0.4, "ks": 1, "kd": 0.5, "p": 5.0, "native_color": 0x00FFFFFF, "min_xyz": "vec(1,-1,-2)", "max_xyz": "vec(1,2,1)"},
            # front wall
            {"material": 0, "ior": 1.333, "ka": 0.4, "ks": 1, "kd": 0.5, "p": 5.0, "native_color": 0x0000FF00, "min_xyz": "vec(-1.65,-1,-2)", "max_xyz": "vec(1.65,1,-2)"},
            # back wall
            {"material": 1, "ior": 1.333, "ka": 0.4, "ks": 1, "kd": 0.5, "p": 5.0, "native_color": 0x00FFFFFF, "min_xyz": "vec(-2,-1.5,1)", "max_xyz": "vec(2,4,1)"}
        ],

        "Plane": [
            #{"material": 1, "ior": 1.333, "ka": 0.4, "ks": 1, "kd": 0.5, "p": 5, "native_color": 0x202020, "const_coord": "'y'", "const_coord_value": 1} 
        ],

        "Sphere": [
            #{"material": 1, "ior": 1.6, "ka": 0.5, "ks": 0.6, "kd": 1, "p": 5, "native_color": 0x00000000, "c": "vec(-0.6,0.5,-1.6)", "rad": 0.4},
            {"material": 1, "ior": 1.333, "ka": 0.4, "ks": 1, "kd": 0.5, "p": 5, "native_color": 0x00FF0000, "c": "vec(0.4, 0, -1.2)", "rad": 0.2},
            #{"material": 0, "ior": 1.333, "ka": 0.4, "ks": 1, "kd": 0.5, "p": 5, "native_color": 0x0000FF00, "c": "vec(0.27,0.0,-0.4)", "rad": 0.1}

        ],

        "Eyes": [
	        {"angle_y": 90, "watching_from": "vec(0,0,0)"}
        ],

        "Light": [
            {"position": "vec(0.5,-0.8,-1.0)", "color": 0x000000FF},
           # {"position": "vec(-0.8,0,-1)", "color": 0xfff917},
           # {"position": "vec(-0.5,0.8,-1.2)", "color": 0x0000FFFF}
        ],
    },

    "scene": {
        "background_color": 0,
        "max_depth": 3,
        "width": 2048/2,
        "height": 2048/2
    }

}




main_before_frame_body = '''
int main(int argc, const char** argv) { 
    std::unordered_map<std::string, std::string> cmdLineParams;
    for (int i=0; i<argc; i++) {
            std::string key(argv[i]);

        if (key.size() > 0 && key[0]=='-') {
            if (i != argc-1) { // not last argument
              cmdLineParams[key] = argv[i+1];
              i++;
            }
            else
                cmdLineParams[key] = "";
        }
    }

    std::string outFilePath = "zout.bmp";
    if (cmdLineParams.find("-out") != cmdLineParams.end())
        outFilePath = cmdLineParams["-out"];

    int sceneId = 0;
        sceneId = atoi(cmdLineParams["-scene"].c_str());

    if (sceneId == 0)
        return 0;

'''

main_after_frame_body = '''

    auto start = std::chrono::high_resolution_clock::now();
    open_eyes(objects, lights, eyes, background_color, image);
    auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop-start);
    // https://www.geeksforgeeks.org/measure-execution-time-function-cpp/

    std::cout << "Время рендеринга == " << duration.count()/1000000.0f << " секунд.\\n";
    SaveBMP(outFilePath.c_str(), image.data(), width, height);
    std::cout << "end." << std::endl;
    objects.clear();
    lights.clear();
    return 0;
}

'''














