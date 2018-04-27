# NLPCC2018ShardTask6  
  
数据处理：  
去掉csv文件第一行：`sed 1d train_data_deled_col.csv > del_line.csv`  
去掉csv文件第一列：del_col.py  
  
可视化：
- 启动服务器：`python -m visdom.server`
    - 命令行选项：`-port`：端口号
- 代码：`vis = visdom.Visdom(port=2333,env='example')  //port缺省值为8097，env缺省值为'main'`

查看显卡情况：`nvidia-smi`，`nvidia-smi -l`
释放显存：
```
$ ps aux|grep python // 查看python程序的pid
$ kill -9 PID // 杀死进程

```
解释（https://webcache.googleusercontent.com/search?q=cache:u9tKrJzaMZkJ:https://discuss.pytorch.org/t/gpu-memory-not-returned/1311+&cd=1&hl=zh-CN&ct=clnk）：
`ps x |grep python|awk '{print $1}'|xargs kill`
`ps x`: show all process of current user
`grep python`: to get process that has python in command line
`awk '{print $1}`': to get the related process pid
`xargs kill`: to kill the process

note: make sure you don’t kill other processes! do `ps x |grep python` first.

since I usually use the jupyter notebook, so I use grep ipykernel

`ps x |grep ipykernel|awk '{print $1}'|xargs kill`
there should be an elegant way to kill the related process using only `ps`+`awk`
