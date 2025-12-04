import matplotlib.pyplot as plt
import numpy as np

tfidf_data = {
    'Friendship & Relationships': {
        'special': 11.78, 'gonna': 10.99, 'scootaloo': 10.75, 
        'student': 8.32, 'sparkle': 8.32, 'my': 8.02, 
        'yeah': 7.69, 'dresses': 7.69, 'might': 7.62, 'twilight': 7.48
    },
    'Identity & Personal Growth': {
        'cutie': 16.64, 'marks': 10.99, 'mark': 10.4, 
        'games': 7.17, 'stuff': 6.59, 'certainly': 5.49, 
        'went': 5.38, 'guy': 5.38, 'either': 5.38, 'recreate': 5.38
    },
    'Authority & Leadership': {
        'discord': 9.7, 'alone': 6.59, 'cadance': 5.55, 
        'harmony': 5.49, 'apologize': 5.38, 'will': 5.29, 
        'them': 5.27, 'ponies': 4.87, 'spike': 4.85, 'sparkle': 4.85
    },
    'History, Lore, & Magic': {
        'harmony': 10.99, 'elements': 9.01, 'discord': 9.01, 
        'has': 8.11, 'spell': 7.69, 'alicorn': 7.17, 
        'book': 7.17, 'dragon': 7.17, 'magic': 6.2, 'crystal': 5.49
    },
    'Nature & Animals': {
        'philomena': 6.59, 'ogres': 5.38, 'oubliettes': 5.38, 
        'phoenix': 4.39, 'ho': 3.58, 'angel': 3.58, 
        'creature': 3.3, 'trees': 2.2, 'sight': 2.2, 'bird': 2.2
    },
    'Food & Drink': {
        'cake': 8.96, 'tea': 5.27, 'delicious': 3.58, 
        'sugarcube': 3.58, 'punch': 3.58, 'green': 2.2, 
        'hungry': 2.2, 'weekend': 2.2, 'needed': 2.2, 'gonna': 2.2
    }
}

fig, axes = plt.subplots(3, 2, figsize=(14, 12))
fig.suptitle('', fontsize=18, fontweight='bold', y=0.995)

topics = list(tfidf_data.keys())
colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']

for idx, (ax, topic) in enumerate(zip(axes.flatten(), topics)):
    words = list(tfidf_data[topic].keys())
    scores = list(tfidf_data[topic].values())
    
    sorted_pairs = sorted(zip(words, scores), key=lambda x: x[1], reverse=True)
    words_sorted = [pair[0] for pair in sorted_pairs]
    scores_sorted = [pair[1] for pair in sorted_pairs]
    
    y_pos = np.arange(len(words_sorted))
    bars = ax.barh(y_pos, scores_sorted, color=colors[idx], alpha=0.8)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(words_sorted, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel('TF-IDF Score', fontsize=10)
    ax.set_title(topic, fontsize=12, fontweight='bold', pad=10)
    
    for i, (bar, score) in enumerate(zip(bars, scores_sorted)):
        width = bar.get_width()
        ax.text(width + 0.2, bar.get_y() + bar.get_height()/2, 
                f'{score:.2f}', ha='left', va='center', fontsize=9)
    
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig('tfidf_top_words.png', dpi=300, bbox_inches='tight')
plt.show()