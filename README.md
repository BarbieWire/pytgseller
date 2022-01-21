# TELEGRAM SELLER BOT

Bot was created for GTA RP server, \
Template that helps you sell internal game currency inside telegram.

- Worker file: app.py


# DATABASE structure
```sql
CREATE TABLE IF NOT EXISTS public.data
(
    img character varying COLLATE pg_catalog."default",
    balance character varying COLLATE pg_catalog."default",
    description character varying COLLATE pg_catalog."default",
    region character varying COLLATE pg_catalog."default",
    price character varying COLLATE pg_catalog."default"
)

```
