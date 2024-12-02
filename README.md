# Secret Santa Draw

Randomly assign secret santa pairs, email all participants.
## Participants

participants.csv
```
Hilberto, hilberto@gmail.com
Chester Dudando, chester@dudando.com
Ivan Perdomo, ivan@perdomo.com
```

## Draw and send emails
```
EMAIL_ADDRESS=<email> EMAIL_PASSWORD=<password> python -m src.secret_santa participants.csv
```
