from xlrd import open_workbook
from xlwt import Workbook

inFile = 'data/excel/sales_2013.xlsx'
outFile = "data/output/out2.xls"


outWorkbook = Workbook()

with open_workbook(inFile) as workbook:
    for worksheet in workbook.sheets():
        sName = worksheet.name
        sRow = worksheet.nrows
        sCol = worksheet.ncols
        
        # 워크 시트 만들기
        outWS = outWorkbook.add_sheet(sName)
        
        for i in range(sRow):
            for k in range(sCol):
                cValue = worksheet.cell_value(i,k)
                ##데이터 가공 부분
                outWS.write(i,k,cValue)
                
    outWorkbook.save(outFile)

print("끝")
 