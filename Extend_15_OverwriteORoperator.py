"""
运算符重载
"""

class Test(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
    def __or__(self, other):
        return MySequence(self, other)


class MySequence(object):
    def __init__(self, *args):
        self.sequence = []
        for arg in args:
            self.sequence.append(arg)

    def __or__(self, other):
        self.sequence.append(other)
        return self
    
    def run(self):
        for arg in self.sequence:
            print(arg)

if __name__ == "__main__":
    xx = Test("a")
    yy = Test("b")
    zz = Test("c")

ww = xx | yy | zz 
ww.run()
print(type(ww))

"""
ww = xx | yy | zz 的执行过程：

第一步：
xx | yy

调用 Test 类里的 __or__ 方法：
Test.__or__(xx, yy)

返回：
MySequence(xx, yy)

此时会调用 MySequence 的 __init__ 方法：
def __init__(self, *args):
    self.sequence = []
    for arg in args:
        self.sequence.append(arg)

👉 注意：
这里存进去的是对象本身：
sequence = [xx, yy]
（不是 ["a", "b"]，而是 Test 对象）

----------------------------------------

第二步：
(MySequence对象) | zz

相当于调用：
MySequence.__or__(MySequence对象, zz)

执行：
self.sequence.append(zz)

👉 此时：
sequence = [xx, yy, zz]

----------------------------------------

最后：
return self（返回 MySequence 对象本身）

所以最终：
ww.sequence = [xx, yy, zz]

----------------------------------------

补充说明：

为什么 print 出来是：
Test(a), Test(b), Test(c)？

因为 print(arg) 时会调用：
arg.__str__()

而 __str__ 定义为：
return f"Test({self.name})"

所以显示的是字符串形式，
但实际存储的是对象本身。
"""