# contrast-artifactory.py

contrast-artifactory.py will download the latest version of the Java contrast.jar file.
It will then upload the jar file to Artifactory, verifying first that it has not already updloaded that contrast.jar version. 

## Installation

Use pip to install requirements.txt

```bash
pip3 install -r requirements.txt
```

## Usage
Fill in these variables. I use Rundeck to encrypt these.
```python
authorization="change-me"
apikey="change-me"
artifactory_auth="change-me"
artifactory_url="change-me"
orgid="change-me"
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
