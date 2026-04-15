import numpy as np

"""
计算两个向量的余弦相似度（衡量方向相似性，剔除长度影响）

参数：
    vec_a:(np.array): 向量a
    vec_b:(np.array):向量b

返回：
    float: 余弦相似度，范围[-1,1], 越接近1表示越相似, 越接近-1表示越不相似

公式：
    cosine_similarity = (vec_a · vec_b) / (||vec_a|| * ||vec_b||)
    拆解：
    1. 点积: vec_a · vec_b = vec_a[0] * vec_b[0] + vec_a[1] * vec_b[1] + ... + vec_a[n] * vec_b[n]
    2. 模长：||vec_a|| = √ (vec_a[0]^2 + vec_a[1]^2 + ... + vec_a[n]^2)
    3. 模长：||vec_b|| = √ (vec_b[0]^2 + vec_b[1]^2 + ... + vec_b[n]^2)

示例：
    A: [0.5, 0.5]
    B: [0.7, 0.7]
    C: [0.7, 0.5]
    D: [-0.6, -0.5]

    所以,
    AB的点积是: 0.5*0.7 + 0.5*0.7
    向量A的模长是:  √(0.5² + 0.5²) =  √0.5
    向量B的模长是:  √(0.7² + 0.7²) =  √0.98
    那么向量A和向量B的余弦相似度计算是: 
    0.5*0.7 + 0.5*0.7 / ( √(0.5² + 0.5²) * √(0.7² + 0.7²) ) = 0.7 / (√0.5 * √0.98) = 0.7 / √(0.5 * 0.98) = 0.7 / √0.49 = 0.7 / 0.7 = 1

"""

def get_dot(vec_a, vec_b):
    """计算两个向量的点积, 2个向量同纬度数字乘积之和"""
    if len(vec_a) != len(vec_b):
        raise ValueError("输入的两个向量必须具有相同的维度")
    """
    zip(vec_a, vec_b)是Python的内置函数,用于将多个可迭代对象打包成元组()
    也就是说vec_a = [0.5, 0.5], vec_b = [0.7, 0.7], 经过zip()后,就变成：
    [(0.5, 0.7), (0.5, 0.7)]
    然后通过：
    for a, b in zip(vec_a, vec_b),遍历这个列表,每次将列表里的元组()里的两个元素、
    分别赋值给a,b, 即, 
    第一次a=0.5, b=0.7, dot_sum = 0.5 * 0.7 = 0.35
    第二次a=0.5, b=0.7, dot_sum = 0.35 + 0.5 * 0.7 = 0.7
    """
    print(list(zip(vec_a, vec_b)))

    return sum(a * b for a, b in zip(vec_a, vec_b))
    # 等价于：
    """
    dot_sum = 0
    for a, b in zip(vec_a, vec_b):
        dot_sum += a * b
    return dot_sum   
    """


def get_magnitude(vec):
    """计算向量的模长, 向量每个元素的平方和的平方根"""
    # return sum(x ** 2 for x in vec) ** 0.5
    return np.sqrt(sum(x ** 2 for x in vec))

    """
    return sum(x ** 2 for x in vec) ** 0.5等价于：

    -----------------------
    magnitude_sum = 0
    for v in vec:
        magnitude_sum += v ** 2
    return magnitude_sum ** 0.5
    ------------------------

    ------------------------
    或者求使用numpy库的sqrt函数:
    import numpy as np

    magnitude_sum = 0
    for v in vec:
        magnitude_sum += v ** 2
    return np.sqrt(magnitude_sum)
    ------------------------

    """

def cosine_similarity(vec_a, vec_b):
    """计算两个向量的余弦相似度"""
    dot_product = get_dot(vec_a, vec_b)
    magnitude_a = get_magnitude(vec_a)
    magnitude_b = get_magnitude(vec_b)

    if magnitude_a == 0 or magnitude_b == 0:
        raise ValueError("输入的向量不能为零向量")

    return dot_product / (magnitude_a * magnitude_b)


if __name__ == "__main__":
    vec_a = [0.5, 0.5]
    vec_b = [0.7, 0.7]
    vec_c = [0.7, 0.5]
    vec_d = [-0.6, -0.5]

    print("A和B的余弦相似度:", cosine_similarity(vec_a, vec_b))
    print("A和C的余弦相似度:", cosine_similarity(vec_a, vec_c))
    print("A和D的余弦相似度:", cosine_similarity(vec_a, vec_d))