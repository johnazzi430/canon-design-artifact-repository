

load database
     from sqlite:///Users/johnazzinaro/Desktop/Coding/utc-persona-playbook/server/data/data.db
     into postgresql://postgres:mypass01@localhost:5111/test

 with include drop, create tables, create indexes, reset sequences;
