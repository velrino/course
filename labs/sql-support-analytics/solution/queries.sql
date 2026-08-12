-- Open workload: LEFT JOIN keeps the unassigned group visible.
SELECT COALESCE(a.name, 'Unassigned') AS agent,
       COUNT(*) AS open_tickets,
       SUM(CASE t.priority
             WHEN 'critical' THEN 4
             WHEN 'high' THEN 3
             WHEN 'medium' THEN 2
             ELSE 1
           END) AS priority_points
FROM tickets AS t
LEFT JOIN agents AS a ON a.agent_id = t.assigned_agent_id
WHERE t.status IN ('open', 'pending')
GROUP BY COALESCE(a.name, 'Unassigned')
ORDER BY open_tickets DESC, agent;

-- Customer report: aggregate each one-to-many relationship before joining.
WITH ticket_rollup AS (
    SELECT customer_id,
           COUNT(*) AS total_tickets,
           SUM(status = 'resolved') AS resolved_tickets,
           SUM(status <> 'resolved') AS open_tickets
    FROM tickets
    GROUP BY customer_id
),
event_rollup AS (
    SELECT t.customer_id, SUM(e.minutes_spent) AS support_minutes
    FROM tickets AS t
    JOIN ticket_events AS e ON e.ticket_id = t.ticket_id
    GROUP BY t.customer_id
)
SELECT c.customer_id, c.name, c.plan,
       COALESCE(tr.total_tickets, 0) AS total_tickets,
       COALESCE(tr.resolved_tickets, 0) AS resolved_tickets,
       COALESCE(tr.open_tickets, 0) AS open_tickets,
       COALESCE(er.support_minutes, 0) AS support_minutes
FROM customers AS c
LEFT JOIN ticket_rollup AS tr ON tr.customer_id = c.customer_id
LEFT JOIN event_rollup AS er ON er.customer_id = c.customer_id
ORDER BY c.customer_id;

-- SLA ranking: rank the slowest resolution within each priority.
WITH durations AS (
    SELECT ticket_id, priority,
           ROUND((julianday(resolved_at) - julianday(opened_at)) * 24, 2)
             AS resolution_hours
    FROM tickets
    WHERE status = 'resolved'
)
SELECT ticket_id, priority, resolution_hours,
       ROW_NUMBER() OVER (
           PARTITION BY priority
           ORDER BY resolution_hours DESC, ticket_id
       ) AS slowest_rank
FROM durations
ORDER BY priority, slowest_rank;
