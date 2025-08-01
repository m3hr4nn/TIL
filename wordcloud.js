// Add this script to your existing index.html
function generateWordCloud() {
    // Extract categories from existing links
    const links = document.querySelectorAll('.posts a');
    const categories = {};
    
    links.forEach(link => {
        const href = link.getAttribute('href');
        if (href && href.includes('/')) {
            // Extract category from URL pattern like: /category/filename.md
            const match = href.match(/\/([^\/]+)\/[^\/]+\.md$/);
            if (match) {
                const category = match[1];
                categories[category] = (categories[category] || 0) + 1;
            }
        }
    });
    
    console.log('Found categories:', categories);
    
    // Create or find word cloud container
    let container = document.getElementById('wordcloud-container');
    if (!container) {
        // Create word cloud container if it doesn't exist
        const header = document.querySelector('header');
        const wordcloudDiv = document.createElement('div');
        wordcloudDiv.className = 'wordcloud css-wordcloud';
        wordcloudDiv.innerHTML = '<div class="cloud-container" id="wordcloud-container"></div>';
        header.appendChild(wordcloudDiv);
        container = document.getElementById('wordcloud-container');
    }
    
    if (Object.keys(categories).length === 0) {
        container.innerHTML = '<div style="color: #fef3c7; padding: 1rem;">📚 Categories will appear as you add posts</div>';
        return;
    }
    
    // Generate word cloud
    const maxCount = Math.max(...Object.values(categories));
    const wordElements = Object.entries(categories).map(([category, count]) => {
        const fontSize = 16 + (count / maxCount) * 16;
        const opacity = 0.8 + (count / maxCount) * 0.2;
        return `<span class="cloud-word" style="font-size: ${fontSize}px; opacity: ${opacity}; color: #fbbf24; font-weight: 700; padding: 0.6rem 1.2rem; margin: 0.3rem; border-radius: 30px; background: rgba(251, 191, 36, 0.15); border: 2px solid rgba(251, 191, 36, 0.4); display: inline-block; transition: all 0.3s ease;">${category}</span>`;
    });
    
    // Shuffle for better visual distribution
    wordElements.sort(() => Math.random() - 0.5);
    
    container.innerHTML = wordElements.join('');
    
    // Add hover effects
    container.querySelectorAll('.cloud-word').forEach(word => {
        word.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px) scale(1.08)';
            this.style.background = 'rgba(251, 191, 36, 0.25)';
            this.style.color = '#ffffff';
            this.style.boxShadow = '0 8px 25px rgba(251, 191, 36, 0.4)';
        });
        
        word.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.background = 'rgba(251, 191, 36, 0.15)';
            this.style.color = '#fbbf24';
            this.style.boxShadow = '';
        });
    });
}

// Run when page loads
document.addEventListener('DOMContentLoaded', generateWordCloud);

// Also run after a short delay in case content loads dynamically
setTimeout(generateWordCloud, 1000);
