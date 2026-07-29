// Chart color roles come from the validated categorical palette (see dataviz
// skill palette.md): slot 1 blue / slot 2 orange, light AND dark steps both
// re-validated for CVD and contrast before use here.
const PALETTE = {
    light: {
        series: "#2a78d6",
        pieSlots: ["#2a78d6", "#eb6834"],
        secondary: "#52514e",
        muted: "#898781",
        grid: "#e1e0d9",
    },
    dark: {
        series: "#3987e5",
        pieSlots: ["#3987e5", "#d95926"],
        secondary: "#c3c2b7",
        muted: "#898781",
        grid: "#2c2c2a",
    },
};

let activeCharts = [];

function isDarkMode() {
    return document.documentElement.classList.contains("dark");
}

function currentPalette() {
    return isDarkMode() ? PALETTE.dark : PALETTE.light;
}

function destroyActiveCharts() {
    activeCharts.forEach((chart) => chart.destroy());
    activeCharts = [];
}

// Single-series bars: swapping category order (gender, education level, prep
// status) doesn't change meaning, so every bar in a chart takes the same
// slot-1 hue rather than one color per bar - identity is already carried by
// the axis label, not color.
function renderBarChart(canvasId, dataObj, palette) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || Object.keys(dataObj).length === 0) {
        return;
    }

    activeCharts.push(
        new Chart(canvas, {
            type: "bar",
            data: {
                labels: Object.keys(dataObj),
                datasets: [
                    {
                        data: Object.values(dataObj),
                        backgroundColor: palette.series,
                        borderRadius: 4,
                        barThickness: 24,
                    },
                ],
            },
            options: {
                plugins: { legend: { display: false } },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: palette.secondary },
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: palette.grid },
                        ticks: { color: palette.muted },
                    },
                },
            },
        })
    );
}

// The lunch-type pie needs true per-slice identity (no axis to label
// against), so it gets two distinct categorical slots.
function renderPieChart(canvasId, dataObj, palette) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || Object.keys(dataObj).length === 0) {
        return;
    }

    activeCharts.push(
        new Chart(canvas, {
            type: "pie",
            data: {
                labels: Object.keys(dataObj),
                datasets: [{ data: Object.values(dataObj), backgroundColor: palette.pieSlots }],
            },
            options: {
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: { color: palette.secondary },
                    },
                    tooltip: {
                        callbacks: {
                            label(ctx) {
                                const total = ctx.dataset.data.reduce((sum, value) => sum + value, 0);
                                const pct = total ? ((ctx.parsed / total) * 100).toFixed(1) : 0;
                                return `${ctx.label}: ${ctx.parsed} (${pct}%)`;
                            },
                        },
                    },
                },
            },
        })
    );
}

function renderAllCharts(data) {
    destroyActiveCharts();
    const palette = currentPalette();
    Chart.defaults.font.family = "system-ui, -apple-system, 'Segoe UI', sans-serif";
    Chart.defaults.color = palette.secondary;

    renderBarChart("genderChart", data.avg_by_gender, palette);
    renderBarChart("parentalEducationChart", data.avg_by_parental_education, palette);
    renderPieChart("lunchChart", data.count_by_lunch, palette);
    renderBarChart("testPrepChart", data.avg_by_test_prep, palette);
}

document.addEventListener("DOMContentLoaded", () => {
    const dataEl = document.getElementById("dashboard-data");
    if (!dataEl) {
        return;
    }
    const data = JSON.parse(dataEl.textContent);

    renderAllCharts(data);
    window.addEventListener("themechange", () => renderAllCharts(data));
});
