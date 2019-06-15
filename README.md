# BagitUp
**BagitUp** is a Pythob based module that enables you to automatically backup your files and databases to Git

## Reading `.env` files  
  
```bash  
# .env  
git_url="https://username:password@git_repo_url"  
mysql_host="hostname"  
mysql_username="user"  
mysql_pass="pass"  
mysql_dbname="Database Name"  
```  
  
## Install
```pip install BagitUp
```

## Basic usage
set environment variables in .env file

```bash
BagitUp -d /folder/to/backup/
```

## License

MIT licensed. See the
[LICENSE](https://github.com/geetanshjindal/BagitUp/blob/master/LICENSE) file
for more details.
