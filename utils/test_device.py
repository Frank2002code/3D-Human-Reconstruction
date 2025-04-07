import torch as T

# 顯示目前的設備
print("目前使用的設備: ", T.device("cuda" if T.cuda.is_available() else "mps" if T.backends.mps.is_available() else "cpu"))

# 是否支援 CUDA？
print("是否支援 CUDA: ", T.cuda.is_available())

# 如果有 CUDA，顯示 GPU 名稱
if T.cuda.is_available():
    print("CUDA 裝置名稱：", T.cuda.get_device_name(0))

# 是否支援 MPS（Mac GPU）
print("是否支援 MPS: ", T.backends.mps.is_available())

# 嘗試建立 float16 張量並執行運算（測試是否真的支援 half precision）
try:
    a = T.randn(2, 2).half().to("cuda" if T.cuda.is_available() else "mps" if T.backends.mps.is_available() else "cpu")
    b = a @ a  # 做個簡單矩陣乘法
    print("float16 運算成功！")
except Exception as e:
    print("float16 運算失敗：", e)
