document.addEventListener('DOMContentLoaded', (event) => {
    // Get all tab buttons
    const tabs = Array.from(document.querySelectorAll('[role="tab"]'));

    // Get all tab panels
    const panels = Array.from(document.querySelectorAll('[role="tabpanel"]'));

    // Function to reset and init tabs
    const resetTabs = () => {
        tabs.forEach(tab => {
            tab.setAttribute('aria-selected', 'false');
            tab.classList.replace('border-indigo-600', 'border-transparent');
            tab.classList.replace('text-indigo-600', 'text-gray-700');
        });

        panels.forEach(panel => {
            panel.setAttribute('hidden', 'true');
        });
    };

    // Set up click event on each tab
    tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            // Reset all tabs before displaying new tab
            resetTabs();

            // Set the clicked tab as selected
            tab.setAttribute('aria-selected', 'true');
            tab.classList.replace('border-transparent', 'border-indigo-600');
            tab.classList.replace('text-gray-700', 'text-indigo-600');

            // Get the panel that this tab controls and show it
            const panelId = tab.getAttribute('aria-controls');
            document.getElementById(panelId).removeAttribute('hidden');
        });
    });

    // Init the first tab
    if (tabs.length > 0) {
        tabs[0].click();
    }
});

