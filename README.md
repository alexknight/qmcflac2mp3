## 项目介绍
本项目可以直接将`qmcflac`文件转换成`mp3`文件，目前支持并发执行

## 执行方式
```bash
python qmcflac.py -o /tmp/mp3_dir -i /tmp/qmcflac_dir
```
在这里
```bash
-o: 转换mp3输出目录
-i: 原始qmcflac目录
-n: 转换文件的进程数，如果不指定，脚本会自动根据转换数量自动决定进程数
```

## 感谢
在这里直接使用了两个开源项目。找过其他实现方案，只有`flac2mp3`这个方案不依赖`ffmpeg`环境，因此使用上不需要过多安装其他依赖库，另外通过
多进程的包装，执行效率也比执行执行速度更快。
```bash
qmc->flac: https://github.com/Presburger/qmc-decoder
flac->mp3: https://github.com/robinbowes/flac2mp3
```