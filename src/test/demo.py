def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# 示例
arr = [3, 6, 8, 10, 1, 2, 1]
print("原始数组：", arr)
print("快速排序后的数组：", quick_sort(arr))
# def bubble_sort(arr):
#     n = len(arr)
#     # 遍历所有数组元素
#     for i in range(n):
#         # Last i elements are already in place
#         for j in range(0, n-i-1):
#             # 遍历数组从0到n-i-1
#             # 交换如果元素大于下一个元素
#             if arr[j] > arr[j+1]:
#                 arr[j], arr[j+1] = arr[j+1], arr[j]
#
# # 测试代码
# arr = [64, 34, 25, 12, 22, 11, 90]
# print("原始数组是:")
# print(arr)
# bubble_sort(arr)
# print("排序后的数组是:")
# print(arr)