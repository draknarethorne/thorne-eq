-- Thorne-EQ bootstrap 02: zone launcher config.
-- These tables are MISSING from the Quarm content dump but are required for eqlaunch to
-- boot zones. Apply to the game DB (quarm). Idempotent.
CREATE TABLE IF NOT EXISTS `launcher` (
  `name` varchar(64) NOT NULL DEFAULT '',
  `dynamics` tinyint(3) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `launcher_zones` (
  `launcher` varchar(64) NOT NULL DEFAULT '',
  `zone` varchar(32) NOT NULL DEFAULT '',
  `port` mediumint(9) NOT NULL DEFAULT 0,
  `enabled` tinyint(1) unsigned zerofill DEFAULT 0,
  `expansion` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`launcher`,`zone`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- 'dynzone1' = a dynamic launcher pool of 8 on-demand zones (any zone boots as
-- players enter). control_server.py starts eqlaunch with this launcher name.
INSERT INTO `launcher` (`name`, `dynamics`) VALUES ('dynzone1', 8)
  ON DUPLICATE KEY UPDATE `dynamics` = 8;
