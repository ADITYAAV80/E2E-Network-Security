import sys
from src.NetworkSecurity.logging.logger import logger

class NetworkSecurityException(Exception):

    def __init__(self, error_message, error_details: sys):

        self.error_message = error_message
        # When an exception occurs, Python automatically stores the details of the exception using sys.exc_info() 
        # returns (type, value, traceback)
        self.type,self.value,exec_tb = error_details.exc_info()
        self.lineno = exec_tb.tb_lineno
        self.file_name = exec_tb.tb_frame.f_code.co_filename
    
    def __str__(self):
        return f"""Error occurred in python 
                    script name:
                    =====================
                    [{self.file_name}] 
                    line number [{self.lineno}] 
                    error message [{self.error_message}]
                    error type [{self.type}]
                    error value [{self.value}]
                    """    

if __name__=="__main__":
    try:
        a = 1/0
        print("This will not be printed",a)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
