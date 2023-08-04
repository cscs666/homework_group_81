from hashlib import md5
import time

class branch:
    def __init__(self) -> None:
        self.type="branch"
        self.children = {'0': None, '1': None, '2': None, '3': None, '4': None, '5': None, '6': None, '7': None, '8': None, '9': None,
                         'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'value': False}
        #value代表终止符，同时记录extension节点的状态

class extension:
    def __init__(self) -> None:
        self.type="extension"
        self.key=None
        #一个extension始终对应一个branch
        self.val=branch()
        self.prefix=None#前缀
        self.dataHash=None#原数据hash值，即为节点内存储的数据
        self.nodeHash=None#节点的hash值
    
class leaf:
    def __init__(self) -> None:
        self.type="leaf"
        self.key_end=None
        #一个extension始终对应一个branch
        self.val=None
        self.prefix=None
        self.dataHash=None
        self.nodeHash=None

class MPT:
    def __init__(self,tree=None) -> None:
        if tree:
            self.root=tree
        else:
            self.root=extension()
            #默认根节点的前缀是root
            self.root.prefix = 'root'
            #定义树的value和hash
            self.data = None
            self.dataHash = None

    def makeLeaf(self,key,profix,value):
        tmp = leaf()
        tmp.key_end = key
        tmp.prefix = profix
        tmp.val = value
        # 添加leaf节点的值和hash
        tmp.dataHash = md5(value.encode('utf-8')).hexdigest()#对数据进行hash
        tmp.nodeHash = md5(str(tmp).encode('utf-8')).hexdigest()#对节点进行hash，顺序在数据hash之后，确保为最后的改动.直接强制转为str即可作出唯一签名。
        return tmp
    
    def comp(self,node,key):#检测node的前缀和key在何处开始出现不同
        l=len(key) if len(key) < len(node.prefix) else len(node.prefix)#两者取其小并用于后续比较
        count = 0
        while count < l:
            if node.prefix[count] != key[count]:#出现不同
                return count
            count+=1
        return count
    
    def Leaf_extension(self,node,commonprefix,key,index,value):#应对leaf冲突
        leaf = node
        tmp = extension()
        tmp.prefix = commonprefix
        tmp.val.children[leaf.key_end[index]] = leaf# 将旧的leaf节点插入branch表中
        tmp.val.children[leaf.key_end[index]].key_end = leaf.key_end[index+1::]#产生共同前缀，leaf节点的key_end发生改变
        tmp.val.children[key[0]] = self.makeLeaf(key[1::],key[0],value)
        return tmp
    def Ext_extension(self,node,prefix,key,index,value):#应对extension冲突
        nodeNewPrefix = node.prefix[index+1::]
        tmp = extension()
        #写入共同前缀
        tmp.prefix = prefix#将旧的extension节点插入branch表中
        tmp.val.children[node.prefix[index]] = node#修改旧的extension节点的共同前缀
        tmp.val.children[node.prefix[index]].prefix = nodeNewPrefix
        tmp.val.children[key[0]] = self.makeLeaf(key[1::],key[0],value)#产生一个leaf
        return tmp
    def addNode(self,node,key,value):
        if node.prefix=="root":#父节点为root
            if self.root.val.children[key[0]]==None:#branch表为空，直接插入，key[0]为root下的branch的索引，剩余的才是新传入的前缀与prefix不同的keyDiffPrefix值
                self.root.val.children[key[0]] = self.makeLeaf(key[1::],key[1::],value)
                # 插入新的leaf节点后，节点数据发生改变,同时改变其他变量
                node.val.children["value"]=False
                return
            else:#branch表发生冲突，进行递归
                self.root.val.children[key[0]] =  self.addNode(self.root.val.children[key[0]],key[1::],value)
                return
        parent=node
        diffIndex=self.comp(parent,key)
        commonPrefix=parent.prefix[:diffIndex]
        keyDiffPrefix=key[diffIndex:]#共同前缀以后的不相同的部分
        #若相同字符数小于parent的prefix长度则新节点与父节点无共同前缀，发生冲突
        if diffIndex<len(parent.prefix):
            #extension冲突
            if parent.type == 'extension':
                return self.Ext_extension(parent,commonPrefix,keyDiffPrefix,diffIndex,value)#调用函数，创建新的extension节点，解决冲突
            #leaf冲突
            elif parent.type == 'leaf':
                return self.Leaf_extension(parent,commonPrefix,keyDiffPrefix,diffIndex,value)# 调用函数，创建新的extension节点，解决冲突
        elif diffIndex==len(parent.prefix):#字符数相等时进入extension中的branch向下遍历
            #判断extension节点下的branch对应key的value是否为空
            #为空，则添加leaf节点
            if parent.val.children[key[diffIndex]] == None:
                parent.val.children[key[diffIndex]] = self.makeLeaf(key[diffIndex+1::],key[diffIndex])
                parent.val.children['value'] = False#插入新的leaf节点后，节点数据发生改变，状态改变
                return parent
                #print(father.value.children[key[index]].key_end)#test
            #不为空，即发生字符表冲突，向下扩展extension
            else:
                parent = self.addNode(parent.val.children[key[diffIndex]],keyDiffPrefix,value)
                return parent
    def search(self,node,index):
        result_node = None
        for key in  node.val.children:#遍历当前extension节点的branch表
            if key == 'value':
                break
            if node.val.children[key] == None:
                continue
            #检索到leaf节点，对比key_end和索引值
            if node.val.children[key].type == 'leaf':
                if index[1::] == node.val.children[key].key_end:
                    result_node =  node.val.children[key]
                    break
                else:
                    continue
            #检索到extension，进入到该节点的branch向下索引
            elif node.val.children[key].type == 'extension':
                short_key = index[len(node.val.children[key].prefix)+1::]#记录去除该extension节点的共同前缀后剩余的索引值
                #递归向下索引
                result_node = self.search(node.val.children[key],short_key)
                if result_node != None:
                    break
        return result_node

    def printMPT(self,node):
        print('extension的前缀是',node.prefix)
        for key in node.val.children:
            if key == 'value':
                break
            if node.val.children[key] == None:
                continue
            if node.val.children[key].type == 'leaf':
                print('branch:', key)
                print('key_end的leaf是',node.val.children[key].key_end)
            elif node.val.children[key].type == 'extension':
                print('branch:', key)
                self.printMPT(node.val.children[key])

    def update(self,node):
        tmpStr=""#组合extension节点下branch表中非空节点的value值，extension的value值产生自它的hash
        if node.val.children['value'] == True:#若节点已更新则直接结束
            return node.dataHash
        for key in node.val.children:
            if key == 'value':
                break
            if node.val.children[key] == None:
                continue
            if node.val.children[key].type == 'leaf':
                tmpStr = tmpStr + node.val.children[key].dataHash
            elif node.val.children[key].type == 'extension':
                tmpStr = tmpStr + self.update(node.val.children[key])
        node.val.children['value'] = True#以下修改节点并把标记改为True
        #更新节点dataHash，nodeHash值
        node.dataHash = md5(tmpStr.encode()).hexdigest()
        node.nodeHAsh = md5(str(node).encode()).hexdigest()
        print('prefix:',node.prefix)
        print('node_value:',node.dataHash)
        return node.dataHash
    #删除节点
    def delete(self,node,hash):#通过遍历检索到需要删除的节点，然后使其对应的branch位置设为None值，再用del回收内存
        for key in node.val.children:
            if key == 'value':
                break
            if node.val.children[key] == None:
                continue
            if node.val.children[key].type == 'leaf':#是leaf节点就删除children，改为空
                if hash[1::] == node.val.children[key].key_end:
                    del node.val.children[key]
                    node.val.children[key] = None
                    return True
                else:
                    continue
            elif node.val.children[key].type == 'extension':#extension节点，类似的操作
                short_hash = hash[len(node.val.children[key].prefix) + 1::]#取出前缀长度+1及之后的值
                if short_hash == '':
                    del node.val.children[key]
                    node.val.children[key] = None
                    #print('delete')
                    return True
                elif self.delete(node.val.children[key],short_hash):
                    return True
    
    def addUp(self,key,value,node=None):#增操作，同时更新MPT
        if node == None:
            node = self.root
        self.addNode(node,key,value)
        self.update(self.root)
    
    def deleteUp(self,key): #删操作，同时更新MPT树
        print('delete a node')
        self.delete(self.root,key)
        self.update(self.root)

    #改操作，同时更新MPT树（简化，只提供修改leaf节点的value值）
    def updateUp(self,index,value):
        if type(index) == str:
            tmp_node = self.search(self.root,index)
            tmp_node.val = value
            # 对数据进行hash
            tmp_node.dataHash = md5(value.encode('utf-8')).hexdigest()
            # 对节点进行hash，顺序在数据hash之后，确保为最后的改动
            tmp_node.nodeHash = md5(str(tmp_node).encode('utf-8')).hexdigest()
        else:
            index.val = value
            # 对数据进行hash
            index.dataHash = md5(value.encode('utf-8')).hexdigest()
            # 对节点进行hash，顺序在数据hash之后，确保为最后的改动
            index.nodeHash = md5(str(index).encode('utf-8')).hexdigest()
        #self.update(self.root,value)
    
    def giveupAllVal(self,node=None):#遍历整个MPT树，设置leaf节点的value值为None，回收内存
        if node == None:#node代表放弃以node为根节点的子树
            node = self.root
        for key in node.val.children:
            if key == 'value':
                break
            if node.val.children[key] == None:
                continue
            if node.val.children[key].type == 'leaf':
                del node.val.children[key].val
                node.val.children[key].val = None
            elif node.val.children[key].type == 'extension':
                self.giveupAllVal(node.val.children[key])

mpt=MPT()
mpt.addUp("123","456")
mpt.addUp("234","567")
mpt.addUp("345","678")
mpt.addUp("356","679")
mpt.deleteUp("234")
mpt.printMPT(mpt.root)