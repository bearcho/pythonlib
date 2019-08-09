import xlrd

inFile = 'data/excel/sales_2013.xlsx'
workbook = xlrd.open_workbook(inFile)

scnt = workbook.nsheets
print(scnt)

for worksheet in workbook.sheets():
    sName = worksheet.name
    sRow = worksheet.nrows
    sCol = worksheet.ncols

    print(sName,sRow,sCol )