
inFile = "data/csv/supplier_data.csv"
outFile = "data/output/out1.csv"

rfp = open(inFile,'r',newline='')
wfp = open(outFile,'w',newline='')

header = rfp.readline()
headerList = header.strip().split(',')

##필요 할경우 가공

headerStr = ','.join(map(str,headerList))

wfp.writelines(headerStr + '\n')

for row1 in rfp :
    row1List = row1.strip().split(',')
    ##가공하기 (필요시)

    row1str = ','.join(map(str, row1List))
    wfp.writelines(row1str + '\n')

rfp.close()
wfp.close()

print("끝")