import pdfplumber
import pandas as pd
import numpy as np
import os

def s120_scan_PDF_function(pdfPath):
    '''PDF扫描'''
    ##依次扫描PDF页面并串联文本
    if os.path.isfile(pdfPath) == False:
        return '没有选择文件!'
    base_name = os.path.basename(pdfPath)
    file_name = os.path.splitext(base_name)
    pageText = ''
    with pdfplumber.open(pdfPath) as pdf:
        for n in range(len(pdf.pages)):
            singlePage = pdf.pages[n]
            singlePageText = singlePage.extract_text()
            pageText = pageText + singlePageText
    ##完整文本转存TXT格式
    txtPath = './TXT/'+file_name[0]+'.txt'
    with open(txtPath, 'w', encoding = 'utf-8') as c:
        c.write(pageText)
        c.close()

    if os.path.isfile(txtPath) == False:
        return 'txt文件生成失败!'
    else:
        pdf_to_txt_result = 'txt文件生成完成! '+'保存在 '+ file_name[0]+'.txt 中。\n'

    ## 获取每行的信息和内容
    with open(txtPath, 'r', encoding = 'utf-8') as f:
        allLine = f.readlines()
        f.close()
    allLineNumber = len(allLine)
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

    ########################
    ###基于面向对象思想编写###
    ########################
    class Foo:
        def __init__(self, search, name, number, lineNumber):
            self.search = search
            self.name = name
            self.number = number
            self.lineNumber = lineNumber

        def searchError(self):                              #检索故障码
            global countNumber
            countNumber = 0
            for x in range(allLineNumber):    
                if self.search in allLine[x]:
                    self.name[self.number] = allLine[x - 1]
                    self.lineNumber[self.number] = x - 1
                    self.number = self.number + 1 
                    countNumber = self.number   

        def searchInformation(self):                        #检索信息值和信息类别
            global countNumber
            countNumber = 0
            for x in range(allLineNumber):
                if self.search in allLine[x]:
                    self.name[self.number] = allLine[x]
                    self.lineNumber[self.number] = x
                    self.number = self.number + 1
                    countNumber = self.number
        
        def searchInformation1(self):                        #检索其他需求信息
            global countNumber
            countNumber = 0
            for x in range(allLineNumber):
                if self.search in allLine[x]:
                    self.lineNumber[self.number] = x
                    self.number = self.number + 1
                    countNumber = self.number

    Failure = Foo('信息值： ', failure, failureNumber, failureLocation)
    Failure.searchError()
    failureNumber = countNumber
    # print(failureNumber)

    InformationValue = Foo('信息值： ', informationValue, informationValueNumber, informationValueLocation)
    InformationValue.searchInformation()
    informationValueNumber = countNumber
    # print(informationValueNumber)

    InformationCatefory = Foo('信息类别： ', informationCatefory, informationCateforyNumber, informationCateforyLocation)
    InformationCatefory.searchInformation()
    informationCateforyNumber = countNumber

    DrivingObject = Foo("驱动对象： ", drivingObject, drivingObjectNumber, drivingObjectLocation)
    DrivingObject.searchInformation1()
    drivingObjectNumber = countNumber
    # print(drivingObjectNumber)

    Component = Foo('组件： ', component, componentNumber, componentLocation)
    Component.searchInformation()
    componentNumber = countNumber
    # print(componentNumber)

    Reason = Foo('原因： ', reason, reasonNumber,reasonLocation)
    Reason.searchInformation1()
    reasonNumber = countNumber

    Processing = Foo('处理： ', processing, processingNumber, processingLocation)
    Processing.searchInformation1()
    processingNumber = countNumber

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
            if drivingObjectLocation[x] == componentLocation[x] - 1:    #如果驱动对象只有一行
                drivingObject[x] = allLine[drivingObjectLocation[x]]
            else:
                dataDrivingObject = ''                                                           #如果驱动对象有多行
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
            if reasonLocation[x] == processingLocation[x] - 1:          #如果原因只有一行
                reason[x] = allLine[reasonLocation[x]]
            else:
                dataReason = ''                                                           #如果原因有多行
                lineRange = processingLocation[x] - reasonLocation[x]
                for y in range(lineRange):
                    lineNumber = reasonLocation[x] + y
                    dataReason = dataReason + allLine[lineNumber]
                    reason[x] = dataReason
            ##提取处理
            if x != processingNumber - 1:                                           #如果处理的不是最后一条
                if processingLocation[x] == failureLocation[x + 1] - 1:     #如果处理只有一行
                    processing[x] = allLine[processingLocation[x]]
                else: 
                    dataProcess = ''                                                              #如果处理有多行
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
    excelPath = './EXCEL/'+file_name[0]+'.xlsx'
    CreateExcel(failure, informationValue, informationCatefory, drivingObject, component, reason, processing, excelPath)
    if os.path.isfile(excelPath) == False:
        return 'Excel文件生成失败!'
    else:
        txt_to_excel_result = 'Excel文件生成完成! '+'保存在 '+ file_name[0]+'.xlsx 中。'
    result = pdf_to_txt_result+txt_to_excel_result
    return result

def CreateExcel(information1, information2, information3, information4, information5, information6, information7, path):
    data = {'故障名称':information1, '信息值':information2, '信息类别':information3, '驱动对象':information4, '组件':information5, '原因':information6, '处理':information7}
    df = pd.DataFrame(data)
    df.to_excel(path) 


# if __name__ == '__main__':
#     a = s120_scan_PDF_function('./PDF/S120_failure_code_list.pdf')
#     print(a)