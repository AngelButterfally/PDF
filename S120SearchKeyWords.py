import os

def get_all_lines(txtPath = './TXT/S120_failure_Code_list.txt'):
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

def data_process(allLine, allLineNumber, dataClass):
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
            informationValue[failureNumber] = allLine[x]            #信息值
            informationCatefory[failureNumber] = allLine[x + 1]     #信息类别

            failureLocation[failureNumber] = x - 1                  #故障码所在行
            informationValueLocation[informationValueNumber] = x
            informationCateforyLocation[informationCateforyNumber] = x + 1

            failureNumber = failureNumber + 1
            informationValueNumber = informationValueNumber + 1
            informationCateforyNumber = informationCateforyNumber + 1
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
                    if y == 0:   
                        lineNumber = drivingObjectLocation[x] + y
                        dataDrivingObject = dataDrivingObject + allLine[lineNumber]
                        drivingObject[x] = dataDrivingObject
                    else:
                        lineNumber = drivingObjectLocation[x] + y
                        dataDrivingObject = dataDrivingObject + '\t' + '\t' + allLine[lineNumber]
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
                    if y == 0:
                        lineNumber = reasonLocation[x] + y
                        dataReason = dataReason + allLine[lineNumber]
                        reason[x] = dataReason
                    else:
                        lineNumber = reasonLocation[x] + y
                        dataReason = dataReason + '\t' + '\t' + allLine[lineNumber]
                        reason[x] = dataReason
            ##提取处理
            if x != processingNumber - 1:                                   #如果处理的不是最后一条
                if processingLocation[x] == failureLocation[x + 1] - 1:     #如果处理只有一行
                    processing[x] = allLine[processingLocation[x]]
                else: 
                    dataProcess = ''                                        #如果处理有多行
                    lineRange = failureLocation[x + 1] - processingLocation[x]
                    for y in range(lineRange):
                        if y == 0:
                            lineNumber = processingLocation[x] + y
                            dataProcess = dataProcess + allLine[lineNumber]
                            processing[x] = dataProcess
                        else:
                            lineNumber = processingLocation[x] + y
                            dataProcess = dataProcess + '\t' + '\t' + allLine[lineNumber]
                            processing[x] = dataProcess
            else:
                dataProcess = ''
                lineRange = allLineNumber - processingLocation[x]
                for y in range(lineRange):   
                    if y == 0:
                        lineNumber = processingLocation[x] + y
                        dataProcess = dataProcess + allLine[lineNumber]
                        processing[x] = dataProcess
                    else:
                        lineNumber = processingLocation[x] + y
                        dataProcess = dataProcess + '\t' + '\t' + allLine[lineNumber]
                        processing[x] = dataProcess
    
    # if dataClass == 'failure':
    #     return failure, failureNumber,failureLocation
    # elif dataClass == 'informationValue':
    #     return informationValue, informationValueNumber, informationValueLocation
    # elif dataClass == 'informationCatefory':
    #     return informationCatefory, informationCateforyNumber, informationCateforyLocation
    # elif dataClass == 'drivingObject':
    #     return drivingObject, drivingObjectNumber, drivingObjectLocation
    # elif dataClass == 'component':
    #     return component, componentNumber, componentLocation
    # elif dataClass == 'reason':
    #     return reason, reasonNumber, reasonLocation
    # elif dataClass == 'processing':
    #     return processing, processingNumber, processingLocation
    if dataClass == 'failure':
        return failure, failureNumber
    elif dataClass == 'informationValue':
        return informationValue, informationValueNumber
    elif dataClass == 'informationCatefory':
        return informationCatefory, informationCateforyNumber
    elif dataClass == 'drivingObject':
        return drivingObject, drivingObjectNumber
    elif dataClass == 'component':
        return component, componentNumber
    elif dataClass == 'reason':
        return reason, reasonNumber
    elif dataClass == 'processing':
        return processing, processingNumber

