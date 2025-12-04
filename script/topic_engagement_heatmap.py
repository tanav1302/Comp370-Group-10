import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

data = {
    'Character': ['Discord', 'Discord', 'Discord', 'Discord', 'Discord', 'Discord',
                  'Princess Celestia', 'Princess Celestia', 'Princess Celestia', 
                  'Princess Celestia', 'Princess Celestia', 'Princess Celestia',
                  'Sweetie Belle', 'Sweetie Belle', 'Sweetie Belle', 
                  'Sweetie Belle', 'Sweetie Belle', 'Sweetie Belle'],
    'Topic': ['Friendship & Relationships', 'Identity & Personal Growth', 
              'Authority & Leadership', 'History, Lore, & Magic', 
              'Nature & Animals', 'Food & Drink',
              'Friendship & Relationships', 'Identity & Personal Growth', 
              'Authority & Leadership', 'History, Lore, & Magic', 
              'Nature & Animals', 'Food & Drink',
              'Friendship & Relationships', 'Identity & Personal Growth', 
              'Authority & Leadership', 'History, Lore, & Magic', 
              'Nature & Animals', 'Food & Drink'],
    'Percentage': [28.57, 34.74, 8.12, 15.91, 4.55, 8.12,
                   36.3, 8.25, 39.93, 25.08, 4.62, 2.64,
                   61.13, 26.33, 1.25, 5.02, 3.45, 2.82]
}

df = pd.DataFrame(data)

heatmap_data = df.pivot(index='Topic', columns='Character', values='Percentage')

topic_order = ['Friendship & Relationships', 'Identity & Personal Growth', 
               'Authority & Leadership', 'History, Lore, & Magic', 
               'Nature & Animals', 'Food & Drink']
heatmap_data = heatmap_data.reindex(topic_order)

character_order = ['Princess Celestia', 'Discord', 'Sweetie Belle']
heatmap_data = heatmap_data[character_order]

plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='YlOrRd', 
            cbar_kws={'label': 'Percentage (%)'}, linewidths=0.5, linecolor='white')

plt.title('', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Character', fontsize=12, fontweight='bold')
plt.ylabel('Topic', fontsize=12, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()

plt.savefig('topic_engagement_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()