# coding = utf-8
'''
Created on 2016-5-17

替换XML相应节点的 EL 错位的问题

@author: HuXiong
'''

import xml.dom.minidom
import re
import os

str_start_exp = '^\s*\$[\{]?[a-zA-Z0-9._\s]*$';

str_end_exp = '^[a-zA-Z0-9._\s]*}[\s]*$';

xml_node_TagName="w:t"

filelist=[]


# 循环文件夹
def list_Dir_file(in_fileDir):
    for file in os.listdir(in_fileDir.decode("utf8")):
        full_path_name=os.path.join(in_fileDir,file)
        if os.path.isfile(full_path_name):
            if full_path_name.endswith("ftl"):
                filelist.append(full_path_name)
        else:
            list_Dir_file(full_path_name)
    return filelist


# 创建不存在文件夹
def createFileDir(fileName):
    if not os.path.exists(os.path.split(fileName)[0]):
        os.makedirs(os.path.split(fileName)[0])


# 循环文件夹相关文件
def replaceNodeValue(in_file,in_fileDir,out_fileDir):
    nodeChangeValue=""
    flag = False
    changeNodeCount = 0
    firstNode = None

    DOMTree = xml.dom.minidom.parse(in_file)

    root = DOMTree.documentElement

    nodes = root.getElementsByTagName(xml_node_TagName)

    for node in nodes:
        if node.firstChild:
            nodedata = node.firstChild.data
            if re.match(str_start_exp,nodedata):
                firstNode = node.firstChild
                changeNodeCount+=1
                flag = True
                nodeChangeValue=""
            if(flag):
                if re.match(str_end_exp,nodedata):
                    flag = False
                nodeChangeValue+= nodedata
                node.firstChild.data=""
                firstNode.data = nodeChangeValue

    target_file = in_file.replace(in_fileDir,out_fileDir)

    createFileDir(target_file)

    f=open(target_file,"w")

    DOMTree.writexml(f)

    f.close()

    print "共有节点：%d\t替换节点：%d\t输出：%s" % (len(nodes),changeNodeCount,target_file)


# 替换节点方法
def format_file_Node(in_fileDir,out_fileDir):
    for file in list_Dir_file(in_fileDir):
        replaceNodeValue(file,in_fileDir,out_fileDir)


format_file_Node(r"D:\Workspaces\MyEclipse\ContractMgt\src\test\resources\ContractTemplate\NEW_Q车贷",r"D:\Workspaces\MyEclipse\ContractTemplateProcess\WebContent\test_folder")
