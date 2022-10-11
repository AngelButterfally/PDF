import os

def get_all_lines(txtPath = './Failure_Code_Table.txt'):
    ## 获取每行的信息和内容
    with open(txtPath, 'r', encoding = 'utf-8') as f:
        allLine = f.readlines()
        f.close()
    allLineNumber = len(allLine)
    # print(allLineNumber)

    ## 剔除不需要的信息行
    with open(txtPath,"w",encoding="utf-8") as f_w:
        for line in allLine:
            if "故障和报警" in line:
                continue
            if "SINAMICS S120/S150" in line:
                continue
            if "参数手册," in line:
                continue
            f_w.write(line)

    ## 刷新每行的信息和内容
    with open(txtPath, 'r', encoding = 'utf-8') as f:
        allLine = f.readlines()
        f.close()
    allLineNumber = len(allLine)
    # print(allLineNumber)
    return allLine,allLineNumber

def data_process(allLine,allLineNumber):
    ## 筛选分类文本信息
    failure = {}                #故障码和名称
    failureNumber = 0
    failureLocation = {}

    informationValue = {}           #信息值
    informationValueNumber = 0
    informationValueLocation = {}

    informationCatefory = {}        #信息类别
    informationCateforyNumber = 0
    informationCateforyLocation = {}

    drivingObject = {}
    drivingObjectNumber = 0         #驱动对象数量
    drivingObjectLocation = {}    #驱动对象所在首行

    component = {}
    componentNumber = 0             #组件数量 
    componentLocation = {}        #组件所在行

    reason = {}
    reasonNumber = 0                #原因数量
    reasonLocation = {}           #原因所在首行

    processing = {}
    processingNumber = 0            #处理数量
    processingLocation = {}       #处理所在首行
    #####################
    ###基于常规方法编写###
    #####################
    for x in range(allLineNumber):
        if "信息值： " in allLine[x]:
            # print(allLine[i])
            failure[failureNumber] = allLine[x - 1]                 #故障码和名称
            failureLocation[failureNumber] = x - 1                  #故障码所在行
            informationValue[failureNumber] = allLine[x]            #信息值
            informationCatefory[failureNumber] = allLine[x + 1]     #信息类别
            failureNumber = failureNumber + 1
        if "驱动对象： " in allLine[x]:
            drivingObjectLocation[drivingObjectNumber] = x
            drivingObjectNumber = drivingObjectNumber + 1
        if "组件： " in allLine[x]:
            componentLocation[componentNumber] = x
            componentNumber = componentNumber + 1
        if "原因： " in  allLine[x]:
            reasonLocation[reasonNumber] = x
            reasonNumber = reasonNumber + 1
        if "处理： " in allLine[x]:
            processingLocation[processingNumber] = x
            processingNumber = processingNumber + 1

    ##提取驱动对象和组件
    if drivingObjectNumber != componentNumber:
        print("信息提取有误！")
        print(drivingObjectNumber)
        print(componentNumber)
    else:
        for x in range(drivingObjectNumber):
            ##提取组件
            component[x] = allLine[componentLocation[x]]
            ##提取驱动对象
            if drivingObjectLocation[x] == componentLocation[x] - 1:        #如果驱动对象只有一行
                drivingObject[x] = allLine[drivingObjectLocation[x]]
            else:
                dataDrivingObject = ''                                      #如果驱动对象有多行
                lineRange = componentLocation[x] - drivingObjectLocation[x]
                for y in range(lineRange):    
                    lineNumber = drivingObjectLocation[x] + y
                    dataDrivingObject = dataDrivingObject + allLine[lineNumber]
                    drivingObject[x] = dataDrivingObject

    ##提取原因和处理
    if reasonNumber != processingNumber:
        print("信息提取有误！")
        print(reasonNumber)
        print(processingNumber)
    elif reasonNumber != failureNumber:
        print("信息提取有误！")
    else:
        for x in range(reasonNumber):
            ##提取原因
            if reasonLocation[x] == processingLocation[x] - 1:              #如果原因只有一行
                reason[x] = allLine[reasonLocation[x]]
            else:
                dataReason = ''                                             #如果原因有多行
                lineRange = processingLocation[x] - reasonLocation[x]
                for y in range(lineRange):
                    lineNumber = reasonLocation[x] + y
                    dataReason = dataReason + allLine[lineNumber]
                    reason[x] = dataReason
            ##提取处理
            if x != processingNumber - 1:                                   #如果处理的不是最后一条
                if processingLocation[x] == failureLocation[x + 1] - 1:     #如果处理只有一行
                    processing[x] = allLine[processingLocation[x]]
                else: 
                    dataProcess = ''                                        #如果处理有多行
                    lineRange = failureLocation[x + 1] - processingLocation[x]
                    for y in range(lineRange):
                        lineNumber = processingLocation[x] + y
                        dataProcess = dataProcess + allLine[lineNumber]
                        processing[x] = dataProcess
            else:
                dataProcess = ''
                lineRange = allLineNumber - processingLocation[x]
                for y in range(lineRange):   
                    lineNumber = processingLocation[x] + y
                    dataProcess = dataProcess + allLine[lineNumber]
                    processing[x] = dataProcess
    return failure, failureNumber,failureLocation


##切割故障码和故障名称
###输入存有故障码和名称的词典failure以及故障码总数failureNumber
###输出分别存有故障码和故障名的两个词典code和name
def cutFailure(information, number):
    code = {}
    name = {}
    for n in range(number):
        str = information[n]
        str2 = str.split(' ', 1)
        code[n] = str2[0]
        name[n] = str2[1]
    return code, name

def getFailureInformation(codeList, number, location, targetCode,allLine):
    '''提取指定故障码的相关信息（提取单个故障码）,输入故障码词典、故障码数量、故障码所在行位置词典、要检索的故障码、输出被检索的故障码和相关信息'''
    missionComplete = False     #故障码查询结果标志位
    targetNumber = {}
    targetCount = 0
    if len(targetCode) != 6:
        missionComplete = False
    else:   
        for m in range(number):
            if targetCode in codeList[m]:
                targetNumber[targetCount] = m
                missionComplete = True
                targetCount = targetCount + 1           

    if missionComplete == True:
        dataTargetDic = {}
        for i in range(targetCount):
            targetLocationUp = location[targetNumber[i]]
            targetLocationDown = location[targetNumber[i] + 1]
            targetRange = targetLocationDown - targetLocationUp

            dataTargetDic[i] = ''
            for n in range(targetRange):
                lineNumber = targetLocationUp + n
                dataTargetDic[i] = dataTargetDic[i] + allLine[lineNumber]
        
        dataTarget = ''
        for j in range(targetCount):
            dataTarget = dataTarget + dataTargetDic[j]
            if j != targetCount - 1:
                dataTarget = dataTarget + '\n'
        return dataTarget
    else:
        missionFailed = '您输入的故障码有误，请核验后再次输入！\n'
        return missionFailed

def search_key_words_function(txtPath,searchingCode = 'N01004'):
    allLine, allLineNumber = get_all_lines(txtPath)
    failure, failureNumber,failureLocation = data_process(allLine,allLineNumber)
    failureCode, failureName = cutFailure(failure, failureNumber)
    result = getFailureInformation(failureCode, failureNumber, failureLocation, searchingCode,allLine)
    return result


# if __name__ == '__main__':
#     a = search_key_words_function('./Failure_Code_Table.txt','N01004')
#     print(a)