BEGIN;

CREATE TABLE alembic_version
(
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 9c6832308e56

CREATE TABLE "user"
(
    id       SERIAL       NOT NULL,
    username VARCHAR(80)  NOT NULL,
    email    VARCHAR(120) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (email),
    UNIQUE (username)
);

INSERT INTO "user" (username, email)
VALUES ('Bruce Wayne', 'bruce.wayne@wayneenterprise.com');

INSERT INTO "user" (username, email)
VALUES ('Clark Kent', 'clark.kent@planetdiary.com');

INSERT INTO "user" (username, email)
VALUES ('Diana Prince', 'diana.prince@defense.gov');

INSERT INTO "user" (username, email)
VALUES ('Barry Allen', 'barry.allen@scpd.gov');

INSERT INTO alembic_version (version_num)
VALUES ('9c6832308e56');

COMMIT;

