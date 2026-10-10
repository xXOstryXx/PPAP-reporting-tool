import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def generate_mock_technical_drawings():
    output_dir = "Characteristics" 
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Utworzono folder: {output_dir}")
        
    details = ['DETAL-A', 'DETAL-B', 'DETAL-C', 'DETAL-D']
    
    base_measurements = {
        'DETAL-A': (0.15, 0.2, 0.7, 0.5),  
        'DETAL-B': (0.25, 0.15, 0.5, 0.7),
        'DETAL-C': (0.1, 0.35, 0.8, 0.3),
        'DETAL-D': (0.2, 0.2, 0.6, 0.6)
    }

    for detal in details:
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_facecolor('#f4f6f9')
        ax.grid(color='white', linestyle='-', linewidth=1.5)
        bx, by, bw, bh = base_measurements[detal]
        cx, cy = bx + bw/2, by + bh/2
        rect = patches.Rectangle((bx, by), bw, bh, linewidth=3, edgecolor='#2c3e50', facecolor='#bdc3c7', alpha=0.5)
        ax.add_patch(rect)
        r1 = min(bw, bh) * 0.25
        circle1 = patches.Circle((cx, cy), r1, linewidth=2, edgecolor='#e74c3c', facecolor='none', linestyle='--')
        ax.add_patch(circle1)
        cx2, cy2 = bx + bw*0.85, by + bh*0.85
        r2 = min(bw, bh) * 0.1
        circle2 = patches.Circle((cx2, cy2), r2, linewidth=2, edgecolor='#2980b9', facecolor='none')
        ax.add_patch(circle2)
        # 501: 
        ax.annotate('', xy=(bx - 0.08, by), xytext=(bx - 0.08, by + bh), arrowprops=dict(arrowstyle='<|-|>', color='black', lw=1.5))
        ax.text(bx - 0.11, by + bh/2, '501', va='center', ha='right', fontsize=12, color='black', fontweight='bold', rotation=90)
        # 502:
        ax.annotate('', xy=(bx, by - 0.08), xytext=(bx + bw, by - 0.08), arrowprops=dict(arrowstyle='<|-|>', color='black', lw=1.5))
        ax.text(bx + bw/2, by - 0.12, '502', ha='center', va='top', fontsize=12, color='black', fontweight='bold')
        # 503:
        ax.annotate('', xy=(bx, by + 0.05), xytext=(cx, by + 0.05), arrowprops=dict(arrowstyle='<|-|>', color='black', lw=1))
        ax.text(bx + bw/4, by + 0.07, '503', ha='center', va='bottom', fontsize=10, fontweight='bold')
        # 504:
        ax.annotate('', xy=(bx + 0.05, by), xytext=(bx + 0.05, cy), arrowprops=dict(arrowstyle='<|-|>', color='black', lw=1))
        ax.text(bx + 0.07, by + bh/4, '504', ha='left', va='center', fontsize=10, fontweight='bold', rotation=90)
        # 505:
        ax.annotate('505', xy=(cx + r1*0.7, cy + r1*0.7), xytext=(cx + 0.15, cy + 0.15), 
                    arrowprops=dict(facecolor='black', shrink=0.01, width=1, headwidth=5), fontsize=11, fontweight='bold', color='red')
        # 506:
        ax.annotate('506', xy=(cx2 + r2*0.7, cy2 + r2*0.7), xytext=(cx2 + 0.1, cy2 + 0.1), 
                    arrowprops=dict(facecolor='black', shrink=0.01, width=1, headwidth=5), fontsize=11, fontweight='bold')
        # 507:
        ax.annotate('', xy=(bx, cy2), xytext=(cx2, cy2), arrowprops=dict(arrowstyle='<|-|>', lw=1, color='#555555'))
        ax.text(bx + (bw*0.85)/2, cy2 + 0.02, '507', ha='center', va='bottom', fontsize=10, fontweight='bold', color='#555555')
        # 508:
        ax.annotate('', xy=(cx2, by + bh), xytext=(cx2, cy2), arrowprops=dict(arrowstyle='<|-|>', lw=1, color='#555555'))
        ax.text(cx2 + 0.02, cy2 + (bh*0.15)/2, '508', ha='left', va='center', fontsize=10, fontweight='bold', color='#555555') 
        # 509:
        ax.annotate('', xy=(cx, cy), xytext=(cx2, cy2), arrowprops=dict(arrowstyle='<|-|>', lw=1, linestyle='dashed'))
        ax.text(cx + (cx2-cx)/2 - 0.02, cy + (cy2-cy)/2 + 0.02, '509', ha='right', va='bottom', fontsize=10, fontweight='bold', rotation=30)
        # 510:
        ax.annotate('510', xy=(bx + bw*0.3, by + bh), xytext=(bx + bw*0.3, by + bh + 0.1), 
                    arrowprops=dict(facecolor='black', shrink=0.01, width=1, headwidth=5), fontsize=11, fontweight='bold')

        ax.set_title(f"Technical drawing: {detal}", fontsize=14, fontweight='bold', pad=20)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        
        filepath = os.path.join(output_dir, f"{detal}.png")
        plt.savefig(filepath, dpi=150, bbox_inches='tight', pad_inches=0.1)
        plt.close()
        print(f"Wygenerowano rysunek: {filepath}")

if __name__ == "__main__":
    generate_mock_technical_drawings()