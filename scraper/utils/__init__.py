import logging, logging.config
from pathlib import Path

BASE = Path(__name__).parent.parent.parent.resolve()

PATH_LOG_FILES = BASE / "logs"

config_dict = {
	"version": 1,
	"formatters": {
		"default": {
			"format": "%(asctime)s %(name)s %(value)s %(message)s"
		},
		"client_error": {
			"format": "%(asctime)s %(name)s %(error)s %(url)s %(message)s"
		}
	},

	"handlers": {
		"console": {
			"class" : "logging.StreamHandler",
    		"formatter": "client_error"
		},
		"file": {
			"class": "logging.FileHandler",
			"formatter": "default",
			"filename": PATH_LOG_FILES / "scraper.log",
			"mode": "w"
		}
	},

	"loggers": {
		"client": {
			"level": "DEBUG",
			"propagate": False,
			"handlers": ["console"]
		},
		"client.scraper": {
			"level": "DEBUG",
			"propagate": False,
			"handlers": ["file"]
		},
	}

}

logging.config.dictConfig(config_dict)


def check_result(value: list | str, scraper: str) -> list | None:
	logger = logging.getLogger("client.scraper")
	if not isinstance(value, list):
		message = f"Scraper {scraper} ha fallado"
		logger.warning(message, extra={"value": value})
		return []

	message = f"Scraper {scraper} ejecutado correctamente"
	logger.info(message, extra={"value": "True"})
	return value


__all__ = ["check_result"]