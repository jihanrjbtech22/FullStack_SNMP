import React, { useEffect, useRef, useState } from 'react';

const StreamViewer = () => {
  const [lines, setLines] = useState([]);
  const listRef = useRef(null);

  useEffect(() => {
    const ev = new EventSource('/api/stream/snmp');
    ev.onmessage = (e) => {
      try {
        const msg = JSON.parse(e.data);
        const text = `${msg.timestamp}  ${msg.engine_id}  ${msg.type}  ${msg.oid || msg.trap_oid}  ${msg.mib_name || msg.trap_name || ''}  ${msg.value ?? ''}`;
        setLines((prev) => {
          const next = [...prev, text];
          return next.length > 1000 ? next.slice(-1000) : next;
        });
      } catch {}
    };
    ev.onerror = () => {
      ev.close();
      setTimeout(() => window.location.reload(), 2000);
    };
    return () => ev.close();
  }, []);

  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [lines]);

  return (
    <div style={{margin: '20px', background: '#0b1020', color: '#d1e3ff', borderRadius: 8, border: '1px solid #1f2a44'}}>
      <div style={{padding: '10px 14px', borderBottom: '1px solid #1f2a44', display: 'flex', justifyContent: 'space-between'}}>
        <div>📡 Live SNMP Stream (requests, responses, traps)</div>
        <div style={{opacity: 0.7}}>showing last {lines.length} lines</div>
      </div>
      <div ref={listRef} style={{height: 360, overflowY: 'auto', fontFamily: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace', fontSize: 12, padding: 12}}>
        {lines.map((l, i) => (
          <div key={i} style={{whiteSpace: 'pre', lineHeight: 1.6}}>{l}</div>
        ))}
      </div>
    </div>
  );
};

export default StreamViewer;


