import numpy as np

def calculate_rop(avg_demand, lead_time, std_dev, service_z):
    return avg_demand * lead_time + service_z * std_dev * np.sqrt(lead_time)
