# embedded i/o

## memory

```
Memory
├── RAM (Random Access Memory) 唯讀、寫入用記憶體、非揮發性
│   ├── SRAM (Static RAM) transistor / 電晶體
│   └── DRAM (Dynamic RAM) capacitor / condenser / 電容器
│
└── ROM (Read Only Memory) 唯讀記憶體、非揮發性
    ├── Mask ROM 不可複寫
    └── PROM (Programable ROM) 可複寫
        ├── One Time PROM 可複寫一次
        └── EPROM (Erasable PROM) 可擦除、複寫
            ├── UVEPROM (Ultra Violet EPROM) 使用紫外線
            ├── EEPROM (Electrically EPROM) 使用高電壓
            └── Flash Memory 使用者可擦除、複寫
```

```
Flash Memory
├── NOR Flash (Code Flash)
└── NAND Flash (Data Flash)
```

```
Card
├── SD (Secure Digital) non-volatile flash memory card
|   ├── standard SD
|   ├── mini SD
|   ├── micro SD
|   └── SDIO
|
└── MMC (Multi Media Card) flash memory card / storage media
    ├── RS-MMC
    ├── DV-MMC
    ├── MMCplus
    ├── MMCmobile
    ├── eMMC
    └── SecureMMC
```

```
port mapper i/o
memory mapper i/o
DMA (Direct Memory Access) mapper i/o

character device:
data transfer 1 byte, lower performance / un-structure

block mode device:
data transfer 1 block, finish block size
```

```
Communication: 帶有資料
Synchronization: 沒帶資料
Inter-Process Communication (IPC)

semaphore / mutex
message queue
pipe
shared memory

semaphore: acquire or release
create semaphore:
semaphore control block
unqiue ID
value (binary or value)
task-waiting list

type of semaphore:
binary semaphore

                            acquire (value = 0)
initial    --->     available   ------>             unavailable    <---  initial
value = 1                       <------                                  value = 0
                             release (value = 1)
counting semaphore
equal resource


mutual-exclusion (mutex) semaphore
ownership
task deletion safety
recursive access
protocol for avoiding mutual exclusion problem


1. wait and signal
2. multiple task waint and signal
3. signle shared resource access



# message queue
system pool
private buffer

## message with block
non-block if full / empty
block with timeout
block forever

## send message
kernel fill queue from head to tail in FIFO order
many implementation allow urgent message to go straigh to the head

## recieve message
destructive read
non-destructive read

## message queue design pattern
non-interlocked, one-way data communication
non-interlocked, two-way data communication
```
