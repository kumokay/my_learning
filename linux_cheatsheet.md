
zip a folder
```
tar -zcvf MYFILE.tar.gz FOLDER_PATH
```

unzip a tarball
```
tar -zxvf MYFILE.tar.gz
```

copy file from remote
```
scp -r -P 2222 -i private_key_path vagrant@127.0.0.1:FOLDER .
scp -P 2222 -i private_key_path vagrant@127.0.0.1:FILE .
```

copy file to remote
```
scp -r -P 2204 -i private_key_path FOLDER vagrant@127.0.0.1:PATH
scp -P 2204 -i private_key_path FILE vagrant@127.0.0.1:PATH
```
