from hashlib import md5#采用md5函数作为哈希函数
import time

class Node:
    def __init__(self) -> None:
        self.leftChild=None#左孩子
        self.rightChild=None#右孩子
        self.parent=None#父节点。子节点更新时，相应的父节点hash值也要更新
        self.hash=""#存储的hash值
        self.data="" #其他数据，需要时采用,不需要时置空
    
    def changeNode(self,data,hash=0):#hash值可以由自定义算法给出，缺省时用默认算法md5
        self.data=data
        if hash:
            self.hash=hash
        self.hash=md5(data.encode("utf-8")).hexdigest()
        return self.hash
    
class MerkelTree:
    def __init__(self) -> None:
        self.root=None
        self.h=0#层数,0代表只有根节点
        self.leaf=0#剩余叶子数目
    
    def AddNode(self,item,h):#递归遍历生成h层树需要的节点
        left=Node()
        right=Node()
        left.parent=item
        item.leftChild=left
        right.parent=item
        item.rightChild=right#创建左右节点并连接到item下方
        h=h-1
        if h==0:#层树够了
            return
        else:
            self.AddNode(left,h)
            self.AddNode(right,h)
    
    def CreateTree(self,h):#创建h层高的树的类并向内添加足够的节点
        self.root=Node()
        self.h=h
        self.leaf=2**h#二叉树的节点数等于2^高度
        self.AddNode(self.root,h)
        return self.root
    
    def updateParents(self,node):#从改变的叶子节点层层上溯改变所有相关节点的hash值
        if node.parent!=None:#直到上溯到根节点
            node=node.parent
            node.hash=md5((str(node.leftChild.hash)+str(node.rightChild.hash)).encode("utf-8")).hexdigest()
            self.updateParents(node)

        
    
    def updateLeaf(self,data,hash=0):#更新叶子节点的数据,hash值由数据算出
        if self.leaf==0:
            print("树的节点被全部占用")
            return
        tmpRoot=self.root
        tmpH=self.h
        tmpLeaf=self.leaf
        while tmpH!=0:#先找到空余的最左边的叶子节点
            if tmpLeaf>2**(tmpH-1):#如果某个节点的剩余叶子节点大于其下所有节点数目的一半，那么下一个空余叶子在左子树上
                tmpLeaf=tmpLeaf-2**(tmpH-1)#向左下探
                tmpRoot=tmpRoot.leftChild
            else:#否则向右下探
                tmpRoot=tmpRoot.rightChild
            tmpH=tmpH-1
        self.leaf=self.leaf-1
        tmpRoot.data=data
        if hash:
            tmpRoot.hash=hash
        else:
            tmpRoot.hash=md5(data.encode("utf-8")).hexdigest()
        self.updateParents(tmpRoot)
        return tmpRoot
        
    def PreorderTrav(self,root):#先序遍历MerkelTree
        if root.leftChild!=None:
            print("本节点的hash值为：",root.hash)
            self.PreorderTrav(root.leftChild)
            self.PreorderTrav(root.rightChild)
        if root.leftChild==None:
            print("本叶子节点的数据为：hash值：",root.hash)
            print("数据：",root.data)


Tree=MerkelTree()
Tree.CreateTree(2)
#print(Tree.root.hash)
for i in range(2**(Tree.h)):#测试
    Tree.updateLeaf(str(i))
Tree.PreorderTrav(Tree.root)

time1=time.time()
Tree=MerkelTree()
Tree.CreateTree(15)
for i in range(2**(Tree.h)):
    Tree.updateLeaf(str(i))
time2=time.time()
print("创建15层的MerkelTree花费的时间为",time2-time1)

