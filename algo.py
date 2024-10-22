import math

REL_TOLERANCE = 1e-9
ABS_TOLERANCE = 0.015
def compare_floats(val1, val2, rel_tol=REL_TOLERANCE, abs_tol=ABS_TOLERANCE):
    """
    Compare two floating-point values using relative tolerance.
    
    Args:
    - val1: First float value
    - val2: Second float value
    - rel_tol: Relative tolerance for the comparison (default is 1e-9)
    
    Returns:
    - True if the values are considered equal within the relative tolerance
    - False otherwise
    """
    return math.isclose(val1, val2, rel_tol=rel_tol, abs_tol=abs_tol)

def checker(data, signs, target_indx, lookahead=2):
    """
    Function to check and avoid false positives for formula cells
    Parameters:
        - data (list): List of lists containing the data to be checked.
        - signs (list): List of integers representing the signs of the formula.
        - target_indx (int): Index of the target cell to be checked.
    Returns:
        - valid (bool): Boolean value indicating whether the formula is valid or not.
    """
    valid = True
    k=0
    for col in data:     
        sum = 0
        for i in range(0, target_indx):
            if col[i] is not None:
                try:
                    sum += (signs[i] * col[i])
                except Exception as e:
                    print(f"Error with sign: {signs}, column value: {col}")
                    raise e
        target_value = col[target_indx]

        if compare_floats(sum, target_value):
            k+=1
        else: 
            break
    return k


def rec(indx, target_indx, curr, nums, signs, comb_signs, data, vis, k):
    """Purpose:
        This function recursively generates all possible combinations of signs for a given set of numbers and a target index.
    Parameters:
        - indx (int): The current index being evaluated.
        - target_indx (int): The target index to be reached.
        - curr (int): The current required value to reach the target index.
        - nums (list): The list of numbers to be evaluated.
        - signs (list): The current list of signs being evaluated.
        - comb_signs (list): The final list of all possible combinations of signs.
        - data (list): List of lists containing the data to be checked.
    Returns:
        - comb_signs (list): The final list of all possible combinations of signs.
    Processing Logic:
        - Checks if the current combination of signs is valid.
        - Recursively calls the function for each possible sign at the current index.
        - Appends the current sign to the list of signs being evaluated.
        - Pops the current sign from the list of signs being evaluated."""

    if len(comb_signs) > 0:
        return

    if compare_floats(curr, nums[target_indx]):
        valid = checker(data, signs, target_indx)
        if valid>=2:
            k[0]=valid
            comb_signs.append(signs[:])

    if indx == -1:
        return

    for new_sign in range(-1, 2):
        signs[indx]=new_sign
        if new_sign == 0:
            rec(indx - 1, target_indx, curr, nums, signs, comb_signs, data, vis, k)
        elif new_sign == 1 and vis[indx] == 0 and nums[indx] is not None:
            rec(indx - 1, target_indx, curr + nums[indx], nums, signs, comb_signs, data, vis, k)
        elif new_sign == -1 and vis[indx] == 0 and nums[indx] is not None:
            rec(indx - 1, target_indx, curr - nums[indx], nums, signs, comb_signs, data, vis, k)
        signs[indx]=0


def find_formula(data, vis, nums, target, target_indx):
    """Finds formula for a single cell.
    """
    k=[0]
    comb_signs = []
    rec(target_indx-1, target_indx, 0, nums, [0]*target_indx, comb_signs, data, vis, k)
    comb_signs.append([])
    return comb_signs[0], k[0]

def get_all_formulas(data):
    all_formulas = []
    nums = data[0]
    vis = [0] * (len(nums))
    k=-1
    for i in range(len(nums)):
        if nums[i] is None:
            all_formulas.append([])
            continue

        target = nums[i]
        result, k_ = find_formula(data, vis, nums, target, i)
        formula = []
        for j in range(i - len(result), i):
            if nums[j] is not None and result[j - (i - len(result))] != 0:
                vis[j] = 1
                formula.append(result[j - (i - len(result))] * (j + 1))
        if len(formula)>10: formula=[]
        if formula!=[]:
            if k==-1: k=k_
            else: k=min(k,k_)
        all_formulas.append(formula)
    return all_formulas, k
