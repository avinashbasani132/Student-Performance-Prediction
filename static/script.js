/**
 * AI Student Performance & CGPA Predictor - Client Controller
 */

document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------
    // 1. Theme Management (Dark / Light)
    // -------------------------------------------------------------
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const savedTheme = localStorage.getItem('app-theme') || 'dark';
    
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('app-theme', newTheme);
            updateThemeIcon(newTheme);
        });
    }

    function updateThemeIcon(theme) {
        if (!themeToggleBtn) return;
        themeToggleBtn.innerHTML = theme === 'dark' ? '☀️' : '🌙';
        themeToggleBtn.setAttribute('title', theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode');
    }

    // -------------------------------------------------------------
    // 2. Tab Navigation
    // -------------------------------------------------------------
    const navTabs = document.querySelectorAll('.nav-tab');
    const viewSections = document.querySelectorAll('.view-section');

    navTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetViewId = tab.getAttribute('data-target');
            
            navTabs.forEach(t => t.classList.remove('active'));
            viewSections.forEach(v => v.classList.remove('active'));

            tab.classList.add('active');
            const targetSection = document.getElementById(targetViewId);
            if (targetSection) {
                targetSection.classList.add('active');
            }
        });
    });

    // -------------------------------------------------------------
    // 3. Form Controls & Dual-Input Synchronization
    // -------------------------------------------------------------
    const pairs = [
        { slider: 'hours_slider', num: 'hours_input' },
        { slider: 'prev_slider', num: 'prev_input' },
        { slider: 'sleep_slider', num: 'sleep_input' },
        { slider: 'papers_slider', num: 'papers_input' }
    ];

    pairs.forEach(pair => {
        const sliderEl = document.getElementById(pair.slider);
        const numEl = document.getElementById(pair.num);

        if (sliderEl && numEl) {
            sliderEl.addEventListener('input', () => {
                numEl.value = sliderEl.value;
                handleInputsChanged();
            });

            numEl.addEventListener('input', () => {
                let val = parseFloat(numEl.value);
                if (!isNaN(val)) {
                    sliderEl.value = val;
                }
                handleInputsChanged();
            });
        }
    });

    const extraSelect = document.getElementById('extra_input');
    if (extraSelect) {
        extraSelect.addEventListener('change', () => {
            handleInputsChanged();
        });
    }

    // -------------------------------------------------------------
    // 4. Real-time 24-Hour Time Budget & Live Validation
    // -------------------------------------------------------------
    const studySeg = document.getElementById('segStudy');
    const sleepSeg = document.getElementById('segSleep');
    const freeSeg = document.getElementById('segFree');
    const budgetStatusText = document.getElementById('budgetStatusText');
    const clientWarningBox = document.getElementById('clientWarningBox');

    function updateTimeBudgetMeter() {
        const hoursEl = document.getElementById('hours_input');
        const sleepEl = document.getElementById('sleep_input');
        if (!hoursEl || !sleepEl) return;

        const hours = parseFloat(hoursEl.value) || 0;
        const sleep = parseFloat(sleepEl.value) || 0;
        const total = hours + sleep;
        const free = Math.max(0, 24 - total);

        const studyPct = Math.min(100, (hours / 24) * 100);
        const sleepPct = Math.min(100, (sleep / 24) * 100);
        const freePct = Math.max(0, 100 - (studyPct + sleepPct));

        if (studySeg) studySeg.style.width = `${studyPct}%`;
        if (sleepSeg) sleepSeg.style.width = `${sleepPct}%`;
        if (freeSeg) freeSeg.style.width = `${freePct}%`;

        if (budgetStatusText) {
            if (total > 24) {
                budgetStatusText.innerHTML = `<span style="color: var(--accent-rose);">❌ ${total.toFixed(1)}h / 24h (Exceeds Day!)</span>`;
            } else {
                budgetStatusText.innerHTML = `<span>${total.toFixed(1)}h / 24h (${free.toFixed(1)}h free)</span>`;
            }
        }

        // Live Warning Alerts
        if (clientWarningBox) {
            if (total > 24) {
                clientWarningBox.className = 'alert-box alert-error';
                clientWarningBox.style.display = 'flex';
                clientWarningBox.innerHTML = `<span>❌ <strong>Impossible Schedule:</strong> Study (${hours}h) + Sleep (${sleep}h) exceeds 24 hours.</span>`;
            } else if (hours > 18) {
                clientWarningBox.className = 'alert-box alert-warning';
                clientWarningBox.style.display = 'flex';
                clientWarningBox.innerHTML = `<span>⚠️ <strong>Health Notice:</strong> Studying ${hours} hours/day is unsustainable and may risk mental fatigue.</span>`;
            } else if (sleep < 5) {
                clientWarningBox.className = 'alert-box alert-warning';
                clientWarningBox.style.display = 'flex';
                clientWarningBox.innerHTML = `<span>⚠️ <strong>Sleep Deficit:</strong> Getting under 5 hours of sleep hinders memory consolidation.</span>`;
            } else {
                clientWarningBox.style.display = 'none';
            }
        }
    }

    // -------------------------------------------------------------
    // 5. Preset Personas
    // -------------------------------------------------------------
    const presetButtons = document.querySelectorAll('.chip-btn');
    const presets = {
        'topper': { hours: 8, prev: 9.2, extra: 1, sleep: 7.5, papers: 8 },
        'balanced': { hours: 5, prev: 7.5, extra: 1, sleep: 7.5, papers: 4 },
        'night-owl': { hours: 6, prev: 6.8, extra: 0, sleep: 5.5, papers: 3 },
        'catch-up': { hours: 7, prev: 5.2, extra: 0, sleep: 7.0, papers: 6 }
    };

    presetButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const presetKey = btn.getAttribute('data-preset');
            if (presets[presetKey]) {
                const p = presets[presetKey];
                setFormValues(p.hours, p.prev, p.extra, p.sleep, p.papers);
                handleInputsChanged(true);
            }
        });
    });

    function setFormValues(hours, prev, extra, sleep, papers) {
        const hSlider = document.getElementById('hours_slider');
        const hInput = document.getElementById('hours_input');
        const pSlider = document.getElementById('prev_slider');
        const pInput = document.getElementById('prev_input');
        const eInput = document.getElementById('extra_input');
        const sSlider = document.getElementById('sleep_slider');
        const sInput = document.getElementById('sleep_input');
        const qSlider = document.getElementById('papers_slider');
        const qInput = document.getElementById('papers_input');

        if (hSlider) hSlider.value = hours;
        if (hInput) hInput.value = hours;
        if (pSlider) pSlider.value = prev;
        if (pInput) pInput.value = prev;
        if (eInput) eInput.value = extra;
        if (sSlider) sSlider.value = sleep;
        if (sInput) sInput.value = sleep;
        if (qSlider) qSlider.value = papers;
        if (qInput) qInput.value = papers;
    }

    // -------------------------------------------------------------
    // 6. Live Async Prediction via REST API (/api/predict)
    // -------------------------------------------------------------
    let debounceTimer;

    function handleInputsChanged(immediate = false) {
        updateTimeBudgetMeter();

        clearTimeout(debounceTimer);
        const delay = immediate ? 0 : 300;

        debounceTimer = setTimeout(() => {
            performAsyncPrediction();
        }, delay);
    }

    async function performAsyncPrediction() {
        const hoursEl = document.getElementById('hours_input');
        const prevEl = document.getElementById('prev_input');
        const extraEl = document.getElementById('extra_input');
        const sleepEl = document.getElementById('sleep_input');
        const papersEl = document.getElementById('papers_input');

        if (!hoursEl || !prevEl || !extraEl || !sleepEl || !papersEl) return;

        const payload = {
            hours: parseFloat(hoursEl.value) || 0,
            prev: parseFloat(prevEl.value) || 0,
            extra: parseInt(extraEl.value) || 0,
            sleep: parseFloat(sleepEl.value) || 0,
            papers: parseInt(papersEl.value) || 0
        };

        if (payload.hours + payload.sleep > 24) {
            return; // Don't predict impossible schedule
        }

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const result = await response.json();
            if (result.success && result.data) {
                renderDashboardResults(result.data);
            }
        } catch (err) {
            console.error('Async prediction error:', err);
        }
    }

    function renderDashboardResults(data) {
        // 1. Update Radial Gauge
        const gaugeCircle = document.getElementById('gaugeCircleProgress');
        const gaugeNumber = document.getElementById('gaugeCgpaNumber');
        const gaugeGrade = document.getElementById('gaugeGradeBadge');
        const tierBadge = document.getElementById('tierBadgePill');

        if (gaugeNumber) gaugeNumber.textContent = data.cgpa.toFixed(2);
        if (gaugeGrade) {
            gaugeGrade.textContent = `Grade: ${data.grade}`;
            gaugeGrade.style.borderColor = data.color;
            gaugeGrade.style.color = data.color;
        }
        if (tierBadge) {
            tierBadge.textContent = `${data.badge} (${data.tier})`;
            tierBadge.style.color = data.color;
        }

        if (gaugeCircle) {
            const circumference = 2 * Math.PI * 90; // 565.48
            const fraction = Math.min(10, Math.max(0, data.cgpa)) / 10.0;
            const offset = circumference - (fraction * circumference);
            gaugeCircle.style.strokeDashoffset = offset;
        }

        // 2. Update Quick Metrics
        const statScore = document.getElementById('statScore');
        const statRatio = document.getElementById('statRatio');
        const statFree = document.getElementById('statFree');

        if (statScore) statScore.textContent = `${data.score} / 100`;
        if (statRatio) {
            const ratio = data.sleep > 0 ? (data.hours / data.sleep).toFixed(2) : 'N/A';
            statRatio.textContent = `${ratio} : 1`;
        }
        if (statFree) statFree.textContent = `${data.free_hours}h / day`;

        // 3. Update AI Recommendations
        const recList = document.getElementById('recommendationsList');
        if (recList && data.recommendations) {
            recList.innerHTML = '';
            data.recommendations.forEach(rec => {
                const card = document.createElement('div');
                card.className = `rec-card ${rec.type}`;
                card.innerHTML = `
                    <div class="rec-icon">${rec.icon}</div>
                    <div class="rec-content">
                        <h4>${rec.title}</h4>
                        <p>${rec.message}</p>
                    </div>
                `;
                recList.appendChild(card);
            });
        }
    }

    // -------------------------------------------------------------
    // 7. Goal Planner Simulator (/api/goal-planner)
    // -------------------------------------------------------------
    const calcGoalBtn = document.getElementById('calcGoalBtn');
    const targetCgpaInput = document.getElementById('target_cgpa_input');
    const currentCgpaInput = document.getElementById('current_cgpa_input');
    const planResultContainer = document.getElementById('planResultContainer');

    if (calcGoalBtn) {
        calcGoalBtn.addEventListener('click', async () => {
            const targetCgpa = parseFloat(targetCgpaInput.value) || 8.5;
            const currentCgpa = parseFloat(currentCgpaInput.value) || 7.0;

            calcGoalBtn.innerHTML = 'Calculating Strategy... ⏳';
            calcGoalBtn.disabled = true;

            try {
                const res = await fetch('/api/goal-planner', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        target_cgpa: targetCgpa,
                        prev_cgpa: currentCgpa,
                        extra: 1,
                        sleep: 7.5,
                        hours: 5,
                        papers: 4
                    })
                });

                const result = await res.json();
                if (result.success && result.plan) {
                    renderGoalPlan(result.plan);
                }
            } catch (err) {
                console.error('Goal planner error:', err);
            } finally {
                calcGoalBtn.innerHTML = 'Generate Target Roadmap 🚀';
                calcGoalBtn.disabled = false;
            }
        });
    }

    function renderGoalPlan(plan) {
        if (!planResultContainer) return;
        planResultContainer.style.display = 'block';

        const planTargetCgpa = document.getElementById('planTargetCgpa');
        const planStudyHours = document.getElementById('planStudyHours');
        const planPapers = document.getElementById('planPapers');
        const planSleep = document.getElementById('planSleep');
        const planStrategy = document.getElementById('planStrategy');
        const planDifficulty = document.getElementById('planDifficulty');

        if (planTargetCgpa) planTargetCgpa.textContent = `${plan.target_cgpa.toFixed(1)} CGPA`;
        if (planStudyHours) planStudyHours.textContent = `${plan.recommended_study_hours} hrs/day`;
        if (planPapers) planPapers.textContent = `${plan.recommended_practice_papers} Papers`;
        if (planSleep) planSleep.textContent = `${plan.recommended_sleep_hours} hrs/day`;
        if (planStrategy) planStrategy.textContent = plan.key_strategy;
        if (planDifficulty) {
            planDifficulty.textContent = `Effort Level: ${plan.difficulty}`;
            planDifficulty.className = `gauge-grade-badge`;
        }
    }

    // -------------------------------------------------------------
    // 8. Print / Export Action
    // -------------------------------------------------------------
    const printReportBtn = document.getElementById('printReportBtn');
    if (printReportBtn) {
        printReportBtn.addEventListener('click', () => {
            window.print();
        });
    }

    // -------------------------------------------------------------
    // Initial Load
    // -------------------------------------------------------------
    updateTimeBudgetMeter();
    performAsyncPrediction();
});
