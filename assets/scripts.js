// Professional Helm Repository JavaScript

// Chart data configuration
const chartConfig = {
    'helper-operator': {
        icon: 'fas fa-cogs',
        category: 'helper',
        description: 'Meta-chart for installing operators with standardized configuration',
        tags: ['helper', 'operator', 'automation'],
        version: '1.0.28'
    },
    'helper-status-checker': {
        icon: 'fas fa-heartbeat',
        category: 'helper',
        description: 'Automated health checking and status validation for deployments',
        tags: ['helper', 'monitoring', 'health'],
        version: '4.0.13'
    },
    'helper-objectstore': {
        icon: 'fas fa-database',
        category: 'helper',
        description: 'Backup utilities and object storage automation',
        tags: ['helper', 'backup', 'storage'],
        version: '1.0.0'
    },
    'etcd-backup': {
        icon: 'fas fa-save',
        category: 'helper',
        description: 'Automated etcd cluster backup with scheduling',
        tags: ['helper', 'etcd', 'backup'],
        version: '1.0.0'
    },
    'setup-rh-keycloak': {
        icon: 'fas fa-key',
        category: 'setup',
        description: 'Red Hat Build of Keycloak with SSO and realm configuration',
        tags: ['setup', 'red-hat', 'keycloak', 'sso'],
        version: '1.0.0'
    },
    'setup-rh-developer-hub': {
        icon: 'fas fa-tools',
        category: 'setup',
        description: 'Red Hat Developer Hub (Backstage) with AI Assistant integration',
        tags: ['setup', 'red-hat', 'backstage', 'ai'],
        version: '1.0.0'
    },
    'setup-app-openshift-ai-asistant': {
        icon: 'fas fa-robot',
        category: 'setup',
        description: 'AI-powered assistant with OpenShift AI and RAG architecture',
        tags: ['setup', 'openshift', 'ai', 'assistant'],
        version: '2.0.0'
    },
    'setup-rh-pipelines': {
        icon: 'fas fa-project-diagram',
        category: 'setup',
        description: 'Red Hat Pipelines (Tekton) for CI/CD automation',
        tags: ['setup', 'red-hat', 'pipelines', 'tekton', 'ci-cd'],
        version: '1.0.0'
    },
    'setup-rh-console': {
        icon: 'fas fa-desktop',
        category: 'setup',
        description: 'Enhanced OpenShift Console operator with customizations',
        tags: ['setup', 'red-hat', 'console', 'ui', 'web-console'],
        version: '1.0.0'
    },
    'setup-platform-bookstack': {
        icon: 'fas fa-book',
        category: 'setup',
        description: 'Corporate documentation platform with backup integration',
        tags: ['setup', 'platform', 'documentation'],
        version: '1.0.0'
    },
    'setup-platform-gitea': {
        icon: 'fab fa-git-alt',
        category: 'setup',
        description: 'Git server with CI/CD and Keycloak integration',
        tags: ['setup', 'platform', 'git', 'ci-cd'],
        version: '1.1.0'
    },
    'demojam-platform': {
        icon: 'fas fa-layer-group',
        category: 'platform',
        description: 'Complete DemoJam platform - entire stack deployment',
        tags: ['platform', 'meta-chart', 'complete'],
        version: '1.0.0'
    }
};

// Create chart card HTML
function createChartCard(name, data) {
    const installName = name.replace(/^(setup-|helper-)/, '');
    
    return `
        <div class="chart-card category-${data.category}" data-name="${name}" data-tags="${data.tags.join(' ')}">
            <div class="chart-header">
                <i class="${data.icon} chart-icon"></i>
                <div>
                    <div class="chart-title">${name}</div>
                    <span class="chart-version">v${data.version}</span>
                </div>
            </div>
            <div class="chart-description">${data.description}</div>
            <div class="chart-tags">
                ${data.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
            </div>
            <div class="chart-install">
                <button class="copy-btn" onclick="copyToClipboard(this)">
                    <i class="fas fa-copy"></i>
                </button>
                helm install ${installName} demojam/${name}
            </div>
        </div>
    `;
}

// Render charts with search filtering
function renderCharts() {
    const container = document.getElementById('charts-grid');
    const searchTerm = document.getElementById('search').value.toLowerCase();
    
    let html = '';
    let visibleCount = 0;
    
    Object.entries(chartConfig).forEach(([name, data]) => {
        const searchContent = `${name} ${data.description} ${data.tags.join(' ')}`.toLowerCase();
        if (searchContent.includes(searchTerm)) {
            html += createChartCard(name, data);
            visibleCount++;
        }
    });
    
    container.innerHTML = html;
    document.getElementById('visible-count').textContent = visibleCount;
    document.getElementById('total-count').textContent = Object.keys(chartConfig).length;
}

// Copy to clipboard functionality
function copyToClipboard(button) {
    const commandText = button.parentElement.textContent.replace(/Copy/g, '').trim();
    
    navigator.clipboard.writeText(commandText).then(() => {
        const originalHTML = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i> Copied!';
        button.style.background = 'rgba(16, 185, 129, 0.2)';
        button.style.borderColor = '#10b981';
        
        setTimeout(() => {
            button.innerHTML = originalHTML;
            button.style.background = '';
            button.style.borderColor = '';
        }, 2000);
    }).catch(() => {
        // Fallback for older browsers
        button.innerHTML = '<i class="fas fa-exclamation"></i> Error';
        setTimeout(() => {
            button.innerHTML = '<i class="fas fa-copy"></i>';
        }, 2000);
    });
}

// Scroll to top functionality
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    // Render charts
    renderCharts();
    
    // Search functionality
    document.getElementById('search').addEventListener('input', renderCharts);
    
    // Scroll to top button
    const scrollButton = document.createElement('button');
    scrollButton.innerHTML = '<i class="fas fa-chevron-up"></i>';
    scrollButton.className = 'scroll-top';
    scrollButton.onclick = scrollToTop;
    scrollButton.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: var(--secondary);
        color: white;
        border: none;
        border-radius: 50%;
        width: 55px;
        height: 55px;
        font-size: 1.2rem;
        cursor: pointer;
        box-shadow: var(--shadow-lg);
        transition: all 0.3s ease;
        opacity: 0;
        pointer-events: none;
        z-index: 1000;
    `;
    
    document.body.appendChild(scrollButton);
    
    // Show/hide scroll button
    window.addEventListener('scroll', () => {
        if (window.scrollY > 500) {
            scrollButton.style.opacity = '1';
            scrollButton.style.pointerEvents = 'auto';
        } else {
            scrollButton.style.opacity = '0';
            scrollButton.style.pointerEvents = 'none';
        }
    });
    
    // Add loading animation to cards
    const cards = document.querySelectorAll('.chart-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.style.animation = 'fadeInUp 0.6s ease-out forwards';
    });
});

// CSS for animations (injected)
const animationStyles = document.createElement('style');
animationStyles.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .chart-card {
        opacity: 0;
    }
`;
document.head.appendChild(animationStyles);