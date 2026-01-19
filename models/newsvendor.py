from scipy.stats import norm

def newsvendor_optimal_q(mu, sigma, cu, co):
    critical_ratio = cu / (cu + co)
    return norm.ppf(critical_ratio, mu, sigma)
