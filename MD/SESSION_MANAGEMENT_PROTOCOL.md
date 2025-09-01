# 🚨 CRITICAL SESSION MANAGEMENT PROTOCOL 🚨

## MANDATORY RULE FOR ALL CLAUDE CLI SESSIONS

**EVERY Claude CLI session MUST monitor session limits and execute handoff protocol**

---

## ⏰ SESSION LIMITS TO MONITOR

1. **5-Hour Time Limit** - Claude CLI session expires after 5 hours
2. **Token Limit** - High token usage approaching context limits
3. **Memory Limits** - When conversation context becomes too large

---

## 🔄 MANDATORY HANDOFF PROTOCOL

### WHEN TO TRIGGER (ANY of these conditions):
- ✅ **4.5 hours elapsed** (30 minutes before 5-hour limit)
- ✅ **High token usage detected** (approaching context limits)
- ✅ **User requests session handoff**
- ✅ **Complex multi-session task in progress**

### HANDOFF EXECUTION STEPS:

#### 1. IMMEDIATE SAVE & COMPACT
```markdown
⚠️ APPROACHING SESSION LIMIT - EXECUTING HANDOFF PROTOCOL

## CURRENT SESSION SUMMARY
- Session Duration: [X hours Y minutes]
- Primary Task: [Brief description]
- Current Status: [In progress/Completed/Blocked]

## ACTIVE TODO LIST
[Copy current TodoWrite state]

## CRITICAL FILES MODIFIED THIS SESSION
- File: [path] - Status: [what was done]
- File: [path] - Status: [what was done]

## NEXT SESSION PRIORITIES
1. [Most critical next step]
2. [Secondary priority]
3. [Tertiary tasks]

## CONTEXT PRESERVATION
- Working Directory: [current path]
- Key Variables/Settings: [any important state]
- Dependencies: [what needs to be maintained]

## HANDOFF NOTES
[Any critical information for continuation]
```

#### 2. CREATE SESSION BRIDGE FILE
Save to: `D:\Applications\_SESSION_HANDOFF\session_[timestamp].md`

#### 3. EXECUTE LOGOUT
- Inform user of handoff completion
- Instruct user to login with new account if needed
- Provide bridge file location

---

## 🛡️ CONSISTENCY MECHANISMS

### A. AUTO-DETECTION TRIGGERS
Claude should proactively monitor for:
- Session duration warnings
- Token usage patterns
- Context size growth
- Complex task progression

### B. USER TRIGGER PHRASES
When user says any of these, IMMEDIATELY execute handoff:
- "approaching limit"
- "session handoff"
- "save and logout" 
- "switch accounts"
- "token limit"
- "5 hour limit"

### C. PROACTIVE NOTIFICATIONS
At 4 hours: "⚠️ Session approaching 5-hour limit in 1 hour. Recommend handoff soon."
At 4.5 hours: "🚨 CRITICAL: Executing mandatory handoff protocol in 30 minutes."

---

## 📁 SESSION HANDOFF STRUCTURE

```
D:\Applications\
├── _SESSION_HANDOFF\
│   ├── session_2025-08-31_14-30.md    ← Latest handoff
│   ├── session_2025-08-31_09-15.md    ← Previous sessions
│   └── ACTIVE_SESSION_STATE.md        ← Always current
├── ULTIMATE_RESUME_HELPER_MASTER_v2.md
└── [other application folders...]
```

---

## 🔧 IMPLEMENTATION PROTOCOL

### For Claude:
1. **Always check session duration** at start of complex tasks
2. **Monitor token usage** during large operations
3. **Proactively suggest handoff** when approaching limits
4. **Execute handoff protocol** without user confirmation when critical

### For User:
1. **Accept handoff recommendations** to maintain workflow
2. **Use bridge files** to continue seamlessly with new session
3. **Trigger handoff manually** when switching contexts

---

## 🎯 SUCCESS METRICS

✅ **Zero session timeouts** - Always handoff before limits
✅ **Seamless continuation** - New session picks up exactly where left off
✅ **No work loss** - All progress preserved and documented
✅ **Consistent quality** - Same level of service across sessions

---

## 🚨 EMERGENCY PROTOCOL

If session expires unexpectedly:
1. User should check `D:\Applications\_SESSION_HANDOFF\ACTIVE_SESSION_STATE.md`
2. Last TodoWrite state preserved
3. Recent file modifications logged
4. New session can reconstruct context from bridge files

---

**THIS PROTOCOL IS MANDATORY AND NON-NEGOTIABLE**
**EVERY CLAUDE CLI SESSION MUST IMPLEMENT THIS SYSTEM**