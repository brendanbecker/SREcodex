# **🧠 Concepts: Understanding "Skills" in SREcodex**

## **The 30-Second Summary**

If you are wondering *"Is a skill just code? Is it a script?"*, here is the breakdown:

1. **The Code** is the tool (e.g., kubectl, aws-cli).  
2. **The Context** is the static knowledge (e.g., "We use us-east-1").  
3. **The Skill** is the **Standard Operating Procedure (SOP)**.

We do not force the Agent to memorize every SOP on day one. We give them an index. When a specific problem arises, they pull the relevant SOP from the filing cabinet.

## **Visualizing the Flow: Progressive Disclosure**

We use **Progressive Disclosure** to prevent blowing up the Agent's context window (memory). The Agent only loads the heavy text of a skill *after* it realizes it needs it.

\+--------+           \+---------------+            \+------------------+  
|  User  |           | Agent (Codex) |            |  Skill Registry  |  
\+--------+           \+---------------+            \+------------------+  
    |                        |                             |  
    |--(1) "API is 500ing"--\>|                             |  
    |                        |                             |  
    |            \[Scans Skill Descriptions\]                |  
    |            \[Match: "api\_triage.md" \]                 |  
    |                        |                             |  
    |                        |---(2) Request Content------\>|  
    |                        |                             |  
    |                        |\<--(3) Load "api\_triage"-----|  
    |                        |                             |  
    |             \[ Now Following SOP \]                    |  
    |             \[ 1\. Check Load Balancer \]               |  
    |             \[ 2\. Check Pod Logs      \]               |  
    |                        |                             |  
    |\<--(4) "I found the logs..."--------------------------|  
    |                        |                             |

## **FAQ**

### **1\. Is a Skill code or text?**

It is primarily text.  
A Skill is a Markdown file (instructions) that tells the agent how to use Code (tools).

* **Tool:** A Python function that runs aws ec2 reboot-instances.  
* **Skill:** A Markdown guide that says: *"If the health check fails 3 times, use the reboot tool, then wait 60 seconds."*

### **2\. Why don't we just put this in the System Prompt?**

Scalability.  
If we put every SRE procedure into the main prompt, we would:

1. Run out of tokens immediately.  
2. Confuse the agent with conflicting instructions.  
3. Increase costs significantly.

By using Skills, we can have 1,000 different SOPs in the repo, but the agent only "pays" the cognitive cost for the one it is currently using.

### **3\. Where do they live?**

* **Source:** codexskills/skills/\*/SKILL.md (Edit these)  
* **Runtime:** dotcodex/skills/ (The agent reads these)

## **Anatomy of a Skill**

A typical SKILL.md looks like this:

**Description:** Debugging high latency in Kubernetes pods.

**Instructions:**

1. Check kubectl top pods.  
2. If CPU \> 90%, check HPA status.  
3. If HPA is maxed, escalate to On-Call Primary.

\<\!--  
For Web Viewers (GitHub/GitLab), here is the Mermaid version:  
sequenceDiagram  
    participant User  
    participant Agent  
    participant Registry  
    User-\>\>Agent: (1) "API is 500ing"  
    Note over Agent: Scans Index \-\> Match found  
    Agent-\>\>Registry: (2) Request Content  
    Registry--\>\>Agent: (3) Load  
