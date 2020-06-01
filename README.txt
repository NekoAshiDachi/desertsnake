#Upgrading database from Mega Flask Tutorial with Shotokan Scholar tables
1. Ensure only the Mega Flask Tutorial tables (`alembic_version, followers, message, notification, post, task, user`) are in db when running migrations after version `19f87c2a8cd2`. 
2. Ensure `flask db current` version is `19f87c2a8cd2`. If not and #1 is fulfilled, `flask db stamp 19f87c2a8cd2`.
3. Create country, state, style, org, dojo, glossary, tech, video, publication, and person tables with `flask db upgrade 39b354802da1` 
4. Add complete data for tables in #3. 
5. Add relationships and constraints for tables in #3, and kata and kata_rel tables, with `flask db upgrade b6a4845f04a2`.
