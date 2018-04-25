DROP TABLE STATS;
DROP TABLE BOARD;

CREATE TABLE STATS (
    redwins        NUMBER,
    blackwins        NUMBER,
    game_over   NUMBER(1),
    turn        VARCHAR(10),
    CONSTRAINT turnname CHECK (turn IN ('Red', 'Black'))
);
INSERT INTO STATS VALUES(0, 0, 0, 'Red');
CREATE TABLE BOARD (
    tile       NUMBER PRIMARY KEY,
    color      VARCHAR(10),
    king       NUMBER(1),
    CONSTRAINT team_color CHECK (color IN ('Red', 'Black', 'None')),
    CONSTRAINT tile_check CHECK (tile BETWEEN 0 AND 31)
);