import RFIDreader
import RFIDwriter
import DBInterface
import time

progTag = 'PROGWITHMEPLEASE                                '
# studentRefreshTime = 1 #  In minutes

x = None

listOfStudentIDs = []

for i in DBInterface.pullAllStudents():
    print(i)
    try:
        ID = i['StudentUID']
        ID = RFIDreader.Padder(ID)
        listOfStudentIDs.append(ID)
    except KeyError:
        pass
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
            time.sleep(3)
            try:
                studentToProgram = DBInterface.getStudentToProgram()
                IDToProgram = studentToProgram['UID']
                print(IDToProgram)
                RFIDwriter.WriteMFRC522(IDToProgram)
                time.sleep(0.1)
                listOfStudentIDs.append(RFIDreader.Padder(IDToProgram))
                prevX = RFIDreader.Padder(IDToProgram)
                DBInterface.onSuccesfulProgram(studentToProgram['StudentName'], studentToProgram['HeadTeacher'], studentToProgram['UID'])
            except IndexError:
                print("NOTHING TO PROGRAM :(")
        else:
            ID = RFIDreader.Padder(ID)
            if ID in listOfStudentIDs:
                print(f"Student with id {ID.split(' ')[0]} was here!")
                DBInterface.StudentChangedState(ID.split(' ')[0])
            else:
                print("Unknown tag!!!")
    else:
        print(
            f"Card with id: {ID.split(' ')[0]} was scanned more than once ignoring it!")
        time.sleep(0.3)
