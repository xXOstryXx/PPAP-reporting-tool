import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats import norm
import numpy as np
from matplotlib.ticker import MaxNLocator, FormatStrFormatter
import os

import calculator


def get_existing_image(base_dir, name):
    if not base_dir:
        if os.path.exists(name): return name
        return None
    img_png = os.path.join(base_dir, f"{name}.png")
    img_jpg = os.path.join(base_dir, f"{name}.jpg")
    if os.path.exists(img_png): return img_png
    if os.path.exists(img_jpg): return img_jpg
    return None

#Tworzy stronę (siatka 2x3) przygotowana do przystosowanie danych do raportu .pdf
def plot_reference_grid_page(pdf, chunk, characteristics_path,ref_id):
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(16, 9))
    axes_flat = axes.flatten()
    chart_iter = iter(chunk)
    image_slot_index = 1 
    grid_outliers= []
    for idx in range(6):
        ax = axes_flat[idx]
        if idx == image_slot_index:
            image_path = get_existing_image(characteristics_path, ref_id)
            if image_path:
                img_wymiary = mpimg.imread(image_path)
                ax.imshow(img_wymiary)
            ax.axis('off')
            ax.set_title(f"Technical Drawing:", fontsize=8, fontweight='bold', color='#2c3e50')
        else:
            try:
                column, measurements, minimum_tolerance = next(chart_iter)
                cleaned_data, outliers = calculator.remove_outliers(measurements, minimum_tolerance)
                if not outliers.empty:
                    for val in outliers:
                        dev=val-minimum_tolerance
                        grid_outliers.append([ref_id,column,f"{val:.3f}",f"{minimum_tolerance:.3f}",f"{dev:.3f}"])
                stats = calculator.calculate_statistics(measurements, minimum_tolerance, cleaned_data)
                y_vals = measurements.tolist()
                x_axis = np.arange(1, stats['n'] + 1)
                under_tol_list = stats['under_tol_mask'].tolist()
                ax.plot(x_axis, y_vals, marker='o', linestyle='', color='blue', alpha=0.7, label="Measurements results")
                ax.axhline(stats['tol_val'], color="black", linestyle='-', linewidth=1.2, label=f"Min. tol ({stats['tol_val']})")
                ax.axhline(stats['mean'], color='#2ecc71', linestyle='-', linewidth=2, label=f"Mean = {stats['mean']:.3f}")
                if stats['number_under_tol'] > 0:
                    x_under = [x_axis[k] for k, val in enumerate(under_tol_list) if val]
                    y_under = measurements[stats['under_tol_mask']].tolist()
                    ax.plot(x_under, y_under, marker='o', linestyle='', color='red', label='Outside tolerance')
                    for x, y in zip(x_under, y_under):
                        ax.annotate(
                            f"{y:.3f}", 
                            (x, y), 
                            textcoords="offset points", 
                            xytext=(3, 3), 
                            ha='left', 
                            va='bottom',
                            fontsize=7, 
                            color='red', 
                        )
                title = (
                    f"Char: {column} | N: {stats['n']} | Out: {stats['number_under_tol']} ({stats['percentage_under_tol']:.1f}%)\n"
                    f"Mean: {stats['mean']:.3f} | Min: {stats['min']:.3f} | Max: {stats['max']:.3f} | Std Dev: {stats['std']:.3f}"
                )
                title_color = '#e74c3c' if stats['number_under_tol'] > 0 else '#2c3e50'
                ax.set_title(title, fontsize=7, pad=4, color=title_color)
                ax.set_xlabel('N', fontsize=7)
                ax.set_ylabel('Value', fontsize=7)
                ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
                ax.tick_params(axis='both', labelsize=6)
                ax.legend(loc='upper right', fontsize=5)
                ymin, ymax = ax.get_ylim()
                ax.set_ylim(min(ymin, stats['tol_val'] - (stats['tol_val'] * 0.05)), 
                            max(ymax, stats['tol_val'] + (stats['tol_val'] * 0.05)))           
            except StopIteration:
                ax.axis('off')
    plt.tight_layout()
    pdf.savefig(fig)
    plt.close(fig)
    return grid_outliers

