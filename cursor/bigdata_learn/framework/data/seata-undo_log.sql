-- Seata AT 模式 undo_log 表结构
CREATE TABLE undo_log (
    branch_id BIGINT NOT NULL COMMENT 'branch transaction id',
    xid VARCHAR(128) NOT NULL COMMENT 'global transaction id',
    context VARCHAR(128) NOT NULL COMMENT 'undo_log context,such as serialization',
    rollback_info LONGBLOB NOT NULL COMMENT 'rollback info',
    log_status INT NOT NULL COMMENT '0:normal status,1:defense status',
    log_created DATETIME(6) NOT NULL COMMENT 'create datetime',
    log_modified DATETIME(6) NOT NULL COMMENT 'modify datetime',
    PRIMARY KEY (branch_id),
    UNIQUE KEY ux_undo_log (xid, branch_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='AT transaction mode undo table';

-- 示例 undo_log 数据（用于验证）
-- 注意：rollback_info 是二进制数据，这里仅展示结构
INSERT INTO undo_log (
    branch_id,
    xid,
    context,
    rollback_info,
    log_status,
    log_created,
    log_modified
) VALUES (
    1,
    '192.168.1.100:8091:1234567890',
    'serializer=jackson',
    UNHEX('7B226272616E63684964223A312C22786964223A223139322E3136382E312E3130303A383039313A31323334353637383930222C22726F6C6C6261636B496E666F223A7B7D7D'),
    0,
    NOW(),
    NOW()
);

-- 查询 undo_log
SELECT 
    branch_id,
    xid,
    context,
    log_status,
    log_created,
    log_modified
FROM undo_log
WHERE xid = '192.168.1.100:8091:1234567890';
