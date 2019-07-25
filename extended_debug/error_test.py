import sys
class UnexpectedError(Exception):
    def __init__(self,):
        error=sys.exc_info()
        message=[str(error[0]).split('\'')[1]+': '+str(error[1])]
        self.args=tuple(message)
        self.with_traceback(error[2])

def expect(expression:str,expected_error:BaseException,*,global_variables:dict=None,local_variables:dict=None)->bool:
    '''test for a given exception'''
    if not isinstance(expression,str):
        raise TypeError('expect() expression argument must be a string, not a '+str(type(expression)))
    if not (issubclass(expected_error,BaseException) or isinstance(expected_error,BaseException)):
        raise TypeError('expect() expected_error argument must be a class derived from BaseException, not '+str(type(expected_error)))
    if not (isinstance(global_variables,dict) or global_variables==None):
        raise TypeError('expect() global_variables argument must be a dictionary or None, not a '+str(type(global_variables)))
    if not (isinstance(local_variables,dict) or local_variables==None):
        raise TypeError('expect() local_variables argument must be a dictionary or None, not a '+str(type(local_variables)))
    try:
        eval(expression,global_variables,local_variables)
    except:
        error=sys.exc_info()[0]
        correct=issubclass(error,expected_error)
        if not correct:
            raise UnexpectedError()
    else:
        correct=False
    return correct
assert expect('1/0',ZeroDivisionError)
assert expect('1/0',BaseException)
assert expect('fg',NameError)
assert not expect('fg',NameError,global_variables=dict({'fg':1}))
assert not expect('fg',NameError,local_variables=dict({'fg':[]}))
assert expect('expect("fg",ArithmeticError)',UnexpectedError,global_variables={'expect':expect})
