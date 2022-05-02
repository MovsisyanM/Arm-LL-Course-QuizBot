/*markdown
### Data definition for the Armenian language and literature quiz-bot
*/

drop table if exists allQuizBot_msges;

create table allQuizBot_msges (
    id integer auto_increment primary key, 
    time timestamp not null default now(),
    sender varchar(32) not null,
    name varchar(32) not null,
    content text not null
)

drop table if exists allQuizBot_states;

create table allQuizBot_states (
    uid integer auto_increment primary key, 
    state text
)