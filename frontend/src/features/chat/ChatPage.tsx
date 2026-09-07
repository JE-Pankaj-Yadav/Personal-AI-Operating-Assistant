import { useEffect, useRef, useState } from 'react';
import { Copy, FileText, History, X, Folder, Link2, MoreVertical, Paperclip, Plus, Send, ThumbsDown, ThumbsUp, Trash2, Check } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import { api } from '../../services/api';
import type { Conversation, Message } from '../../types';
import 'highlight.js/styles/github-dark.css';

function CodeBlock({ children, className }: { children: React.ReactNode; className?: string }) {
  const text = String(children).replace(/\n$/, '');
  const [copied, setCopied] = useState(false);
  const copy = async () => { await navigator.clipboard.writeText(text); setCopied(true); window.setTimeout(() => setCopied(false), 1400); };
  return <div className="codeBlock"><button className="codeCopy" onClick={() => void copy()}>{copied ? <Check size={13}/> : <Copy size={13}/>} {copied ? 'Copied' : 'Copy'}</button><pre><code className={className}>{children}</code></pre></div>;
}

function MarkdownContent({ content }: { content: string }) {
  return <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]} components={{ code({ className, children, ...props }) { const inline = !className && !String(children).includes('\n'); return inline ? <code className="inlineCode" {...props}>{children}</code> : <CodeBlock className={className}>{children}</CodeBlock>; } }}>{content}</ReactMarkdown>;
}

