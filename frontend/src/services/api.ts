import type { Alert, Conversation, Message, Provider, User } from '../types';

const API = '/api';

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const r = await fetch(API + path, {
    credentials: 'include',
    ...options,
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
  });
  const text = await r.text();
  let data: unknown = null;
  try { data = text ? JSON.parse(text) : null; } catch { data = { message: text }; }
  if (!r.ok) {
    const error = data as { detail?: string; message?: string } | null;
    throw new Error(error?.detail || error?.message || `Request failed (${r.status})`);
  }
  return data as T;
}

type AuthResponse = { user: User };
type ProviderTestResponse = { status: string; latency_ms?: number | null; request_id?: string | null; http_status?: number | null; message?: string | null; category?: string | null };
export type Telemetry = { cpu:any; ram:any; battery:any; network:any; disk:any; uptime:any };
export type ControlCenter = { provider: Provider|null; usage: {total_tokens:number;requests:number;exact_tokens:number;estimated_tokens:number;usage_percent:number|null}; telemetry: Telemetry; weather: any };

export type WeatherConfig = { provider?: string | null; location?: string | null; units?: string | null; configured?: boolean; api_key?: string | null };
type WeatherSaveResponse = { location?: string | null; configured?: boolean };


export const api = {
  me: () => request<AuthResponse>('/auth/me'),
  login: (x: unknown) => request<AuthResponse>('/auth/login', { method: 'POST', body: JSON.stringify(x) }),
  register: (x: unknown) => request<AuthResponse>('/auth/register', { method: 'POST', body: JSON.stringify(x) }),
  logout: () => request<void>('/auth/logout', { method: 'POST' }),
  conversations: (t: string) => request<Conversation[]>(`/conversations?type=${encodeURIComponent(t)}`),
  messages: (id: number) => request<Message[]>(`/conversations/${id}/messages`),
  newConversation: (type: 'chat' | 'voice') => request<Conversation>('/conversations', { method: 'POST', body: JSON.stringify({ conversation_type: type }) }),
  send: (x: { conversation_id: number; content: string }) => request<{ conversation_id:number; conversation: Conversation; user_message_id:number; message_id:number; message:string; provider?:string; display_name?:string; model?:string; usage?:number; usage_source?:string; context_window?:number; fallback_reason?:string|null }>('/chat/message', { method: 'POST', body: JSON.stringify(x) }),
  rename: (id: number, title: string) => request<Conversation>(`/conversations/${id}`, { method: 'PATCH', body: JSON.stringify({ title }) }),
  del: (id: number) => request<void>(`/conversations/${id}`, { method: 'DELETE' }),
  archive: (id: number) => request<Conversation>(`/conversations/${id}/archive`, { method: 'POST' }),
  feedback: (id: number, feedback: 'like'|'dislike'|'none') => request<{ok:boolean;feedback:string|null}>(`/messages/${id}/feedback`, { method: 'POST', body: JSON.stringify({feedback}) }),
  providers: () => request<Provider[]>('/providers'),
  addProvider: (x: unknown) => request<Provider>('/providers', { method: 'POST', body: JSON.stringify(x) }),
  testProvider: (id: number) => request<ProviderTestResponse>(`/providers/${id}/test`, { method: 'POST' }),
  updateProvider: (id: number, x: unknown) => request<Provider>(`/providers/${id}`, { method: 'PATCH', body: JSON.stringify(x) }),
  removeProvider: (id: number) => request<void>(`/providers/${id}`, { method: 'DELETE' }),
  reorder: (ids: number[]) => request<void>('/providers/reorder', { method: 'POST', body: JSON.stringify({ ids }) }),
  profile: () => request<User>('/profile'),
  avatarUpload: (f: File) => {
    const fd = new FormData(); fd.append('file', f);
    return fetch(API + '/profile/avatar', { method: 'POST', credentials: 'include', body: fd }).then(async r => {
      const d = await r.json(); if (!r.ok) throw new Error(d.detail || 'Avatar upload failed'); return d as User;
    });
  },
  removeAvatar: () => request<void>('/profile/avatar', { method: 'DELETE' }),
  saveProfile: (x: unknown) => request<User>('/profile', { method: 'PATCH', body: JSON.stringify(x) }),
  alerts: () => request<Alert[]>('/alerts'),
  readAlert: (id: number) => request<void>(`/alerts/${id}/read`, { method: 'POST' }),
  files: () => request<unknown[]>('/files'),
  link: (url: string) => request<{id:number;name:string;size:number;mime:string;url:string}>('/links', { method: 'POST', body: JSON.stringify({url}) }),
  upload: (f: File) => {
    const fd = new FormData(); fd.append('file', f);
    return fetch(API + '/files', { method: 'POST', credentials: 'include', body: fd }).then(async r => {
      const d = await r.json(); if (!r.ok) throw new Error(d.detail || 'Upload failed'); return d;
    });
  },
  telemetry: () => request<Telemetry>('/telemetry'),
  controlCenter: () => request<ControlCenter>('/control-center'),
  weather: () => request<WeatherConfig>('/weather'),
  weatherCurrent: () => request<any>('/weather/current'),
  saveWeather: (x: WeatherConfig) => request<WeatherSaveResponse>('/weather', { method: 'POST', body: JSON.stringify(x) }),
  projects: () => request<unknown[]>('/projects'),
  newProject: (x: unknown) => request<unknown>('/projects', { method: 'POST', body: JSON.stringify(x) }),
};
