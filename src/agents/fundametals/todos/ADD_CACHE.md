## Caching Strategy
- [ v] Implement request-scoped cache for SEC downloads
- [ v] Add optional TTL-based cache (24h default)
- [ v] Ensure cache does not persist stale data indefinitely
- [ v] Add cache invalidation on new filing detection
- [ v] Add per-ticker file locking for parallel recompute safety (future)
- [ ] Make sure FundamentalsManager is initialised once agent starts so that cache is reused, check if there is a framework which initializes things at start and you use same object everytime. 

Goal:
Prevent redundant downloads and recomputations while preserving correctness.

Option 3 (Enterprise Pattern – File Locking Per Ticker)

If multiple independent processes may run (e.g., cron + API server), you should use file locking per ticker.

Example idea:

from filelock import FileLock

lock = FileLock(f"data/{ticker}/.lock")
with lock:
    recompute_if_needed()


Now:

Only one recompute per ticker

Other calls wait

No corruption

Works across processes

This is what production data systems do.