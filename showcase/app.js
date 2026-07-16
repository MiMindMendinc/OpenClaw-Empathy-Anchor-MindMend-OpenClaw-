(() => {
  const statusEl = document.getElementById('connStatus');
  const outputEl = document.getElementById('output');
  const flagsEl = document.getElementById('flags');
  const scenarioEl = document.getElementById('scenario');
  const customEl = document.getElementById('customMessage');

  const messages = {
    neutral: 'I had a good day at school today.',
    distress: 'I feel anxious and overwhelmed about everything.',
    crisis: 'I want to kill myself.',
    night: "I can't sleep and I'm scared.",
  };

  function setStatus(text, ok) {
    statusEl.textContent = text;
    statusEl.className = `status-line ${ok === true ? 'ok' : ok === false ? 'bad' : ''}`;
  }

  function renderFlags(scan) {
    flagsEl.innerHTML = '';
    if (!scan) return;

    const severity = scan.severity || 'low';
    const sev = document.createElement('span');
    sev.className = `flag ${severity}`;
    sev.textContent = severity;
    flagsEl.appendChild(sev);

    const flags = scan.flags || {};
    Object.entries(flags).forEach(([key, value]) => {
      if (!value) return;
      const el = document.createElement('span');
      el.className = 'flag critical';
      if (key === 'distress') el.className = 'flag high';
      if (key === 'night_mode') el.className = 'flag moderate';
      el.textContent = key;
      flagsEl.appendChild(el);
    });

    if (scan.safe === true && !Object.values(flags).some(Boolean)) {
      const el = document.createElement('span');
      el.className = 'flag low';
      el.textContent = 'safe';
      flagsEl.appendChild(el);
    }
  }

  function showJson(data) {
    outputEl.innerHTML = `<code>${JSON.stringify(data, null, 2)}</code>`;
  }

  async function getToken() {
    const res = await fetch('/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: 'showcase_demo' }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || `Login failed (${res.status})`);
    }
    const data = await res.json();
    return data.token;
  }

  async function runChat(message) {
    const token = await getToken();
    const res = await fetch('/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || `Chat failed (${res.status})`);
    renderFlags(data.scan_result);
    showJson(data);
    setStatus(
      data.alert_created
        ? `Alert persisted (${data.scan_result.severity})`
        : `Scan complete (${data.scan_result.severity})`,
      true,
    );
  }

  async function runGeofence() {
    const token = await getToken();
    const res = await fetch('/location', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        lat: 43.0,
        lon: -84.2,
        safe_zones: [
          {
            lat: 42.9956,
            lon: -84.1762,
            radius: 100,
            name: 'Home (Owosso, MI)',
          },
        ],
      }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || `Location failed (${res.status})`);
    flagsEl.innerHTML = '';
    const el = document.createElement('span');
    el.className = data.alert_created ? 'flag high' : 'flag low';
    el.textContent = data.alert_created ? 'geofence_alert' : 'in_safe_zone';
    flagsEl.appendChild(el);
    showJson(data);
    setStatus(
      data.alert_created ? 'Geofence alert persisted to SQLite' : 'Inside safe zone',
      true,
    );
  }

  async function runSelected() {
    try {
      const custom = customEl.value.trim();
      const key = scenarioEl.value;
      if (key === 'geofence' && !custom) {
        await runGeofence();
        return;
      }
      const message = custom || messages[key] || messages.crisis;
      await runChat(message);
    } catch (err) {
      setStatus(err.message, false);
      showJson({ error: err.message });
    }
  }

  async function runAllDemo() {
    try {
      const res = await fetch('/demo');
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || `Demo failed (${res.status})`);
      flagsEl.innerHTML = '';
      (data.chat_scenarios || []).forEach((s) => {
        const el = document.createElement('span');
        const severity = s.scan_result?.severity || 'low';
        el.className = `flag ${severity}`;
        el.textContent = s.scenario;
        flagsEl.appendChild(el);
      });
      showJson(data);
      setStatus('GET /demo returned all scenarios', true);
    } catch (err) {
      setStatus(err.message, false);
      showJson({ error: err.message });
    }
  }

  async function checkHealth() {
    try {
      const res = await fetch('/health');
      const data = await res.json();
      if (!res.ok) throw new Error('unhealthy');
      setStatus(
        `Connected · ${data.service} · v${data.version || '?'} · offline=${data.offline_mode}`,
        true,
      );
    } catch {
      setStatus('API not reachable — start with docker compose up --build', false);
    }
  }

  document.getElementById('runDemo').addEventListener('click', runSelected);
  document.getElementById('runAll').addEventListener('click', runAllDemo);

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add('visible');
      });
    },
    { threshold: 0.15 },
  );
  document.querySelectorAll('[data-reveal]').forEach((el) => observer.observe(el));

  checkHealth();
})();
