export function useExport() {
    /**
     * Triggers a CSV download for the given data and columns.
     * @param {Array} data - Array of objects to export.
     * @param {Array} columns - Array of column definitions { key, label }.
     * @param {string} filename - Output filename (without extension).
     */
    const exportToCSV = (data, columns, filename = 'export') => {
        if (!data || !data.length) return;

        const headers = columns.map(col => `"${col.label}"`).join(',');
        const rows = data.map(item => {
            return columns.map(col => {
                let value = item[col.key];
                // Handle nested objects if key contains dots
                if (col.key && typeof col.key === 'string' && col.key.includes('.')) {
                    const keys = col.key.split('.');
                    value = keys.reduce((acc, curr) => (acc ? acc[curr] : ''), item);
                }

                // Escape quotes and wrap in quotes
                const escaped = String(value ?? '').replace(/"/g, '""');
                return `"${escaped}"`;
            }).join(',');
        });

        const csvContent = [headers, ...rows].join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.setAttribute('href', url);
        link.setAttribute('download', `${filename}_${new Date().getTime()}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    /**
     * Triggers a print/PDF dialog.
     * Note: Highly dependent on print-specific CSS.
     */
    const triggerPrint = () => {
        window.print();
    };

    return {
        exportToCSV,
        triggerPrint
    };
}
