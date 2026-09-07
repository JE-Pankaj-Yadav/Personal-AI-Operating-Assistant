export function Toast({message,onClose}:{message:string;onClose:()=>void}){return <div className="toast"><span>{message}</span><button onClick={onClose}>×</button></div>}