#Tworzy histogram dla pełnych danych do łatwości zrzucania 
def plot_histogram_page(pdf,column,measurements,minimum_tolerance):
    stats=calculator.calculate_statistics(measurements,minimum_tolerance)
    y_vals=measurements.tolist()
    fig,ax =plt.subplots(figsize=(10,6))
    _,bins_edges,patches=ax.hist(y_vals,bins='auto',color='lightgreen',edgecolor='black',alpha=0.7,label = 'Measurements')
    ax.axvline(stats['tol_val'],color='black',linestyle='--',linewidth=2,label=f'Min. tolerance = {minimum_tolerance}')
    bin_width = bins_edges[1] - bins_edges[0]
    if stats['std']>0:
        xmin,xmax =ax.get_xlim()
        x_axis_curve = np.linspace(xmin,xmax,200)
        p=norm.pdf(x_axis_curve,stats['mean'],stats['std'])*stats['n']*bin_width
        ax.plot(x_axis_curve,p,'k-',linewidth=2.5,label="Normal dist. (scaled to n)")  
    for patch, left_edge in zip(patches, bins_edges[:-1]):
        if left_edge < stats['tol_val']:
            patch.set_facecolor('red')   
    title = (
        f"Characteristic: {column}\n"
        f"N: {stats['n']} | Out of bounds: {stats['number_under_tol']} ({stats['percentage_under_tol']:.1f}%)\n"
        f"Mean: {stats['mean']:.3f} | Min: {stats['min']:.3f} | Max: {stats['max']:.3f} | Std Dev: {stats['std']:.3f}"
    )
    title_color = 'red' if stats['number_under_tol'] > 0 else 'black'
    ax.set_title(title, fontsize=12, pad=15, color=title_color)
    ax.set_xlabel('Measured value')
    ax.set_ylabel('Measurements amount')
    ax.legend(loc='upper right', bbox_to_anchor=(1, 1))
    target_char_img = get_existing_image('Measurements', column)
    if target_char_img:
        try:
            img_char = mpimg.imread(target_char_img)
            ax_inset = ax.inset_axes([0.68, 0.45, 0.3, 0.3]) 
            ax_inset.imshow(img_char)
            ax_inset.axis('off')
        except Exception as e:
            print(f"Nie udało się wkleić miniatury dla charakterystyki {column}: {e}")  
    plt.tight_layout()
    pdf.savefig(fig)
    plt.close(fig) 
    
#tworzy tabelę outlierów i dodaje na koniec raportu, aby ułatwić analizę    
def add_outliers_table_page(pdf, outliers):
    if not outliers:
        outliers = [["-", "-", "-", "-", "-"]] 
    columns = ['Part ID', 'Characteristic', 'Measured', 'Min. Tol.', 'Deviation']
    chunk_size = 25 
    for i in range(0, len(outliers), chunk_size):
        chunk = outliers[i:i + chunk_size]
        fig, ax = plt.subplots(figsize=(11.69, 8.27))
        ax.axis('off')
        title = "Outliers summary" if i == 0 else "Summary continuation"
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        row_height = 0.04
        row_number = len(chunk)+1
        total_height = row_number*row_height
        y_start = 1.0 - total_height
        bbox_final = [0, y_start, 1, total_height]
        table = ax.table(cellText=chunk, colLabels=columns, loc='top', cellLoc='center',bbox = bbox_final)
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.8) 
        for (row, col), cell in table.get_celld().items():
            if row == 0:
                cell.set_text_props(weight='bold', color='white')
                cell.set_facecolor('aqua')
            elif row % 2 == 0:
                cell.set_facecolor('white')

        pdf.savefig(fig)
        plt.close(fig)
        
        
#Dodaje pełne zdjęcie na stronę (tytułowa/rysunek/końcowa)
def add_full_page_img(pdf,image_path):
    if not image_path or not os.path.exists(image_path):
        return
    img_data = mpimg.imread(image_path)
    fig,ax=plt.subplots(figsize=(11.69,8.27))
    ax.set_position([0,0,1,1])
    ax.imshow(img_data)
    ax.axis('off')
    pdf.savefig(fig,bbox_inches='tight',pad_inches=0)
    plt.close(fig)

##Dodaje stronę tytułową    
def add_titled_image_page(pdf,image_path,title):
    if not image_path or not os.path.exists(image_path):
        return
    try:
        img_data = mpimg.imread(image_path)
        fig=plt.figure(figsize=(10,6))
        fig.text(0.5,0.92,title,ha='center',va='center',fontsize=13,fontweight='bold')
        ax=fig.add_axes([0.1,0.1,0.8,0.75])
        ax.imshow(img_data)
        ax.axis('off')
        pdf.savefig(fig,bbox_inches='tight',pad_inches=0)
        plt.close(fig)
    except Exception as e:
        print(f"Błąd wczytywania zdjęcia ({title}): {e}")