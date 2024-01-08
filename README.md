# test-constructor-bot

---

# Installation

1. Create .env file
   ```bash
    cp .env.dist .env && nano .env
   ```
   
2. Start database container
   ```bash
   docker compose -f docker-compose-local.yaml up -d
   ```
   
3. Create tables in database
   ```bash
   python -m bot.database.session
   ```

4. Start bot
   ```bash
   python -m bot
   ```