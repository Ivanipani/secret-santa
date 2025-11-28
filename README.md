# Secret Santa Draw

Randomly assign secret santa pairs, email all participants.

## Participants

Create a `participants.yaml` file with the following format:

```yaml
participants:
  - name: Hilberto
    email: hilberto@gmail.com
  - name: Chester Dudando
    email: chester@dudando.com
  - name: Ivan Perdomo
    email: ivan@perdomo.com
```

## Draw and send emails
```bash
EMAIL_ADDRESS=<email> EMAIL_PASSWORD=<password> python -m secret_santa participants.yaml
```

Or use the dry-run flag to test without sending emails:
```bash
EMAIL_ADDRESS=<email> EMAIL_PASSWORD=<password> python -m secret_santa participants.yaml --dry-run
```
