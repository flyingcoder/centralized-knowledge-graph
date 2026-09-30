# Sync worker

MVP flow:

Git webhook/poll
-> resolve repository
-> compare last indexed commit with HEAD
-> collect changed paths
-> extract affected knowledge
-> write provenance records
-> update graph relationships

Start with polling/reconciliation before provider-specific webhooks.