export default function ChatPage() {
  const [convs, setConvs] = useState<Conversation[]>([]), [active, setActive] = useState<Conversation | null>(null), [messages, setMessages] = useState<Message[]>([]), [input, setInput] = useState(''), [busy, setBusy] = useState(false), [menu, setMenu] = useState<number | null>(null), [search, setSearch] = useState(''), [provider, setProvider] = useState('No provider'), [notice, setNotice] = useState(''), [historyOpen, setHistoryOpen] = useState(() => window.innerWidth > 1024);
  const bottom = useRef<HTMLDivElement | null>(null); const fileRef = useRef<HTMLInputElement | null>(null); const folderRef = useRef<HTMLInputElement | null>(null);
  useEffect(() => { void api.conversations('chat').then(setConvs).catch(() => {}); void api.providers().then(ps => { const p = ps.find(x => x.enabled && x.health === 'HEALTHY'); if (p) setProvider(p.display_name); }).catch(() => {}); }, []);
  useEffect(() => { const mq = window.matchMedia('(min-width: 1025px)'); const sync = () => { if (mq.matches) setHistoryOpen(false); }; sync(); mq.addEventListener?.('change', sync); return () => mq.removeEventListener?.('change', sync); }, []);
  useEffect(() => { if (active) void api.messages(active.id).then(setMessages).catch(() => {}); }, [active]);
  useEffect(() => { bottom.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);
  const newC = async () => { const c = await api.newConversation('chat'); setConvs(v => [c, ...v]); setActive(c); setMessages([]); setHistoryOpen(false); };
  const send = async () => {
    const text = input.trim();
    if (!text || busy) return;
    setInput('');
    setNotice('');
    const conversation: Conversation = active ?? await api.newConversation('chat');
    if (!active) {
      setConvs(v => [conversation, ...v]);
    }
    const optimisticUserId = -Date.now();
    setMessages(v => [...v, { id: optimisticUserId, role: 'user', content: text, created_at: new Date().toISOString() }]);
    setBusy(true);
    try {
      const r = await api.send({ conversation_id: conversation.id, content: text });
      setProvider(r.display_name || r.provider || 'Provider');
      setMessages(v => {
        const withoutOptimistic = v.filter(m => m.id !== optimisticUserId);
        return [...withoutOptimistic, { id: r.user_message_id, role: 'user', content: text, created_at: new Date().toISOString() }, { id: r.message_id, role: 'assistant', content: r.message, provider: r.provider, model: r.model, created_at: new Date().toISOString() }];
      });
      if (r.fallback_reason) setNotice(r.fallback_reason);
      setConvs(await api.conversations('chat'));
      setActive(r.conversation);
    } catch (e) {
      setNotice(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  };
  const key = (e: React.KeyboardEvent<HTMLTextAreaElement>) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); void send(); } };
  const uploadFiles = async (files: File[]) => { try { for (const f of files) await api.upload(f); setNotice(`${files.length} file${files.length > 1 ? 's' : ''} uploaded`); } catch (e) { setNotice((e as Error).message); } };
  const addLink = async () => { const url = window.prompt('Paste a web link'); if (!url?.trim()) return; try { await api.link(url.trim()); setNotice('Link attached to Files'); } catch (e) { setNotice((e as Error).message); } };
  const feedback = async (m: Message, value: 'like'|'dislike') => { const next = m.feedback === value ? 'none' : value; try { await api.feedback(m.id, next); setMessages(v => v.map(x => x.id === m.id ? { ...x, feedback: next === 'none' ? null : next } : x)); } catch (e) { setNotice((e as Error).message); } };
  const copyMessage = async (m: Message) => { await navigator.clipboard.writeText(m.content); setNotice('Response copied'); };
  const rename = async (c: Conversation) => { const title = window.prompt('Rename conversation', c.title); if (title?.trim()) { const n = await api.rename(c.id, title.trim()); setConvs(v => v.map(x => x.id === c.id ? n : x)); if (active?.id === c.id) setActive(n); } setMenu(null); };
  const del = async (c: Conversation) => { if (window.confirm('Delete this conversation permanently?')) { await api.del(c.id); setConvs(v => v.filter(x => x.id !== c.id)); if (active?.id === c.id) { setActive(null); setMessages([]); } } setMenu(null); };
  return <div className={"chatPage "+(historyOpen?"historyExpanded":"historyClosed")}>
    {historyOpen&&<button className="historyBackdrop" aria-label="Close history" onClick={()=>setHistoryOpen(false)}/>}<aside className={'chatHistory '+(historyOpen?'historyOpen':'')}><div className="historyDrawerHead"><strong>Conversation History</strong><button className="historyClose" aria-label="Close conversation history" onClick={()=>setHistoryOpen(false)}><X size={17}/></button></div><button className="primary wide" onClick={() => void newC()}><Plus size={17}/> New Conversation</button><input className="search" placeholder="Search conversations..." value={search} onChange={e => setSearch(e.target.value)}/><div className="historyList">{convs.filter(c => c.title.toLowerCase().includes(search.toLowerCase())).map(c => <div key={c.id} className={'historyRow '+(active?.id===c.id?'active':'')} onClick={() => { setActive(c); setHistoryOpen(false); }}><span title={c.title}>{c.title}</span><small>{new Date(c.updated_at).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}</small><button className="more" aria-label="Conversation options" onClick={e=>{e.stopPropagation();setMenu(menu===c.id?null:c.id)}}><MoreVertical size={15}/></button>{menu===c.id&&<div className="rowMenu"><button onClick={()=>void rename(c)}>Rename</button><button onClick={()=>void api.archive(c.id).then(()=>{setConvs(v=>v.filter(x=>x.id!==c.id));setMenu(null)})}>Archive</button><button onClick={()=>void del(c)}><Trash2 size={14}/> Delete</button></div>}</div>)}</div><div className="fileBox"><strong>Attachments</strong><p>Attach a file, folder or web link directly from this chat.</p></div></aside>
    <section className="chatMain"><div className="chatHeader"><div className="mobileHistoryToggle"><button className="iconBtn" title={historyOpen?"Close conversation history":"Open conversation history"} aria-label={historyOpen?"Close conversation history":"Open conversation history"} onClick={()=>setHistoryOpen(v=>!v)}>{historyOpen?<X size={17}/>:<History size={17}/>}</button></div><div><h1>Chat with J.A.R.V.I.S</h1><p>Your AI Assistant is ready to help you</p></div><span className="sourceTag">AI Provider: {provider}</span></div><div className="messages">{busy&&<div className="answerWaiting" role="status" aria-live="polite"><div className="waitingSpinner"/><strong>Waiting for answer…</strong><span>Please wait while the AI provider processes your request.</span></div>}{messages.length===0?<div className="welcome"><div className="orb">A</div><h2>Start a conversation</h2><p>Ask anything. Enter sends; Shift+Enter creates a new line.</p></div>:messages.map(m=><div key={m.id} className={'message '+m.role}><div className="bubble"><div className="messageTop"><b>{m.role==='user'?'You':'J.A.R.V.I.S'}</b><small>{m.provider ? `${m.provider} · ` : ''}{new Date(m.created_at).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}</small></div><div className="content">{m.role==='assistant'?<MarkdownContent content={m.content}/>:m.content}</div>{m.role==='assistant'&&<div className="actions"><button title="Copy" onClick={()=>void copyMessage(m)}><Copy size={14}/></button><button title="Like" className={m.feedback==='like'?'selected':''} onClick={()=>void feedback(m,'like')}><ThumbsUp size={14}/></button><button title="Dislike" className={m.feedback==='dislike'?'selected dislike':''} onClick={()=>void feedback(m,'dislike')}><ThumbsDown size={14}/></button></div>}</div></div>)}<div ref={bottom}/></div><div className="composer"><textarea value={input} onChange={e=>setInput(e.target.value)} onKeyDown={key} placeholder="Type your message or prompt here..." rows={3}/><div className="composerBar"><div className="attachActions"><button className="iconBtn" title="Upload file" onClick={()=>fileRef.current?.click()}><Paperclip size={17}/></button><button className="iconBtn" title="Upload folder" onClick={()=>folderRef.current?.click()}><Folder size={17}/></button><button className="iconBtn" title="Attach link" onClick={()=>void addLink()}><Link2 size={17}/></button><input ref={fileRef} type="file" multiple hidden onChange={e=>{void uploadFiles(Array.from(e.target.files||[]));e.currentTarget.value=''}}/><input ref={el=>{folderRef.current=el;if(el)el.setAttribute('webkitdirectory','')}} type="file" multiple hidden onChange={e=>{void uploadFiles(Array.from(e.target.files||[]));e.currentTarget.value=''}}/></div><button className="sendBtn" onClick={()=>void send()} disabled={busy}>{busy?'…':<Send size={18}/>}</button></div>{notice&&<div className="composerNotice">{notice}</div>}</div></section>
  </div>;
}
