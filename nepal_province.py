import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib.colors import Normalize, LinearSegmentedColormap
from matplotlib.cm import ScalarMappable
import pandas as pd

class ProvincePlotter:
    def __init__(self, hdi_data_path, shapefile_path):
        self.df = pd.read_csv(hdi_data_path)
        self.nepal = gpd.read_file(shapefile_path)

    def generate_colors(self):
        cmap = LinearSegmentedColormap.from_list('custom_cmap', [
            (1, 0.8, 1),    
            (0.9, 0.6, 0.9),
            (0.8, 0.4, 0.8),
            (0.7, 0.2, 0.7),
            (0.6, 0, 0.6),  
            (0.5, 0, 0.5)   
        ])
        norm = Normalize(vmin=min(self.df['HDI']), vmax=max(self.df['HDI']))
        mapper = ScalarMappable(norm=norm, cmap=cmap)
        
        colors = []
        for state in self.nepal['PROVINCE']:
            hdi = self.df[self.df['Province']==state]['HDI'].values[0]
            if hdi is not None:
                color = mapper.to_rgba(hdi, alpha=0.5 + hdi * 0.5)
                colors.append(color)
            else:
                colors.append('gray')
        return colors, mapper

    def plot(self, output_path):
        colors, mapper = self.generate_colors()
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        self.nepal.plot(ax=ax, color=colors, edgecolor='black')

        for idx, row in self.nepal.iterrows():
            state_num = int(row['PROVINCE'])
            state_name = self.df[self.df['Province']==state_num]['Pname'].values[0]
            hdi = self.df[self.df['Province']==state_num]['HDI'].values[0]
            print(state_name,state_num)
            text = f"{state_name}\nHDI: {hdi}"

            x, y = row.geometry.centroid.x, row.geometry.centroid.y
            text_color = "black" if hdi < self.df['HDI'].mean() else "white"
            text_size = 14
            if state_num in [3, 4, 6, 1, 7]:
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
        ax.text(0.88, 0.6, f"{self.df['HDI'].mean():.3f}", transform=ax.transAxes, ha='right', va='top', fontsize=32,color="gold", fontweight='bold')

        ax.text(0.02, 0.02, "@viz.onnepal", transform=ax.transAxes, ha='left', va='bottom', fontsize=12, fontweight='bold')
        for text in ax.texts:
            text.set_fontfamily('Helvetica')

        plt.tight_layout()
        plt.savefig(output_path, dpi=300)  
        plt.show()

if __name__ == "__main__":
    plotter = ProvincePlotter('./data/province_hdi.csv', './maps/nepal/province/hermes_NPL_new_wgs_1.shp')
    
    plotter.plot( "./output/nepal_hdi_insta.png")
