import { useState } from "react"
import {
  Activity, Bot, CheckCircle2, ChevronDown, Clock3,
  Database, Globe2, Loader2, Play, Search,
  Sparkles, Target, Zap
} from "lucide-react"

const API = import.meta.env.VITE_API_URL || "/api"

function AgentCard({ agent, index }) {
  const [open, setOpen] = useState(false)
  const icons = [Search, Target, Zap]
  const Icon = icons[index] || Bot

  return (
    <div className="agent-card">
      <div className="agent-top">
        <div className="agent-icon"><Icon size={20}/></div>
        <div>
          <div className="agent-name">{agent.agent}</div>
          <div className="agent-role">
            {index === 0 ? "External research" :
             index === 1 ? "Task planning" : "External API execution"}
          </div>
        </div>
        <span className="done"><CheckCircle2 size={15}/> {agent.status}</span>
      </div>

      <button className="details" onClick={() => setOpen(!open)}>
        {open ? "Hide details" : "View details"}
        <ChevronDown size={15} className={open ? "rotate" : ""}/>
      </button>

      {open && <pre className="json">{JSON.stringify(agent, null, 2)}</pre>}
    </div>
  )
}

export default function App() {
  const [task, setTask] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [history, setHistory] = useState([])

  async function runWorkflow(e) {
    e?.preventDefault()
    if (!task.trim() || loading) return

    setLoading(true)
    setResult(null)

    try {
      const response = await fetch(`${API}/api/workflow`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({task})
      })

      const data = await response.json()
      if (!response.ok) throw new Error(data.error || "Workflow failed")

      setResult(data)
      setHistory(prev => [
        {task, time: new Date().toLocaleTimeString()},
        ...prev
      ].slice(0, 5))
    } catch (error) {
      setResult({error: error.message})
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark"><Sparkles size={19}/></div>
          <div>
            <strong>Multi-Agent</strong>
            <span>STUDIO</span>
          </div>
        </div>

        <div className="side-section">
          <div className="side-title">WORKFLOW</div>
          <div className="nav active"><Activity size={17}/> Live Run</div>
          <div className="nav"><Clock3 size={17}/> Run History</div>
        </div>

        <div className="side-section">
          <div className="side-title">AGENTS</div>
          <div className="agent-mini"><span className="dot"/> Researcher</div>
          <div className="agent-mini"><span className="dot"/> Planner</div>
          <div className="agent-mini"><span className="dot"/> Executor</div>
        </div>

        <div className="side-bottom">
          <div className="connection"><span className="green-dot"/> APIs Connected</div>
          <small>Flask + React</small>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <div className="eyebrow">AUTONOMOUS WORKFLOW</div>
            <h1>Research → Plan → Execute</h1>
            <p>Coordinate specialized agents to complete multi-step tasks.</p>
          </div>
          <div className="live"><span/> SYSTEM ONLINE</div>
        </header>

        <section className="input-panel">
          <form onSubmit={runWorkflow}>
            <div className="input-label"><Bot size={17}/> What should the agents accomplish?</div>
            <div className="input-row">
              <input
                value={task}
                onChange={e => setTask(e.target.value)}
                placeholder="Example: Plan a 3-day Hyderabad tourist trip"
              />
              <button className="run-btn" disabled={loading}>
                {loading ? <Loader2 className="spin" size={18}/> : <Play size={18}/>}
                {loading ? "Running..." : "Run Workflow"}
              </button>
            </div>
          </form>
        </section>

        <div className="workspace">
          <section>
            <div className="section-head">
              <div><span className="eyebrow">ORCHESTRATION</span><h2>Agent Execution</h2></div>
              {result && !result.error && <span className="completed"><CheckCircle2 size={16}/> Completed</span>}
            </div>

            {!result && !loading && (
              <div className="empty">
                <div className="empty-icon"><Sparkles size={26}/></div>
                <h3>Ready to orchestrate</h3>
                <p>Enter a complex task above. The Coordinator will delegate it to specialized agents.</p>
              </div>
            )}

            {loading && (
              <div className="empty">
                <Loader2 className="spin" size={30}/>
                <h3>Agents are working...</h3>
                <p>Researching, planning and executing your task.</p>
              </div>
            )}

            {result?.error && <div className="error">⚠ {result.error}</div>}

            {result?.agents && result.agents.map((agent, i) => (
              <AgentCard key={agent.agent} agent={agent} index={i}/>
            ))}

            {result?.summary && (
              <div className="report">
                <div className="report-title"><Sparkles size={18}/> Synthesized Report</div>
                <div className="report-body">{result.summary}</div>
              </div>
            )}
          </section>

          <aside>
            <div className="section-head compact">
              <div><span className="eyebrow">HISTORY</span><h2>Recent Runs</h2></div>
            </div>

            <div className="history">
              {history.length === 0 && <div className="history-empty">No runs yet.</div>}
              {history.map((item, i) => (
                <div className="history-item" key={i}>
                  <div className="history-icon"><Clock3 size={15}/></div>
                  <div><strong>{item.task}</strong><small>{item.time}</small></div>
                </div>
              ))}
            </div>

            <div className="api-card">
              <div className="api-title"><Globe2 size={17}/> External APIs</div>
              <div className="api-row"><Database size={15}/> Wikipedia Search</div>
              <div className="api-row"><Globe2 size={15}/> Open-Meteo</div>
              <div className="api-note">No LLM API key required for the core workflow.</div>
            </div>
          </aside>
        </div>
      </main>
    </div>
  )
}
