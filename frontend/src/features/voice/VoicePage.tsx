import {useEffect,useRef,useState} from 'react';
import {Mic,Square,Volume2,MoreVertical,Plus,Search,History,X,Trash2} from 'lucide-react';
import {api} from '../../services/api';
import type {Conversation} from '../../types';

declare global {interface Window {webkitSpeechRecognition:any;SpeechRecognition:any}}

const SILENCE_MS=1800;
const cleanVoiceText=(value:string)=>value.replace(/(^|\n)\s*(#{1,6}|\*{1,3}|`{1,3}|---+)\s*/g,'$1').replace(/\*\*/g,'').replace(/__+/g,'').trim();

export default function VoicePage(){
 const [state,setState]=useState<'IDLE'|'LISTENING'|'PROCESSING'|'SPEAKING'|'ERROR'>('IDLE');
 const [convs,setConvs]=useState<Conversation[]>([]); const [active,setActive]=useState<Conversation|null>(null);
 const [response,setResponse]=useState('Speak naturally — I’m listening when you are ready.'); const [provider,setProvider]=useState('No provider');
 const [historyOpen,setHistoryOpen]=useState(() => window.innerWidth > 1024); const [menu,setMenu]=useState<number|null>(null); const [search,setSearch]=useState(''); const [seconds,setSeconds]=useState(0);
 const rec=useRef<any>(null); const timer=useRef<number|undefined>(); const silenceTimer=useRef<number|undefined>(); const transcript=useRef(''); const listening=useRef(false); const processing=useRef(false); const speaking=useRef(false); const utterance=useRef<SpeechSynthesisUtterance|null>(null);

 useEffect(()=>{void api.conversations('voice').then(setConvs).catch(()=>{});void api.providers().then(ps=>{const p=ps.find(x=>x.enabled&&(x.preferred||x.health==='HEALTHY'))||ps.find(x=>x.enabled);if(p)setProvider(p.display_name)}).catch(()=>{})},[]);
 useEffect(()=>{const mq=window.matchMedia('(min-width: 1025px)');const sync=()=>{if(mq.matches)setHistoryOpen(false)};sync();mq.addEventListener?.('change',sync);return()=>mq.removeEventListener?.('change',sync)},[]);
 useEffect(()=>{if(state==='LISTENING'){timer.current=window.setInterval(()=>setSeconds(s=>s+1),1000)}else if(timer.current)window.clearInterval(timer.current);return()=>{if(timer.current)window.clearInterval(timer.current)}},[state]);
 useEffect(()=>()=>{try{rec.current?.abort()}catch{};if(silenceTimer.current)window.clearTimeout(silenceTimer.current);window.speechSynthesis?.cancel()},[]);

 const closeHistory=()=>{setHistoryOpen(false);setMenu(null)};
 const stopAll=()=>{listening.current=false;processing.current=false;try{rec.current?.abort()}catch{};rec.current=null;if(silenceTimer.current)window.clearTimeout(silenceTimer.current);window.speechSynthesis?.cancel();utterance.current=null;setState('IDLE');setResponse('Ready for another request.');};
 const speakResponse=(text:string)=>{const cleaned=cleanVoiceText(text);window.speechSynthesis?.cancel();const u=new SpeechSynthesisUtterance(cleaned);utterance.current=u;speaking.current=true;setState('SPEAKING');u.onend=()=>{speaking.current=false;utterance.current=null;if(listening.current) setState('LISTENING'); else setState('IDLE')};u.onerror=()=>{speaking.current=false;utterance.current=null;if(listening.current)setState('LISTENING');else setState('IDLE')};window.speechSynthesis?.speak(u)};
 const finishUtterance=async()=>{if(processing.current)return;const text=transcript.current.trim();if(!text)return;processing.current=true;listening.current=false;try{rec.current?.stop()}catch{};rec.current=null;if(silenceTimer.current)window.clearTimeout(silenceTimer.current);setState('PROCESSING');try{let current=active;if(!current){current=await api.newConversation('voice');setConvs(v=>[current!,...v]);setActive(current)}const r=await api.send({conversation_id:current!.id,content:text});setProvider(r.display_name||r.provider||'Provider');const cleaned=cleanVoiceText(r.message);setResponse(cleaned);const list=await api.conversations('voice');setConvs(list);const updated=list.find(c=>c.id===current!.id)||r.conversation;setActive(updated);if(r.fallback_reason)setResponse(`${cleaned}\n\n${cleanVoiceText(r.fallback_reason)}`);speakResponse(cleaned)}catch(err){speaking.current=false;setState('ERROR');setResponse(err instanceof Error?err.message:String(err))}finally{processing.current=false;transcript.current=''}};
 const resetSilence=()=>{if(silenceTimer.current)window.clearTimeout(silenceTimer.current);silenceTimer.current=window.setTimeout(()=>void finishUtterance(),SILENCE_MS)};
 const beginRecognition=()=>{const Speech=window.SpeechRecognition||window.webkitSpeechRecognition;if(!Speech){setState('ERROR');setResponse('Speech recognition is unavailable in this browser. Please use Chrome or Edge.');return false}const r=new Speech();rec.current=r;r.continuous=true;r.interimResults=true;r.lang='en-US';listening.current=true;processing.current=false;transcript.current='';
  r.onresult=(e:any)=>{let text='';for(let i=e.resultIndex;i<e.results.length;i++)text+=e.results[i][0].transcript+' ';text=text.trim();if(!text)return;const lower=text.toLowerCase();if(speaking.current&&/(^|\s)(stop|stop it|be quiet|quiet)(\s|$)/i.test(lower)){window.speechSynthesis?.cancel();speaking.current=false;utterance.current=null;listening.current=false;try{r.stop()}catch{};setState('IDLE');setResponse('Speech stopped. Say or click Start Listening when you are ready.');return}
    if(speaking.current&&text.length>2){window.speechSynthesis?.cancel();speaking.current=false;setState('LISTENING')}
    transcript.current=text;setState('LISTENING');resetSilence();
  };
  r.onerror=(e:any)=>{if(!listening.current)return;if(e.error==='aborted')return;if(e.error==='no-speech'||e.error==='audio-capture'){try{r.start()}catch{};return}setState('ERROR');setResponse(`Microphone error: ${e.error||'permission denied'}`);listening.current=false};
  r.onend=()=>{if(listening.current&&!processing.current){try{r.start()}catch{}}};
  try{r.start();setSeconds(0);setState('LISTENING');return true}catch(e){listening.current=false;setState('ERROR');setResponse(e instanceof Error?e.message:String(e));return false}
 };
 const start=()=>{if(state==='SPEAKING'){window.speechSynthesis?.cancel();speaking.current=false;utterance.current=null} if(!listening.current)beginRecognition()};
 const stop=()=>stopAll();
 const again=()=>{window.speechSynthesis?.cancel();speaking.current=false;setResponse('Ready — speak naturally. I will respond after a short pause.');beginRecognition()};
 const rename=async(c:Conversation)=>{const title=window.prompt('Rename conversation',c.title);if(title?.trim()){const n=await api.rename(c.id,title.trim());setConvs(v=>v.map(x=>x.id===c.id?n:x));if(active?.id===c.id)setActive(n)}setMenu(null)};
 const del=async(c:Conversation)=>{if(window.confirm('Delete this conversation permanently?')){await api.del(c.id);setConvs(v=>v.filter(x=>x.id!==c.id));if(active?.id===c.id){setActive(null);setResponse('New voice conversation ready.')}}setMenu(null)};
 const archive=async(c:Conversation)=>{await api.archive(c.id);setConvs(v=>v.filter(x=>x.id!==c.id));setMenu(null);if(active?.id===c.id)setActive(null)};
 const filtered=convs.filter(c=>c.title.toLowerCase().includes(search.toLowerCase()));
 return <div className={"voicePage "+(historyOpen?"historyExpanded":"historyClosed")}>
  {historyOpen&&<button className="historyBackdrop" aria-label="Close history" onClick={closeHistory}/>}
  <aside className={'voiceHistory '+(historyOpen?'historyOpen':'')}>
   <div className="historyDrawerHead"><strong>Voice History</strong><button className="historyClose" aria-label="Close voice history" onClick={closeHistory}><X size={17}/></button></div>
   <button className="primary wide" onClick={async()=>{const c=await api.newConversation('voice');setConvs(v=>[c,...v]);setActive(c);setResponse('New voice conversation ready.');closeHistory()}}><Plus size={17}/> New Conversation</button>
   <div className="searchMini"><Search size={15}/><input placeholder="Search voice history..." value={search} onChange={e=>setSearch(e.target.value)}/></div>
   <div className="historyList">{filtered.map(c=><div key={c.id} className={'voiceHistoryRow '+(active?.id===c.id?'active':'')} onClick={()=>{setActive(c);closeHistory()}}><button className="voiceHistorySelect" title={c.title}><span>{c.title}</span><small>{new Date(c.updated_at).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}</small></button><button className="more" aria-label="Conversation options" onClick={e=>{e.stopPropagation();setMenu(menu===c.id?null:c.id)}}><MoreVertical size={16}/></button>{menu===c.id&&<div className="rowMenu"><button onClick={()=>void rename(c)}>Rename</button><button onClick={()=>void archive(c)}>Archive</button><button onClick={()=>void del(c)}><Trash2 size={14}/> Delete</button></div>}</div>)}</div>
   <div className="fileBox"><strong>Voice conversation</strong><p>History stays available on desktop, tablet and phone.</p></div>
  </aside>
  <section className="voiceMain">
   <div className="voiceTop"><div className="mobileHistoryToggle"><button className="iconBtn" title={historyOpen?"Close voice history":"Open voice history"} aria-label={historyOpen?"Close voice history":"Open voice history"} onClick={()=>setHistoryOpen(v=>!v)}>{historyOpen?<X size={17}/>:<History size={17}/>}</button></div><div className="voiceTitle"><h1><span className="waveGlyph">≋</span> Voice Interaction</h1><p>{state==='LISTENING'?'Speak naturally, I’m listening...':state==='PROCESSING'?'Processing your request...':state==='SPEAKING'?'J.A.R.V.I.S is speaking — say “stop” to interrupt.':state==='ERROR'?'Voice service needs attention':'Ready for voice interaction'}</p></div><span className="sourceTag">AI Provider: {provider}</span></div>
   <div className={'voiceCore '+state.toLowerCase()}><div className="waves left">{Array.from({length:16}).map((_,i)=><i key={i}/>)}</div><button className="micOrb" onClick={state==='LISTENING'?stop:start} aria-label={state==='LISTENING'?'Stop Listening':'Start Listening'}><div className="ring r1"><div className="ring r2"><Mic size={58}/></div></div></button><div className="waves right">{Array.from({length:16}).map((_,i)=><i key={i}/>)}</div></div>
   <div className="voiceStatus"><strong>{state==='LISTENING'?'LISTENING':state}</strong><span>{String(Math.floor(seconds/60)).padStart(2,'0')}:{String(seconds%60).padStart(2,'0')}</span><button className="outline" onClick={state==='LISTENING'||state==='SPEAKING'?stop:start}>{state==='LISTENING'?<><Square size={15}/> Stop Listening</>:<><Mic size={15}/> Start Listening</>}</button></div>
   <div className="voiceResponse"><div className="assistantBadge">A</div><div className="responseText"><h3>J.A.R.V.I.S <small className="providerInline">{provider}</small></h3><p>{response}</p><div className="responseWave">{Array.from({length:40}).map((_,i)=><i key={i}/>)}</div></div><button className="iconBtn" title="Speak response" onClick={()=>speakResponse(response)}><Volume2 size={19}/></button></div>
   <button className="speakAgain" onClick={again}><Mic size={18}/> Speak Again</button>
  </section>
 </div>
}
