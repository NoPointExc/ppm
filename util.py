def num_to_str(val, num_sys = 10):
    result = str(val)
    if num_sys == 2:
        result = bin(val)
    elif num_sys == 16:
        result = hex(val)
    return result 

def get_adjance(index, arr):
    result=0
    left=index - 1
    while(left > 0 and arr[left] == arr[index]):
        left=left - 1
        result=result + 1
    
    right=index + 1
    while (right < len(arr) and arr[right] == arr[index]):
        right=right + 1
        result=result + 1

    return result

def get_code_reward(index, arr, code_digits):    
    result=0
    if index < 2:
        return result
    if arr[2] == code_digits[0]: result=result + 1    
    if arr[3] == code_digits[1]: result=result + 1
    return result
