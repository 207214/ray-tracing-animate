dir=$(pwd)
pre_condition=$(( $(ls | grep "main.cpp\|Bitmap.cpp\|Bitmap.h" | wc -l) == 3 ))

if [ ${pre_condition} -ne 1 ]; then
    echo "Скрипт запущен не из нужного каталога. Выход"
    exit 
fi

function compile() {
    rm -rf build
    mkdir build
    cd build
    cmake −DCMAKE_BUILD_TYPE=Release ..
    make -j 4
}

function run() {
    ./rt -out ${1}.bmp -scene 1
}


for f in $(ls mains/ | sort -n)
do
   cd ${dir}
   cat mains/${f} > main.cpp
   compile
   run ${f}
   mv *bmp ${dir}/frames/.
done

