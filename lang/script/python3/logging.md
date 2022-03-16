# logging

## logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG, filename='app.log')

logging.debug('debug message')
logging.info('info message')
logging.warning('warning message')
logging.error('error message')
logging.critical('critical message')
```


---

## logger

```python
import logging

formatter = logging.Formatter(f"[%(asctime)s]/%(levelname)s/%(name): %(message)")
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)

logger = logging.getLogger('app')
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('error message')
logger.critical('critical message')
```
