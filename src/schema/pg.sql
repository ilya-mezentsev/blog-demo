DROP SCHEMA IF EXISTS blog_demo CASCADE;
CREATE SCHEMA blog_demo;

DROP TABLE IF EXISTS blog_demo.user CASCADE;
CREATE TABLE blog_demo.user (
    id SERIAL,
    uuid VARCHAR(36) NOT NULL,
    nickname VARCHAR(64) NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    modified TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    PRIMARY KEY (uuid),
    UNIQUE (uuid),
    UNIQUE (nickname)
);

DROP TABLE IF EXISTS blog_demo.article CASCADE;
CREATE TABLE blog_demo.article (
    id SERIAL,
    uuid VARCHAR(36) NOT NULL,
    author_id VARCHAR(36) REFERENCES blog_demo.user(uuid) ON DELETE SET NULL,
    title VARCHAR(256) NOT NULL,
    description VARCHAR(1024) NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    modified TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    PRIMARY KEY (uuid),
    UNIQUE (uuid)
);

DROP TABLE IF EXISTS blog_demo.comment;
CREATE TABLE blog_demo.comment (
    id SERIAL,
    uuid VARCHAR(36) NOT NULL,
    article_id VARCHAR(36) REFERENCES blog_demo.article(uuid) ON DELETE CASCADE,
    author_id VARCHAR(36) REFERENCES blog_demo.user(uuid) ON DELETE SET NULL,
    text VARCHAR(2048) NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    modified TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    PRIMARY KEY (uuid),
    UNIQUE (uuid)
);
