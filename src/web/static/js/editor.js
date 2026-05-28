const GRID_WIDTH = 52;
const GRID_HEIGHT = 7;
let currentLevel = 0;
let gridData = Array(GRID_HEIGHT).fill(null).map(() => Array(GRID_WIDTH).fill(0));

// 初始化网格
function initGrid() {
    const grid = document.getElementById('heatmap-grid');
    grid.innerHTML = '';

    for (let week = 0; week < GRID_WIDTH; week++) {
        const column = document.createElement('div');
        column.className = 'week-column';

        for (let day = 0; day < GRID_HEIGHT; day++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.level = gridData[day][week];
            cell.dataset.week = week;
            cell.dataset.day = day;

            cell.addEventListener('click', () => {
                gridData[day][week] = currentLevel;
                cell.dataset.level = currentLevel;
            });

            cell.addEventListener('mouseenter', (e) => {
                if (e.buttons === 1) {
                    gridData[day][week] = currentLevel;
                    cell.dataset.level = currentLevel;
                }
            });

            column.appendChild(cell);
        }

        grid.appendChild(column);
    }
}

// 设置当前画笔级别
document.querySelectorAll('.level-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.level-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentLevel = parseInt(btn.dataset.level);
    });
});

// 清空网格
document.getElementById('clear-btn').addEventListener('click', () => {
    gridData = Array(GRID_HEIGHT).fill(null).map(() => Array(GRID_WIDTH).fill(0));
    initGrid();
});

// 随机填充
document.getElementById('random-btn').addEventListener('click', () => {
    for (let day = 0; day < GRID_HEIGHT; day++) {
        for (let week = 0; week < GRID_WIDTH; week++) {
            if (Math.random() < 0.5) {
                gridData[day][week] = Math.floor(Math.random() * 4) + 1;
            } else {
                gridData[day][week] = 0;
            }
        }
    }
    initGrid();
});

// 加载预设图案
async function loadPresets() {
    const response = await fetch('/api/patterns');
    const data = await response.json();
    const select = document.getElementById('preset-select');

    data.patterns.forEach(name => {
        const option = document.createElement('option');
        option.value = name;
        option.textContent = name;
        select.appendChild(option);
    });
}

document.getElementById('preset-select').addEventListener('change', async (e) => {
    if (!e.target.value) return;

    const response = await fetch(`/api/patterns/${e.target.value}`);
    const pattern = await response.json();
    gridData = pattern.data;
    initGrid();
});

// 执行创建
document.getElementById('execute-btn').addEventListener('click', async () => {
    const repo = document.getElementById('repo-path').value;
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;

    if (!startDate || !endDate) {
        alert('请设置日期范围');
        return;
    }

    const response = await fetch('/api/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            repo: repo,
            pattern: { name: 'custom', data: gridData },
            start_date: startDate,
            end_date: endDate
        })
    });

    const result = await response.json();
    const resultDiv = document.getElementById('result');

    if (result.success) {
        resultDiv.className = 'success';
        resultDiv.textContent = `成功！创建了 ${result.commits} 个提交到 ${result.repo}`;
    } else {
        resultDiv.className = 'error';
        resultDiv.textContent = `错误: ${result.error}`;
    }
});

// 初始化
initGrid();
loadPresets();

// 设置默认日期
const today = new Date();
const year = today.getFullYear();
document.getElementById('start-date').value = `${year}-01-01`;
document.getElementById('end-date').value = `${year}-12-31`;
