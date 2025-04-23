/**
 * DiabetesPredict - Chart.js Visualization Functions
 * This file contains helper functions for creating and managing data visualizations
 */

// Define color schemes for consistent styling
const chartColors = {
    primary: 'rgba(13, 110, 253, 0.7)',
    secondary: 'rgba(108, 117, 125, 0.7)',
    success: 'rgba(25, 135, 84, 0.7)',
    danger: 'rgba(220, 53, 69, 0.7)',
    warning: 'rgba(255, 193, 7, 0.7)',
    info: 'rgba(13, 202, 240, 0.7)',
    light: 'rgba(248, 249, 250, 0.7)',
    dark: 'rgba(33, 37, 41, 0.7)',
    // Additional colors for charts with many categories
    colors: [
        'rgba(75, 192, 192, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(153, 102, 255, 0.7)',
        'rgba(255, 159, 64, 0.7)',
        'rgba(255, 99, 132, 0.7)',
        'rgba(201, 203, 207, 0.7)',
        'rgba(255, 205, 86, 0.7)',
        'rgba(59, 130, 246, 0.7)'
    ]
};

// Common chart options for consistent styling
const commonChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: {
                color: 'rgba(255, 255, 255, 0.7)'
            }
        },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            titleColor: 'rgba(255, 255, 255, 0.9)',
            bodyColor: 'rgba(255, 255, 255, 0.9)',
            borderColor: 'rgba(255, 255, 255, 0.1)',
            borderWidth: 1
        }
    },
    scales: {
        x: {
            ticks: {
                color: 'rgba(255, 255, 255, 0.7)'
            },
            grid: {
                color: 'rgba(255, 255, 255, 0.1)'
            }
        },
        y: {
            ticks: {
                color: 'rgba(255, 255, 255, 0.7)'
            },
            grid: {
                color: 'rgba(255, 255, 255, 0.1)'
            }
        }
    }
};

/**
 * Creates a bar chart for feature importance visualization
 * @param {string} canvasId - The ID of the canvas element
 * @param {Object} featureImportance - Object with feature names as keys and importance values as values
 * @param {Object} options - Additional chart options
 * @returns {Chart} The created Chart.js instance
 */
function createFeatureImportanceChart(canvasId, featureImportance, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) {
        console.error(`Canvas element with ID "${canvasId}" not found`);
        return null;
    }

    const ctx = canvas.getContext('2d');
    
    // Sort features by importance (highest first)
    const sortedFeatures = Object.entries(featureImportance)
        .sort((a, b) => b[1] - a[1]);
    
    const features = sortedFeatures.map(item => item[0]);
    const values = sortedFeatures.map(item => item[1]);
    
    // Create chart configuration
    const chartConfig = {
        type: 'bar',
        data: {
            labels: features,
            datasets: [{
                label: 'Feature Importance',
                data: values,
                backgroundColor: chartColors.colors.slice(0, features.length),
                borderColor: chartColors.colors.map(color => color.replace('0.7', '1')),
                borderWidth: 1
            }]
        },
        options: {
            ...commonChartOptions,
            indexAxis: 'y',
            plugins: {
                ...commonChartOptions.plugins,
                legend: {
                    display: false
                },
                tooltip: {
                    ...commonChartOptions.plugins.tooltip,
                    callbacks: {
                        label: function(context) {
                            return `Importance: ${context.raw.toFixed(3)}`;
                        }
                    }
                }
            },
            ...options
        }
    };
    
    return new Chart(ctx, chartConfig);
}

/**
 * Creates a radar chart for comparing user data with normal ranges
 * @param {string} canvasId - The ID of the canvas element
 * @param {Object} userData - User's health metrics
 * @param {Object} normalRanges - Normal/healthy ranges for comparison
 * @returns {Chart} The created Chart.js instance
 */
function createHealthRadarChart(canvasId, userData, normalRanges) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) {
        console.error(`Canvas element with ID "${canvasId}" not found`);
        return null;
    }

    const ctx = canvas.getContext('2d');
    
    // Prepare data structure
    const labels = Object.keys(userData);
    const userValues = Object.values(userData);
    const normalValues = labels.map(label => normalRanges[label] || 0);
    
    // Create chart configuration
    const chartConfig = {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Your Values',
                    data: userValues,
                    backgroundColor: chartColors.primary,
                    borderColor: chartColors.primary.replace('0.7', '1'),
                    pointBackgroundColor: chartColors.primary.replace('0.7', '1'),
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: chartColors.primary.replace('0.7', '1')
                },
                {
                    label: 'Normal Range',
                    data: normalValues,
                    backgroundColor: chartColors.success,
                    borderColor: chartColors.success.replace('0.7', '1'),
                    pointBackgroundColor: chartColors.success.replace('0.7', '1'),
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: chartColors.success.replace('0.7', '1')
                }
            ]
        },
        options: {
            ...commonChartOptions,
            elements: {
                line: {
                    borderWidth: 2
                },
                point: {
                    radius: 4
                }
            }
        }
    };
    
    return new Chart(ctx, chartConfig);
}

