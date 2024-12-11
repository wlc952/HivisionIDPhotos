#!/bin/bash

wget https://modelscope.cn/models/wlc952/aigchub_models/resolve/master/rmbg/rmbg-1.4_1024.tar.gz
tar zxvf rmbg-1.4_1024.tar.gz
mv rmbg-1.4_1024.bmodel hivision/creator/weights/rmbg-1.4.bmodel
rm rmbg-1.4_1024.tar.gz

wget https://modelscope.cn/models/wlc952/aigchub_models/resolve/master/retinaface/retinaface-resnet50_512.tar.gz
tar zxvf retinaface-resnet50_512.tar.gz
mv retinaface-resnet50_512.bmodel hivision/creator/retinaface/weights/retinaface-resnet50.bmodel
rm retinaface-resnet50_512.tar.gz
