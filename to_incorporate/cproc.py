import os, datetime, time

def make_cproc(rc_exp, rc_store, coverslips):
    #define and make folder to record job processing
    proc_folder = rc_store + rc_exp + 'processing_jobs/'
    today = datetime.date.today()  
    todaystr = today.isoformat()
    if not os.path.exists(proc_folder):                          
        os.mkdir(proc_folder)
    if not os.path.exists(proc_folder + todaystr):                          
        os.mkdir(proc_folder + todaystr)
    now = (time.strftime("%I_%M_%p_%S",time.localtime()))
    print (now)
    os.mkdir(proc_folder + todaystr + '/' + now)
    cproc_folder = proc_folder + todaystr + '/' + now
    for c in coverslips:
        local_exp = c + "/"
        leseg =  local_exp.split('/')
        lefolder =  str(leseg[-2:-1])[1:-1]
        coverslip = int(lefolder[-3:-1])
        c_cproc_folder = cproc_folder + '/' + str(coverslip)
        os.mkdir (c_cproc_folder)
        print ("making folder for coverslip " + str(coverslip))
    return (cproc_folder)

def make_proc(rc_exp, rc_store):
    #define and make folder to record job processing
    proc_folder = rc_store + rc_exp + 'processing_jobs/'
    today = datetime.date.today()  
    todaystr = today.isoformat()
    if not os.path.exists(proc_folder):                          
        os.mkdir(proc_folder)
    if not os.path.exists(proc_folder + todaystr):                          
        os.mkdir(proc_folder + todaystr)
    now = (time.strftime("%I_%M_%p_%S",time.localtime()))
    print (now)
    os.mkdir(proc_folder + todaystr + '/' + now)
    cproc_folder = proc_folder + todaystr + '/' + now

    return (cproc_folder)
