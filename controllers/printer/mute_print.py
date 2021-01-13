from setting import OS_WIN32, TEMP_DIR, NAME_PDF, ACROBAT_READER
import subprocess
from flask import abort

if OS_WIN32:
    try:
        import win32api
        import win32print

    except ImportError:
        abort(500, 'system no windows')

def auto_print():
    try:
        filename= TEMP_DIR+NAME_PDF
        currentprinter = win32print.GetDefaultPrinter()
        acroread=ACROBAT_READER
        # acroread=r'C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe' 
        """ '"%s"'is to wrap double quotes around paths 
        as subprocess will use list2cmdline internally if we pass it a list 
        which escapes double quotes and Adobe Reader doesn't like that  """
        cmd='"%s" /N /T "%s" "%s"'%(acroread,filename,currentprinter)  
        proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE) 
        stdout,stderr=proc.communicate() 
        exit_code=proc.wait()  
        return currentprinter
    except Exception as e:
        abort(500, e)