# Archive Metadata

Load all metadata from a specific month. _Note: This loads a very large JSON file (\~20 MB), thus likely it takes a while._

## Usage

```python
NYTAPI.archive_metadata(date)
```

### Parameters

| Variables | Description                       | Data type           | Required |
| --------- | --------------------------------- | ------------------- | -------- |
| `date`    | Date of month of all the metadata | `datetime.datetime` | True     |

## Example

```python
import datetime

data = nyt.archive_metadata(
    date = datetime.datetime(2019, 1, 1)
)
```
