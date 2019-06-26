## 项目介绍
本项目可以直接将`qmcflac`文件转换成`mp3`文件，目前支持并发

## 执行方式
```bash
python qmcflac.py -o /tmp/mp3_dir -i /tmp/qmcflac_dir -n 5
```
在这里
```bash
-o: 转换mp3输出目录
-i: 原始qmcflac目录
-n: 转换文件的进程数，如果不指定，脚本会自动根据转换数量自动决定进程数
```

## 感谢
在这里直接使用了两个开源项目
```bash
qmc->flac: https://github.com/Presburger/qmc-decoder
flac->mp3: https://github.com/robinbowes/flac2mp3
```