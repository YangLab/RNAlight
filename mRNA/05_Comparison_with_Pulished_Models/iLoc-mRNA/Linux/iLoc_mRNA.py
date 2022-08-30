# coding=utf-8

import sys

def detectExistDirectory(tempDir):
    if os.path.exists(tempDir):
        shutil.rmtree(tempDir)

    os.makedirs(tempDir)

#计算
def Calculate_fre(seq,eighttuple_matrix):
    eightNC_num = len(seq)-9+1
    eighttuple_matrix_dict = dict()
    eighttuple_matrix_dict = eighttuple_matrix_dict.fromkeys(eighttuple_matrix,0)
    
    for each_seq_th in range(eightNC_num):
        octNC = seq[each_seq_th:each_seq_th+9]
        try:
            eighttuple_matrix_dict[octNC] += 1
        except:
            pass
    numth = 0
    g = open('./temp/seq.svm','a')
    g.write("0\t")
    for eighttuple_th in eighttuple_matrix:
        numth += 1
        fre = eighttuple_matrix_dict[eighttuple_th]/float(eightNC_num)
        if numth != 29745:
            g.write('%d:%.6f\t' % (numth,fre))
        else:
            g.write('%d:%.6f\n' % (numth,fre))
    g.close()

##get model features
def getfeaturelist(featurefile):
    f = open(featurefile,'r')

    featurelist = []
    for eachfeature in f:
        featurelist.append(eachfeature.strip())

    f.close()
    return featurelist

def getseq(seqFile,featurelist):
    f = open(seqFile,'r')
    seqFile_g = f.readlines()
    seqFile_length = len(seqFile_g)
    annotation = dict()
    countn = 0
    seq=''
    for eachth in range(seqFile_length):
        if seqFile_g[eachth][0] == '>':
            annotation[countn] = seqFile_g[eachth].strip()
            countn+=1
            if seq !='':
                Calculate_fre(seq,featurelist)
                seq=''
        else:
            seqFile_g[eachth] = seqFile_g[eachth].upper()   #将碱基序列转换成大写
            seq += seqFile_g[eachth].strip()     #去掉行末换行符
    if seq !='':
        Calculate_fre(seq,featurelist)
    return annotation

def runSVM():
    commands = []
    commands.append(r"./libsvm-3.22/svm-scale -r ./model/mRNAscale.rule ./temp/seq.svm > ./temp/seq.scale")
    commands.append(r"./libsvm-3.22/svm-predict -b 1 ./temp/seq.scale ./model/iLoc_mRNA.model ./temp/res.txt >out.txt")

    for eachCmd in commands:
        os.system(eachCmd)
    print("	Prediction Finished !")
    os.remove('out.txt')

def generateResult(annotation,outfile):
    outResult = "./temp/res.txt"
    f = open(outResult,'r')
    countn = 0
    g = open(outfile,'w')
    g.write('Sequence number\tAnnotation information\tSubcellular location\tProbability\n')
    for eachline in f:
        temp = eachline.split(' ')
        if temp[0]=='labels':
            pass
        else:
            countn+=1
            temp = eachline.split(' ')
            if(temp[0]=='1'):
                g.write('%s\t%s\tCytosol/Cytoplasm\t%s\n'%(countn,annotation[countn-1],temp[1]))
            if(temp[0]=='2'):
                g.write('%s\t%s\tRibosome\t%s\n'%(countn,annotation[countn-1],temp[2]))
            if(temp[0]=='3'):
                g.write('%s\t%s\tEndoplasmic reticulum\t%s\n'%(countn,annotation[countn-1],temp[3]))
            if(temp[0]=='4'):
                g.write('%s\t%s\tNucleus/Exosome/Dendrite/Mitochondrion\t%s\n'%(countn,annotation[countn-1],temp[4]))

    g.close()

import os
import sys
import shutil

pathPrefix = os.getcwd() + os.path.sep
tempDir = pathPrefix + "temp"

if __name__=='__main__':

    detectExistDirectory(tempDir)
    featurelist = getfeaturelist('./model/m_optimalfeaturelist.txt')
    seqfile = sys.argv[1]
    annotation = getseq(seqfile,featurelist)
    runSVM()
    generateResult(annotation,sys.argv[2])