/**
 * Creates a doughnut chart for diabetes risk visualization
 * @param {string} canvasId - The ID of the canvas element
 * @param {number} riskPercentage - The risk percentage (0-100)
 * @returns {Chart} The created Chart.js instance
 */
function createRiskDoughnutChart(canvasId, riskPercentage) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) {
        console.error(`Canvas element with ID "${canvasId}" not found`);
        return null;
    }

    const ctx = canvas.getContext('2d');
    
    // Determine color based on risk level
    let riskColor;
    if (riskPercentage < 30) {
        riskColor = chartColors.success;
    } else if (riskPercentage < 70) {
        riskColor = chartColors.warning;
    } else {
        riskColor = chartColors.danger;
    }
    
    // Create chart configuration
    const chartConfig = {
        type: 'doughnut',
        data: {
            labels: ['Risk', 'Safe'],
            datasets: [{
                data: [riskPercentage, 100 - riskPercentage],
                backgroundColor: [
                    riskColor,
                    'rgba(200, 200, 200, 0.2)'
                ],
                borderColor: [
                    riskColor.replace('0.7', '1'),
                    'rgba(200, 200, 200, 0.1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            cutout: '70%',
            plugins: {
                ...commonChartOptions.plugins,
                tooltip: {
                    ...commonChartOptions.plugins.tooltip,
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.raw}%`;
                        }
                    }
                }
            }
        }
    };
    
    return new Chart(ctx, chartConfig);
}

/**
 * Creates a line chart for glucose trends over time
 * @param {string} canvasId - The ID of the canvas element
 * @param {Array} dates - Array of date strings
 * @param {Array} values - Array of glucose values
 * @returns {Chart} The created Chart.js instance
 */
function createGlucoseTrendChart(canvasId, dates, values) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) {
        console.error(`Canvas element with ID "${canvasId}" not found`);
        return null;
    }

    const ctx = canvas.getContext('2d');
    
    // Create chart configuration
    const chartConfig = {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Glucose Level (mg/dL)',
                data: values,
                backgroundColor: chartColors.warning,
                borderColor: chartColors.warning.replace('0.7', '1'),
                tension: 0.2,
                fill: false
            }]
        },
        options: {
            ...commonChartOptions,
            plugins: {
                ...commonChartOptions.plugins,
                annotation: {
                    annotations: {
                        normalLine: {
                            type: 'line',
                            yMin: 70,
                            yMax: 70,
                            borderColor: 'rgba(0, 200, 0, 0.5)',
                            borderWidth: 1,
                            label: {
                                content: 'Lower Normal',
                                enabled: true,
                                position: 'left'
                            }
                        },
                        preDiabetesLine: {
                            type: 'line',
                            yMin: 100,
                            yMax: 100,
                            borderColor: 'rgba(255, 200, 0, 0.5)',
                            borderWidth: 1,
                            label: {
                                content: 'Pre-Diabetes',
                                enabled: true,
                                position: 'left'
                            }
                        },
                        diabetesLine: {
                            type: 'line',
                            yMin: 125,
                            yMax: 125,
                            borderColor: 'rgba(255, 0, 0, 0.5)',
                            borderWidth: 1,
                            label: {
                                content: 'Diabetes',
                                enabled: true,
                                position: 'left'
                            }
                        }
                    }
                }
            }
        }
    };
    
    return new Chart(ctx, chartConfig);
}

/**
 * Creates a horizontal bar chart for comparison with population averages
 * @param {string} canvasId - The ID of the canvas element
 * @param {Object} userData - User's health metrics
 * @param {Object} populationAverages - Population average values for metrics
 * @returns {Chart} The created Chart.js instance
 */
function createPopulationComparisonChart(canvasId, userData, populationAverages) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) {
        console.error(`Canvas element with ID "${canvasId}" not found`);
        return null;
    }

    const ctx = canvas.getContext('2d');
    
    // Prepare data structure
    const metrics = Object.keys(userData);
    const userValues = Object.values(userData);
    const populationValues = metrics.map(metric => populationAverages[metric] || 0);
    
    // Create chart configuration
    const chartConfig = {
        type: 'bar',
        data: {
            labels: metrics,
            datasets: [
                {
                    label: 'Your Values',
                    data: userValues,
                    backgroundColor: chartColors.primary,
                    borderColor: chartColors.primary.replace('0.7', '1'),
                    borderWidth: 1
                },
                {
                    label: 'Population Average',
                    data: populationValues,
                    backgroundColor: chartColors.secondary,
                    borderColor: chartColors.secondary.replace('0.7', '1'),
                    borderWidth: 1
                }
            ]
        },
        options: {
            ...commonChartOptions,
            indexAxis: 'y',
            plugins: {
                ...commonChartOptions.plugins
            }
        }
    };
    
    return new Chart(ctx, chartConfig);
}

// Export functions if using modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        createFeatureImportanceChart,
        createHealthRadarChart,
        createRiskDoughnutChart,
        createGlucoseTrendChart,
        createPopulationComparisonChart
    };
}
