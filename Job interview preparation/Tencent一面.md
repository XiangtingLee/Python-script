# 进程与线程
## 一. 进程和线程的关系

|                   |  进程                           | 线程                                       |
| :--------------: |  :---------------------------:  | :-------------------------------------:   |
| **最小单位**      | 系统分配资源的最小单位             | CPU调度的最小单位                           |
| **独立空间**      | 进程有独立的空间地址               | 没有独立的空间地址，线程共享该进程下的空间地址  |
| **包含关系**      | 进程由OS/父进程创建，含有1-n个线程  | 由进程创建，每个线程只能归属于一个进程         |
| **创建消耗时间**   | 相对较少                         | 相对较多                                   |


## 二. 进程之间的通信方法

1. **管道**（pipe）: 是一种半双工的通信方式，数据只能单向流动，且只能在具有亲缘关系的进程间通信
2. **明明管道**（FIFO）：也是半双工的通信方式，可以在不具有亲缘关系的进程间通信
3. **消息队列**（MessageQueue）：本质是链队列，存放在内核中由消息队列标识符标识。 `优点： 克服了信号传递信息少，管道只能承载字节流等缺点`
4. **共享内存**（ShardMemory）
5. **信号量**（Semaphore）：可以控制多个进程对共享资源的访问。常作为一种 `锁机制`，用作进程间或同进程不同线程间的 `同步手段`
6. **套接字**（Socket）
7. **信号**（Signal）：唯一一种`异步`机制，用来通知进程某个事件已经发生

## 三. 线程的同步方法

1. ### 什么是进程同步和互斥
    按照预定的先后次序顺序进行运行
2. ### 线程同步机制和方式
    1. 互斥控制：**临界区**、**互斥对象**（mutex）：都是具有`拥有权`的控制方法，即拥有该线程的对象才可执行，所以执行完毕后一定要释放对象
    2. 同步控制：**信号量**（Semaphore）、**事件对象**（Event）：主要以`通知`方式进行
	