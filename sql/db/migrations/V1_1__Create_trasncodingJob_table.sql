create table TranscodingJob (
    Id INT NOT NULL PRIMARY KEY,
    Src varchar(100) NOT NULL,
    Dst varchar(100) NOT NULL,
    Config varchar(100) NOT NULL,
    Vendor varchar(100) NOT NULL,
    Progress INT NOT NULL,
    Webhook varchar(300),
    Created_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);