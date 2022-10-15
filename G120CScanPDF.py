import pdfplumber
import pandas as pd
import numpy as np
import os

def scan_PDF_function(pdfPath):
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

    informationCatefory = {}        #信息类别
    informationCateforyNumber = 0
    informationCateforyLocation = {}

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
                    if '信息值： ' not in allLine[x - 1]:
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

    Failure = Foo('信息类别： ', failure, failureNumber, failureLocation)
    Failure.searchError()
    failureNumber = countNumber

    InformationCatefory = Foo('信息类别： ', informationCatefory, informationCateforyNumber, informationCateforyLocation)
    InformationCatefory.searchInformation()
    informationCateforyNumber = countNumber

    Reason = Foo('原因： ', reason, reasonNumber,reasonLocation)
    Reason.searchInformation1()
    reasonNumber = countNumber

    Processing = Foo('处理： ', processing, processingNumber, processingLocation)
    Processing.searchInformation1()
    processingNumber = countNumber

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
    if failureNumber == informationCateforyNumber:
        CreateExcel(failure, informationCatefory, reason, processing, excelPath)
    if os.path.isfile(excelPath) == False:
        txt_to_excel_result = '文件生成失败! 请选择G120C故障手册文件!'
        txtDocument = './TXT'
        txtName = file_name[0]+'.txt'
        os.remove(os.path.join(txtDocument, txtName))
        return txt_to_excel_result
    else:
        txt_to_excel_result = pdf_to_txt_result + 'Excel文件生成完成! '+'保存在 '+ file_name[0]+'.xlsx 中。'
    result = txt_to_excel_result
    return result

def CreateExcel(information1, information2, information3, information4, path):
    data = {'故障名称':information1, '信息类别':information2, '原因':information3, '处理':information4}
    df = pd.DataFrame(data)
    df.to_excel(path) 


if __name__ == '__main__':
    a = scan_PDF_function('./PDF/G120C_failure_code_list.pdf')
    print(a)