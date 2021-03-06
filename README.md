# Luogu-paint-toolkit

## 项目简介

这是一个用于洛谷冬日绘板的工具包。其中包含像素画生成器、自动绘图脚本和监视工具。

## 环境依赖

运行环境：Python 3.7.2

```
Package          Version  
---------------- ---------
Pillow           8.1.0    
pygame           2.0.1
requests         2.25.1
websocket-client 0.57.0
```

## 使用方法

### 生成像素画

将原图像放在 `data/src/` 下，然后运行 `pixelart.py` ，输入原图像文件名（带后缀）以及每个像素块的边长。运行完成后，会显示预览图片并保存在 `data/pa/` 下，文件名为原图像文件名（格式均为png）；在 `data/dst` 下会生成一个同名的json文件，存储的是像素画的数据。

### 自动绘图

在根目录下创建配置文件 `config.json`，内容包含所拥有账号的cookie，以及绘图任务。具体格式见样例文件 `config.example.json` 。配置完成后，运行 `paint.py` 即可。

### 绘图监视

运行 `ui.py` 即可。其界面上显示亮度较高的像素为监视开始后有更新的，点击 `DEL` 删除键即可重置监视起始点，点击 `TAB` 键即可切换是否显示阴影层。滚动鼠标滑轮以改变缩放大小，单击并拖动鼠标以移动监控区域。

## 协议

MIT © Leohh 