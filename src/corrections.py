import numpy as np
def benjamini_hochberg(p_values):
    p_values = np.array(p_values)
    sorted_p_values = np.sort(p_values)
    m = len(sorted_p_values)
    bh_threshold = (np.arange(1, m + 1) / m) * 0.05
    passing = sorted_p_values <= bh_threshold
    if passing.any():
        max_k = np.max(np.where(passing))
        significant = np.zeros(m, dtype = bool)
        significant[:max_k + 1] = True
    else:
        significant = np.zeros(m , dtype = bool)
    return significant , sorted_p_values ,bh_threshold

