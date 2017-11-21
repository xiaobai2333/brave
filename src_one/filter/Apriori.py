#coding=utf-8
def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]


def createC1(dataSet):  # 构建所有候选项集的集合
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])  # C1添加的是列表，对于每一项进行添加，{1},{3},{4},{2},{5}
    C1.sort()
    return map(frozenset, C1)  # 使用frozenset，被“冰冻”的集合，为后续建立字典key-value使用。


def scanD(D, Ck, minSupport):  # 由候选项集生成符合最小支持度的项集L。参数分别为数据集、候选项集列表，最小支持度
    ssCnt = {}
    for tid in D:  # 对于数据集里的每一条记录
        for can in Ck:  # 每个候选项集can
            if can.issubset(tid):  # 若是候选集can是作为记录的子集，那么其值+1,对其计数
                if not ssCnt.has_key(can):  # ssCnt[can] = ssCnt.get(can,0)+1一句可破，没有的时候为0,加上1,有的时候用get取出，加1
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems  # 除以总的记录条数，即为其支持度
        if support >= minSupport:
            retList.insert(0, key)  # 超过最小支持度的项集，将其记录下来。
        supportData[key] = support
    return retList, supportData


def aprioriGen(Lk, k):  # 创建符合置信度的项集Ck,
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1,
                       lenLk):  # k=3时，[:k-2]即取[0],对{0,1},{0,2},{1,2}这三个项集来说，L1=0，L2=0，将其合并得{0,1,2}，当L1=0,L2=1不添加，
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList


def apriori(dataSet, minSupport=0.5):
    C1 = createC1(dataSet)
    D = map(set, dataSet)

    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]  # L将包含满足最小支持度，即经过筛选的所有频繁n项集，这里添加频繁1项集
    k = 2
    while (len(L[k - 2]) > 0):  # k=2开始，由频繁1项集生成频繁2项集，直到下一个打的项集为空
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)  # supportData为字典，存放每个项集的支持度，并以更新的方式加入新的supK
        L.append(Lk)
        k += 1
    return L, supportData


def generateRules(L, supportData, minConf=0.7):
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList


# 辅助函数——计算规则的可信度，并过滤出满足最小可信度要求的规则
def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    ''' 对候选规则集进行评估 '''
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            # print freqSet - conseq, '-->', conseq, 'conf:', conf
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

#辅助函数——根据当前候选规则集H生成下一层候选规则集
def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    ''' 生成候选规则集 '''
    m = len(H[0])
    while (len(freqSet) > m):  # 判断长度 > m，这时即可求H的可信度
        H = calcConf(freqSet, H, supportData, brl, minConf)
        if (len(H) > 1):  # 判断求完可信度后是否还有可信度大于阈值的项用来生成下一层H
            H = aprioriGen(H, m + 1)
            m += 1
        else:  # 不能继续生成下一层候选关联规则，提前退出循环
            break


def test():
    dataSet = loadDataSet()
    print dataSet
    C1 = createC1(dataSet)
    # print "所有候选1项集C1:\n", C1

    L, suppData = apriori(dataSet, minSupport=0.1)

    print '.......'
    print "所有符合最小支持度为0.5的项集L：\n", L
    print '========= '
    rules = generateRules(L, suppData, minConf=0.5)
    print rules

if __name__ == '__main__':
    test()