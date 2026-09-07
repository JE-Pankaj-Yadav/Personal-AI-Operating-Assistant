import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import { api } from '../services/api';
import type { User } from '../types';

type Credentials = Record<string, unknown>;
type C = { user: User | null; loading: boolean; refresh: () => Promise<void>; login: (x: Credentials) => Promise<void>; register: (x: Credentials) => Promise<void>; logout: () => Promise<void> };
const Auth = createContext<C>({ user: null, loading: true, refresh: async () => {}, login: async () => {}, register: async () => {}, logout: async () => {} });

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null), [loading, setLoading] = useState(true);
  const refresh = async () => { try { setUser((await api.me()).user); } catch { setUser(null); } finally { setLoading(false); } };
  useEffect(() => { void refresh(); }, []);
  const login = async (x: Credentials) => { setUser((await api.login(x)).user); };
  const register = async (x: Credentials) => { setUser((await api.register(x)).user); };
  const logout = async () => { await api.logout(); setUser(null); };
  return <Auth.Provider value={{ user, loading, refresh, login, register, logout }}>{children}</Auth.Provider>;
}
export const useAuth = () => useContext(Auth);
