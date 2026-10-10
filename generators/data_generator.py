import pandas as pd
import numpy as np

def generate_qc_data(file_name='data/dane_testowe.csv', n_rows=200):
    characteristics = ['501', '502', '503', '504', '505', 
                       '506', '507', '508', '509', '510']
    
   
    np.random.seed(42)
    data = {
        'Referencja': np.random.choice(['DETAL-A', 'DETAL-B', 'DETAL-C', 'DETAL-D'], size=n_rows)
    }
    mock_tolerances = {}
    for col in characteristics:
        nominal_value = np.round(np.random.uniform(10.0, 50.0), 2)
        std_dev = np.random.uniform(0.05, 0.2)
        measurements = np.random.normal(loc=nominal_value, scale=std_dev, size=n_rows)
        outlier_indices = np.random.choice(n_rows, size=4, replace=False)
        measurements[outlier_indices] += np.random.uniform(1.5, 3.0, size=4) * np.random.choice([-1, 1], size=4)
        data[col] = np.round(measurements, 3)
        mock_tolerances[col] = np.round(nominal_value - (std_dev * 3), 2)

    df = pd.DataFrame(data)
    df = df[['Referencja'] + characteristics]
    df.to_csv(file_name, sep=';', decimal=',', index=False)
    
    print(f"Pomyślnie wygenerowano plik: {file_name} ({n_rows} wierszy, {len(characteristics)} charakterystyk).")
    print("-" * 40)
    print("Skopiuj poniższy słownik min_tol do swojego głównego skryptu, aby przetestować wykresy:")
    print("min_tol = {")
    for k, v in mock_tolerances.items():
        print(f"    '{k}': {v},")
    print("}")

if __name__ == "__main__":
    generate_qc_data()