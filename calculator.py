import pandas as pd

##Wylicza dane na bazie zapisanych tolerancji,szuka outlierów i zwraca słownika:
### rozmiar probki, czy pod tolerancja, liczbę poniżej, procent poniżej, średnią, minmium,maksimu,odchylenie standardowe i tolerancje
def calculate_statistics(measurements:pd.DataFrame,minimum_tolerance:float,cleaned_data=None) -> dict:
    if cleaned_data is None:
          cleaned_data = measurements
    under_tol = measurements<minimum_tolerance
    number_under_tol=under_tol.sum()
    percentage_under_tol = (number_under_tol/len(measurements))*100
    return {
        'n' : len(measurements),
        'under_tol_mask':under_tol,
        'number_under_tol': number_under_tol,
        'percentage_under_tol': percentage_under_tol,
        'mean': cleaned_data.mean() if not cleaned_data.empty else measurements.mean(),
        'min':measurements.min(),
        'max':measurements.max(),
        'std':cleaned_data.std() if len(cleaned_data)>1 else 0.0,
        'tol_val': float(minimum_tolerance)
    }
#wyszukuje wartości skrajne czyszcząc z nich wartości skrajne oraz listę outlierów
#używa MAD lub IQR zależnie od rozmiaru próbki IQR dla n>=15 4<n<15 dla MAD
def remove_outliers(measurements:pd.DataFrame,minimum_tolerance: float) -> tuple[pd.DataFrame,pd.DataFrame]:
    n_mass = len(measurements)
    if n_mass<=4:
        statistical_outliers = pd.Series(dtype=float)
    elif 4<n_mass<15:
        median_val = measurements.median()
        abs_dev = (measurements - median_val).abs()
        mad = abs_dev.median()
        if mad == 0:
            mad = 1e-4
        mod = 0.6745*abs_dev/mad
        statistical_outliers  =measurements[mod>3.5]
    else:
        Q1= measurements.quantile(0.25)
        Q3 = measurements.quantile(0.75)
        IQR = Q3-Q1
        lower_Q = Q1-1.5*IQR
        upper_Q = Q3+3*IQR
        statistical_outliers = measurements[(measurements<lower_Q)|(measurements>upper_Q)]
    critical_outliers= statistical_outliers[statistical_outliers<minimum_tolerance]
    cleaned_data = measurements.drop(critical_outliers.index)
    return cleaned_data,critical_outliers
    
