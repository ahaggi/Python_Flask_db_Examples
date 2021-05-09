CREATE TABLE User (
  id TEXT not null,
  username TEXT not null,
  primary key (id)
);

CREATE TABLE Note (
  id TEXT not null,
  content TEXT not null,
  createdOn TEXT not null,
  priority INTEGER not null,
  primary key (id)
);

CREATE TABLE PublishedBy ( 
  id TEXT not null,
  userId TEXT not null,
  noteId TEXT not null,
  unique(userId, noteId),
  foreign key (userId) references User(id) ON DELETE CASCADE,
  foreign key (noteId) references Note(id) ON DELETE CASCADE,
  primary key (id)
);

CREATE TABLE category (
  id TEXT not null,
  type TEXT not null,
  unique(type),
  primary key (id)
);

CREATE TABLE categoriesToNotes ( 
  id TEXT not null,
  noteId TEXT not null,
  categoryId TEXT not null,
  unique(noteId, categoryId),
  foreign key (noteId) references Note(id) ON DELETE CASCADE,
  foreign key (categoryId) references category(id) ON DELETE CASCADE,
  primary key (id)
);

insert into User values
('1' , 'user1'),
('2' , 'user2'),
('3' , 'user3');


insert into Note values
 ('1' , "Integer in libero vitae lorem consectetur rutrum at a turpis. Aliquam mi nisl, placerat at bibendum at...", '2020-04-01T22:00:00.000Z' , 1),
 ('2' , "Mauris dapibus a ante et pellentesque. Pellentesque iaculis pellentesque tortor ac mollis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed pretium ultricies eros vel sodales. ", '2020-04-01T22:00:00.000Z' , 5),
 ('3' , "Pellentesque fringilla nibh non sem ultrices hendrerit. Nunc pellentesque quis libero vel dignissim...", '2020-04-01T22:00:00.000Z' , 2),
 ('4' , "Sed et finibus ante. Etiam et elementum elit. Sed suscipit, enim a pellentesque laoreet, urna ante bibendum ante, id molestie ipsum mi consectetur ligula. Donec commodo arcu vitae ante porta imperdiet eu eget dui. ", '2020-04-02T22:00:00.000Z' , 4),
 ('5' , "Curabitur sit amet tellus risus. Maecenas dictum neque in nibh dapibus, sit amet molestie nibh sodales. Nullam ut velit in lectus blandit lobortis. Fusce ullamcorper tellus at lacus interdum, sed tempus sem porttitor.", '2020-04-02T22:00:00.000Z' , 3),
 ('6' , "Duis sodales tristique mauris sit amet aliquet. Nulla ac molestie justo. Interdum et malesuada fames ac ante ipsum primis in faucibus. In sed tincidunt felis. Pellentesque eget nibh volutpat, elementum erat ut, placerat arcu. ", '2020-04-03T22:00:00.000Z' , 2),
 ('7' , "Maecenas eget ante sit amet ante convallis consectetur. Nullam venenatis ut nisl sed luctus. Cras egestas condimentum diam in egestas. Integer imperdiet elit eget elit maximus ultricies. Aliquam tempus ligula vestibulum sollicitudin dictum. ", '2020-04-03T22:00:00.000Z' , 1),
 ('8' , "Integer iaculis laoreet turpis, vitae faucibus dolor fringilla eget. Proin molestie nunc lorem, in pharetra sem faucibus in. In ut justo non lacus faucibus molestie. ", '2020-04-04T22:00:00.000Z' , 5),
 ('9' , "In nec cursus elit, at bibendum odio. Integer enim dui, tempor sed iaculis vitae, gravida nec velit. Duis lobortis ante in orci consequat tristique. Nulla laoreet laoreet nisl ac laoreet. ", '2020-04-04T22:00:00.000Z' , 4),
 ('10' , "Praesent sed lobortis turpis. Phasellus id ultricies velit. Sed sem nulla, tincidunt in euismod et, placerat quis velit. Nulla blandit erat et elit dignissim, vitae porttitor sem faucibus.", '2020-04-05T22:00:00.000Z' , 3);


insert into PublishedBy values
('1' , '1', '1'),
('2' , '1', '2'),
('3' , '2', '3'),
('4' , '2', '4'),
('5' , '3', '5'),
('6' , '3', '6'),
('7' , '1', '7'),
('8' , '2', '8'),
('9' , '3', '8'),
('10' , '1', '10');


insert into category values
('1' , 'type1'),
('2' , 'type2'),
('3' , 'type3'),
('4' , 'type4'),
('5' , 'type5');


insert into categoriesToNotes values
('1' , '1', '1'),
('2' , '2', '5'),
('3' , '3', '2'),
('4' , '4', '4'),
('5' , '5', '3'),
('6' , '6', '5'),
('7' , '7', '4'),
('8' , '8', '3'),
('9' , '9', '2'),
('10' , '10', '1');


PRAGMA foreign_keys = ON;


-- SELECT *
-- FROM user u, note n, PublishedBy pb
-- WHERE u.id=pb.userId AND n.id=pb.id AND pb.userId=1;

-- SELECT *
-- FROM author a
-- WHERE NOT EXISTS(
-- 		 SELECT *
-- 		 FROM book b
-- 		 WHERE NOT EXISTS(
-- 				  SELECT *
-- 				  FROM _BooksToAuthors bk_ar
-- 				  WHERE bk_ar.bookId=b.id AND bk_ar.authorId=a.id
-- 				  )
-- 		 )
-- ;




