The situation

You work at a small company called Loopy Analytics. They have a tiny internal service that other teams query to look up user account tiers by ID — e.g. is user u_4471 on free, pro, or enterprise. It's called by a few internal dashboards throughout the day.

Right now it's one Flask/FastAPI process on one server. Last week it went down for 90 seconds during a deploy, and every dashboard that depends on it threw errors. Your manager doesn't want to pay for a managed load balancer yet (budget), so she's asked you:

"Can you put together a quick internal proxy that spreads requests across a few copies of this service, and takes an instance out of rotation automatically if it's unhealthy? Doesn't need to be fancy — just needs to survive one instance dying without anyone downstream noticing."

That's the whole brief. No architecture diagram, no spec doc — just that.

Your actual task, broken into concrete deliverables

1. Build the thing being load balanced
The "account tier lookup service." Not the load balancer yet — the thing it protects.

GET /account/{user_id} → returns {"served_by": "instance-8001", "user_id": "u_4471", "tier": "pro"}
GET /health → {"status": "ok"}
Seed a small in-memory dict of ~10 fake user IDs → tiers.
Run 3 copies on 8001/8002/8003.

2. Build the proxy Loopy actually asked for

Single entrypoint, e.g. http://localhost:9000/account/u_4471.
It picks one of the 3 backends and forwards the request, relays the response.
Round-robin to start — that alone satisfies "spreads requests across a few copies."

3. Prove the "survive one instance dying" requirement
This is the part your manager actually cares about, so it's the part you should be able to demo, not just claim:

Add the background health checker.
Open three terminal tabs hammering curl localhost:9000/account/u_1 in a loop (or a tiny script).
Ctrl+C one of the three worker processes mid-loop.
Watch: a couple of requests either fail or get momentarily rerouted, then all subsequent traffic quietly avoids the dead instance.
Bring the worker back up, watch it get added back into rotation without restarting the LB.

4. Write the one-paragraph answer to your manager
After building it, you should be able to say, concretely: "I round-robin across N instances, health-check every 3 seconds, and pull dead instances out of rotation automatically — here's what happens when instance 2 dies," and back it up by actually doing it live.