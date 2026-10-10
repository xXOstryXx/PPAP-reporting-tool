import pandas as pd
import sys  

##Pobiera dane z pliku .csv wymienia przecinki na kropki dla czystości danych i zwraca w fomacie dataframe
def load_and_clear_data(measurements_file: str) -> tuple[pd.DataFrame,str] :
    try:
        df = pd.read_csv(measurements_file, sep=';', decimal=',')
        df.columns = df.columns.astype(str).str.strip().str.replace('\ufeff', '').str.replace(',','.')
        print(f"Wczytano plik pomiarowy: {measurements_file}")
        print(f"Wykryte kolumny do analizy: {df.columns.tolist()}\n" + "-"*40)
        ref_column_name = df.columns[0]
        char_cols = df.columns[1:]
        try:
            sorted_char_cols = sorted(char_cols, key = lambda x: float(x))
        except ValueError:
            sorted_char_cols = sorted(char_cols)
        return df[[ref_column_name]+sorted_char_cols],ref_column_name
    except FileNotFoundError:
        print(f"BŁĄD: Nie znaleziono pliku '{measurements_file}'. Sprawdź nazwę i lokalizację.")
        sys.exit()
    except Exception as e:
        print(f"BŁĄD Wczytywania: {e}")
        sys.exit()
