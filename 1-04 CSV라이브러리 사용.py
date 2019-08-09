import csv

inFile = "data/csv/supplier_data.csv"
outFile = "data/output/out2.csv"

with open(inFile,'r',newline='') as rfp:
    with open(outFile,'w',newline='') as wfp:
        csv_rfp = csv.reader(rfp,delimiter=',')
        csv_wfp = csv.writer(wfp, delimiter=',')


        header = next(csv_rfp)
        csv_wfp.writerow(header)
        
        for rowList in csv_rfp:
            #필요시 rowList 가공

            print(int(rowList[2]))
            print(float(rowList[3][1:]))
            if(int(rowList[2]) > 5000):
                rowList[3] = '$' + str(float(rowList[3][1:]) * 1.2)
            csv_wfp.writerow(rowList)
        pass

print("끝")