export type User={id:number;email:string;username:string;display_name:string;timezone:string;language:string;theme:string;avatar_path?:string|null};
export type Conversation={id:number;title:string;conversation_type:'chat'|'voice';created_at:string;updated_at:string;archived:boolean};
export type Message={id:number;role:'user'|'assistant';content:string;provider?:string|null;model?:string|null;feedback?:'like'|'dislike'|null;created_at:string};
export type Provider={id:number;company:string;provider_type:string;display_name:string;model:string;base_url?:string|null;masked_key:string;priority:number;enabled:boolean;preferred:boolean;capabilities:string[];health:string;last_tested_at?:string|null;latency_ms?:number|null;usage_source:string;context_window:number};
export type Alert={id:number;severity:string;title:string;message:string;source:string;read:boolean;created_at:string};
