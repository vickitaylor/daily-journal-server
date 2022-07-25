CREATE TABLE `Entry` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept`    TEXT NOT NULL,
    `entry`    TEXT NOT NULL,
    `mood_id`    INTEGER NOT NULL,
    `date`    TEXT NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

CREATE TABLE `Mood` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label`    TEXT NOT NULL
);

INSERT INTO `Mood` VALUES (null, "Happy");
INSERT INTO `Mood` VALUES (null, "Sad");
INSERT INTO `Mood` VALUES (null, "Angry");
INSERT INTO `Mood` VALUES (null, "Ok");

INSERT INTO `Entry` VALUES (null, "Javascript", "I learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.", 1, "Wed Sep 15 2021 10:10:47 ");
INSERT INTO `Entry` VALUES (null, "Python", "Python is named after the Monty Python comedy group from the UK. I'm sad because I thought it was named after the snake", 2, "Wed Sep 15 2021 10:11:33");
INSERT INTO `Entry` VALUES (null, "Python", "Why did it take so long for python to have a switch statement? It's much cleaner than if/elif blocks", 3, "Wed Sep 15 2021 10:13:11");
INSERT INTO `Entry` VALUES (null, "Javascript", "Dealing with Date is terrible. Why do you have to add an entire package just to format a date. It makes no sense.", 4, "Wed Sep 15 2021 10:13:11");


SELECT 
    e.id,
    e.concept,
    e.entry,
    e.mood_id,
    e.date
FROM Entry e


CREATE TABLE `Tag` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `name`    TEXT NOT NULL
);

CREATE TABLE `Entrytag` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `entry_id`    INTERGER NOT NULL,
    `tag_id`    INTERGER NOT NULL,
    FOREIGN KEY(`entry_id`) REFERENCES `Entry`(`id`),
    FOREIGN KEY(`tag_id`) REFERENCES `Tag`(`id`)
);

INSERT INTO `Tag` VALUES (null, "API");
INSERT INTO `Tag` VALUES (null, "Components");
INSERT INTO `Tag` VALUES (null, "Fetch");
INSERT INTO `Tag` VALUES (null, "Other");
INSERT INTO `Tag` VALUES (null, "Random");


INSERT INTO `Entrytag` VALUES (null, 1, 4);
INSERT INTO `Entrytag` VALUES (null, 1, 1);
INSERT INTO `Entrytag` VALUES (null, 2, 4);
INSERT INTO `Entrytag` VALUES (null, 2, 5);
INSERT INTO `Entrytag` VALUES (null, 5, 2);
INSERT INTO `Entrytag` VALUES (null, 5, 3);
INSERT INTO `Entrytag` VALUES (null, 6, 1);
INSERT INTO `Entrytag` VALUES (null, 6, 5);

SELECT 
    e.id,
    e.concept,
    e.entry,
    e.mood_id,
    e.date,
    m.label mood_label,
    t.name tag_name
FROM Entry e
JOIN Mood m 
    ON e.mood_id = m.id
JOIN Entrytag et 
    ON et.entry_id = e.id
JOIN Tag t 
    ON et.tag_id = t.id


SELECT 
    e.id,
    e.concept,
    e.entry,
    e.mood_id,
    e.date,
    m.label mood_label,
    t.name tag_name
FROM Entry e
JOIN Mood m 
    ON e.mood_id = m.id
JOIN Entrytag et 
    ON et.entry_id = e.id
JOIN Tag t 
ORDER BY e.id


SELECT 
    et.id, 
    et.entry_id,
    t.name tag_name
FROM Entrytag et
JOIN Tag t 
    ON et.tag_id = t.id