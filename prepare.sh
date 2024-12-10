#!/bin/bash
# 确保脚本在出错时终止执行
set -e

pip install --upgrade pip

if [ "$ARCH" == "x86_64" ]; then
    pip install https://modelscope.cn/models/wlc952/aigchub_models/resolve/master/tpu_perf-1.2.60-py3-none-manylinux2014_x86_64.whl
elif [ "$ARCH" == "aarch64" ]; then
    pip install https://modelscope.cn/models/wlc952/aigchub_models/resolve/master/tpu_perf-1.2.60-py3-none-manylinux2014_aarch64.whl
else
    echo "不支持的系统架构: $ARCH"
    exit 1
fi

pip install -r requirements-bmodel.txt