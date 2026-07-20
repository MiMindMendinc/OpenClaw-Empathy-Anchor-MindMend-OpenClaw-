(() => {
  const statusEl = document.getElementById('connStatus');
  const form = document.getElementById('demoForm');
  const scenarioEl = document.getElementById('scenario');
  const customEl = document.getElementById('customMessage');
  const emptyState = document.getElementById('emptyState');
  const loadingState = document.getElementById('loadingState');
  const errorState = document.getElementById('errorState');
  const resultState = document.getElementById('resultState');
  const outputCode = document.querySelector('#output code');
  const navToggle = document.getElementById('navToggle');
  const siteNav = document.getElementById('siteNav');

  const messages = {
    neutral: 'I had a good day at school today.',
    distress: 'I feel anxious and overwhelmed about everything.',
    night: "I can't sleep and I'm scared.",
    crisis: 'I want to kill myself.',
  };

  let lastJson = null;

  function setStatus(text, ok) {
    statusEl.textContent = text;
    statusEl.className = `status-line ${ok === true ? 'ok' : ok === false ? 'bad' : ''}`;
  }

  function showOnly(state) {
    emptyState.classList.toggle('hidden', state !== 'empty');
    loadingState.classList.toggle('hidden', state !== 'loading');
    errorState.classList.toggle('hidden', state !== 'error');
    resultState.classList.toggle('hidden', state !== 'result');
  }

  function setPill(id, text, ok) {
    const el = document.getElementById(id);
    el.textContent = text;
    el.className = ok === true ? 'ok' : ok === false ? 'bad' : '';
  }

  async function getToken() {
    const res = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: 'showcase_demo' }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error?.message || data.error || `Login failed (${res.status})`);
    return data.token || data.data?.token;
  }

  function renderSummary(summary, supportiveText, technical) {
    const severity = summary.severity || 'low';
    const sevEl = document.getElementById('rSeverity');
    sevEl.innerHTML = `<span class="severity ${severity}" aria-label="Severity ${severity}">${severity.toUpperCase()}</span>`;

    document.getElementById('rCategories').textContent =
      (summary.detected_categories || []).join(', ') || 'none';
    const matches = summary.matched_indicators || {};
    document.getElementById('rMatches').textContent =
      Object.keys(matches).length
        ? Object.entries(matches).map(([k, v]) => `${k}: ${v.join(', ')}`).join(' · ')
        : 'none';
    document.getElementById('rActions').textContent =
      (summary.recommended_actions || []).join(', ') || 'none';
    document.getElementById('rPersisted').textContent = summary.alert_persisted ? 'Yes (local SQLite)' : 'No';
    document.getElementById('rAlertId').textContent = summary.alert_id || '—';
    document.getElementById('rCreated').textContent = summary.created_at || '—';
    document.getElementById('rStorage').textContent = summary.storage_mode || 'none';
    document.getElementById('rScanner').textContent = summary.scanner_version || '—';

    document.getElementById('flowPersist').textContent = summary.alert_persisted
      ? 'Alert persisted to local SQLite'
      : 'No alert persisted for this result';
    document.getElementById('flowResources').textContent = summary.resources
      ? 'Crisis-resource guidance available (informational)'
      : 'No crisis-resource block required for this result';

    const box = document.getElementById('supportiveBox');
    box.textContent = supportiveText || summary.note || '';

    lastJson = technical;
    outputCode.textContent = JSON.stringify(technical, null, 2);
    showOnly('result');
  }

  async function runChat(message) {
    const token = await getToken();
    const res = await fetch('/api/v1/scan', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ message, persist_alert: true }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error?.message || data.error || `Scan failed (${res.status})`);
    const payload = data.data || data;
    renderSummary(payload.summary, payload.response, payload);
    setStatus(
      payload.alert_created
        ? `Alert persisted (${payload.summary.severity})`
        : `Scan complete (${payload.summary.severity})`,
      true,
    );
  }

  async function runGeofence() {
    const token = await getToken();
    const res = await fetch('/api/v1/location', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        lat: 43.0,
        lon: -84.2,
        safe_zones: [{ lat: 42.0, lon: -84.0, radius: 100, name: 'Home (demo)' }],
      }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error?.message || data.error || `Location failed (${res.status})`);
    const summary = {
      severity: data.alert_created ? 'high' : 'low',
      detected_categories: data.alert_created ? ['geofence'] : [],
      matched_indicators: {},
      recommended_actions: data.alert_created ? ['RECOMMEND_REVIEW_BY_CAREGIVER'] : [],
      alert_persisted: !!data.alert_created,
      alert_id: data.alert?.id || null,
      created_at: data.alert?.created_at || null,
      storage_mode: data.alert_created ? 'sqlite_local' : 'none',
      scanner_version: 'geofence-v1',
      note: data.note,
    };
    renderSummary(
      summary,
      data.in_safe_zone ? 'Inside configured safe zone.' : 'Outside configured safe zone. Recommendation only — no automatic emergency contact.',
      data,
    );
    setStatus(data.alert_created ? 'Geofence alert persisted' : 'Inside safe zone', true);
  }

  async function onSubmit(event) {
    event.preventDefault();
    const key = scenarioEl.value;
    const custom = customEl.value.trim();
    showOnly('loading');
    setStatus('Scanning…', null);
    document.getElementById('runDemo').disabled = true;
    try {
      if (key === 'geofence' && !custom) {
        await runGeofence();
      } else if (key === 'custom') {
        if (!custom) throw new Error('Enter a custom message or choose another scenario.');
        await runChat(custom);
      } else {
        await runChat(custom || messages[key]);
      }
    } catch (err) {
      errorState.textContent = err.message || 'Request failed';
      showOnly('error');
      setStatus(err.message || 'Request failed', false);
    } finally {
      document.getElementById('runDemo').disabled = false;
    }
  }

  function resetDemo() {
    scenarioEl.value = 'neutral';
    customEl.value = '';
    lastJson = null;
    outputCode.textContent = '';
    showOnly('empty');
    setStatus('Demo reset. Ready for a new scan.', true);
  }

  async function checkRuntime() {
    try {
      const [healthRes, readyRes, statusRes] = await Promise.all([
        fetch('/api/v1/health'),
        fetch('/api/v1/ready'),
        fetch('/api/v1/status'),
      ]);
      const health = await healthRes.json();
      const ready = await readyRes.json();
      const status = await statusRes.json();
      setPill('pillApi', `API: ${health.status || 'up'}`, healthRes.ok);
      setPill('pillStorage', `Storage: ${ready.status || 'unknown'}`, readyRes.ok && ready.status === 'ready');
      setPill('pillOffline', `Offline mode: ${status.offline_mode ? 'on' : 'off'}`, true);
      setStatus(`Connected · ${status.product || 'MindMend Empathy Anchor'} · ${status.version || ''}`, true);
    } catch {
      setPill('pillApi', 'API: unreachable', false);
      setPill('pillStorage', 'Storage: unknown', false);
      setPill('pillOffline', 'Offline mode: unknown', false);
      setStatus('API not reachable — start with docker compose up --build', false);
    }
  }

  navToggle.addEventListener('click', () => {
    const open = siteNav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  siteNav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      siteNav.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });

  form.addEventListener('submit', onSubmit);
  document.getElementById('resetDemo').addEventListener('click', resetDemo);
  document.getElementById('copyJson').addEventListener('click', async () => {
    if (!lastJson) return;
    try {
      await navigator.clipboard.writeText(JSON.stringify(lastJson, null, 2));
      setStatus('Technical JSON copied', true);
    } catch {
      setStatus('Could not copy JSON', false);
    }
  });

  checkRuntime();
})();
