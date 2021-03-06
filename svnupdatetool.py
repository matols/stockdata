import subprocess
 
 
def executeSvnCmd(cmds):
    p = subprocess.Popen(cmds, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    datas=p.stdout.read().decode("utf-8")
    return datas

def getChangedFiles():
    
    datas=executeSvnCmd(['svn', 'status'])
    dlist=datas.split("\r\n")
    files=[]
    for tt in dlist:
        #print(tt)
        tfile=tt.split("       ")
        if len(tfile)<2:
            print(tt)
            continue
        if tfile[0]=="?":
            print("? add")
            submitAddFile(tfile[1].replace("\\","/"))
            continue
        
        tfile=tfile[1]
        tfile=tfile.replace("\\","/")
        if tfile.find(".csv.")>0:
            continue
        files.append(tfile)
    
    #print(files)
    return files
    
def submitFiles(files):
    print("files:",files)
    filesStr=" ".join(files)
    print(filesStr)
    cmds=["svn","commit","-m","hihi",filesStr]
    print(cmds)
    cmsStr=" ".join(cmds)
    print("cmsStr",cmsStr)
    executeSvnCmd("svn cleanup")
    datas=executeSvnCmd(cmsStr)
    print("submit",datas)
    
def updateFiles(files):
    print("files:",files)
    filesStr=" ".join(files)
    print(filesStr)
    cmds=["svn","update",filesStr]
    print(cmds)
    cmsStr=" ".join(cmds)
    print("cmsStr",cmsStr)
    #executeSvnCmd("svn cleanup")
    datas=executeSvnCmd(cmsStr)
    print("update",datas)

def submitAddFile(file):
    executeSvnCmd("svn add "+file)
    executeSvnCmd("svn commit -m hihi "+file)
    
def workLoop():
    executeSvnCmd("svn cleanup")
    changefiles=getChangedFiles()
    allLen=len(changefiles)
    print(allLen)
    sublen=allLen
    maxLen=50
    if sublen>maxLen:
        sublen=maxLen
    if sublen<1:
        return False
    start=0
    oneCount=20
    endPos=start+oneCount
    while start<maxLen:
        print("updateFiles",start,endPos)
        updateFiles(changefiles[start:endPos])
        start=endPos
        endPos=start+oneCount
    return False
    
def doWork():
    while True:
        rst=workLoop()
        if rst:
            pass
        else:
            break
#datas=executeSvnCmd('svn commit -m hihi stockdatas/000009.csv stockdatas/000010.csv')
#print(datas)
#workLoop()
doWork()