##切割名称和内容
def cutMessage(inforamtion, number):
    '''输入存有名称和内容的词典及总数'''
    '''输出存有名称和内容的词典name和content'''
    name = {}
    content = {}
    for n in range(number):
        str = inforamtion[n]
        str2 = str.split(' ', 1)
        name[n] = str2[0]
        content[n] = str2[1]
    return name, content

def formatting(name, content, number):
    information = {}
    for n in range(number):
        result = name[n] + '\t' + '\t' + content[n]
        information[n] = result
    return information

def formatting1(name, content, number):
    information = {}
    for n in range(number):
        result = name[n] + '\t' + content[n]
        information[n] = result
    return information

def s120_getFailureInformation(txtPath, targetCode = 'N01004'):
    '''提取指定故障码的相关信息（提取单个故障码）,输入故障码词典、故障码数量、故障码所在行位置词典、要检索的故障码、输出被检索的故障码和相关信息'''
    allLine, allLineNumber = get_all_lines(txtPath)

    failure, failureNumber = data_process(allLine,allLineNumber,'failure')
    code, name = cutMessage(failure, failureNumber)
    failure = formatting(code, name, failureNumber)

    informationValue, informationValueNumber = data_process(allLine,allLineNumber,'informationValue')
    name, content = cutMessage(informationValue, informationValueNumber)
    informationValue = formatting1(name, content, informationValueNumber) 

    informationCatefory, informationCateforyNumber = data_process(allLine,allLineNumber,'informationCatefory')
    name, content = cutMessage(informationCatefory, informationCateforyNumber)
    informationCatefory = formatting1(name, content, informationCateforyNumber) 

    drivingObject, drivingObjectNumber = data_process(allLine,allLineNumber,'drivingObject')
    name, content = cutMessage(drivingObject, drivingObjectNumber)
    drivingObject = formatting1(name, content, drivingObjectNumber)

    component, componentNumber = data_process(allLine,allLineNumber,'component')
    name, content = cutMessage(component, componentNumber)
    component = formatting(name, content, componentNumber)

    reason, reasonNumber = data_process(allLine,allLineNumber,'reason')
    name, content = cutMessage(reason, reasonNumber)
    reason = formatting(name, content, reasonNumber)

    processing, processingNumber = data_process(allLine,allLineNumber,'processing')
    name, content = cutMessage(processing, processingNumber)
    processing = formatting(name, content, processingNumber)
  
    missionComplete = False     #故障码查询结果标志位
    targetNumber = {}
    targetCount = 0
    if len(targetCode) != 6:
        missionComplete = False
    else:   
        for m in range(failureNumber):
            if targetCode in code[m]:
                targetNumber[targetCount] = m
                missionComplete = True
                targetCount = targetCount + 1           

    if missionComplete == True:
        dataTargetDic = {}
        for i in range(targetCount):
            serialNumber = targetNumber[i]
            dataTargetDic[i] = ''
            dataTargetDic[i] = failure[serialNumber] + informationValue[serialNumber] + informationCatefory[serialNumber] + \
                drivingObject[serialNumber] + component[serialNumber] + reason[serialNumber] + processing[serialNumber]
        
        dataTarget = ''
        for j in range(targetCount):
            dataTarget = dataTarget + dataTargetDic[j]
            if j != targetCount - 1:
                dataTarget = dataTarget + '\n'
        return dataTarget
    else:
        missionFailed = '您输入的故障码有误，请核验后再次输入！\n'
        return missionFailed

def s120_search_key_words_function(txtPath,searchingCode = 'N01004'):
    allLine, allLineNumber = get_all_lines(txtPath)
    failure, failureNumber,failureLocation = data_process(allLine,allLineNumber,'failure')
    failureCode, failureName = cutMessage(failure, failureNumber)
    result = getFailureInformation(failureCode, failureNumber, failureLocation, searchingCode,allLine)
    return result


# if __name__ == '__main__':
#     a = s120_getFailureInformation('./TXT/S120_failure_Code_list.txt', 'N01004')
#     #a = s120_search_key_words_function('./TXT/S120_failure_Code_list.txt','N01004')
#     print(a)