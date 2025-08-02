/**
 * Port Authority Application Registry JavaScript
 * Handles application interactions, clipboard operations, and UI feedback
 */

// Main application object to avoid global namespace pollution
const PortAuthority = {

    /**
     * Opens an application in a new tab
     * @param {string} fullAddress - The complete URL to open
     * @param {string} displayName - Display name for notifications
     */
    openApplication: function (fullAddress, displayName) {
        try {
            // Validate URL before opening
            if (!this.isValidUrl(fullAddress)) {
                this.showNotification('Invalid URL format', 'error');
                return;
            }

            // Open in new tab (using _blank target without window features)
            const newTab = window.open(fullAddress, '_blank');

            // Focus the new tab if it was successfully opened
            if (newTab) {
                newTab.focus();

                // Show success notification
                this.showNotification(`Opening ${displayName}...`, 'success');
            } else {
                // Fallback if popup was blocked
                this.showNotification('Pop-up blocked. Please allow pop-ups for this site.', 'warning');
            }
        } catch (error) {
            console.error('Error opening application:', error);
            this.showNotification('Error opening application. Please try again.', 'error');
        }
    },

    /**
     * Validates if a URL is safe to open
     * @param {string} url - URL to validate
     * @return {boolean} - Whether URL is safe
     */
    isValidUrl: function (url) {
        try {
            const urlObj = new URL(url);
            // Only allow http and https protocols
            return ['http:', 'https:'].includes(urlObj.protocol);
        } catch (error) {
            console.error('Invalid URL:', error);
            return false;
        }
    },

    /**
     * Copies text to clipboard using modern API with fallback
     * @param {string} text - Text to copy to clipboard
     */
    copyToClipboard: function (text) {
        try {
            if (navigator.clipboard && window.isSecureContext) {
                // Use modern clipboard API if available
                navigator.clipboard.writeText(text).then(() => {
                    this.showNotification('Address copied to clipboard!', 'success');
                }).catch((error) => {
                    console.error('Error copying to clipboard:', error);
                    this.fallbackCopyToClipboard(text);
                });
            } else {
                // Fallback for older browsers or non-secure contexts
                this.fallbackCopyToClipboard(text);
            }
        } catch (error) {
            console.error('Error copying to clipboard:', error);
            this.showNotification('Failed to copy to clipboard', 'error');
        }
    },

    /**
     * Fallback clipboard method for older browsers
     * @param {string} text - Text to copy to clipboard
     */
    fallbackCopyToClipboard: function (text) {
        try {
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.opacity = '0';
            textArea.style.left = '-9999px';
            textArea.style.top = '-9999px';

            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();

            const successful = document.execCommand('copy');
            document.body.removeChild(textArea);

            if (successful) {
                this.showNotification('Address copied to clipboard!', 'success');
            } else {
                this.showNotification('Failed to copy to clipboard', 'error');
            }
        } catch (error) {
            console.error('Fallback copy failed:', error);
            this.showNotification('Copy not supported in this browser', 'warning');
        }
    },

    /**
     * Shows a notification message to the user
     * @param {string} message - Message to display
     * @param {string} type - Type of notification (success, warning, error, info)
     */
    showNotification: function (message, type = 'info') {
        // Remove any existing notifications first
        const existingNotifications = document.querySelectorAll('.pa-notification');
        existingNotifications.forEach(notification => {
            notification.remove();
        });

        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'pa-notification';
        notification.textContent = message;

        // Set base styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 6px;
            color: white;
            font-weight: 500;
            font-size: 14px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            z-index: 1000;
            max-width: 320px;
            word-wrap: break-word;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transform: translateX(100%);
            transition: transform 0.3s ease-out;
            cursor: pointer;
        `;

        // Set background color based on type
        const colors = {
            success: '#27ae60',
            warning: '#f39c12',
            error: '#e74c3c',
            info: '#3498db'
        };

        notification.style.backgroundColor = colors[type] || colors.info;

        // Add click to dismiss
        notification.addEventListener('click', () => {
            this.dismissNotification(notification);
        });

        // Add to page
        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Auto-dismiss after delay
        const dismissDelay = type === 'error' ? 5000 : 3000;
        setTimeout(() => {
            this.dismissNotification(notification);
        }, dismissDelay);
    },

    /**
     * Dismisses a notification with animation
     * @param {HTMLElement} notification - Notification element to dismiss
     */
    dismissNotification: function (notification) {
        if (notification && notification.parentNode) {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }
    },

    /**
     * Initializes keyboard shortcuts and other event listeners
     */
    initializeEventListeners: function () {
        // Keyboard shortcuts
        document.addEventListener('keydown', (event) => {
            // Ctrl/Cmd + G to focus first "Go To" button
            if ((event.ctrlKey || event.metaKey) && event.key === 'g') {
                event.preventDefault();
                const firstGoButton = document.querySelector('.btn-primary:not(.btn-disabled)');
                if (firstGoButton) {
                    firstGoButton.focus();
                    this.showNotification('Focused on first available "Go To" button', 'info');
                }
            }

            // Ctrl/Cmd + C when focused on a card to copy its address
            if ((event.ctrlKey || event.metaKey) && event.key === 'c') {
                const focusedElement = document.activeElement;
                const card = focusedElement.closest('.application-card');
                if (card) {
                    const copyButton = card.querySelector('.btn-secondary');
                    if (copyButton && !event.defaultPrevented) {
                        event.preventDefault();
                        copyButton.click();
                    }
                }
            }

            // Escape to dismiss notifications
            if (event.key === 'Escape') {
                const notifications = document.querySelectorAll('.pa-notification');
                notifications.forEach(notification => {
                    this.dismissNotification(notification);
                });
            }
        });

        // Add focus management for application cards
        this.initializeCardFocus();

        // Add loading state management
        this.initializeLoadingStates();
    },

    /**
     * Initializes focus management for application cards
     */
    initializeCardFocus: function () {
        const cards = document.querySelectorAll('.application-card');
        cards.forEach((card, index) => {
            // Make cards focusable
            if (!card.hasAttribute('tabindex')) {
                card.setAttribute('tabindex', '0');
            }

            // Add keyboard navigation
            card.addEventListener('keydown', (event) => {
                switch (event.key) {
                    case 'Enter':
                    case ' ':
                        event.preventDefault();
                        const goButton = card.querySelector('.btn-primary:not(.btn-disabled)');
                        if (goButton) {
                            goButton.click();
                        }
                        break;

                    case 'ArrowDown':
                        event.preventDefault();
                        const nextCard = cards[index + 1];
                        if (nextCard) {
                            nextCard.focus();
                        }
                        break;

                    case 'ArrowUp':
                        event.preventDefault();
                        const prevCard = cards[index - 1];
                        if (prevCard) {
                            prevCard.focus();
                        }
                        break;
                }
            });
        });
    },

    /**
     * Initializes loading states for buttons
     */
    initializeLoadingStates: function () {
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(button => {
            button.addEventListener('click', () => {
                if (!button.disabled && !button.classList.contains('btn-disabled')) {
                    this.setButtonLoading(button, true);

                    // Reset loading state after a short delay
                    setTimeout(() => {
                        this.setButtonLoading(button, false);
                    }, 1000);
                }
            });
        });
    },

    /**
     * Sets loading state for a button
     * @param {HTMLElement} button - Button element
     * @param {boolean} isLoading - Whether button is in loading state
     */
    setButtonLoading: function (button, isLoading) {
        if (isLoading) {
            button.classList.add('loading');
            button.disabled = true;
        } else {
            button.classList.remove('loading');
            button.disabled = false;
        }
    }
};

// Global function wrappers for template compatibility
function openApplication(fullAddress, displayName) {
    PortAuthority.openApplication(fullAddress, displayName);
}

function copyToClipboard(text) {
    PortAuthority.copyToClipboard(text);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
    PortAuthority.initializeEventListeners();

    // Show welcome message for empty state
    const noAppsMessage = document.querySelector('.no-applications');
    if (noAppsMessage) {
        PortAuthority.showNotification('No applications registered yet. Add some to get started!', 'info');
    }
});

// Export for module systems (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PortAuthority;
}