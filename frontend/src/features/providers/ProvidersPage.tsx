import { useEffect, useState } from 'react';
import { Activity, CheckCircle2, GripVertical, Plus, RefreshCw, Trash2, XCircle } from 'lucide-react';
import { api } from '../../services/api';
import type { Provider } from '../../types';

function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}

export default function ProvidersPage() {
  const [items, setItems] = useState<Provider[]>([]);
  const [form, setForm] = useState({
    company: '',
    provider_type: '',
    display_name: '',
    model: '',
    api_key: '',
    base_url: '',
  });
  const [notice, setNotice] = useState('');
  const [busyId, setBusyId] = useState<number | null>(null);

  const refresh = async () => {
    try {
      setItems(await api.providers());
    } catch (error) {
      setNotice(errorMessage(error));
    }
  };

  useEffect(() => {
    void refresh();
  }, []);

  const add = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!form.company || !form.provider_type || !form.model.trim() || !form.display_name.trim() || !form.api_key.trim()) {
      setNotice('Company, model, display name, and API key are required.');
      return;
    }
    try {
      setNotice('Saving provider securely…');
      const provider = await api.addProvider(form);
      setItems((current) => [...current, provider]);
      setBusyId(provider.id);
      setNotice('Provider saved. Verifying the exact model and API key…');
      try {
        const result = await api.testProvider(provider.id);
        const healthy = result.status === 'healthy';
        setItems((current) => current.map((item) => item.id === provider.id ? { ...item, health: healthy ? 'HEALTHY' : 'UNHEALTHY', latency_ms: result.latency_ms ?? null } : item));
        setNotice(healthy ? `${provider.display_name} is HEALTHY · ${result.latency_ms ?? '—'} ms` : `${provider.display_name} is UNHEALTHY${result.http_status ? ` · HTTP ${result.http_status}` : ''}: ${result.message || 'Verify the API key, endpoint, and exact model name.'}`);
      } finally {
        setBusyId(null);
      }
      setForm({ company: '', provider_type: '', display_name: '', model: '', api_key: '', base_url: '' });
    } catch (error) {
      setBusyId(null);
      setNotice(errorMessage(error));
    }
  };

  const test = async (provider: Provider) => {
    if (busyId !== null) return;
    setBusyId(provider.id);
    try {
      const result = await api.testProvider(provider.id);
      setNotice(result.status === 'healthy' ? `${provider.company}: HEALTHY · ${result.latency_ms ?? '—'} ms · request ${result.request_id || '—'}` : `${provider.company}: UNHEALTHY · ${result.http_status ? `HTTP ${result.http_status} · ` : ''}${result.category ? `[${result.category}] ` : ''}${result.message || 'Provider rejected the request.'}`);
      setItems((current) => current.map((item) => item.id === provider.id
        ? { ...item, health: result.status === 'healthy' ? 'HEALTHY' : 'UNHEALTHY', latency_ms: result.latency_ms ?? null }
        : item));
    } catch (error) {
      setNotice(errorMessage(error));
      // The provider may have been deleted while the request was in flight.
      await refresh();
    } finally {
      setBusyId(null);
    }
  };

  const move = async (index: number, delta: number) => {
    const next = [...items];
    const target = index + delta;
    if (target < 0 || target >= next.length) return;
    [next[index], next[target]] = [next[target], next[index]];
    setItems(next);
    try {
      await api.reorder(next.map((item) => item.id));
    } catch (error) {
      setNotice(errorMessage(error));
      await refresh();
    }
  };

  const remove = async (provider: Provider) => {
    if (!confirm('Remove this provider?')) return;
    if (busyId !== null) return;
    setBusyId(provider.id);
    try {
      await api.removeProvider(provider.id);
      setItems((current) => current.filter((item) => item.id !== provider.id));
      setNotice(`${provider.display_name} removed.`);
    } catch (error) {
      setNotice(errorMessage(error));
      await refresh();
    } finally {
      setBusyId(null);
    }
  };

  const toggle = async (provider: Provider) => {
    if (busyId !== null) return;
    setBusyId(provider.id);
    try {
      const updated = await api.updateProvider(provider.id, { enabled: !provider.enabled });
      setItems((current) => current.map((item) => item.id === provider.id ? updated : item));
    } catch (error) {
      setNotice(errorMessage(error));
      await refresh();
    } finally {
      setBusyId(null);
    }
  };

  return (
    <div className="settingsPage">
      <div className="pageIntro">
        <div>
          <h1>AI Providers</h1>
          <p>Only the providers and exact models you configure are used. No hidden mock provider is created.</p>
        </div>
        <span className="sourceTag">Secrets encrypted server-side</span>
      </div>

      <div className="providerLayout">
        <section className="panel">
          <div className="panelTitle">Add Provider</div>
          <form className="providerForm" onSubmit={add}>
            <label>Company
              <select value={form.company} onChange={(event) => { const company = event.target.value; const provider_type = company === 'Custom' ? 'custom' : company.toLowerCase(); setForm({ ...form, company, provider_type }); }}>
                <option value="">Select provider</option><option>OpenAI</option><option>Gemini</option><option>Anthropic</option><option>NVIDIA</option><option>Custom</option>
              </select>
            </label>
            <label>Model<input value={form.model} onChange={(event) => setForm({ ...form, model: event.target.value })} required /></label>
            <label>Display name<input value={form.display_name} onChange={(event) => setForm({ ...form, display_name: event.target.value })} required /></label>
            <label>API key<input required type="password" autoComplete="off" value={form.api_key} onChange={(event) => setForm({ ...form, api_key: event.target.value })} placeholder="Never shown after save" /></label>
            <label>Endpoint<input value={form.base_url} onChange={(event) => setForm({ ...form, base_url: event.target.value })} placeholder="Optional provider endpoint" /></label>
            <button className="primary" type="submit"><Plus size={16} /> Save Provider</button>
          </form>
        </section>

        <section className="providerList">
          <div className="panelTitle">Configured Providers <span>{items.length}</span></div>
          {items.length === 0 ? <div className="empty">No providers yet. Add a real provider with a valid API key and exact model name.</div> : items.map((provider, index) => {
            const busy = busyId === provider.id;
            return (
              <article className="providerCard" key={provider.id}>
                <GripVertical className="dragIcon" size={18} />
                <div className="providerInfo">
                  <div className="providerName"><h2>{provider.display_name}</h2><span>{provider.company}</span></div>
                  <p><strong>{provider.model}</strong> · {provider.masked_key}</p>
                  <div className="tags">{provider.capabilities.map((capability) => <span key={capability}>{capability}</span>)}<span>{provider.usage_source}</span></div>
                </div>
                <div className="providerHealth">
                  <span className={provider.health === 'HEALTHY' ? 'healthy' : 'muted'}>{provider.health === 'HEALTHY' ? <CheckCircle2 size={15} /> : <XCircle size={15} />} {provider.health}</span>
                  <small>Priority {provider.priority}</small>
                  <small>{provider.latency_ms ? `${provider.latency_ms} ms` : 'Not tested'}</small>
                </div>
                <div className="providerActions">
                  <button onClick={() => void test(provider)} disabled={busy} title="Test connection"><RefreshCw size={15} /></button>
                  <button onClick={() => void move(index, -1)} disabled={busy} aria-label="Move up">↑</button>
                  <button onClick={() => void move(index, 1)} disabled={busy} aria-label="Move down">↓</button>
                  <button onClick={() => void toggle(provider)} disabled={busy}>{provider.enabled ? 'Disable' : 'Enable'}</button>
                  <button onClick={() => void remove(provider)} disabled={busy}><Trash2 size={15} /></button>
                </div>
              </article>
            );
          })}
        </section>
      </div>
      {notice && <div className="inlineNotice"><Activity size={15} />{notice}</div>}
    </div>
  );
}
