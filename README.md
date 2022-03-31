# Heroes PostgreSQL database in Docker containers 
## todo:
- use argparse package
- write logs to database
## Tables:
#### Heroes:
- id
- side (Hero side, either 'radiant' or 'dire')
- name
- birthday
- attribute ('Strength', 'Intelligence', or 'Agility')
- power (Hero power from 1 to 100)
#### Mottos:
- id 
- hero_id
- motto_id
- motto
#### HeroStories:
- id
- hero_id
- story
#### Fights:
- id
- hero1_id
- hero2_id
- hero1_id_motto_id
- hero2_id_motto_id
- winner (0 for draw, 1 if first won, 2 else)
## How to run containers
### development
To deploy from the root folder:

`docker-compose up -d`

Then, to run scripts from container:

`docker exec -it korolev_scripts_dev bash`

`python scripts.py <func_name> <argument_1> <argument_2> ... <argument_n>`

Once you are done running scripts:

`exit`

To switch containers off:

`docker-compose down`

### production
To deploy from the root folder:

`docker-compose -f docker-compose.prod.yml up -d`

Then, to run scripts from container:

`docker exec -it korolev_scripts_prod bash`

To switch cotnainers off:

`docker-compose down`
## Python functions calls examples
### add_hero(name, side=None, attribute=None, power=None, birthday=None)
`python scripts.py add_hero Pepega radiant Strength 100`
### add_motto(hero_id, *motto)
`python scripts.py add_motto 100 FORSAAAAN`
### print_row(table_name, id_)
`python scripts.py print_row Heroes 100`
### add_fight()
`python scripts.py add_fight`
### add_story(hero_id, story)
`python scripts.py add_story 100 Pepega is a beautiful, but naive creature`
### delete_hero(hero_id)
`python scripts.py delete_hero 100`
## Checking logs.txt
`cat logs.txt`
