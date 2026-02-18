#!/bin/bash
# fio 磁盘IO性能测试脚本示例

# 1. 顺序读测试（Sequential Read）
echo "=== 顺序读测试 ==="
fio --name=seq_read \
    --filename=/tmp/test_file \
    --size=1G \
    --rw=read \
    --bs=4k \
    --direct=1 \
    --ioengine=libaio \
    --iodepth=32 \
    --runtime=60 \
    --time_based

# 2. 随机写测试（Random Write）
echo "=== 随机写测试 ==="
fio --name=rand_write \
    --filename=/tmp/test_file \
    --size=1G \
    --rw=randwrite \
    --bs=4k \
    --direct=1 \
    --ioengine=libaio \
    --iodepth=32 \
    --runtime=60 \
    --time_based

# 3. 混合读写测试（Mixed Read/Write）
echo "=== 混合读写测试（70%读，30%写）==="
fio --name=mixed \
    --filename=/tmp/test_file \
    --size=1G \
    --rw=randrw \
    --rwmixread=70 \
    --bs=4k \
    --direct=1 \
    --ioengine=libaio \
    --iodepth=32 \
    --runtime=60 \
    --time_based
