import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
import warnings
import reporter
import load_data

warnings.filterwarnings('ignore')

def main():
    
    ##zbieranie nazw danych do pliku, miejsc zapisu, daty do przygotowania raportu
    end_slide_path = 'assets/End_page.jpg' 
    measurements_file = 'data/dane_testowe.csv' 
    date_of_report = datetime.now().strftime('%Y-%m-%d')
    report_name = f'raport_statystyczny_{date_of_report}.pdf' 
    characteristics_path = 'Characteristics' 
    title_slide_path = 'assets/Title_page.jpg'
    min_tol = {
        '501': 10.82,
        '502': 20.63,
        '503': 10.83,
        '504': 35.83,
        '505': 34.5,
        '506': 29.2,
        '507': 10.69,
        '508': 27.73,
        '509': 35.15,
        '510': 25.68,
    }
    common_tol = None
    df, ref_column_name = load_data.load_and_clear_data(measurements_file)
    all_outliers=[]
    with PdfPages(report_name) as pdf:
        #odwołanie do reporter.py do wygenerowania strony tytułowej 
        reporter.add_full_page_img(pdf, title_slide_path)
        
        for column in df.columns[1:]:
            minimum_tolerance = min_tol.get(column, common_tol)
            if minimum_tolerance is None:
                continue
            seria = df[column].astype(str).str.replace(',', '.') if df[column].dtype == 'object' else df[column]
            measurements = pd.to_numeric(seria, errors='coerce').dropna()
            if measurements.empty:
                continue
            reporter.plot_histogram_page(pdf, column, measurements, minimum_tolerance)
        for ref_id, group in df.groupby(ref_column_name):
            print(f"Przetwarzanie referencji ID: {ref_id}")
            target_image_path = reporter.get_existing_image("Parts_foto", ref_id)
            if target_image_path:
                reporter.add_titled_image_page(pdf, target_image_path, f"Part Reference: {ref_id} - Part Photo")
                print(f"Dodano stronę ze zdjęciem dla referencji: {ref_id}")
            valid_characteristics = []
            for column in df.columns[1:]:
                minimum_tolerance = min_tol.get(column, common_tol)
                if minimum_tolerance is None:
                    continue
                seria = group[column].astype(str).str.replace(',', '.') if group[column].dtype == 'object' else group[column]
                measurements = pd.to_numeric(seria, errors='coerce').dropna()
                if not measurements.empty:
                    valid_characteristics.append((column, measurements, minimum_tolerance))
            chunk_size = 5
            for i in range(0, len(valid_characteristics), chunk_size):
                chunk = valid_characteristics[i:i + chunk_size]
                returned_outliers = reporter.plot_reference_grid_page(pdf, chunk, characteristics_path, ref_id)
                if returned_outliers:
                    all_outliers.extend(returned_outliers)
        reporter.add_outliers_table_page(pdf, all_outliers)
        reporter.add_full_page_img(pdf, end_slide_path)
        
if __name__ == "__main__":
    main()