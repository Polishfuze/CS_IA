import RFIDreader 
import RFIDwriter
import DBInterface
import time

progTag = 'PROGWITHMEPLEASE                                '
# studentRefreshTime = 1 #  In minutes

x = None

listOfStudentIDs = []

for i in DBInterface.pullAllStudents()['Items']:
    ID = i['StudentID']
    ID = RFIDreader.Padder(ID)
    listOfStudentIDs.append(ID)
print(listOfStudentIDs)

prevX = ()
lastScan = 0
while True:
    x = RFIDreader.ReadMFRC522()
    # print(type(x))
    if x != prevX or time.time()-lastScan > 10:
        prevX = x
        lastScan = time.time()
        ID = x[1]
        if ID == progTag:
            print("Programming Mode!")
            studentToProgram = DBInterface.getStudentToProgram()
            IDToProgram = studentToProgram['StudentID']
            RFIDwriter.WriteMFRC522(IDToProgram)
            time.sleep(0.1)
            if RFIDreader.ReadMFRC522() != RFIDreader.Padder(IDToProgram):
                print("Write Failed!!!")
            prevX = RFIDreader.Padder(IDToProgram)
        else:
            while len(ID) < len(progTag):
                ID += ' '
            if ID in listOfStudentIDs:
                print(f"Student with id {ID.split(' ')[0]} was here!")
                DBInterface.pushStudent(ID.split(' ')[0])
            else:
                print("Unknown tag!!!")
    else:
        print(f"Card with id: {ID.split(' ')[0]} was scanned more than once ignoring it!")
        time.sleep(0.3)
