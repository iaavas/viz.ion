import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib.colors import Normalize, LinearSegmentedColormap
from matplotlib.cm import ScalarMappable


nepal = gpd.read_file('./maps/nepal/province/hermes_NPL_new_wgs_1.shp')


state_hdi = {
    '1': 0.580,
    '2': 0.519,
    '3': 0.669,
    '4': 0.621,
    '5': 0.563,
    '6': 0.538,
    '7': 0.547
}
overall_avg_hdi = sum(state_hdi.values()) / len(state_hdi)


states = {
    1: "Koshi",
    2: "Madhesh",
    3: "Bagmati",
    4: "Gandaki",
    5: "Lumbini",
    6: "Karnali",
    7: "Sudurpaschim"
}


colors = [
    (1, 0.8, 1),    
    (0.9, 0.6, 0.9),
    (0.8, 0.4, 0.8),
    (0.7, 0.2, 0.7),
    (0.6, 0, 0.6),  
    (0.5, 0, 0.5)   
]


cmap = LinearSegmentedColormap.from_list('custom_cmap', colors)


norm = Normalize(vmin=min(state_hdi.values()), vmax=max(state_hdi.values()))


mapper = ScalarMappable(norm=norm, cmap=cmap)

colors = []
for state in nepal['PROVINCE']:
    hdi = state_hdi.get(str(state))
    if hdi is not None:
        
        color = mapper.to_rgba(hdi, alpha=0.5 + hdi * 0.5)  
        colors.append(color)
    else:
        colors.append('gray')  

fig, ax = plt.subplots(1, 1, figsize=(12, 8))


bg_ax = fig.add_axes(ax.get_position(), frameon=False, zorder=-1)
bg_ax.set_xlim(0, 1)
bg_ax.set_ylim(0, 1)
bg_ax.set_xticks([])
bg_ax.set_yticks([])
bg_text = '@viz.onnepal' * 20  
bg_ax.text(0.5, 0.5, bg_text, fontsize=12, color='lightgray', alpha=0.5,
            ha='center', va='center')

nepal.plot(ax=ax, color=colors, edgecolor='black')


for idx, row in nepal.iterrows():
    state_num = int(row['PROVINCE'])
    state_name = states.get(state_num, "Unknown")
    hdi = state_hdi.get(str(state_num), "N/A")
    text = f"{state_name}\nHDI: {hdi:.3f}"


    
    
    x, y = row.geometry.centroid.x, row.geometry.centroid.y
    text_color = "black" if hdi < overall_avg_hdi else "white"
    text_size = 14
    if state_num == 3 or state_num == 4 or state_num == 6 or state_num == 1 or state_num == 7:
        ax.text(x, y, text, fontsize=text_size, ha='center', va='center', color=text_color, fontweight='bold')
    elif state_num == 5:
        ax.text(x, y - 0.1, text, fontsize=text_size, ha='center', va='center', color=text_color, fontweight='bold')
    elif state_num == 2:
        ax.text(x, y - 0.6, text, fontsize=text_size, ha='center', va='center', color=text_color, fontweight='bold')

ax.axis('off')


cax = fig.add_axes([0.75, 0.8, 0.2, 0.03])  
cax.text(0.5, 4.7, 'HDI Distribution Across ', transform=cax.transAxes,
               ha='center', va='center', fontsize=20, fontweight='bold',fontname='Helvetica')
cax.text(0.5, 3.2, 'Provinces ', transform=cax.transAxes,
               ha='center', va='center', fontsize=20, fontweight='bold',fontname='Helvetica')
cbar = plt.colorbar(mapper, cax=cax, orientation='horizontal')
cbar.ax.xaxis.set_ticks_position('top')


cbar.set_label('HDI', fontsize=10, fontweight='bold')


ax.text(0.93, 0.64, f"ALL NEPAL AVG", transform=ax.transAxes, ha='right', va='top', fontsize=20, fontweight='bold')
ax.text(0.88, 0.6, f"{overall_avg_hdi:.3f}", transform=ax.transAxes, ha='right', va='top', fontsize=32,color="gold", fontweight='bold')

ax.text(0.02, 0.02, "@viz.onnepal", transform=ax.transAxes, ha='left', va='bottom', fontsize=12, fontweight='bold')
for text in ax.texts:
    text.set_fontfamily('Helvetica')

plt.tight_layout()
plt.savefig("./output/nepal_hdi_insta.png", dpi=300)  
plt.show()
