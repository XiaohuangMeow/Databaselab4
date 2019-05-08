import os


class Buffer:
    def __init__(self, bufsize, blksize):
        self.numIO = 0
        self.bufSize = bufsize
        self.blkSize = blksize
        self.numAllBlk = bufsize // (blksize + 1)
        self.numFreeBlk = self.numAllBlk
        self.data = []
        self.used = []
        for i in range(self.numAllBlk):
            self.data.append([])
            self.used.append(False)

    def freeBuffer(self):
        self.data = []
        self.used = []
        for i in range(self.numAllBlk):
            self.data.append([])
            self.used.append(False)
        print("Buffer free")

    def getNewBlockInBuffer(self):
        if (self.numFreeBlk == 0):
            print("No free Block")
            return False;
        for i in range(8):
            if self.used[i] == False:
                self.numFreeBlk -= 1
                self.used[i] = True
                return i

    def freeBlockInBuffer(self, free_num):
        if self.used[free_num] == True:
            self.used[free_num] = False
            self.numFreeBlk += 1
        self.data[free_num] = []

    def readBlockFromDisk(self, addr):
        fileName = "Block/" + addr + ".blk"
        if self.numFreeBlk == 0:
            print("Buffer Overflow")
            return False
        f = open(fileName)
        if not f:
            print("Open File Fail")
            return False
        line = f.readline()
        line_spilt = line.split(" ")
        f.close()
        for i in range(self.numAllBlk):
            if self.used[i] == False:
                self.used[i] = True
                self.data[i] = line_spilt
                self.numFreeBlk -= 1
                self.numIO += 1
                return i

    def writeBlockToDisk(self, addr, write_num):
        fileName = "Block/" + str(addr) + ".blk"
        f = open(fileName, "w")
        if not f:
            print("Open File Fail")
            return False
        for i in self.data[write_num]:
            f.write(str(i) + " ")
        f.close()
        self.data[write_num]=[]
        self.used[write_num]=False
        self.numFreeBlk += 1
        self.numIO += 1
        return True


def dropBlockOnDisk(addr):
    fileName = "Block/" + addr + ".blk"
    if not os.path.exists(fileName):
        return False
    os.remove(fileName)
    return True
