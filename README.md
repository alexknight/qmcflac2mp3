## 项目介绍
本项目可以直接将`qmcflac`文件转换成`mp3`文件，暂时没有支持并发，对性能要求高的可以自行扩展

## 执行方式
```bash
python qmcflac.py -o /tmp/music -i /tmp/music
```
在这里
```bash
-o: 转换mp3输出目录
-i: 原始qmcflac目录
```

## 感谢
在这里直接使用了两个开源项目
```bash
qmc->flac: https://github.com/Presburger/qmc-decoder
flac->mp3: https://github.com/robinbowes/flac2mp3
```